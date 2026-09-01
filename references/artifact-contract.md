# Artifact and HTML contract

## Project structure

Keep source and generated artifacts separate:

```text
<project>/
  <slug>-script.md
  <slug>-storyboard.md
  <slug>-slides.html
  <slug>-timing.json
  <slug>-bilingual.ass
  voice/
  audio/
  render/
  qa/
```

## HTML presentation contract

The HTML deck must satisfy the `frontend-slides` skill and these video-specific requirements:

- Single self-contained HTML file with inline CSS and JavaScript.
- Fixed 1920x1080 stage; slides use `.slide`, `.active`, and `.visible`.
- One `.slide` per locked storyboard row unless a deliberate multi-slide beat is documented.
- Every slide has `data-duration="<milliseconds>"`.
- `?render=1` hides controls/editing UI and starts automatic playback after about 100 ms.
- Render mode must ignore stale `localStorage` text edits so the file is authoritative.
- Auto playback reads each slide's `data-duration` and stops after the final slide.
- Use CSS/inline SVG for visuals when possible; no runtime CDN dependency that can fail during recording.
- Include reduced-motion support for ordinary viewing, but record with normal motion.

Recommended render hook:

```js
if (new URLSearchParams(location.search).get('render') === '1') {
  document.body.classList.add('render-mode');
  setTimeout(() => deck.startAuto(), 100);
}
```

## Timing manifest

`scripts/prepare_timing.py` writes JSON containing:

- real duration and path of every voice asset;
- slide start and duration;
- voice placement start;
- target total duration;
- configured initial lead, gap, final hold, and render delay.

The order of `.slide` elements, voice files, manifest rows, and ASS segment groups must match exactly.

## Recording

Use `scripts/record_slides.mjs` after the timing manifest has patched the deck. Record slightly beyond the manifest duration; the composition step trims precisely.

If Playwright or Chromium paths differ, locate the workspace-bundled dependency/runtime rather than installing an unverified browser. A sandboxed browser launch may require explicit approval.
