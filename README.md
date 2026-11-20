# Phrase Studio

A student picks a musical style and a seed, then listens to a newly sampled melody. The same controls also drive a random-note baseline so the audience can hear what learning adjacent notes contributes.

Run `python3 studio.py` from the checkout and open `http://127.0.0.1:8000` on the presenting computer. Use Python 3.9+ and a browser with WAV playback. Everything runs locally using the Python standard library and HTML audio. No package install, database, agent framework, or API key is required.

## Fifteen-minute demo

- **0–2 min:** Ask “If two generators use the same pitches, will they sound equally musical?” Introduce a student composer looking for a short idea.
- **2–5 min:** Show the diagram in [the design](DESIGN.md). Walk through the first bright phrase. After pitch 60 the training examples offer several possible successors. Repeated transitions get more chances in the draw.
- **5–9 min:** Compose bright, seed 7 and open the blind listening challenge. Play both clips to the end, ask for a show of hands, then select the class preference or a tie. Reveal the models, pitch contours and counts of familiar note pairs. Repeat with wistful, seed 21. Each visit shuffles A/B while keeping the two melodies reproducible. Check classroom speakers before presenting.
- **9–12 min:** Run `python3 evaluate.py`. Explain why a high transition score measures resemblance to training patterns and cannot establish listener preference.
- **12–15 min:** Invite questions. **Is it generative AI?** It estimates a conditional probability distribution from examples and samples sequences. **Why no LLM?** The output is pitches and the corpus is small enough to inspect directly. **Can it copy?** Yes. Short fragments recur and novelty needs a separate check.
