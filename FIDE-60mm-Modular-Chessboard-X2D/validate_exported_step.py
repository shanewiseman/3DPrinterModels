"""Validate slicer-critical solid closure after STEP export and re-import."""

from __future__ import annotations

from pathlib import Path
import sys

from build123d import import_step
from OCP.BRep import BRep_Tool


DEFAULT_STEP = Path("separated_print_kit.step")


def _walk(shape):
    yield shape
    for child in getattr(shape, "children", []) or []:
        yield from _walk(child)


def _is_closed_solid(shape) -> bool:
    solids = shape.solids()
    shells = shape.shells()
    closed_shells = [BRep_Tool.IsClosed_s(shell.wrapped) for shell in shells]
    return (
        len(solids) == 1
        and len(shells) == 1
        and closed_shells == [True]
        and shape.is_valid
    )


def main() -> None:
    step_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_STEP
    imported = import_step(str(step_path))
    if len(imported.children) != 9:
        raise AssertionError(
            f"Expected 9 virtual plate modules after STEP import, found "
            f"{len(imported.children)}"
        )

    playing_surface_bodies = [
        shape
        for shape in _walk(imported)
        if str(getattr(shape, "label", "")).startswith("playing_surface_body:")
    ]
    if len(playing_surface_bodies) != 4:
        raise AssertionError(
            f"Expected 4 playing-surface bodies, found "
            f"{len(playing_surface_bodies)}"
        )

    surface_failures = [
        str(surface.label)
        for surface in playing_surface_bodies
        if not _is_closed_solid(surface)
    ]
    for surface in playing_surface_bodies:
        print(
            f"{surface.label}: solids={len(surface.solids())}, "
            f"closed={_is_closed_solid(surface)}, valid={surface.is_valid}"
        )
    if surface_failures:
        raise AssertionError(
            f"STEP contains invalid playing-surface bodies: {surface_failures}"
        )

    dark_inlays = [
        shape
        for shape in _walk(imported)
        if str(getattr(shape, "label", "")).startswith("dark_square_inlay:")
    ]
    if len(dark_inlays) != 32:
        raise AssertionError(f"Expected 32 glue-in dark squares, found {len(dark_inlays)}")
    inlay_failures = []
    for inlay in dark_inlays:
        bounds = inlay.bounding_box()
        expected_size = (59.6, 59.6, 1.6)
        actual_size = (bounds.size.X, bounds.size.Y, bounds.size.Z)
        size_ok = all(
            abs(actual - expected) <= 1e-6
            for actual, expected in zip(actual_size, expected_size)
        )
        if not _is_closed_solid(inlay) or not size_ok:
            inlay_failures.append(str(inlay.label))
    print(
        f"dark_square_inlay: count={len(dark_inlays)}, "
        f"closed_and_sized={len(dark_inlays) - len(inlay_failures)}/32, "
        "size_mm=[59.6, 59.6, 1.6]"
    )
    if inlay_failures:
        raise AssertionError(f"STEP contains invalid dark-square inlays: {inlay_failures}")

    rail_bodies = [
        shape
        for shape in _walk(imported)
        if str(getattr(shape, "label", "")).startswith("perimeter_body:")
    ]
    if len(rail_bodies) != 8:
        raise AssertionError(f"Expected 8 perimeter bodies, found {len(rail_bodies)}")

    failures = []
    for body in rail_bodies:
        solids = body.solids()
        shells = body.shells()
        closed_shells = [BRep_Tool.IsClosed_s(shell.wrapped) for shell in shells]
        print(
            f"{body.label}: type={type(body).__name__}, solids={len(solids)}, "
            f"shells={len(shells)}, closed={closed_shells}, valid={body.is_valid}"
        )
        if len(solids) != 1 or len(shells) != 1 or closed_shells != [True] or not body.is_valid:
            failures.append(str(body.label))

    if failures:
        raise AssertionError(f"STEP contains non-closed perimeter bodies: {failures}")


if __name__ == "__main__":
    main()
