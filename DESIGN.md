# Design review

1. **Problem and users.** Beginning composers need a short, repeatable idea to audition during a lesson. Success means hearing a playable phrase and comparing it with a control. Playback must always require a listener action.
2. **Why generation.** Our five decision criteria are output diversity, suitability of examples, controllability, cost of mistakes, and measurable improvement over a baseline. Multiple melodies are valid, examples encode adjacent pitches, and a style and seed control sampling. A poor phrase costs seconds to discard. Compare a first-order Markov model against independent draws from the same style’s pitch frequencies. Neither prompting, retrieval nor fine-tuning is needed.
3. **Scope.** Two authored styles, one instrument, fixed rhythm and 16 notes. Unsupported style, mode or out-of-range seed returns HTTP 400. Lyrics, uploads and full arrangements are outside scope.
4. **Requirements.** Both modes produce four seconds of mono PCM. Equal inputs reproduce pitches. Target local generation under one second per request. Embedded phrases update on code release. Local execution has zero API cost and sends no inputs to a provider. The server logs request paths locally. Use only project-authored phrases and synthesized tones.
5. **Architecture.**

   ```mermaid
   flowchart LR
     UI[Browser controls] --> V[Validate style, mode and seed]
     P[Authored phrases] --> M[Count pitch transitions]
     P --> B[Pool individual notes]
     V --> S[Seeded sampler]
     M --> S
     B --> S
     S --> W[PCM synthesizer]
     W --> A[Browser audio player]
     S --> E[Count adjacent pairs seen in the style corpus]
     A --> VOTE[Blind A/B preference or tie]
     E --> R[Reveal models and pitch contours]
     VOTE --> R
   ```

   Validation bounds inputs. The two statistical paths support a controlled comparison. The seeded sampler supports replay and the synthesizer makes results audible offline.

   The challenge route renders both modes with the same style, seed and synthesizer, then independently shuffles presentation order. The browser enables voting after both clips end. The reveal explains the count of familiar adjacent pairs for each clip. Preferences last for the current page only. This provides classroom blinding; anyone inspecting the page source can see model labels.
6. **Failures.** A tiny corpus can repeat phrases. First-order context can produce aimless endings. Fixed duration bounds output but cannot guarantee quality. A pitch with no observed successor falls back to the style pool. Visible pitches also support discussion on a muted machine.
7. **Evaluation.** Cross both styles and modes with 20 seeds. Check lengths, determinism, WAV duration and observed-transition fractions. Gate the demo on passing assertions and a higher pooled transition fraction for learned generation. Target subsecond synthesis. Before presenting, ask three listeners to compare five randomized pairs each with mode hidden. Target at least 10 of 15 preferences for learned output. Record ties separately. Listening results are pending.
8. **Open questions.** Do listeners identify the intended mood? Ask them to label clips blind. Does the model replay long training fragments? Compare longest shared subsequences before enlarging the corpus. The instructor’s exact five lecture criteria were unavailable, so confirm the criteria in section 2 against class notes.
