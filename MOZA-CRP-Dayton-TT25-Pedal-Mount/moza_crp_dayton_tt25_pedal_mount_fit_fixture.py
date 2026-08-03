"""Print-ready CRP2 partial-ring yoke for a lower-material fit check.

This separate fixture reuses the production yoke's complete left and right
arms, including the pivot receivers, reinforced lever profiles, and 28 mm
ring-junction lobes. A clipped section of the exact production ring connects
both lobes and holds their installed spacing; the remainder of the 106 mm
speaker-carrier ring is omitted.
"""

from __future__ import annotations

from build123d import Align, Axis, Box, Color, Location

from moza_crp_dayton_tt25_mount import (
    BOOLEAN_OVERSHOOT,
    FORK_RING_LOBE_CENTER_Z,
    FORK_RING_LOBE_DIAMETER,
    HOLDER_OUTER_DIAMETER,
    PUCK_CENTER_Z,
    _single_solid,
    build_holder_details,
)


FIXTURE_RING_SEGMENT_SIDE_MARGIN = 4.0
FIXTURE_RING_SEGMENT_Z_MIN = (
    PUCK_CENTER_Z - HOLDER_OUTER_DIAMETER / 2.0
)
FIXTURE_RING_SEGMENT_Z_MAX = (
    FORK_RING_LOBE_CENTER_Z + FORK_RING_LOBE_DIAMETER / 2.0
)
FIXTURE_COLOR = Color(0.86, 0.42, 0.10)


def _build_ring_connection_segment(holder_details):
    """Retain only the production ring material surrounding both lobes."""
    x_min = (
        holder_details["left_outer_x"]
        - FIXTURE_RING_SEGMENT_SIDE_MARGIN
    )
    x_max = (
        holder_details["right_outer_x"]
        + FIXTURE_RING_SEGMENT_SIDE_MARGIN
    )
    y_min = holder_details["ring_back_y"] - BOOLEAN_OVERSHOOT
    y_max = holder_details["ring_front_y"] + BOOLEAN_OVERSHOOT
    z_min = FIXTURE_RING_SEGMENT_Z_MIN - BOOLEAN_OVERSHOOT
    z_max = FIXTURE_RING_SEGMENT_Z_MAX
    clip = Box(
        x_max - x_min,
        y_max - y_min,
        z_max - z_min,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((x_min, y_min, z_min)))
    segment = _single_solid(
        holder_details["ring_blank"].intersect(clip),
        "partial production ring connection segment",
    )
    return segment, {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "z_min": z_min,
        "z_max": z_max,
    }


def _settle_ring_face_down(part):
    rotated = part.rotate(Axis.X, 90.0)
    bbox = rotated.bounding_box()
    return rotated.moved(Location((0.0, 0.0, -bbox.min.Z)))


def build_fixture_details():
    holder_details = build_holder_details()
    ring_segment, ring_segment_clip = _build_ring_connection_segment(
        holder_details
    )

    fixture_blank = _single_solid(
        ring_segment.fuse(holder_details["left_arm"])
        .fuse(holder_details["right_arm"])
        .fuse(holder_details["left_receiver_boss"])
        .fuse(holder_details["right_receiver_boss"]),
        "connected partial-ring yoke fixture blank",
    )

    # Apply all production cuts that intersect the retained arms, lobes, or
    # local ring section so this is an exact subset of the complete holder.
    fixture_installed = _single_solid(
        fixture_blank.cut(holder_details["pivot_bore"])
        .cut(holder_details["left_hex_pocket"])
        .cut(holder_details["right_hex_pocket"])
        .cut(holder_details["puck_nut_pockets"])
        .cut(holder_details["carrier_center_relief"])
        .cut(holder_details["rear_cover_relief"])
        .cut(holder_details["cable_pass_through"]),
        "finished connected partial-ring yoke fixture",
    )
    fixture_installed.label = "connected_partial_ring_yoke_fit_fixture"
    fixture_installed.color = FIXTURE_COLOR

    fixture_print = _settle_ring_face_down(fixture_installed)
    fixture_print.label = "connected_partial_ring_yoke_fit_fixture"
    fixture_print.color = FIXTURE_COLOR

    return {
        "final": fixture_print,
        "fixture_print": fixture_print,
        "fixture_installed": fixture_installed,
        "fixture_blank": fixture_blank,
        "ring_segment": ring_segment,
        "ring_segment_clip": ring_segment_clip,
        "left_pivot_bore": holder_details["pivot_bore"],
        "right_pivot_bore": holder_details["pivot_bore"],
        "left_hex_pocket": holder_details["left_hex_pocket"],
        "right_hex_pocket": holder_details["right_hex_pocket"],
        "left_interface_profile": holder_details["left_receiver_boss"],
        "right_interface_profile": holder_details["right_receiver_boss"],
        "left_outer_x": holder_details["left_outer_x"],
        "left_inner_x": holder_details["left_inner_x"],
        "right_inner_x": holder_details["right_inner_x"],
        "right_outer_x": holder_details["right_outer_x"],
        "block_thickness": (
            holder_details["left_inner_x"] - holder_details["left_outer_x"]
        ),
        "ring_lobe_center_y": holder_details["ring_lobe_center_y"],
        "ring_lobe_center_z": holder_details["ring_lobe_center_z"],
        "ring_back_y": holder_details["ring_back_y"],
        "ring_front_y": holder_details["ring_front_y"],
    }


def gen_step():
    return build_fixture_details()["final"]
