"""Remove the separately modeled inner perimeter wall from the imported lid."""

from pathlib import Path

from build123d import Solid, import_step


SOURCE_STEP_FILENAME = "arduino_giga_r1_enclosure_lid_original.step"
EXPECTED_SOLID_COUNT = 2


def _contains_xy(outer: Solid, inner: Solid) -> bool:
    outer_box = outer.bounding_box()
    inner_box = inner.bounding_box()
    return (
        inner_box.min.X > outer_box.min.X
        and inner_box.max.X < outer_box.max.X
        and inner_box.min.Y > outer_box.min.Y
        and inner_box.max.Y < outer_box.max.Y
    )


def gen_step() -> Solid:
    source_path = Path(__file__).with_name(SOURCE_STEP_FILENAME)
    imported = import_step(source_path)
    solids = sorted(imported.solids(), key=lambda solid: solid.volume, reverse=True)

    if len(solids) != EXPECTED_SOLID_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_SOLID_COUNT} imported solids, found {len(solids)}"
        )

    lid_body, inner_wall = solids
    lid_box = lid_body.bounding_box()
    wall_box = inner_wall.bounding_box()
    if not (
        _contains_xy(lid_body, inner_wall)
        and wall_box.min.Z > lid_box.min.Z
        and wall_box.max.Z < lid_box.max.Z
    ):
        raise ValueError("The smaller imported solid does not match the inner-wall envelope")

    # The inner perimeter wall is a separate solid in the source STEP. Returning
    # only the primary lid body preserves all fused plate, cutout, and post geometry.
    lid_body.label = "arduino_giga_r1_enclosure_lid_inner_wall_removed"
    return lid_body
