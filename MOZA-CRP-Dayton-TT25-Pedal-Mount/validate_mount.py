"""Deterministic validation for the perpendicular CRP/TT25 yoke mount."""

from __future__ import annotations

import json
from math import hypot, sqrt

from moza_crp_dayton_tt25_fit_check import (
    M8_BOLT_CLEARANCE_DIAMETER,
    M8_BOLT_HEAD_DIAMETER,
    M8_BOLT_HEAD_HEIGHT,
    M8_BOLT_LENGTH,
    M8_BOLT_NOMINAL_DIAMETER,
    M8_BOLT_SOCKET_AF,
    M8_BOLT_SOCKET_DEPTH,
    M8_NUT_AF,
    M8_NUT_THICKNESS,
    build_fit_details,
)
from moza_crp_dayton_tt25_mount import (
    CABLE_PASS_THROUGH_CENTER_X,
    CABLE_PASS_THROUGH_CENTER_Z,
    CABLE_PASS_THROUGH_DIAMETER,
    FORK_ARM_THICKNESS,
    FORK_INNER_SPAN,
    FORK_PIVOT_BOSS_DIAMETER,
    HOLDER_OUTER_DIAMETER,
    HOLDER_THICKNESS,
    PEDAL_MOUNT_WIDTH_ASSUMED,
    PEDAL_PIVOT_CLEARANCE_DIAMETER,
    PEDAL_SIDE_CLEARANCE,
    PIVOT_HEX_POCKET_AF,
    PIVOT_HEX_POCKET_DEPTH,
    PIVOT_NUT_SUPPORT_FLOOR,
    PUCK_CENTER_Y,
    PUCK_CENTER_Z,
    PUCK_NUT_POCKET_DEPTH,
    TT25_HOLDER_HOLE_DIAMETER,
    TT25_MOUNTING_HOLE_POSITIONS,
    TT25_REAR_COVER_RELIEF_DEPTH,
    TT25_REAR_COVER_RELIEF_DIAMETER,
    TT25_RELIEF_DIAMETER,
    _cylinder_x,
    _cylinder_y,
    build_holder_details,
)


def _volume(shape_or_shapes):
    if shape_or_shapes is None:
        return 0.0
    return sum(solid.volume for solid in shape_or_shapes.solids())


def _bounds(shape):
    bbox = shape.bounding_box()
    return {
        "min": [bbox.min.X, bbox.min.Y, bbox.min.Z],
        "max": [bbox.max.X, bbox.max.Y, bbox.max.Z],
        "size": [bbox.size.X, bbox.size.Y, bbox.size.Z],
    }


def main():
    details = build_holder_details()
    holder = details["holder"]
    fit = build_fit_details()
    fit_assembly = fit["final"]
    puck = fit["bare_puck"]
    pedal_reference = fit["pedal_reference"]
    pivot_nut = fit["pivot_nut"]
    right_receiver_test_nut = fit["right_receiver_test_nut"]
    pivot_bolt = fit["pivot_bolt"]
    hardware = fit["hardware"]

    ring_back_y = details["ring_back_y"]
    ring_front_y = details["ring_front_y"]
    carrier_relief_probe = _cylinder_y(
        TT25_RELIEF_DIAMETER / 2.0,
        ring_back_y - 1.0,
        ring_front_y + 1.0,
        z=PUCK_CENTER_Z,
    )
    rear_cover_probe = _cylinder_y(
        TT25_REAR_COVER_RELIEF_DIAMETER / 2.0,
        ring_back_y - 0.1,
        ring_back_y + TT25_REAR_COVER_RELIEF_DEPTH - 0.05,
        z=PUCK_CENTER_Z,
    )
    hole_probes = [
        _cylinder_y(
            TT25_HOLDER_HOLE_DIAMETER / 2.0,
            ring_back_y - 1.0,
            ring_front_y + 1.0,
            x=x,
            z=PUCK_CENTER_Z + local_z,
        )
        for x, local_z in TT25_MOUNTING_HOLE_POSITIONS
    ]
    cable_probe = _cylinder_y(
        CABLE_PASS_THROUGH_DIAMETER / 2.0,
        ring_back_y - 1.0,
        ring_front_y + 1.0,
        x=CABLE_PASS_THROUGH_CENTER_X,
        z=CABLE_PASS_THROUGH_CENTER_Z,
    )
    cable_inner_ligament = (
        PUCK_CENTER_Z
        - TT25_RELIEF_DIAMETER / 2.0
        - CABLE_PASS_THROUGH_CENTER_Z
        - CABLE_PASS_THROUGH_DIAMETER / 2.0
    )
    cable_outer_ligament = (
        CABLE_PASS_THROUGH_CENTER_Z
        - CABLE_PASS_THROUGH_DIAMETER / 2.0
        - (PUCK_CENTER_Z - HOLDER_OUTER_DIAMETER / 2.0)
    )
    lower_screw_pair = (
        TT25_MOUNTING_HOLE_POSITIONS[2],
        TT25_MOUNTING_HOLE_POSITIONS[5],
    )
    lower_screw_pair_midpoint_x = sum(
        x for x, _ in lower_screw_pair
    ) / len(lower_screw_pair)
    cable_to_screw_pair_midpoint_offset = abs(
        CABLE_PASS_THROUGH_CENTER_X - lower_screw_pair_midpoint_x
    )
    cable_left_arm_clearance = (
        CABLE_PASS_THROUGH_CENTER_X
        - CABLE_PASS_THROUGH_DIAMETER / 2.0
        + FORK_INNER_SPAN / 2.0
    )
    cable_right_arm_clearance = (
        FORK_INNER_SPAN / 2.0
        - CABLE_PASS_THROUGH_CENTER_X
        - CABLE_PASS_THROUGH_DIAMETER / 2.0
    )
    pivot_probe = _cylinder_x(
        PEDAL_PIVOT_CLEARANCE_DIAMETER / 2.0,
        details["left_outer_x"] - 1.0,
        details["right_outer_x"] + 1.0,
    )

    hole_center_radii = [hypot(x, z) for x, z in TT25_MOUNTING_HOLE_POSITIONS]
    minimum_outer_ligament = min(
        HOLDER_OUTER_DIAMETER / 2.0
        - radius
        - TT25_HOLDER_HOLE_DIAMETER / 2.0
        for radius in hole_center_radii
    )
    minimum_inner_ligament = min(
        radius
        - TT25_HOLDER_HOLE_DIAMETER / 2.0
        - TT25_RELIEF_DIAMETER / 2.0
        for radius in hole_center_radii
    )
    minimum_pivot_radial_ligament = (
        FORK_PIVOT_BOSS_DIAMETER / 2.0
        - PIVOT_HEX_POCKET_AF / sqrt(3.0)
    )

    left_nut_outside_receiver = _volume(
        pivot_nut.cut(details["left_hex_pocket"])
    )
    right_nut_outside_receiver = _volume(
        right_receiver_test_nut.cut(details["right_hex_pocket"])
    )
    bolt_holder_overlap = _volume(pivot_bolt.intersect(holder))
    bolt_nut_overlap = _volume(pivot_bolt.intersect(pivot_nut))
    bolt_pedal_overlap = _volume(pivot_bolt.intersect(pedal_reference))
    bolt_puck_overlap = _volume(pivot_bolt.intersect(puck))
    holder_puck_overlap = _volume(holder.intersect(puck))
    holder_pedal_overlap = _volume(holder.intersect(pedal_reference))
    threaded_axial_overlap = max(
        0.0,
        min(hardware["bolt_shaft_x_max"], hardware["nut_x_max"])
        - max(hardware["bolt_shaft_x_min"], hardware["nut_x_min"]),
    )

    result = {
        "valid": {
            "holder": holder.is_valid,
            "fit_assembly": fit_assembly.is_valid,
            "official_puck_reference": puck.is_valid,
            "pedal_reference": pedal_reference.is_valid,
            "pivot_nut_reference": pivot_nut.is_valid,
            "right_receiver_test_nut": right_receiver_test_nut.is_valid,
            "pivot_bolt_reference": pivot_bolt.is_valid,
        },
        "holder": {
            "solid_count": len(holder.solids()),
            "bbox_mm": _bounds(holder),
            "carrier_outer_diameter_mm": HOLDER_OUTER_DIAMETER,
            "carrier_thickness_y_mm": ring_front_y - ring_back_y,
            "carrier_center_yz_mm": [PUCK_CENTER_Y, PUCK_CENTER_Z],
            "central_relief_diameter_mm": TT25_RELIEF_DIAMETER,
            "central_relief_blocked_volume_mm3": _volume(
                holder.intersect(carrier_relief_probe)
            ),
            "rear_cover_relief_diameter_mm": TT25_REAR_COVER_RELIEF_DIAMETER,
            "rear_cover_relief_depth_mm": TT25_REAR_COVER_RELIEF_DEPTH,
            "rear_cover_relief_blocked_volume_mm3": _volume(
                holder.intersect(rear_cover_probe)
            ),
            "cable_pass_through_diameter_mm": CABLE_PASS_THROUGH_DIAMETER,
            "cable_pass_through_center_x_mm": CABLE_PASS_THROUGH_CENTER_X,
            "cable_pass_through_center_z_mm": CABLE_PASS_THROUGH_CENTER_Z,
            "cable_pass_through_blocked_volume_mm3": _volume(
                holder.intersect(cable_probe)
            ),
            "cable_pass_through_inner_ligament_mm": cable_inner_ligament,
            "cable_pass_through_outer_ligament_mm": cable_outer_ligament,
            "lower_screw_pair_midpoint_x_mm": lower_screw_pair_midpoint_x,
            "cable_to_lower_screw_pair_midpoint_offset_mm": (
                cable_to_screw_pair_midpoint_offset
            ),
            "cable_left_arm_clearance_mm": cable_left_arm_clearance,
            "cable_right_arm_clearance_mm": cable_right_arm_clearance,
        },
        "orientation": {
            "pedal_side_plane": "YZ",
            "puck_face_plane": "XZ",
            "included_angle_degrees": 90.0,
        },
        "puck_interface": {
            "mounting_hole_count": len(TT25_MOUNTING_HOLE_POSITIONS),
            "holder_hole_diameter_mm": TT25_HOLDER_HOLE_DIAMETER,
            "blocked_hole_probe_volumes_mm3": [
                _volume(holder.intersect(probe)) for probe in hole_probes
            ],
            "minimum_outer_ligament_mm": minimum_outer_ligament,
            "minimum_inner_ligament_mm": minimum_inner_ligament,
            "m3_nut_pocket_depth_mm": PUCK_NUT_POCKET_DEPTH,
            "installed_holder_puck_overlap_mm3": holder_puck_overlap,
        },
        "pedal_yoke": {
            "assumed_pedal_width_mm": PEDAL_MOUNT_WIDTH_ASSUMED,
            "side_clearance_total_mm": PEDAL_SIDE_CLEARANCE,
            "fork_inner_span_mm": FORK_INNER_SPAN,
            "fork_arm_thickness_mm": FORK_ARM_THICKNESS,
            "pivot_boss_diameter_mm": FORK_PIVOT_BOSS_DIAMETER,
            "pivot_clearance_diameter_mm": PEDAL_PIVOT_CLEARANCE_DIAMETER,
            "pivot_hole_blocked_volume_mm3": _volume(
                holder.intersect(pivot_probe)
            ),
            "installed_holder_pedal_overlap_mm3": holder_pedal_overlap,
            "hex_pocket_af_mm": PIVOT_HEX_POCKET_AF,
            "hex_pocket_depth_mm": PIVOT_HEX_POCKET_DEPTH,
            "nut_receiver_count": 2,
            "nut_support_floor_mm": PIVOT_NUT_SUPPORT_FLOOR,
            "minimum_pivot_radial_ligament_mm": minimum_pivot_radial_ligament,
            "left_nut_outside_receiver_mm3": left_nut_outside_receiver,
            "right_nut_outside_receiver_mm3": right_nut_outside_receiver,
        },
        "hardware": {
            "bolt_nominal_diameter_mm": M8_BOLT_NOMINAL_DIAMETER,
            "bolt_clearance_diameter_mm": M8_BOLT_CLEARANCE_DIAMETER,
            "bolt_length_mm": M8_BOLT_LENGTH,
            "bolt_head_diameter_mm": M8_BOLT_HEAD_DIAMETER,
            "bolt_head_height_mm": M8_BOLT_HEAD_HEIGHT,
            "bolt_socket_af_mm": M8_BOLT_SOCKET_AF,
            "bolt_socket_depth_mm": M8_BOLT_SOCKET_DEPTH,
            "nut_af_mm": M8_NUT_AF,
            "nut_thickness_mm": M8_NUT_THICKNESS,
            "threaded_axial_engagement_mm": threaded_axial_overlap,
            "reference_bolt_solid_count": len(pivot_bolt.solids()),
            "reference_nut_solid_count": len(pivot_nut.solids()),
            "reference_bolt_holder_overlap_mm3": bolt_holder_overlap,
            "reference_bolt_nut_overlap_mm3": bolt_nut_overlap,
            "reference_bolt_pedal_overlap_mm3": bolt_pedal_overlap,
            "reference_bolt_puck_overlap_mm3": bolt_puck_overlap,
        },
        "fit_assembly": {
            "top_level_occurrence_count": len(fit_assembly.children),
            "bbox_mm": _bounds(fit_assembly),
        },
    }

    assert all(result["valid"].values())
    assert result["holder"]["solid_count"] == 1
    assert abs(result["holder"]["carrier_thickness_y_mm"] - HOLDER_THICKNESS) < 1e-6
    assert result["holder"]["central_relief_blocked_volume_mm3"] < 1e-6
    assert result["holder"]["rear_cover_relief_blocked_volume_mm3"] < 1e-6
    assert result["holder"]["cable_pass_through_blocked_volume_mm3"] < 1e-6
    assert result["holder"]["cable_pass_through_inner_ligament_mm"] >= 3.5
    assert result["holder"]["cable_pass_through_outer_ligament_mm"] >= 3.5
    assert result["holder"]["cable_to_lower_screw_pair_midpoint_offset_mm"] < 1e-6
    assert result["holder"]["cable_left_arm_clearance_mm"] >= 5.0
    assert result["holder"]["cable_right_arm_clearance_mm"] >= 5.0
    assert result["orientation"]["included_angle_degrees"] == 90.0
    assert result["puck_interface"]["mounting_hole_count"] == 6
    assert all(
        volume < 1e-6
        for volume in result["puck_interface"]["blocked_hole_probe_volumes_mm3"]
    )
    assert result["puck_interface"]["minimum_outer_ligament_mm"] >= 2.0
    assert result["puck_interface"]["minimum_inner_ligament_mm"] >= 10.0
    assert result["puck_interface"]["installed_holder_puck_overlap_mm3"] < 1e-6
    assert result["pedal_yoke"]["fork_inner_span_mm"] > result["pedal_yoke"]["assumed_pedal_width_mm"]
    assert result["pedal_yoke"]["pivot_hole_blocked_volume_mm3"] < 1e-6
    assert result["pedal_yoke"]["installed_holder_pedal_overlap_mm3"] < 1e-6
    assert result["pedal_yoke"]["nut_support_floor_mm"] >= 4.0
    assert result["pedal_yoke"]["nut_receiver_count"] == 2
    assert result["pedal_yoke"]["minimum_pivot_radial_ligament_mm"] >= 8.0
    assert result["pedal_yoke"]["left_nut_outside_receiver_mm3"] < 1e-6
    assert result["pedal_yoke"]["right_nut_outside_receiver_mm3"] < 1e-6
    assert result["hardware"]["threaded_axial_engagement_mm"] >= 6.0
    assert result["hardware"]["reference_bolt_solid_count"] == 1
    assert result["hardware"]["reference_nut_solid_count"] == 1
    assert result["hardware"]["reference_bolt_holder_overlap_mm3"] < 1e-6
    assert result["hardware"]["reference_bolt_nut_overlap_mm3"] < 1e-6
    assert result["hardware"]["reference_bolt_pedal_overlap_mm3"] < 1e-6
    assert result["hardware"]["reference_bolt_puck_overlap_mm3"] < 1e-6
    assert result["fit_assembly"]["top_level_occurrence_count"] == 5

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
