# Teach yourself Phrase Studio in ten minutes

## 1. Play it before you explain it

From the repository folder run `python3 studio.py` (Windows: `py -3 studio.py`). Open `http://127.0.0.1:8000`. Keep **Bright · C4 E4 G4 · 108 BPM · seed 7 · Causal self-attention**. Play the audio, then click note four. The peach notes are the opening you supplied. The mint notes are the continuation. The number in C4 identifies the octave; C5 is one octave higher.

## 2. Explain training with three notes

Take the start of one teaching phrase, C4 → E4 → G4. During training, C4 is the input and E4 is the target. Next, C4 and E4 are the input and G4 is the target. Each eight-note phrase produces seven such examples. The model trains separately on the bright and wistful examples. Cross-entropy penalizes assigning low probability to the observed target. Small gradient updates change the model's parameters. In the app training is deterministic and cached, so changing the variation seed changes the composition without retraining the model.

## 3. Read the note inspector aloud

For the default example, the fourth note is C5. There are two different sets of percentages on screen.

| Question | What the workbench shows |
|---|---|
| Which earlier positions supplied information? | Approximately 1% C4, 3% E4, 96% G4. These are attention weights over **input positions**. |
| What could the model play next? | After chord weighting, E4 has probability 64.6% and C5 has 16.7%. These are sampling probabilities over **output pitches**. |

The latest pitch supplies a query. It scores learned keys for up to four prior pitches, with a learned bias for each relative position. Softmax turns the scores into weights that sum to one. The model mixes learned value vectors in those proportions and applies another softmax to produce pitch probabilities. On a beat the arranger doubles the weight of chord tones and normalizes again. A seeded draw then chose C5. Sampling lets a less likely continuation occur. Append C5 and repeat to get the following pitch. “Causal” means each prediction sees only the notes available before its target.

**Try it:** Change only seed 7 to 8. Your opening survives and the arrangement can vary. Restore seed 7 to reproduce it. Then select **Context-count baseline**. This generator looks for matching pitch suffixes in the teaching phrases and counts their successors. Compare the inspector on the same opening.

## 4. Connect the algorithm to the application

| Open this file | Find this part of your explanation |
|---|---|
| `attention.py` | `PitchHead.forward` computes context and output probabilities. `update` and `train` learn keys, values and relative biases. |
| `arranger.py` | `arrange` keeps the motif, samples new pitches and places them in bars. `mix` turns the three voices into PCM audio and packages it as WAV. |
| `studio.py` and `workbench.html` | The browser sends controls to a local Python HTTP endpoint and receives the same timed notes used for playback plus the audio and inspection data. |
| `check_arranger.py` | Whole-phrase holdout compares three predictors. Run it to reproduce the numbers on the results slide. |

## 5. Answer the likely viva questions

- **Is this GPT?** It implements one causal self-attention head from scratch over eight pitch tokens. The syllabus connection is the attention mechanism and next-token prediction. GPT uses a much larger stack of transformer components.
- **Which part is generated?** The continuation pitches are sampled from learned distributions. The opening is copied from the user. Chords, available rhythms, bass and synthesis are programmed.
- **What does 2.190 bits per note mean?** On unseen bright phrases, attention assigned the true next note a better probability on average than either count baseline. More confident correct predictions cost fewer bits. This is a prediction score, not a percentage of listeners who liked the song.
- **Is the listening lab testing the attention head?** It compares a simpler first-order sketch model against random draws with the same pitch pool. Use the workbench and held-out report for claims about attention. Collect actual listener votes before claiming a preference.
- **What is the main weakness?** Each style has nine short phrases. Similar fragments may recur even across held-out phrases. A stronger follow-up would test on new composers and compare equally arranged outputs with model identities hidden.

**Practice check:** Close this file. Explain how C4 E4 G4 can lead to C5 even when E4 has the largest probability. If you can distinguish the input weights, the output probabilities and the seeded draw, you can teach the central idea.
