"""Deterministic validation for the perpendicular CRP/TT25 yoke mount."""

from __future__ import annotations

import json
from math import hypot, sqrt

from moza_crp_dayton_tt25_fit_check import (
    M6_BOLT_CLEARANCE_DIAMETER,
    M6_BOLT_HEAD_DIAMETER,
    M6_BOLT_HEAD_HEIGHT,
    M6_BOLT_LENGTH,
    M6_BOLT_NOMINAL_DIAMETER,
    M6_BOLT_SOCKET_AF,
    M6_BOLT_SOCKET_DEPTH,
    M6_NUT_AF,
    M6_NUT_THICKNESS,
    PUCK_M3_RECOMMENDED_LENGTH,
    PUCK_M3_STACK_TO_NUT_OUTER_FACE,
    TT25_MOUNTING_LUG_THICKNESS,
    build_fit_details,
)
from moza_crp_dayton_tt25_m6_insert import (
    INSERT_FLANGE_DIAMETER,
    INSERT_FLANGE_THICKNESS,
    INSERT_NUT_SUPPORT_FLOOR,
    INSERT_PILOT_AF,
    INSERT_PILOT_LENGTH,
    INSERT_TEST_NUT_THICKNESS,
    INSERT_TOTAL_HEIGHT,
    build_insert_details,
)
from moza_crp_dayton_tt25_mount import (
    CABLE_PASS_THROUGH_CENTER_X,
    CABLE_PASS_THROUGH_CENTER_Z,
    CABLE_PASS_THROUGH_DIAMETER,
    CRP2_ATTACHMENT_WIDTH,
    CRP2_INTERNAL_HEX_AF,
    FORK_ARM_THICKNESS,
    FORK_INNER_SPAN,
    FORK_PIVOT_BOSS_DIAMETER,
    FORK_PIVOT_BOSS_Y_DEPTH,
    FORK_RING_LOBE_CENTER_Y,
    FORK_RING_LOBE_CENTER_Z,
    FORK_RING_LOBE_DIAMETER,
    FORK_RING_LOBE_REAR_CLEARANCE,
    HOLDER_OUTER_DIAMETER,
    HOLDER_THICKNESS,
    PEDAL_BACK_PLANE_Y,
    PEDAL_BACK_TO_PIVOT_FRAME_OUTER,
    PEDAL_PIVOT_CLEARANCE_DIAMETER,
    PEDAL_SIDE_CLEARANCE,
    PIVOT_FRAME_OUTER_Y,
    PIVOT_HEX_POCKET_AF,
    PIVOT_HEX_POCKET_DEPTH,
    PIVOT_NUT_SUPPORT_FLOOR,
    PUCK_CENTER_Y,
    PUCK_CENTER_Z,
    PUCK_NUT_POCKET_DEPTH,
    TT25_HOLDER_HOLE_DIAMETER,
    TT25_MOUNTING_HOLE_DIAMETER,
    TT25_MOUNTING_HOLE_POSITIONS,
    TT25_REAR_COVER_RELIEF_DEPTH,
    TT25_REAR_COVER_RELIEF_DIAMETER,
    TT25_RELIEF_DIAMETER,
    TT25_ROTATION_ABOUT_INSTALLED_Z_DEGREES,
    TT25_SOURCE_MOUNTING_HOLE_POSITIONS,
    _cylinder_x,
    _cylinder_y,
    _hex_prism_x,
    build_holder_details,
)
from moza_crp_dayton_tt25_print_set import build_print_set_details


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
    insert_details = build_insert_details()
    insert = insert_details["insert"]
    print_set_details = build_print_set_details()
    print_set = print_set_details["final"]

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
    puck_bbox = puck.bounding_box()
    official_puck_hole_probes = [
        _cylinder_y(
            TT25_MOUNTING_HOLE_DIAMETER / 2.0 - 0.05,
            puck_bbox.min.Y - 1.0,
            puck_bbox.max.Y + 1.0,
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
    cable_left_arm_nominal_clearance = (
        CABLE_PASS_THROUGH_CENTER_X
        - CABLE_PASS_THROUGH_DIAMETER / 2.0
        + FORK_INNER_SPAN / 2.0
    )
    cable_right_arm_nominal_clearance = (
        FORK_INNER_SPAN / 2.0
        - CABLE_PASS_THROUGH_CENTER_X
        - CABLE_PASS_THROUGH_DIAMETER / 2.0
    )
    cable_left_arm_relief_depth = max(0.0, -cable_left_arm_nominal_clearance)
    cable_right_arm_relief_depth = max(0.0, -cable_right_arm_nominal_clearance)
    minimum_local_arm_thickness_after_cable_relief = min(
        FORK_ARM_THICKNESS - cable_left_arm_relief_depth,
        FORK_ARM_THICKNESS - cable_right_arm_relief_depth,
    )
    pivot_probe = _cylinder_x(
        PEDAL_PIVOT_CLEARANCE_DIAMETER / 2.0,
        details["left_outer_x"] - 1.0,
        details["right_outer_x"] + 1.0,
    )
    pedal_hex_probe = _hex_prism_x(
        CRP2_INTERNAL_HEX_AF,
        -CRP2_ATTACHMENT_WIDTH / 2.0 - 0.1,
        CRP2_ATTACHMENT_WIDTH + 0.2,
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
    minimum_pivot_flat_ligament = min(
        PEDAL_BACK_PLANE_Y - PIVOT_HEX_POCKET_AF / 2.0,
        PIVOT_HEX_POCKET_AF / 2.0 - PIVOT_FRAME_OUTER_Y,
    )
    minimum_pivot_material_ligament = min(
        minimum_pivot_radial_ligament,
        minimum_pivot_flat_ligament,
    )

    production_arms = []
    for arm_name in ("left_arm", "right_arm"):
        production_arm = details[arm_name]
        for cutter_name in (
            "carrier_center_relief",
            "rear_cover_relief",
            "cable_pass_through",
            "puck_nut_pockets",
        ):
            production_arm = production_arm.cut(details[cutter_name])
        production_arms.append(production_arm)
    arm_ring_contact_volumes = tuple(
        _volume(arm.intersect(details["ring_blank"]))
        for arm in production_arms
    )
    receiver_y_bounds = tuple(
        (
            details[name].bounding_box().min.Y,
            details[name].bounding_box().max.Y,
        )
        for name in ("left_receiver_boss", "right_receiver_boss")
    )
    arm_pedal_side_max_ys = tuple(
        details[name].bounding_box().max.Y
        for name in ("left_arm", "right_arm")
    )
    ring_lobe_rear_edge_y = (
        FORK_RING_LOBE_CENTER_Y - FORK_RING_LOBE_DIAMETER / 2.0
    )
    ring_lobe_to_carrier_back_clearance = ring_lobe_rear_edge_y - ring_back_y

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
    insert_pilot_outside_measured_hex = _volume(
        insert_details["pilot"].cut(insert_details["measured_hex_envelope"])
    )
    insert_test_nut_outside_pocket = _volume(
        insert_details["test_nut"].cut(insert_details["nut_pocket"])
    )
    insert_bore_blocked_volume = _volume(
        insert.intersect(insert_details["bore"])
    )
    print_holder_insert_overlap = _volume(
        print_set_details["holder"].intersect(print_set_details["insert"])
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
            "keyed_m6_nut_insert": insert.is_valid,
            "two_object_print_set": print_set.is_valid,
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
            "cable_left_arm_relief_depth_mm": cable_left_arm_relief_depth,
            "cable_right_arm_relief_depth_mm": cable_right_arm_relief_depth,
            "minimum_local_arm_thickness_after_cable_relief_mm": (
                minimum_local_arm_thickness_after_cable_relief
            ),
        },
        "orientation": {
            "pedal_side_plane": "YZ",
            "puck_face_plane": "XZ",
            "included_angle_degrees": 90.0,
            "puck_rotation_about_installed_z_degrees": (
                TT25_ROTATION_ABOUT_INSTALLED_Z_DEGREES
            ),
            "logo_direction": "negative Y, outward from pedal pivot",
        },
        "puck_interface": {
            "mounting_hole_count": len(TT25_MOUNTING_HOLE_POSITIONS),
            "rotated_mounting_hole_centers_xz_mm": [
                [x, PUCK_CENTER_Z + local_z]
                for x, local_z in TT25_MOUNTING_HOLE_POSITIONS
            ],
            "holder_hole_diameter_mm": TT25_HOLDER_HOLE_DIAMETER,
            "blocked_hole_probe_volumes_mm3": [
                _volume(holder.intersect(probe)) for probe in hole_probes
            ],
            "official_puck_blocked_hole_probe_volumes_mm3": [
                _volume(puck.intersect(probe))
                for probe in official_puck_hole_probes
            ],
            "minimum_outer_ligament_mm": minimum_outer_ligament,
            "minimum_inner_ligament_mm": minimum_inner_ligament,
            "m3_nut_pocket_depth_mm": PUCK_NUT_POCKET_DEPTH,
            "official_lug_thickness_mm": TT25_MOUNTING_LUG_THICKNESS,
            "m3_stack_to_nut_outer_face_mm": (
                PUCK_M3_STACK_TO_NUT_OUTER_FACE
            ),
            "recommended_m3_screw_length_mm": PUCK_M3_RECOMMENDED_LENGTH,
            "recommended_m3_tip_projection_mm": (
                PUCK_M3_RECOMMENDED_LENGTH
                - PUCK_M3_STACK_TO_NUT_OUTER_FACE
            ),
            "installed_holder_puck_overlap_mm3": holder_puck_overlap,
        },
        "pedal_yoke": {
            "measured_crp2_attachment_width_mm": CRP2_ATTACHMENT_WIDTH,
            "measured_crp2_internal_hex_af_mm": CRP2_INTERNAL_HEX_AF,
            "side_clearance_total_mm": PEDAL_SIDE_CLEARANCE,
            "fork_inner_span_mm": FORK_INNER_SPAN,
            "fork_arm_thickness_mm": FORK_ARM_THICKNESS,
            "pivot_boss_diameter_mm": FORK_PIVOT_BOSS_DIAMETER,
            "pivot_boss_y_depth_mm": FORK_PIVOT_BOSS_Y_DEPTH,
            "pedal_back_plane_y_mm": PEDAL_BACK_PLANE_Y,
            "pivot_frame_outer_y_mm": PIVOT_FRAME_OUTER_Y,
            "pedal_back_to_pivot_frame_outer_mm": (
                PEDAL_BACK_TO_PIVOT_FRAME_OUTER
            ),
            "receiver_y_bounds_mm": receiver_y_bounds,
            "arm_pedal_side_max_ys_mm": arm_pedal_side_max_ys,
            "pivot_clearance_diameter_mm": PEDAL_PIVOT_CLEARANCE_DIAMETER,
            "pivot_hole_blocked_volume_mm3": _volume(
                holder.intersect(pivot_probe)
            ),
            "pedal_hex_opening_blocked_volume_mm3": _volume(
                pedal_reference.intersect(pedal_hex_probe)
            ),
            "installed_holder_pedal_overlap_mm3": holder_pedal_overlap,
            "hex_pocket_af_mm": PIVOT_HEX_POCKET_AF,
            "hex_pocket_depth_mm": PIVOT_HEX_POCKET_DEPTH,
            "nut_receiver_count": 2,
            "nut_support_floor_mm": PIVOT_NUT_SUPPORT_FLOOR,
            "minimum_pivot_radial_ligament_mm": minimum_pivot_radial_ligament,
            "minimum_pivot_flat_ligament_mm": minimum_pivot_flat_ligament,
            "minimum_pivot_material_ligament_mm": (
                minimum_pivot_material_ligament
            ),
            "ring_lobe_diameter_mm": FORK_RING_LOBE_DIAMETER,
            "ring_lobe_center_yz_mm": [
                FORK_RING_LOBE_CENTER_Y,
                FORK_RING_LOBE_CENTER_Z,
            ],
            "ring_lobe_rear_clearance_mm": FORK_RING_LOBE_REAR_CLEARANCE,
            "ring_lobe_to_carrier_back_clearance_mm": (
                ring_lobe_to_carrier_back_clearance
            ),
            "arm_ring_contact_volumes_mm3": arm_ring_contact_volumes,
            "left_nut_outside_receiver_mm3": left_nut_outside_receiver,
            "right_nut_outside_receiver_mm3": right_nut_outside_receiver,
        },
        "hardware": {
            "bolt_nominal_diameter_mm": M6_BOLT_NOMINAL_DIAMETER,
            "bolt_clearance_diameter_mm": M6_BOLT_CLEARANCE_DIAMETER,
            "bolt_length_mm": M6_BOLT_LENGTH,
            "bolt_head_diameter_mm": M6_BOLT_HEAD_DIAMETER,
            "bolt_head_height_mm": M6_BOLT_HEAD_HEIGHT,
            "bolt_socket_af_mm": M6_BOLT_SOCKET_AF,
            "bolt_socket_depth_mm": M6_BOLT_SOCKET_DEPTH,
            "nut_af_mm": M6_NUT_AF,
            "nut_thickness_mm": M6_NUT_THICKNESS,
            "threaded_axial_engagement_mm": threaded_axial_overlap,
            "reference_bolt_solid_count": len(pivot_bolt.solids()),
            "reference_nut_solid_count": len(pivot_nut.solids()),
            "reference_bolt_holder_overlap_mm3": bolt_holder_overlap,
            "reference_bolt_nut_overlap_mm3": bolt_nut_overlap,
            "reference_bolt_pedal_overlap_mm3": bolt_pedal_overlap,
            "reference_bolt_puck_overlap_mm3": bolt_puck_overlap,
        },
        "keyed_m6_nut_insert": {
            "solid_count": len(insert.solids()),
            "bbox_mm": _bounds(insert),
            "pilot_af_mm": INSERT_PILOT_AF,
            "pilot_length_mm": INSERT_PILOT_LENGTH,
            "flange_diameter_mm": INSERT_FLANGE_DIAMETER,
            "flange_thickness_mm": INSERT_FLANGE_THICKNESS,
            "nut_pocket_af_mm": PIVOT_HEX_POCKET_AF,
            "nut_pocket_depth_mm": PIVOT_HEX_POCKET_DEPTH,
            "nut_support_floor_mm": INSERT_NUT_SUPPORT_FLOOR,
            "test_nut_thickness_mm": INSERT_TEST_NUT_THICKNESS,
            "total_height_mm": INSERT_TOTAL_HEIGHT,
            "pilot_outside_measured_hex_mm3": (
                insert_pilot_outside_measured_hex
            ),
            "test_nut_outside_pocket_mm3": insert_test_nut_outside_pocket,
            "bore_blocked_volume_mm3": insert_bore_blocked_volume,
        },
        "print_set": {
            "top_level_occurrence_count": len(print_set.children),
            "solid_count": len(print_set.solids()),
            "bbox_mm": _bounds(print_set),
            "holder_insert_overlap_mm3": print_holder_insert_overlap,
            "minimum_z_mm": print_set.bounding_box().min.Z,
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
    assert (
        result["holder"]["minimum_local_arm_thickness_after_cable_relief_mm"]
        >= 3.5
    )
    assert result["orientation"]["included_angle_degrees"] == 90.0
    assert (
        result["orientation"]["puck_rotation_about_installed_z_degrees"]
        == 180.0
    )
    assert TT25_MOUNTING_HOLE_POSITIONS == tuple(
        (-x, local_z)
        for x, local_z in TT25_SOURCE_MOUNTING_HOLE_POSITIONS
    )
    assert result["puck_interface"]["mounting_hole_count"] == 6
    assert result["puck_interface"]["official_lug_thickness_mm"] == 8.5
    assert result["puck_interface"]["m3_stack_to_nut_outer_face_mm"] == 17.0
    assert result["puck_interface"]["recommended_m3_screw_length_mm"] == 18.0
    assert (
        0.5
        <= result["puck_interface"]["recommended_m3_tip_projection_mm"]
        <= 1.5
    )
    assert all(
        volume < 1e-6
        for volume in result["puck_interface"]["blocked_hole_probe_volumes_mm3"]
    )
    assert all(
        volume < 1e-6
        for volume in result["puck_interface"][
            "official_puck_blocked_hole_probe_volumes_mm3"
        ]
    )
    assert result["puck_interface"]["minimum_outer_ligament_mm"] >= 2.0
    assert result["puck_interface"]["minimum_inner_ligament_mm"] >= 10.0
    assert result["puck_interface"]["installed_holder_puck_overlap_mm3"] < 1e-6
    assert result["pedal_yoke"]["measured_crp2_attachment_width_mm"] == 8.0
    assert result["pedal_yoke"]["measured_crp2_internal_hex_af_mm"] == 10.0
    assert result["pedal_yoke"]["fork_inner_span_mm"] == 8.6
    assert result["pedal_yoke"]["side_clearance_total_mm"] == 0.6
    assert result["pedal_yoke"]["pivot_boss_y_depth_mm"] == 20.0
    assert result["pedal_yoke"]["pedal_back_plane_y_mm"] == 10.0
    assert result["pedal_yoke"]["pivot_frame_outer_y_mm"] == -10.0
    assert (
        result["pedal_yoke"]["pedal_back_to_pivot_frame_outer_mm"]
        == 20.0
    )
    assert all(
        abs(y_min - PIVOT_FRAME_OUTER_Y) < 1e-6
        and abs(y_max - PEDAL_BACK_PLANE_Y) < 1e-6
        for y_min, y_max in result["pedal_yoke"]["receiver_y_bounds_mm"]
    )
    assert all(
        abs(max_y - PEDAL_BACK_PLANE_Y) < 1e-6
        for max_y in result["pedal_yoke"]["arm_pedal_side_max_ys_mm"]
    )
    assert result["pedal_yoke"]["pivot_hole_blocked_volume_mm3"] < 1e-6
    assert result["pedal_yoke"]["pedal_hex_opening_blocked_volume_mm3"] < 1e-6
    assert result["pedal_yoke"]["installed_holder_pedal_overlap_mm3"] < 1e-6
    assert result["pedal_yoke"]["nut_support_floor_mm"] >= 4.0
    assert result["pedal_yoke"]["nut_receiver_count"] == 2
    assert result["pedal_yoke"]["minimum_pivot_material_ligament_mm"] >= 4.5
    assert result["pedal_yoke"]["ring_lobe_diameter_mm"] == 28.0
    assert abs(
        result["pedal_yoke"]["ring_lobe_to_carrier_back_clearance_mm"]
        - result["pedal_yoke"]["ring_lobe_rear_clearance_mm"]
    ) < 1e-6
    assert all(
        contact_volume >= 500.0
        for contact_volume in result["pedal_yoke"][
            "arm_ring_contact_volumes_mm3"
        ]
    )
    assert result["pedal_yoke"]["left_nut_outside_receiver_mm3"] < 1e-6
    assert result["pedal_yoke"]["right_nut_outside_receiver_mm3"] < 1e-6
    assert result["hardware"]["bolt_nominal_diameter_mm"] == 6.0
    assert result["hardware"]["nut_af_mm"] == 10.0
    assert result["hardware"]["threaded_axial_engagement_mm"] >= 5.0
    assert result["hardware"]["reference_bolt_solid_count"] == 1
    assert result["hardware"]["reference_nut_solid_count"] == 1
    assert result["hardware"]["reference_bolt_holder_overlap_mm3"] < 1e-6
    assert result["hardware"]["reference_bolt_nut_overlap_mm3"] < 1e-6
    assert result["hardware"]["reference_bolt_pedal_overlap_mm3"] < 1e-6
    assert result["hardware"]["reference_bolt_puck_overlap_mm3"] < 1e-6
    assert result["keyed_m6_nut_insert"]["solid_count"] == 1
    assert abs(
        result["keyed_m6_nut_insert"]["bbox_mm"]["size"][2]
        - result["keyed_m6_nut_insert"]["total_height_mm"]
    ) < 1e-6
    assert result["keyed_m6_nut_insert"]["pilot_af_mm"] == 9.6
    assert result["keyed_m6_nut_insert"]["nut_pocket_af_mm"] == 10.4
    assert result["keyed_m6_nut_insert"]["nut_support_floor_mm"] >= 1.5
    assert result["keyed_m6_nut_insert"]["pilot_outside_measured_hex_mm3"] < 1e-6
    assert result["keyed_m6_nut_insert"]["test_nut_outside_pocket_mm3"] < 1e-6
    assert result["keyed_m6_nut_insert"]["bore_blocked_volume_mm3"] < 1e-6
    assert result["print_set"]["top_level_occurrence_count"] == 2
    assert result["print_set"]["solid_count"] == 2
    assert result["print_set"]["holder_insert_overlap_mm3"] < 1e-6
    assert abs(result["print_set"]["minimum_z_mm"]) < 1e-6
    assert result["fit_assembly"]["top_level_occurrence_count"] == 5

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
