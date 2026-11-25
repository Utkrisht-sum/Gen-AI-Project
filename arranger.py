"""A small conditional pitch model and a three-voice, four-bar renderer."""
from array import array
from collections import Counter, defaultdict
from functools import lru_cache
import io
import math
import random
import sys
import wave
from attention import train

PITCH = dict(zip("C4 D4 E4 F4 G4 A4 B4 C5".split(), (60,62,64,65,67,69,71,72)))
NAME = {v:k for k,v in PITCH.items()}
# Additional original exercises for the arranger. The blind lab keeps its original corpus.
EXERCISES = {
    "bright": ["C4 E4 G4 E4 F4 A4 G4 E4", "E4 D4 C4 G4 A4 G4 E4 D4",
               "G4 A4 C5 G4 E4 G4 D4 C4", "C4 D4 E4 F4 G4 E4 D4 C4",
               "F4 A4 G4 E4 D4 G4 E4 C4", "G4 E4 G4 C5 B4 A4 G4 E4"],
    "wistful": ["A4 G4 F4 E4 D4 F4 E4 D4", "E4 F4 A4 G4 E4 D4 C4 E4",
                "A4 C5 B4 A4 F4 E4 D4 E4", "D4 E4 F4 A4 G4 F4 E4 D4",
                "F4 E4 C4 D4 E4 G4 F4 E4", "A4 E4 F4 E4 D4 C4 E4 A4"],
}
CHORDS = {"bright":[("C",(60,64,67)),("Am",(57,60,64)),("F",(53,57,60)),("G",(55,59,62))],
          "wistful":[("Am",(57,60,64)),("F",(53,57,60)),("Em",(52,55,59)),("Am",(57,60,64))]}
RHYTHMS = [(1,1,2,1,1,2),(2,1,1,2,2),(1,2,1,1,1,2)]
RATE = 16000


def corpus(style, phrases):
    return phrases[style] + [[PITCH[n] for n in line.split()] for line in EXERCISES[style]]


def fit(phrases):
    table = defaultdict(Counter)
    for phrase in phrases:
        for i, pitch in enumerate(phrase):
            for k in range(min(i, 2)+1):
                table[tuple(phrase[i-k:i])][pitch] += 1
    return table


def candidates(table, history):
    for size in range(min(2,len(history)), -1, -1):
        key = tuple(history[len(history)-size:])
        if key in table:
            return size, table[key]


def arrange(style, seed, motif, tempo, phrases, model="attention"):
    data = corpus(style, phrases)
    table = fit(data)
    head = train(tuple(map(tuple,data)),tuple(NAME)) if model == "attention" else None
    rng = random.Random(seed)
    notes, events, chords = [], [], []
    tick = 0
    for bar,(label, chord) in enumerate(CHORDS[style]):
        chords.append(label)
        rhythm = rng.choice(RHYTHMS)
        for duration in rhythm:
            row = {"tick":tick,"length":duration}
            if len(notes) < len(motif):
                pitch = motif[len(notes)]
                row.update(source="motif")
            else:
                if head:
                    _, attention, probs = head.forward(notes)
                    counts = dict(zip(head.vocab, probs))
                    row.update(source="attention", attention=attention)
                else:
                    order, counts = candidates(table, notes)
                    row.update(source=f"order {order}")
                pitches = sorted(counts)
                weights = [counts[p] * (2 if tick%2==0 and p%12 in {n%12 for n in chord} else 1) for p in pitches]
                pitch = rng.choices(pitches, weights)[0]
                row.update(options={NAME[p]:round(w/sum(weights),3) for p,w in zip(pitches,weights)})
            notes.append(pitch)
            events.append(dict(row,pitch=pitch,name=NAME[pitch]))
            tick += duration
    return dict(style=style,seed=seed,tempo=tempo,events=events,chords=chords)


@lru_cache(maxsize=128)
def tone(pitch, frames, voice):
    phase = 2*math.pi*440*2**((pitch-69)/12)/RATE
    amp, harmonic = {"lead":(7200,.27),"bass":(4200,.12),"pad":(1250,.04)}[voice]
    return array("h",(int(amp * min(1,i/140,(frames-1-i)/400) *
                         (math.sin(i*phase)+harmonic*math.sin(2*i*phase))) for i in range(frames)))


def mix(song):
    unit = RATE*30/song["tempo"]
    samples = array("h",[0])*round(32*unit)
    def add(pitch,tick,length,voice):
        start = round(tick*unit)
        count = round((tick+length)*unit)-start
        for i,value in enumerate(tone(pitch,count,voice),start):
            samples[i] += value
    for e in song["events"]:
        add(e["pitch"],e["tick"],e["length"]*.92,"lead")
    for bar,(_,chord) in enumerate(CHORDS[song["style"]]):
        for pitch in chord:
            add(pitch-12,8*bar,7.9,"pad")
        for beat in (0,4):
            add(chord[0]-24,bar*8+beat,3.3,"bass")
    if sys.byteorder != "little":
        samples.byteswap()
    buf = io.BytesIO()
    with wave.open(buf,"wb") as out:
        out.setparams((1,2,RATE,0,"NONE",""))
        out.writeframes(samples.tobytes())
    return buf.getvalue()
