# Final QA

Do not report completion until all applicable checks pass.

## Structural

- MP4 exists and is non-empty.
- H.264 video, AAC audio, 1920x1080, 16:9, broadly playable pixel format.
- Duration matches the timing manifest within about 0.1 seconds.
- Previous finished output was preserved before replacement.

## Visual

- Inspect a contact sheet with at least one settled frame from every slide.
- Inspect exact opening and closing frames separately.
- No blank frame, stale local edit, overflow, overlap, missing font, or visible editor control.
- Cover and closing title match the locked storyboard independently.

## Sync

- Check start, middle, and end of every segment.
- Narration never begins before its visual anchor appears.
- Captions reproduce the spoken claim and stay within the matching voice segment.
- Page gaps feel like natural breathing, normally about 0.18-0.28 seconds.
- No old narration or caption survives after a retime.

## Audio

- Listen to opening, one dense middle segment, two page transitions, and the closing.
- Narration remains clear on laptop speakers and headphones.
- Music is audible but does not mask consonants; ducking recovers smoothly.
- No clipping, abrupt music cut, long unintended silence, or doubled voice.

## Delivery report

Report the final file, duration, resolution, narration voice, caption language, music treatment, and a compact `Final sync check`. Mention any remaining uncertainty honestly.
