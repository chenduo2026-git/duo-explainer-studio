# Subtitles and audio

## Narration

- Generate one file per storyboard segment.
- Prefer a slightly brisk, conversational performance over an announcer cadence.
- Do not insert long pauses merely to match slide boundaries.
- Measure the generated file; never rely on requested duration.

## Bilingual ASS captions

Use Chinese as the primary line and English as a smaller secondary line. Translate meaning, not Chinese word order.

Recommended 1920x1080 baseline:

- Chinese: 48-56 px, semibold/bold.
- English: 27-31 px, regular, muted gray.
- Bottom safe margin: about 95-120 px.
- Dark translucent box or outline sufficient for contrast.
- Emphasize only 1-2 Chinese keywords per caption using the deck accent color and a modest size increase.
- Keep captions stable. Do not use per-character bouncing, karaoke motion, or constant color changes.
- Break long narration into phrase-level captions that follow breath and meaning.

Every caption time must fall inside its corresponding voice segment. Use the segment's real start from the timing manifest, then distribute phrases by actual delivery or verified listening—not by equal character count when speech rhythm differs.

If translation would be sent to an unspecified third-party service, obtain explicit consent first. Translation performed directly in the current model does not require a separate external transfer.

## Music and mix

Choose instrumental music with a simple arrangement and no competing lead melody. Match tempo and energy to the narration.

Useful starting targets:

- Narration: around -16 LUFS integrated, true peak below -1.5 dB.
- Music bed before ducking: about 10-14 dB below narration.
- Duck music during speech with a quick attack and 200-350 ms release.
- Fade music in over roughly 1 second and out over 2-3 seconds.

These are starting points, not substitutes for listening. If the user says the music is only meant to be felt, favor the lower end and preserve voice clarity.
