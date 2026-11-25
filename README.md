# Phrase Studio

**A motif-to-music instrument for the classroom.** Give it up to four notes. A small statistical generative model keeps that opening and samples a continuation. A synthesizer performs it over four bars of chords and bass. Click a generated note to see which pitches competed for that position, or download the arrangement as a WAV.

## Run the demo

1. Open a terminal in this project directory. Run `python3 studio.py` (Windows: `py -3 studio.py`).
2. On the same computer, open `http://127.0.0.1:8000` in Chrome, Edge, or Firefox. Press play after the score appears. Stop the server with Ctrl+C.
3. Choose **Presentation** for the overview. Page Down advances through the deck. An offline copy lives in [slides.html](slides.html) with its WAVs in the examples folder. Follow the [timed script, rehearsal plan and Q&A](PRESENT.md).

**Stack:** Python 3.9+ standard library for local HTTP, count-based training and PCM synthesis. HTML, CSS and vanilla JavaScript for controls, playback and the interactive score. No database, agent framework, cloud model, API key or package installation.

| Example | Controls | What to show |
|---|---|---|
| Finish my tune | Bright, C4 E4 G4, 108 BPM, seed 7 | Select the three peach notes and the first mint note. Explain how the model continues the given motif. |
| A softer arrangement | Wistful, A4 G4 E4, 84 BPM, seed 21 | Listen to the slower chord changes. Change only the seed to 22 to hear another continuation. Download a WAV. |
| Audience experiment | Open Blind listening lab, play A and B through to the end | Ask for a vote, select A, B or tie, and reveal the identities. This experiment isolates first-order pitch learning using an unaccompanied, fixed-rhythm sketch. |

## Deliverables

- [Use case, scope, technical design, architecture diagram and evaluation](DESIGN.md)
- [Presentation slides](slides.html) and [15-minute speaker guide with Q&A](PRESENT.md)
- `studio.py` serves the workbench, sketches and listening rounds. `arranger.py` fits the sequence model and synthesizes layered audio. The browser interface uses HTML, CSS and plain JavaScript. Run with Python 3.9+ using its standard library. The project needs no database, API key, network service or framework installation.
- Run `python3 check_arranger.py` for held-out prediction, motif preservation, reproducibility, variation and audio export checks. Run `python3 evaluate.py` for the 80 sketch and baseline cases.
- [GitHub repository](https://github.com/Utkrisht-sum/Gen-AI-Project)
