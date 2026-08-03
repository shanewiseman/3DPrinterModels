"""Geometric validation for the separate CRP2 ringless-yoke fixture."""

from __future__ import annotations

import json

from moza_crp_dayton_tt25_mount import (
    FORK_ARM_THICKNESS,
    FORK_INNER_SPAN,
    FORK_PIVOT_BOSS_DIAMETER,
    FORK_PIVOT_BOSS_Y_DEPTH,
    FORK_RING_LOBE_CENTER_Y,
    FORK_RING_LOBE_CENTER_Z,
    FORK_RING_LOBE_DIAMETER,
    PEDAL_BACK_PLANE_Y,
    PEDAL_PIVOT_CLEARANCE_DIAMETER,
    PUCK_CENTER_Z,
    PIVOT_FRAME_OUTER_Y,
    PIVOT_HEX_POCKET_AF,
    PIVOT_HEX_POCKET_DEPTH,
    PIVOT_NUT_SUPPORT_FLOOR,
    _cylinder_x,
    _cylinder_y,
)
from moza_crp_dayton_tt25_pedal_mount_fit_fixture import (
    FIXTURE_RING_SEGMENT_SIDE_MARGIN,
    FIXTURE_RING_SEGMENT_Z_MAX,
    build_fixture_details,
)


def _bbox(shape):
    bbox = shape.bounding_box()
    return {
        "min": [bbox.min.X, bbox.min.Y, bbox.min.Z],
        "max": [bbox.max.X, bbox.max.Y, bbox.max.Z],
        "size": [bbox.size.X, bbox.size.Y, bbox.size.Z],
    }


def _volume(shape):
    if shape is None:
        return 0.0
    return sum(solid.volume for solid in shape.solids())


def validate():
    details = build_fixture_details()
    fixture_installed = details["fixture_installed"]
    fixture_print = details["fixture_print"]
    fixture_print_bbox = fixture_print.bounding_box()
    installed_gap = details["right_inner_x"] - details["left_inner_x"]
    left_profile_bbox = details["left_interface_profile"].bounding_box()
    left_arm_x_min = details["left_inner_x"] - FORK_ARM_THICKNESS
    right_arm_x_max = details["right_inner_x"] + FORK_ARM_THICKNESS
    left_lobe_probe = _cylinder_x(
        2.0,
        left_arm_x_min + 0.5,
        left_arm_x_min + 2.5,
        y=FORK_RING_LOBE_CENTER_Y,
        z=FORK_RING_LOBE_CENTER_Z,
    )
    right_lobe_probe = _cylinder_x(
        2.0,
        right_arm_x_max - 2.5,
        right_arm_x_max - 0.5,
        y=FORK_RING_LOBE_CENTER_Y,
        z=FORK_RING_LOBE_CENTER_Z,
    )
    bridge_probe = _cylinder_y(
        1.0,
        details["ring_back_y"] + 0.5,
        details["ring_front_y"] - 0.5,
        x=0.0,
        z=14.5,
    )

    result = {
        "fixture": {
            "valid": fixture_print.is_valid,
            "solid_count": len(fixture_print.solids()),
            "print_bbox_mm": _bbox(fixture_print),
            "print_min_z_mm": fixture_print_bbox.min.Z,
        },
        "production_interface": {
            "installed_inner_span_mm": installed_gap,
            "block_thickness_mm": details["block_thickness"],
            "profile_y_bounds_mm": [left_profile_bbox.min.Y, left_profile_bbox.max.Y],
            "profile_z_height_mm": left_profile_bbox.size.Z,
            "pivot_bore_diameter_mm": PEDAL_PIVOT_CLEARANCE_DIAMETER,
            "hex_pocket_af_mm": PIVOT_HEX_POCKET_AF,
            "hex_pocket_depth_mm": PIVOT_HEX_POCKET_DEPTH,
            "nut_support_floor_mm": PIVOT_NUT_SUPPORT_FLOOR,
            "left_pivot_bore_blocked_volume_mm3": _volume(
                fixture_installed.intersect(details["left_pivot_bore"])
            ),
            "right_pivot_bore_blocked_volume_mm3": _volume(
                fixture_installed.intersect(details["right_pivot_bore"])
            ),
            "left_hex_pocket_blocked_volume_mm3": _volume(
                fixture_installed.intersect(details["left_hex_pocket"])
            ),
            "right_hex_pocket_blocked_volume_mm3": _volume(
                fixture_installed.intersect(details["right_hex_pocket"])
            ),
        },
        "partial_ring_connection": {
            "connected_solid_count": len(fixture_installed.solids()),
            "full_ring_omitted": (
                fixture_installed.bounding_box().max.Z
                <= FIXTURE_RING_SEGMENT_Z_MAX + 1e-6
            ),
            "ring_segment_valid": details["ring_segment"].is_valid,
            "ring_segment_volume_mm3": _volume(details["ring_segment"]),
            "ring_segment_bbox_mm": _bbox(details["ring_segment"]),
            "ring_segment_side_margin_mm": FIXTURE_RING_SEGMENT_SIDE_MARGIN,
            "lobe_diameter_mm": FORK_RING_LOBE_DIAMETER,
            "lobe_center_y_mm": details["ring_lobe_center_y"],
            "lobe_center_z_mm": details["ring_lobe_center_z"],
            "bridge_probe_missing_volume_mm3": _volume(
                bridge_probe.cut(fixture_installed)
            ),
            "left_lobe_probe_missing_volume_mm3": _volume(
                left_lobe_probe.cut(fixture_installed)
            ),
            "right_lobe_probe_missing_volume_mm3": _volume(
                right_lobe_probe.cut(fixture_installed)
            ),
            "installed_bbox_mm": _bbox(fixture_installed),
        },
    }

    fixture = result["fixture"]
    interface = result["production_interface"]
    assert fixture["valid"]
    assert fixture["solid_count"] == 1
    assert abs(fixture["print_min_z_mm"]) < 1e-6

    assert abs(interface["installed_inner_span_mm"] - FORK_INNER_SPAN) < 1e-6
    assert abs(interface["profile_y_bounds_mm"][0] - PIVOT_FRAME_OUTER_Y) < 1e-6
    assert abs(interface["profile_y_bounds_mm"][1] - PEDAL_BACK_PLANE_Y) < 1e-6
    assert abs(
        interface["profile_y_bounds_mm"][1]
        - interface["profile_y_bounds_mm"][0]
        - FORK_PIVOT_BOSS_Y_DEPTH
    ) < 1e-6
    assert abs(
        interface["profile_z_height_mm"] - FORK_PIVOT_BOSS_DIAMETER
    ) < 1e-6
    assert interface["pivot_bore_diameter_mm"] == 6.6
    assert interface["hex_pocket_af_mm"] == 10.4
    assert interface["hex_pocket_depth_mm"] == 5.2
    assert interface["nut_support_floor_mm"] == 4.0
    assert interface["left_pivot_bore_blocked_volume_mm3"] < 1e-6
    assert interface["right_pivot_bore_blocked_volume_mm3"] < 1e-6
    assert interface["left_hex_pocket_blocked_volume_mm3"] < 1e-6
    assert interface["right_hex_pocket_blocked_volume_mm3"] < 1e-6
    connection = result["partial_ring_connection"]
    assert connection["connected_solid_count"] == 1
    assert connection["full_ring_omitted"]
    assert connection["ring_segment_valid"]
    assert connection["ring_segment_volume_mm3"] > 0.0
    assert connection["lobe_diameter_mm"] == 28.0
    assert connection["lobe_center_y_mm"] == FORK_RING_LOBE_CENTER_Y
    assert connection["lobe_center_z_mm"] == FORK_RING_LOBE_CENTER_Z
    assert connection["bridge_probe_missing_volume_mm3"] < 1e-6
    assert connection["left_lobe_probe_missing_volume_mm3"] < 1e-6
    assert connection["right_lobe_probe_missing_volume_mm3"] < 1e-6
    assert connection["installed_bbox_mm"]["min"][1] < PIVOT_FRAME_OUTER_Y
    expected_segment_width = (
        details["right_outer_x"]
        - details["left_outer_x"]
        + 2.0 * FIXTURE_RING_SEGMENT_SIDE_MARGIN
    )
    assert abs(
        connection["ring_segment_bbox_mm"]["size"][0]
        - expected_segment_width
    ) < 1e-6
    return result


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
    print("PEDAL MOUNT FIT FIXTURE VALIDATION PASSED")
