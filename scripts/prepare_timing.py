#!/usr/bin/env python3
"""Build a real-audio timing manifest and optionally patch HTML slide durations."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


AUDIO_EXTENSIONS = {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav", ".webm"}


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def probe_duration(ffprobe: str, path: Path) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    duration = float(json.loads(result.stdout)["format"]["duration"])
    if duration <= 0:
        raise ValueError(f"Non-positive audio duration: {path}")
    return duration


def slide_tag_is_slide(tag: str) -> bool:
    match = re.search(r"\bclass\s*=\s*(['\"])(.*?)\1", tag, flags=re.I | re.S)
    return bool(match and "slide" in match.group(2).split())


def patch_html_durations(html_path: Path, durations_ms: list[int]) -> None:
    source = html_path.read_text(encoding="utf-8")
    tags = list(re.finditer(r"<section\b[^>]*>", source, flags=re.I | re.S))
    slide_tags = [match for match in tags if slide_tag_is_slide(match.group(0))]
    if len(slide_tags) != len(durations_ms):
        raise ValueError(
            f"Slide/audio count mismatch: {len(slide_tags)} slide tags vs {len(durations_ms)} audio files"
        )

    replacements: list[tuple[int, int, str]] = []
    for match, duration_ms in zip(slide_tags, durations_ms):
        tag = match.group(0)
        if re.search(r"\bdata-duration\s*=", tag, flags=re.I):
            new_tag = re.sub(
                r"(\bdata-duration\s*=\s*['\"])\d+(['\"])",
                rf"\g<1>{duration_ms}\2",
                tag,
                count=1,
                flags=re.I,
            )
        else:
            new_tag = tag[:-1] + f' data-duration="{duration_ms}">'
        replacements.append((match.start(), match.end(), new_tag))

    for start, end, new_tag in reversed(replacements):
        source = source[:start] + new_tag + source[end:]
    html_path.write_text(source, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice-dir", required=True, type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--initial-lead", type=float, default=0.20)
    parser.add_argument("--inter-gap", type=float, default=0.20)
    parser.add_argument("--voice-offset", type=float, default=0.10)
    parser.add_argument("--render-delay", type=float, default=0.10)
    parser.add_argument("--final-hold", type=float, default=0.60)
    parser.add_argument("--apply-html", action="store_true")
    args = parser.parse_args()

    voice_files = sorted(
        (path for path in args.voice_dir.iterdir() if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS),
        key=natural_key,
    )
    if not voice_files:
        raise SystemExit(f"No supported voice files found in {args.voice_dir}")
    if args.apply_html and not args.html:
        raise SystemExit("--apply-html requires --html")

    audio_durations = [probe_duration(args.ffprobe, path) for path in voice_files]
    slide_durations = [duration + args.inter_gap for duration in audio_durations]
    slide_durations[-1] = audio_durations[-1] + args.final_hold

    segments = []
    cumulative = 0.0
    for index, (path, audio_duration, slide_duration) in enumerate(
        zip(voice_files, audio_durations, slide_durations), start=1
    ):
        slide_start = 0.0 if index == 1 else args.render_delay + cumulative
        voice_start = args.initial_lead if index == 1 else slide_start + args.voice_offset
        segments.append(
            {
                "index": index,
                "voice_file": str(path.resolve()),
                "audio_duration": round(audio_duration, 6),
                "slide_start": round(slide_start, 6),
                "slide_duration": round(slide_duration, 6),
                "slide_duration_ms": int(round(slide_duration * 1000 / 10) * 10),
                "voice_start": round(voice_start, 6),
                "voice_end": round(voice_start + audio_duration, 6),
            }
        )
        cumulative += slide_duration

    manifest = {
        "version": 1,
        "initial_lead": args.initial_lead,
        "inter_gap": args.inter_gap,
        "voice_offset": args.voice_offset,
        "render_delay": args.render_delay,
        "final_hold": args.final_hold,
        "target_duration": round(args.render_delay + sum(slide_durations), 6),
        "record_duration": round(args.render_delay + sum(slide_durations) + 0.8, 6),
        "segments": segments,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.apply_html:
        patch_html_durations(args.html, [segment["slide_duration_ms"] for segment in segments])

    print(json.dumps({"segments": len(segments), "target_duration": manifest["target_duration"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
