# Fifteen-minute presentation

| Clock | Projector | Suggested words and action |
|---|---|---|
| 0–1 | Slide 1 | “If I give a computer C, E and G, can it finish my phrase and tell me why it chose the next note?” |
| 1–3 | Slide 2 | Introduce a beginner who can invent an opening but wants several continuations. Trace training prefixes → learned attention → next-pitch distribution → sampling → audio. Identify which decisions the composer still controls. |
| 3–6 | Workbench | Play the default arrangement. Click the first generated note. Read the displayed candidates and their probabilities. Read the attention weights on earlier notes. Switch to the context-count baseline using the same motif and seed, then switch back. Change only seed 7 to 8 and compare. |
| 6–8 | Workbench | Enter A4 G4 E4, wistful, 84 BPM, seed 21. Generate, play and download the WAV. Explain that chords, bass and rhythmic templates are arranged rules. Slide 3 has prerecorded outputs if the server fails. |
| 8–10 | Blind listening lab | Play both sketches through. Ask “Which sounds more connected?” Take a show of hands, choose the preference or tie, and reveal. Discuss even if baseline wins. |
| 10–12 | Slides 4–5 | Describe the whole-phrase holdout, numerical improvement and corpus size. Explain what a listening trial would measure. |
| 12–15 | Questions | Invite one implementation and one design question. Share the GitHub link from the README. |

**How does it learn?** Hide each next note in turn and train the attention head to predict it. The last pitch queries the preceding context. A weighted mix of learned values produces next-pitch probabilities. The count baseline instead looks for matching pitch suffixes.

**Where is the AI?** In the learned conditional probability distribution used to generate the continuation. Rhythm patterns, accompaniment and waveform synthesis are programmed. The note inspector shows their interaction.

**Why evaluate on held-out phrases?** Testing only training transitions rewards memorization. Removing a whole phrase prevents its adjacent pairs from being included through another position in the same phrase. Similar fragments can still occur in other phrases.

**What if the audience prefers random?** Report it. Preference is subjective, and local next-note prediction does not capture whole-song structure.

**What would you improve with more time?** Collect more rights-cleared phrases, measure repeated fragments and compare learned rhythm against the current templates in a blinded study.

**Two-hour preparation budget:** 15 min to launch and check speakers, 25 min to trace one generated note and run the evaluations, 25 min to practice both examples, 15 min to assign speaker handoffs, 30 min for two timed rehearsals, and 10 min to verify the submission link and backup audio.
