"""Validate the individual manufacturing-oriented STEP export set."""

from __future__ import annotations

from math import isclose
from pathlib import Path

from build123d import import_step

from printable_parts.sources.printable_part_source import (
    EXPECTED_EXPORT_SIZES,
    PART_IDS,
    build_printable_part,
)
from x2d_dual_ams_mount_geometry import PRINT_PART_LIMIT


PROJECT_DIR = Path(__file__).resolve().parent
EXPORT_DIR = PROJECT_DIR / "printable_parts"
TOL = 1.0e-5


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS  {message}")


def close(a: float, b: float) -> bool:
    return isclose(a, b, abs_tol=TOL, rel_tol=0.0)


def main() -> None:
    check(len(PART_IDS) == 14, "catalog contains 14 printable object exports")
    for part_id in PART_IDS:
        path = EXPORT_DIR / f"{part_id}.step"
        check(path.is_file() and path.stat().st_size > 0, f"{path.name} exists")

        imported = import_step(path)
        solids = list(imported.solids())
        check(imported.is_valid, f"{path.name} is a valid B-rep")
        check(len(solids) == 1, f"{path.name} contains exactly one solid")

        bounds = imported.bounding_box()
        actual_size = (bounds.size.X, bounds.size.Y, bounds.size.Z)
        expected_size = EXPECTED_EXPORT_SIZES[part_id]
        check(
            all(close(actual, expected) for actual, expected in zip(actual_size, expected_size)),
            f"{path.name} has expected print-orientation bounds "
            f"{expected_size[0]:.1f} x {expected_size[1]:.1f} x {expected_size[2]:.1f} mm",
        )
        check(close(bounds.center().X, 0.0), f"{path.name} is centered on X=0")
        check(close(bounds.center().Y, 0.0), f"{path.name} is centered on Y=0")
        check(close(bounds.min.Z, 0.0), f"{path.name} rests on Z=0")
        check(
            max(actual_size) <= PRINT_PART_LIMIT + TOL,
            f"{path.name} fits the 252 mm single-part envelope",
        )

        source = build_printable_part(part_id)
        check(
            close(imported.volume, source.volume),
            f"{path.name} preserves source solid volume",
        )

    print("PRINTABLE PART VALIDATION COMPLETE")


if __name__ == "__main__":
    main()
