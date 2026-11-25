"""Offline quality report and regression checks. Run with python3 check_arranger.py."""
import io
import math
import statistics
import time
import wave

from arranger import PITCH, RATE, arrange, candidates, corpus, fit, mix
from studio import PHRASES
from attention import train


def validation_loss(style):
    phrases = corpus(style, PHRASES)
    losses = [[], [], []]
    for i, held in enumerate(phrases):
        training = phrases[:i] + phrases[i+1:]
        table = fit(training)
        head = train(tuple(map(tuple,training)),tuple(PITCH.values()))
        for j, target in enumerate(held[1:],1):
            _, conditional = candidates(table, held[:j])
            _, weights, probs = head.forward(held[:j])
            assert len(weights)==min(j,4) and abs(sum(weights)-1)<1e-8
            losses[2].append(-math.log2(probs[head.index[target]]))
            for loss, counts in zip(losses, (table[()], conditional)):
                # Add-one smoothing gives even unseen targets finite test loss.
                prob = (counts[target]+1)/(sum(counts.values())+len(PITCH))
                loss.append(-math.log2(prob))
    return [statistics.mean(loss) for loss in losses]


if __name__ == "__main__":
    for style in PHRASES:
        base, model, attn = validation_loss(style)
        print(f"{style}: held-out bits/note | unigram {base:.3f} | context {model:.3f} | attention {attn:.3f}")
        for motif in ([60], [71,71,71,71], [60,64,67]):
            for tempo in (64,108,160):
                variants = set()
                for seed in range(10):
                    song = arrange(style, seed, motif, tempo, PHRASES)
                    events = song["events"]
                    notes = tuple(e["pitch"] for e in events)
                    assert list(notes[:len(motif)]) == motif
                    assert all(n in PITCH.values() for n in notes)
                    assert song == arrange(style, seed, motif, tempo, PHRASES)
                    assert sum(e["length"] for e in events)==32
                    assert all(abs(sum(e["options"].values())-1)<.005 for e in events[len(motif):])
                    variants.add(notes)
                assert len(variants)>1
    for tempo in (64,108,160):
        start = time.perf_counter()
        data = mix(arrange("bright",7,[60,64,67],tempo,PHRASES))
        with wave.open(io.BytesIO(data)) as clip:
            assert clip.getframerate()==RATE and clip.getnframes()==round(RATE*960/tempo)
        print(f"{tempo} BPM: {len(data)} WAV bytes, {time.perf_counter()-start:.3f}s")
    print("180 arrangements passed, plus 3 audio exports.")
