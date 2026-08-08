"""Render the README chessboard rotation GIF from the assembled STEP model."""

from __future__ import annotations

import argparse
import json
from math import cos, pi, sin
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image


FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAMES_PER_AXIS = 25
FRAME_DURATION_MS = 80
CAMERA_TARGET = (0.0, 0.0, 5.8)
CAMERA_VECTOR = (650.0, -650.0, 500.0)


def _rotate_z(vector: tuple[float, float, float], angle: float):
    x, y, z = vector
    return (
        x * cos(angle) - y * sin(angle),
        x * sin(angle) + y * cos(angle),
        z,
    )


def _rotate_x(vector: tuple[float, float, float], angle: float):
    x, y, z = vector
    return (
        x,
        y * cos(angle) - z * sin(angle),
        y * sin(angle) + z * cos(angle),
    )


def _camera_output(path: Path, relative_position, up):
    return {
        "path": str(path),
        "width": FRAME_WIDTH,
        "height": FRAME_HEIGHT,
        "camera": {
            "position": [
                CAMERA_TARGET[0] + relative_position[0],
                CAMERA_TARGET[1] + relative_position[1],
                CAMERA_TARGET[2] + relative_position[2],
            ],
            "target": list(CAMERA_TARGET),
            "up": list(up),
            "zoom": 1.18,
        },
    }


def _render_job(input_step: Path, frame_directory: Path):
    outputs = []
    frame_index = 0
    for axis in ("z", "x"):
        for sample in range(FRAMES_PER_AXIS):
            angle = 2.0 * pi * sample / (FRAMES_PER_AXIS - 1)
            if axis == "z":
                position = _rotate_z(CAMERA_VECTOR, angle)
                up = (0.0, 0.0, 1.0)
            else:
                position = _rotate_x(CAMERA_VECTOR, angle)
                up = _rotate_x((0.0, 0.0, 1.0), angle)
            outputs.append(
                _camera_output(
                    frame_directory / f"frame_{frame_index:03d}.png",
                    position,
                    up,
                )
            )
            frame_index += 1

    return {
        "input": str(input_step),
        "mode": "view",
        "outputs": outputs,
        "appearance": {
            "background": {"type": "solid", "solidColor": "#f0f4f9"},
            "floor": {
                "mode": "none",
                "enabled": False,
                "grid": {"enabled": False},
            },
            "environment": {"enabled": False},
        },
        "display": {"mode": "rendered", "projection": "orthographic"},
        "render": {
            "lockFraming": True,
            "padding": 0.1,
            "sizeProfile": "orbit",
        },
    }


def _shared_palette(frames: list[Image.Image]):
    samples = frames[:: max(1, len(frames) // 10)]
    sample_width = 160
    sample_height = 120
    sheet = Image.new("RGB", (sample_width * len(samples), sample_height))
    for index, frame in enumerate(samples):
        preview = frame.resize((sample_width, sample_height), Image.Resampling.LANCZOS)
        sheet.paste(preview, (index * sample_width, 0))
    return sheet.quantize(colors=128, method=Image.Quantize.MEDIANCUT)


def _assemble_gif(frame_paths: list[Path], output_path: Path):
    rgb_frames = []
    for frame_path in frame_paths:
        with Image.open(frame_path) as image:
            rgb_frames.append(image.convert("RGB"))

    palette = _shared_palette(rgb_frames)
    gif_frames = [
        frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG)
        for frame in rgb_frames
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    gif_frames[0].save(
        output_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
        comment=b"Z-axis rotation followed by X-axis rotation",
    )


def main():
    project_root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=project_root / "eight_panel_chessboard_assembly.step",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "docs" / "chessboard_rotation.gif",
    )
    parser.add_argument(
        "--snapshot-cli",
        type=Path,
        default=Path.home() / ".agents" / "skills" / "cad" / "scripts" / "snapshot",
    )
    args = parser.parse_args()

    input_step = args.input.resolve()
    output_path = args.output.resolve()
    if not input_step.is_file():
        raise FileNotFoundError(f"STEP input does not exist: {input_step}")
    if not args.snapshot_cli.exists():
        raise FileNotFoundError(f"CAD snapshot CLI does not exist: {args.snapshot_cli}")

    with tempfile.TemporaryDirectory(prefix="chessboard-readme-animation-") as temp:
        temp_root = Path(temp)
        frame_directory = temp_root / "frames"
        frame_directory.mkdir()
        job_path = temp_root / "render_job.json"
        job_path.write_text(
            json.dumps(_render_job(input_step, frame_directory), indent=2),
            encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, str(args.snapshot_cli), "--job", str(job_path)],
            check=True,
            cwd=project_root,
        )
        frame_paths = sorted(frame_directory.glob("frame_*.png"))
        expected_frames = 2 * FRAMES_PER_AXIS
        if len(frame_paths) != expected_frames:
            raise RuntimeError(
                f"Expected {expected_frames} rendered frames, found {len(frame_paths)}"
            )
        _assemble_gif(frame_paths, output_path)

    with Image.open(output_path) as animation:
        saved_frame_count = animation.n_frames
    print(
        f"saved {saved_frame_count}-frame GIF from "
        f"{2 * FRAMES_PER_AXIS} rendered poses: {output_path} "
        f"({output_path.stat().st_size} bytes)"
    )


if __name__ == "__main__":
    main()
