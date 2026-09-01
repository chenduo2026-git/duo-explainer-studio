# Duo Explainer Studio

**Duo 讲解动画短视频全流程**

Duo Explainer Studio is a reusable Codex skill for turning a knowledge or finance topic into a finished 1-2 minute animated explainer video.

It covers the complete workflow:

1. Discuss and select the script framework.
2. Write a natural spoken script.
3. Build and lock the slide-by-slide storyboard.
4. Create an animated 1920x1080 HTML presentation.
5. Generate segmented narration from a confirmed voice.
6. Calculate timing from real audio durations.
7. Produce stable Chinese-English captions with highlighted keywords.
8. Add restrained background music with automatic voice ducking.
9. Record the HTML animation and compose the final MP4.
10. Verify visual layout, playback, captions, audio, and synchronization.

## Content-lock principle

The full narration, cover, closing slide, and every slide's on-screen content are locked before voice, subtitle, music, or video production begins. The cover and closing title remain independent unless the user explicitly requests a relationship between them.

## Install

Clone the repository into your personal Codex skills folder:

```bash
git clone https://github.com/chenduo2026-git/duo-explainer-studio.git ~/.codex/skills/duo-explainer-studio
```

Then invoke it with:

```text
Use $duo-explainer-studio to develop an animated explainer video, starting with the script framework.
```

中文调用示例：

```text
使用 $duo-explainer-studio，从讲解短视频的脚本框架开始，与我逐步确认并生成最终视频。
```

## Included tools

- `scripts/prepare_timing.py` — reads real narration durations, creates the timing manifest, and patches slide durations.
- `scripts/record_slides.mjs` — records the locked HTML presentation as a 1920x1080 WebM animation.
- `scripts/compose_video.py` — mixes narration and ducked background music, burns ASS captions, and exports H.264/AAC MP4.

The main workflow and production rules are defined in [`SKILL.md`](SKILL.md).

## License

MIT License. See [`LICENSE`](LICENSE).
