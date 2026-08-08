"""Check closure and inventory after eight-panel STEP export/re-import."""

from __future__ import annotations

from pathlib import Path
import sys

from build123d import import_step
from OCP.BRep import BRep_Tool


DEFAULT_STEP = Path("eight_panel_print_kit.step")


def _walk(shape):
    yield shape
    for child in getattr(shape, "children", []) or []:
        yield from _walk(child)


def _closed_single_solid(shape) -> bool:
    solids = shape.solids()
    shells = shape.shells()
    return (
        len(solids) == 1
        and len(shells) == 1
        and BRep_Tool.IsClosed_s(shells[0].wrapped)
        and shape.is_valid
    )


def _labeled(imported, prefix: str):
    return [
        shape
        for shape in _walk(imported)
        if str(getattr(shape, "label", "")).startswith(prefix)
    ]


def main():
    step_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_STEP
    imported = import_step(str(step_path))
    if len(imported.children) != 13:
        raise AssertionError(
            f"Expected 13 virtual plate modules, found {len(imported.children)}"
        )
    if len(imported.solids()) != 100:
        raise AssertionError(f"Expected 100 leaf solids, found {len(imported.solids())}")

    expected = {
        "playing_surface_body:": 8,
        "dark_square_inlay:": 32,
        "perimeter_body:": 8,
        "seam_bridge:": 16,
        "corner_cap:": 4,
    }
    report = {}
    for prefix, expected_count in expected.items():
        shapes = _labeled(imported, prefix)
        if len(shapes) != expected_count:
            raise AssertionError(
                f"{prefix} expected {expected_count}, found {len(shapes)}"
            )
        failures = [shape.label for shape in shapes if not _closed_single_solid(shape)]
        if failures:
            raise AssertionError(f"Invalid or open solids for {prefix}: {failures}")
        report[prefix.rstrip(":")] = len(shapes)

    print(f"{step_path}: closed STEP inventory passed: {report}")


if __name__ == "__main__":
    main()
