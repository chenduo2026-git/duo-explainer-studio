---
name: duo-explainer-studio
description: Develop a 1-2 minute Chinese knowledge or finance short video from script-framework discussion through a locked script and storyboard, animated HTML slides, segmented narration, bilingual emphasis captions, background music, synchronized composition, export, and playback QA. Use when the user wants the complete script-to-video pipeline; do not use for ordinary PPT-only work or footage-led talking-head editing.
---

# Duo Explainer Studio

Turn an idea into a finished 16:9 short video through explicit content gates. The default deliverable is an editable single-file HTML presentation plus an MP4 containing the same animation, narration, Chinese-English captions, and restrained background music.

## Required companion skills

Load these only when their phase begins:

- Use `frontend-slides` for the HTML presentation.
- Use `chatcut:voice` for voice selection or TTS, and read its video-sync reference.
- Use `chatcut:music` when generating original background music.
- Use `browser:control-in-app-browser` only when authenticated browser download or visible local-page testing is needed.

If the user explicitly names another writing skill, use it during the script phase without changing factual claims.

## Workflow and gates

1. **Frame the video.** Establish topic, audience, intended platform, approximate 60-120 second duration, aspect ratio, and desired effect. Infer already-known choices instead of re-asking them.
2. **Discuss the framework.** Produce only the content spine first: hook, misconception or tension, core answer, 3-5 reasoning beats, example or analogy, and closing thought. Keep competing structures visible until the user chooses one.
3. **Write the spoken script.** After the framework is accepted, write natural spoken Chinese. Prefer short sentences, concrete analogies, contrast, one light punchline, and a decisive close. Preserve numbers and claims. Avoid lecture tone and unexplained jargon.
4. **Create the storyboard.** Map one narration segment to one slide or intentional multi-slide beat. Include narration, on-screen text, visual anchor, emphasis words, and estimated duration.
5. **Lock content before production.** Ask the user to approve the full narration and every slide's content. Do not generate final voice, subtitles, music, or recorded animation until this gate passes. If wording changes later, mark all affected downstream timing rows stale and rebuild them.
6. **Build the HTML deck.** Use `frontend-slides`, follow the fixed 1920x1080 stage, and implement the render contract in [references/artifact-contract.md](references/artifact-contract.md). The cover comes from the locked storyboard. Never derive or replace the cover with the closing-slide title unless the user explicitly requests that separate creative decision.
7. **Generate segmented narration.** Use one audio asset per storyboard segment. Use the user's confirmed voice; otherwise follow the voice-audition flow. Generate only after mapping each line to its visual segment. Read every real audio duration.
8. **Rebuild timing from real audio.** Run `scripts/prepare_timing.py` to calculate slide durations and voice starts, patch the HTML, and save a timing manifest. Default to 0.18-0.28 seconds between segments, about 0.20 seconds before the first voice, and about 0.50-0.80 seconds of final hold.
9. **Author bilingual subtitles.** Base timing on the manifest and actual speech, not estimates. Keep subtitles stable; emphasize only selected Chinese keywords. Follow [references/subtitles-and-audio.md](references/subtitles-and-audio.md).
10. **Add music.** Generate or use a user-provided instrumental bed suited to the pacing. Keep it clearly below narration and duck it during speech. Do not spend generation credits on variants the user did not request.
11. **Record and compose.** Record the `?render=1` HTML with `scripts/record_slides.mjs`, then combine picture, segmented narration, music, and ASS subtitles with `scripts/compose_video.py`.
12. **Verify before delivery.** Follow [references/qa.md](references/qa.md). Open the final MP4 for playback only after file, visual, sync, subtitle, and audio checks pass. Preserve the prior finished MP4 as a backup when replacing it.

## Production invariants

- One authoritative script and storyboard. Do not maintain conflicting text in chat, HTML, subtitles, and voice prompts.
- One visual anchor per narration segment; no equal-duration splitting by guess.
- The PPT content-lock gate precedes all costly or timing-sensitive generation.
- A visual retime invalidates affected narration and caption placement; a narration rewrite invalidates its slide duration and subtitles.
- Aim for conversational continuity. Page boundaries are visual transitions, not long audio pauses.
- Keep the HTML editable and the MP4 distribution-ready.
- Do not claim completion from a successful render alone; playback and representative-frame QA are required.

## Output set

Use a dedicated project folder and deliver:

- `<slug>-script.md`
- `<slug>-storyboard.md`
- `<slug>-slides.html`
- `<slug>-timing.json`
- `<slug>-bilingual.ass`
- `voice/01.* ... voice/NN.*`
- `<slug>-bgm.*`
- `<slug>-visuals.webm`
- `<slug>-video.mp4`
- `<slug>-qa-contact-sheet.jpg`

Read [references/editorial-workflow.md](references/editorial-workflow.md) while developing the framework, script, and storyboard. Read [references/artifact-contract.md](references/artifact-contract.md) when building or recording the HTML. Read [references/subtitles-and-audio.md](references/subtitles-and-audio.md) for captions and mix choices. Read [references/qa.md](references/qa.md) for final verification.
