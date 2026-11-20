import io
import time
import wave
from studio import PHRASES, compose, render

scores = {"learned": 0, "baseline": 0}
slowest = 0
for style, phrases in PHRASES.items():
    known = {edge for phrase in phrases for edge in zip(phrase, phrase[1:])}
    for mode in scores:
        hits = 0
        for seed in range(20):
            start = time.perf_counter()
            notes = compose(style, seed, mode)
            assert len(notes) == 16 and notes == compose(style, seed, mode)
            with wave.open(io.BytesIO(render(notes))) as clip:
                assert clip.getnframes() == 32000 and clip.getframerate() == 8000
            slowest = max(slowest, time.perf_counter() - start)
            hits += sum(edge in known for edge in zip(notes, notes[1:]))
        scores[mode] += hits
        print(style, mode, f"{hits}/300 observed transitions")
assert scores["learned"] > scores["baseline"]
print(f"80 cases passed. Slowest generation: {slowest:.3f}s")
