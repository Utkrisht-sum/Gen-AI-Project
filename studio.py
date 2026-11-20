"""Seeded melody studio. Run with Python 3.9+."""
import base64
import io
import json
import math
import random
import struct
import wave
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

# Original teaching phrases, encoded as MIDI pitches.
PHRASES = {
    "bright": [[60,64,67,69,67,64,62,60], [64,67,72,69,67,62,64,60], [60,62,64,67,64,62,67,72]],
    "wistful": [[69,67,64,62,60,62,64,69], [69,72,71,67,64,62,64,60], [64,65,64,60,62,65,64,69]],
}


def compose(style, seed, mode):
    rng = random.Random(seed)
    phrases = PHRASES[style]
    transitions = defaultdict(list)
    for phrase in phrases:
        for current, following in zip(phrase, phrase[1:]):
            transitions[current].append(following)
    pool = sum(phrases, [])
    notes = [rng.choice([p[0] for p in phrases])]
    for _ in range(15):
        options = transitions.get(notes[-1], pool) if mode == "learned" else pool
        notes.append(rng.choice(options))
    return notes


def render(notes):
    stream = io.BytesIO()
    with wave.open(stream, "wb") as out:
        out.setparams((1, 2, 8000, 0, "NONE", ""))
        for pitch in notes:
            step = 2 * math.pi * 440 * 2 ** ((pitch - 69) / 12) / 8000
            samples = [int(9000 * math.sin(i*step) * min(1,i/80,(1999-i)/240)) for i in range(2000)]
            out.writeframes(struct.pack("<2000h", *samples))
    return stream.getvalue()


class Studio(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path)
        if path.path not in {"/", "/challenge"}:
            return self.send_error(404)
        q = parse_qs(path.query)
        style = q.get("style", ["bright"])[0]
        mode = q.get("mode", ["learned"])[0]
        try:
            seed = int(q.get("seed", ["7"])[0])
            if style not in PHRASES or mode not in {"learned","baseline"} or not 0 <= seed <= 99999:
                raise ValueError
        except ValueError:
            return self.send_error(400, "Choose a listed style and mode and a seed from 0 to 99999")
        if path.path == "/challenge":
            pairs = {pair for phrase in PHRASES[style] for pair in zip(phrase, phrase[1:])}
            clips = []
            for model in ("learned", "baseline"):
                melody = compose(style, seed, model)
                clips.append(dict(model=model, notes=melody,
                                  matches=sum(pair in pairs for pair in zip(melody, melody[1:])),
                                  wav=base64.b64encode(render(melody)).decode()))
            random.SystemRandom().shuffle(clips)
            template = Path(__file__).with_name("challenge.html").read_text()
            return self.send_page(template.replace("ROUND_DATA", json.dumps(dict(
                clips=clips, seed=seed, style=style))))
        notes = compose(style, seed, mode)
        clip = base64.b64encode(render(notes)).decode()
        def select(name, choices, current):
            return f'<label>{name.title()} <select name="{name}">' + ''.join(
                f'<option {"selected" if v == current else ""}>{v}</option>' for v in choices) + '</select></label>'
        html = f"""<!doctype html><meta charset=utf-8><title>Phrase Studio</title>
        <style>body{{font:1.15rem system-ui;max-width:48rem;margin:8vh auto;padding:1rem;background:#faf6eb;color:#272a22}}
        h1{{font:3rem Georgia}} form{{display:flex;flex-wrap:wrap;gap:1rem}}button,select,input{{font:inherit}}audio{{width:100%}}</style>
        <h1>Phrase Studio</h1><p>Compose a four-second melody from patterns learned in short musical phrases.</p>
        <p><a href="/challenge?style={style}&amp;seed={seed}">Open the blind listening challenge →</a></p>
        <form>{select('style',PHRASES,style)}{select('mode',['learned','baseline'],mode)}
        <label>Seed <input name=seed type=number min=0 max=99999 value={seed}></label><button>Compose</button></form>
        <h2>Your melody</h2><audio controls src="data:audio/wav;base64,{clip}"></audio>
        <p>MIDI pitches: {' · '.join(map(str,notes))}</p>"""
        self.send_page(html)

    def send_page(self, html):
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())


if __name__ == "__main__":
    HTTPServer(("127.0.0.1",8000),Studio).serve_forever()
