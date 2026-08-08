"""Shared builders and print-orientation transforms for individual STEP files."""

from __future__ import annotations

from functools import partial

from build123d import Axis

from x2d_dual_ams_mount_geometry import (
    BRACKET_DROP,
    BRACKET_THICKNESS,
    BRACKET_Y_CENTERS,
    BRIDGE_CENTER_BOSS_HEIGHT,
    BRIDGE_DEPTH,
    BRIDGE_HALF_OUTER_X,
    SHELF_DEPTH,
    SHELF_RIB_DEPTH,
    SHELF_SPAN,
    SHELF_THICKNESS,
    SIDE_PAD_DEPTH,
    SIDE_PAD_HEIGHT,
    SIDE_PAD_THICKNESS,
    make_bracket,
    make_bridge_segment,
    make_shelf,
    make_side_pad,
)


FRONT_Y, REAR_Y = BRACKET_Y_CENTERS

# Each tuple is (zero-argument builder, optional print-orientation axis, angle).
PART_SPECS = {
    "left_shelf": (partial(make_shelf, -1), None, 0.0),
    "right_shelf": (partial(make_shelf, 1), None, 0.0),
    "left_front_bracket": (partial(make_bracket, -1, FRONT_Y), Axis.X, 90.0),
    "left_rear_bracket": (partial(make_bracket, -1, REAR_Y), Axis.X, 90.0),
    "right_front_bracket": (partial(make_bracket, 1, FRONT_Y), Axis.X, 90.0),
    "right_rear_bracket": (partial(make_bracket, 1, REAR_Y), Axis.X, 90.0),
    "front_tie_left_half": (partial(make_bridge_segment, "front", -1), None, 0.0),
    "front_tie_right_half": (partial(make_bridge_segment, "front", 1), None, 0.0),
    "rear_tie_left_half": (partial(make_bridge_segment, "rear", -1), None, 0.0),
    "rear_tie_right_half": (partial(make_bridge_segment, "rear", 1), None, 0.0),
    "left_front_side_pad": (partial(make_side_pad, -1, FRONT_Y), Axis.Y, 90.0),
    "left_rear_side_pad": (partial(make_side_pad, -1, REAR_Y), Axis.Y, 90.0),
    "right_front_side_pad": (partial(make_side_pad, 1, FRONT_Y), Axis.Y, 90.0),
    "right_rear_side_pad": (partial(make_side_pad, 1, REAR_Y), Axis.Y, 90.0),
}

PART_IDS = tuple(PART_SPECS)

SHELF_EXPORT_SIZE = (SHELF_SPAN, SHELF_DEPTH, SHELF_THICKNESS + SHELF_RIB_DEPTH)
BRACKET_EXPORT_SIZE = (SHELF_SPAN, BRACKET_DROP, BRACKET_THICKNESS)
TIE_EXPORT_SIZE = (BRIDGE_HALF_OUTER_X, BRIDGE_DEPTH, BRIDGE_CENTER_BOSS_HEIGHT)
PAD_EXPORT_SIZE = (SIDE_PAD_HEIGHT, SIDE_PAD_DEPTH, SIDE_PAD_THICKNESS)

EXPECTED_EXPORT_SIZES = {
    **{part_id: SHELF_EXPORT_SIZE for part_id in ("left_shelf", "right_shelf")},
    **{
        part_id: BRACKET_EXPORT_SIZE
        for part_id in (
            "left_front_bracket",
            "left_rear_bracket",
            "right_front_bracket",
            "right_rear_bracket",
        )
    },
    **{
        part_id: TIE_EXPORT_SIZE
        for part_id in (
            "front_tie_left_half",
            "front_tie_right_half",
            "rear_tie_left_half",
            "rear_tie_right_half",
        )
    },
    **{
        part_id: PAD_EXPORT_SIZE
        for part_id in (
            "left_front_side_pad",
            "left_rear_side_pad",
            "right_front_side_pad",
            "right_rear_side_pad",
        )
    },
}


def build_printable_part(part_id: str):
    """Build one part, apply its print orientation, and place it on Z=0."""
    try:
        builder, rotation_axis, rotation_angle = PART_SPECS[part_id]
    except KeyError as exc:
        raise ValueError(f"Unknown printable part: {part_id}") from exc

    shape = builder()
    if rotation_axis is not None:
        shape = shape.rotate(rotation_axis, rotation_angle)

    bounds = shape.bounding_box()
    shape = shape.translate((-bounds.center().X, -bounds.center().Y, -bounds.min.Z))
    shape.label = f"{part_id}_print_oriented"
    return shape
