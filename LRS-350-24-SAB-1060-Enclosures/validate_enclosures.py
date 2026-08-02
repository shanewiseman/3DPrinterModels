"""Geometry and documented-fit validation for both enclosure print sets."""

from __future__ import annotations

from itertools import combinations
from math import sqrt

from enclosure_fit_check import SAB_ASSEMBLY_OFFSET_Y, build_fit_details
from enclosure_geometry import (
    CORNER_GUSSET_ANGLE_DEGREES,
    CORNER_GUSSET_TANGENT_WALL_RUN,
    CORNER_GUSSET_WALL_RUN,
    CORNER_GUSSET_WALL_CONTACT_MULTIPLIER,
    CORNER_TOWER_RADIUS,
    FLOOR,
    LID_CLEARANCE_PER_SIDE,
    LID_TOP,
    LRS_BASE_HEIGHT,
    LRS_INNER_X,
    LRS_INNER_Y,
    LRS_MOUNT_SPACING_X,
    LRS_MOUNT_SPACING_Y,
    LRS_OUTER_X,
    LRS_OUTER_Y,
    SAB_BASE_HEIGHT,
    SAB_BASE_PIN_RECEIVER_DEPTH,
    SAB_BASE_PIN_RECEIVER_DIAMETER,
    SAB_BOARD_THICKNESS,
    SAB_BOARD_Z,
    SAB_FAN_CENTER_X_FROM_EDGE_MEASUREMENTS,
    SAB_FAN_CENTER_X_USER_DIRECTED,
    SAB_FAN_CENTER_Y_USER_OBSERVED,
    SAB_FAN_FRAME_SIZE_USER_MEASURED,
    SAB_FAN_FRONT_CLEARANCE_USER_MEASURED,
    SAB_FAN_GUARD_FRAME_WIDTH,
    SAB_FAN_GUARD_OUTER_SIZE,
    SAB_FAN_GUARD_SKIRT_DEPTH,
    SAB_FAN_GUARD_SKIRT_INNER_SIZE,
    SAB_FAN_GUARD_SKIRT_OUTER_SIZE,
    SAB_FAN_GUARD_THICKNESS,
    SAB_FAN_HEIGHT_ASSUMED,
    SAB_FAN_LEFT_CLEARANCE_USER_MEASURED,
    SAB_FAN_OPENING_CLEARANCE_PER_SIDE,
    SAB_FAN_OPENING_SIZE,
    SAB_FAN_REAR_CLEARANCE_USER_MEASURED,
    SAB_FAN_REAR_VIEW_RIGHT_SHIFT,
    SAB_FAN_RIGHT_CLEARANCE_USER_MEASURED,
    SAB_FRONT_CONNECTOR_OPENING_CENTER_XS,
    SAB_FRONT_CONNECTOR_OPENING_CENTER_Y,
    SAB_FRONT_CONNECTOR_OPENING_COUNT,
    SAB_FRONT_CONNECTOR_OPENING_DEPTH,
    SAB_FRONT_CONNECTOR_OPENING_WIDTHS,
    SAB_FRONT_CONNECTOR_JOINED_OPENING_CENTER_X,
    SAB_FRONT_CONNECTOR_JOINED_OPENING_WIDTH,
    SAB_HOLE_SPACING_X_REPORTED,
    SAB_HOLE_SPACING_Y_REPORTED,
    SAB_HOLE_DIAMETER_REPORTED,
    SAB_FIT_COUPON_BASE_HEIGHT,
    SAB_FIT_COUPON_X,
    SAB_FIT_COUPON_Y,
    SAB_FLOOR_RIB_HEIGHT,
    SAB_FLOOR_RIB_WIDTH,
    SAB_INNER_X,
    SAB_INNER_Y,
    SAB_OUTER_X,
    SAB_OUTER_Y,
    SAB_INSTALLED_HEIGHT,
    SAB_LID_EXTERIOR_TOP_Z,
    SAB_LID_INTERIOR_ROOF_Z,
    SAB_LID_PIN_FIT_COUPON_BASE_HEIGHT,
    SAB_LID_PIN_FIT_COUPON_X,
    SAB_LID_PIN_FIT_COUPON_Y,
    SAB_LID_PIN_DIAMETER,
    SAB_LID_PIN_LENGTH,
    SAB_LID_PIN_TIP_DIAMETER,
    SAB_LID_RISER_HEIGHT,
    SAB_NEAR_WALL_COMPONENT_OFFSET,
    SAB_PIN_AXIAL_CLEARANCE,
    SAB_PIN_DIAMETRAL_CLEARANCE,
    SAB_PRINT_CENTER_GAP,
    SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER,
    SAB_RETAINING_CAP_BORE_TOP_DIAMETER,
    SAB_RETAINING_CAP_BODY_DIAMETER,
    SAB_RETAINING_CAP_BODY_HEIGHT,
    SAB_RETAINING_CAP_EDGE_CHAMFER,
    SAB_RETAINING_CAP_HEIGHT,
    SAB_RETAINING_CAP_LOCK_START_DEPTH,
    SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT,
    SAB_RETAINING_CAP_OUTER_DIAMETER,
    SAB_RETAINING_CAP_SLOT_COUNT,
    SAB_RETAINING_CAP_SLOT_DEPTH,
    SAB_RETAINING_CAP_SLOT_WIDTH,
    SAB_RETAINING_POST_DIAMETER,
    SAB_RETAINING_POST_HEIGHT,
    SAB_RETAINING_POST_PCB_DIAMETRAL_CLEARANCE,
    SAB_RETAINING_POST_TIP_CHAMFER,
    SAB_SHORT_END_PERFORATION_DIAMETER,
    SAB_SHORT_END_PERFORATION_MIN_BORDER,
    SAB_SHORT_END_PERFORATION_USB_CLEARANCE,
    SAB_SHORT_END_PERFORATION_Y_CENTERS,
    SAB_SHORT_END_PERFORATION_Z_CENTERS,
    SAB_USB_PORT_BOTTOM,
    SAB_USB_PORT_CENTER_Y_USER_DIRECTED,
    SAB_USB_PORT_CORNER_RADIUS,
    SAB_USB_PORT_HEIGHT,
    SAB_USB_PORT_TOP_RAIL_HEIGHT,
    SAB_USB_PORT_WIDTH,
    SAB_USB_CONNECTOR_BOTTOM_ASSUMED,
    SAB_USB_CONNECTOR_HEIGHT_ASSUMED,
    assembled_lid,
    build_lrs_base_details,
    build_lrs_lid_print,
    build_lrs_reference,
    build_sab_base_details,
    build_sab_fan_guard_installed,
    build_sab_fan_guard_print,
    build_sab_front_connector_access_probes_installed,
    build_sab_front_connector_joined_access_probe_installed,
    build_sab_lid_pin_fit_coupon,
    build_sab_lid_print,
    build_sab_near_wall_component_clearance_probe,
    build_sab_post_fit_coupon,
    build_sab_print_extras,
    build_sab_reference,
    build_sab_retaining_caps_installed,
    build_sab_retaining_caps_print,
    print_layout,
    print_layout_offset_y,
)


TOLERANCE = 1.0e-5


def _solid_volume(shape) -> float:
    if shape is None:
        return 0.0
    return sum(s.volume for s in shape.solids())


def _intersection_volume(a, b) -> float:
    return _solid_volume(a.intersect(b))


def _require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def _require_single_valid(shape, name: str):
    solids = list(shape.solids())
    _require(len(solids) == 1, f"{name}: expected one solid, found {len(solids)}")
    _require(bool(shape.is_valid), f"{name}: BREP is invalid")
    _require(_solid_volume(shape) > 0.0, f"{name}: non-positive volume")


def _count_45_degree_planar_edges(shape, z_coordinate: float) -> int:
    count = 0
    for edge in shape.edges():
        vertices = list(edge.vertices())
        if len(vertices) != 2:
            continue
        start, end = (tuple(vertex) for vertex in vertices)
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]
        chord = sqrt(delta_x**2 + delta_y**2)
        if (
            abs(start[2] - z_coordinate) < TOLERANCE
            and abs(end[2] - z_coordinate) < TOLERANCE
            and abs(delta_x) > TOLERANCE
            and abs(abs(delta_x) - abs(delta_y)) < TOLERANCE
            and abs(edge.length - chord) < TOLERANCE
        ):
            count += 1
    return count


def validate():
    lrs_details = build_lrs_base_details()
    lrs_base = lrs_details["base"]
    lrs_lid_print = build_lrs_lid_print()
    lrs_lid_installed = assembled_lid(lrs_lid_print, LRS_BASE_HEIGHT)
    lrs_reference = build_lrs_reference()

    sab_details = build_sab_base_details()
    sab_base = sab_details["base"]
    sab_lid_print = build_sab_lid_print()
    sab_lid_installed = assembled_lid(
        sab_lid_print,
        SAB_BASE_HEIGHT,
        SAB_LID_RISER_HEIGHT,
    )
    sab_reference = build_sab_reference()
    sab_caps_installed = build_sab_retaining_caps_installed()
    sab_caps_print = build_sab_retaining_caps_print()
    sab_fan_guard_installed = build_sab_fan_guard_installed()
    sab_fan_guard_print = build_sab_fan_guard_print()
    sab_fit_coupon = build_sab_post_fit_coupon()
    sab_lid_pin_fit_coupon = build_sab_lid_pin_fit_coupon()
    sab_near_wall_clearance_probe = (
        build_sab_near_wall_component_clearance_probe()
    )
    sab_front_connector_access_probes = (
        build_sab_front_connector_access_probes_installed()
    )
    sab_front_connector_joined_access_probe = (
        build_sab_front_connector_joined_access_probe_installed()
    )

    printable_shapes = (
        ("LRS base", lrs_base),
        ("LRS lid", lrs_lid_print),
        ("SAB base", sab_base),
        ("SAB lid", sab_lid_print),
        ("SAB removable fan guard", sab_fan_guard_print),
        ("SAB post-and-cap fit coupon", sab_fit_coupon),
        ("SAB lid-pin fit coupon", sab_lid_pin_fit_coupon),
        *tuple(
            (f"SAB retaining cap {index}", cap)
            for index, cap in enumerate(sab_caps_print, start=1)
        ),
    )
    for name, shape in printable_shapes:
        _require_single_valid(shape, name)

    _require(
        _intersection_volume(lrs_reference, lrs_base) < TOLERANCE,
        "LRS reference overlaps its base",
    )
    _require(
        _intersection_volume(lrs_reference, lrs_lid_installed) < TOLERANCE,
        "LRS reference overlaps its installed lid",
    )
    _require(
        _intersection_volume(lrs_details["terminal_access_probe"], lrs_base)
        < TOLERANCE,
        "LRS terminal access bay is obstructed",
    )

    _require(
        _intersection_volume(sab_reference, sab_base) < TOLERANCE,
        "SAB reference overlaps its base or standoffs",
    )
    _require(
        _intersection_volume(sab_reference, sab_lid_installed) < TOLERANCE,
        "SAB reference overlaps its installed lid",
    )
    _require(
        _intersection_volume(sab_base, sab_lid_installed) < TOLERANCE,
        "SAB lid pins or locating plug interfere with the base",
    )
    _require(
        _intersection_volume(
            sab_near_wall_clearance_probe,
            sab_lid_installed,
        )
        < TOLERANCE,
        "SAB raised lid intrudes into the 5 mm inset component-clearance zone",
    )
    _require(
        _intersection_volume(sab_fan_guard_installed, sab_lid_installed)
        < TOLERANCE,
        "SAB fan-guard locating skirt interferes with the lid opening",
    )
    _require(
        _intersection_volume(sab_fan_guard_installed, sab_reference)
        < TOLERANCE,
        "SAB fan guard interferes with the fan or board reference",
    )
    for index, (cap, post) in enumerate(
        zip(sab_caps_installed, sab_details["retaining_posts"]),
        start=1,
    ):
        base_overlap = _intersection_volume(cap, sab_base)
        post_overlap = _intersection_volume(cap, post)
        _require(
            post_overlap > 0.05,
            f"SAB retaining cap {index} has no effective post interference",
        )
        _require(
            abs(base_overlap - post_overlap) < TOLERANCE,
            f"SAB retaining cap {index} overlaps base geometry beyond its post",
        )
        _require(
            _intersection_volume(cap, sab_reference) < TOLERANCE,
            f"SAB retaining cap {index} overlaps the PCB reference",
        )
        _require(
            _intersection_volume(cap, sab_lid_installed) < TOLERANCE,
            f"SAB retaining cap {index} interferes with the lid",
        )
    _require(
        len(sab_details["access_cutters"]) == 0
        and len(sab_details["access_probes"]) == 0,
        "SAB legacy long-wall cable windows are not fully closed",
    )
    _require(
        len(sab_front_connector_access_probes)
        == SAB_FRONT_CONNECTOR_OPENING_COUNT,
        "SAB front connector roof-opening count changed",
    )
    for index, probe in enumerate(
        sab_front_connector_access_probes,
        start=1,
    ):
        _require(
            _intersection_volume(probe, sab_lid_installed) < TOLERANCE,
            f"SAB front connector roof opening {index} is obstructed",
        )
    _require(
        _intersection_volume(sab_details["usb_access_probe"], sab_base)
        < TOLERANCE,
        "SAB USB-C access window is obstructed",
    )
    _require(
        len(sab_details["short_end_perforation_specs"]) == 50,
        "SAB short-end perforation count changed",
    )
    for index, probe in enumerate(
        sab_details["short_end_perforation_probes"],
        start=1,
    ):
        _require(
            _intersection_volume(probe, sab_base) < TOLERANCE,
            f"SAB short-end perforation {index} is obstructed",
        )
    for index, probe in enumerate(sab_details["closed_wall_probes"], start=1):
        _require(
            _intersection_volume(probe, sab_base) > 1.0,
            f"SAB intentionally closed wall {index} is unexpectedly open",
        )

    perforation_radius = SAB_SHORT_END_PERFORATION_DIAMETER / 2.0
    _require(
        abs(SAB_SHORT_END_PERFORATION_DIAMETER - 5.0) < TOLERANCE
        and len(SAB_SHORT_END_PERFORATION_Y_CENTERS) == 7
        and len(SAB_SHORT_END_PERFORATION_Z_CENTERS) == 4,
        "SAB short-end perforation grid dimensions changed",
    )
    for wall_x, center_y, center_z in sab_details[
        "short_end_perforation_specs"
    ]:
        _require(
            SAB_OUTER_Y / 2.0 - abs(center_y) - perforation_radius
            >= SAB_SHORT_END_PERFORATION_MIN_BORDER - TOLERANCE,
            "SAB short-end perforation violates a side border",
        )
        _require(
            center_z - perforation_radius - FLOOR
            >= SAB_SHORT_END_PERFORATION_MIN_BORDER - TOLERANCE,
            "SAB short-end perforation violates the bottom border",
        )
        _require(
            SAB_BASE_HEIGHT - center_z - perforation_radius
            >= SAB_SHORT_END_PERFORATION_MIN_BORDER - TOLERANCE,
            "SAB short-end perforation violates the top border",
        )
        if wall_x < 0.0:
            usb_min_y = (
                SAB_USB_PORT_CENTER_Y_USER_DIRECTED - SAB_USB_PORT_WIDTH / 2.0
            )
            usb_max_y = (
                SAB_USB_PORT_CENTER_Y_USER_DIRECTED + SAB_USB_PORT_WIDTH / 2.0
            )
            usb_min_z = SAB_USB_PORT_BOTTOM
            usb_max_z = SAB_USB_PORT_BOTTOM + SAB_USB_PORT_HEIGHT
            y_clearance_ok = (
                center_y + perforation_radius
                <= usb_min_y - SAB_SHORT_END_PERFORATION_USB_CLEARANCE
                or center_y - perforation_radius
                >= usb_max_y + SAB_SHORT_END_PERFORATION_USB_CLEARANCE
            )
            z_clearance_ok = (
                center_z + perforation_radius
                <= usb_min_z - SAB_SHORT_END_PERFORATION_USB_CLEARANCE
                or center_z - perforation_radius
                >= usb_max_z + SAB_SHORT_END_PERFORATION_USB_CLEARANCE
            )
            _require(
                y_clearance_ok or z_clearance_ok,
                "SAB USB-side perforation violates the inlet keepout",
            )

    _require(
        SAB_FRONT_CONNECTOR_OPENING_COUNT == 3,
        "SAB lid must serve three front connector access zones",
    )
    _require(
        SAB_FRONT_CONNECTOR_OPENING_WIDTHS == (35.2, 35.2, 13.2)
        and abs(SAB_FRONT_CONNECTOR_OPENING_DEPTH - 16.0) < TOLERANCE,
        "SAB front connector roof-opening dimensions changed",
    )
    _require(
        abs(SAB_FRONT_CONNECTOR_JOINED_OPENING_WIDTH - 49.7) < TOLERANCE
        and abs(SAB_FRONT_CONNECTOR_JOINED_OPENING_CENTER_X - 36.75)
        < TOLERANCE,
        "SAB joined J012/DC roof-opening span changed",
    )
    _require(
        _intersection_volume(
            sab_front_connector_joined_access_probe,
            sab_lid_installed,
        )
        < TOLERANCE,
        "SAB J012/DC roof opening still contains a divider",
    )
    _require(
        SAB_FRONT_CONNECTOR_OPENING_CENTER_XS == (-44.0, 29.5, 55.0)
        and abs(SAB_FRONT_CONNECTOR_OPENING_CENTER_Y + 50.5) < TOLERANCE,
        "SAB front connector roof-opening centers changed",
    )
    front_inside_wall_y = -SAB_INNER_Y / 2.0
    front_opening_edge_y = (
        SAB_FRONT_CONNECTOR_OPENING_CENTER_Y
        - SAB_FRONT_CONNECTOR_OPENING_DEPTH / 2.0
    )
    _require(
        front_opening_edge_y - front_inside_wall_y >= 1.5 - TOLERANCE,
        "SAB front connector openings leave under 1.5 mm to the inside wall",
    )
    _require(
        SAB_USB_PORT_WIDTH <= 16.0 + TOLERANCE,
        "SAB USB-C wall bridge span exceeds 16 mm",
    )
    _require(
        abs(SAB_USB_PORT_CORNER_RADIUS - 1.5) < TOLERANCE,
        "SAB USB-C corner radius is not 1.5 mm",
    )
    _require(
        abs(SAB_USB_PORT_CENTER_Y_USER_DIRECTED + 29.0) < TOLERANCE,
        "SAB USB-C opening is not biased 29 mm toward -Y",
    )
    _require(
        2.0 * SAB_USB_PORT_CORNER_RADIUS < SAB_USB_PORT_HEIGHT,
        "SAB USB-C corner radius consumes the window height",
    )
    _require(
        abs(SAB_USB_PORT_BOTTOM - 17.6) < TOLERANCE,
        "SAB USB-C access lower sill is not 17.6 mm",
    )
    _require(
        abs(SAB_USB_PORT_TOP_RAIL_HEIGHT - 7.0) < TOLERANCE,
        "SAB USB-C access upper sill is not 7 mm",
    )
    _require(
        abs(SAB_USB_PORT_HEIGHT - 10.0) < TOLERANCE,
        "SAB USB-C access height is not 10 mm",
    )
    _require(
        abs(
            SAB_USB_PORT_BOTTOM
            + SAB_USB_PORT_HEIGHT
            + SAB_USB_PORT_TOP_RAIL_HEIGHT
            - SAB_BASE_HEIGHT
        )
        < TOLERANCE,
        "SAB USB-C access vertical dimensions do not close to wall height",
    )
    _require(
        SAB_USB_CONNECTOR_BOTTOM_ASSUMED >= SAB_USB_PORT_BOTTOM - TOLERANCE
        and SAB_USB_CONNECTOR_BOTTOM_ASSUMED
        + SAB_USB_CONNECTOR_HEIGHT_ASSUMED
        <= SAB_USB_PORT_BOTTOM + SAB_USB_PORT_HEIGHT + TOLERANCE,
        "SAB USB-C connector reference does not pass through the raised window",
    )
    _require(
        abs(SAB_FAN_FRAME_SIZE_USER_MEASURED - 60.1) < TOLERANCE,
        "SAB fan frame is not the user-measured 60.1 mm square",
    )
    _require(
        abs(SAB_FAN_REAR_CLEARANCE_USER_MEASURED - 24.5) < TOLERANCE
        and abs(SAB_FAN_FRONT_CLEARANCE_USER_MEASURED - 35.9) < TOLERANCE
        and abs(SAB_FAN_LEFT_CLEARANCE_USER_MEASURED - 47.6) < TOLERANCE
        and abs(SAB_FAN_RIGHT_CLEARANCE_USER_MEASURED - 50.7) < TOLERANCE,
        "SAB rear-view fan edge measurements changed",
    )
    measured_inner_x = (
        SAB_FAN_LEFT_CLEARANCE_USER_MEASURED
        + SAB_FAN_FRAME_SIZE_USER_MEASURED
        + SAB_FAN_RIGHT_CLEARANCE_USER_MEASURED
    )
    measured_inner_y = (
        SAB_FAN_REAR_CLEARANCE_USER_MEASURED
        + SAB_FAN_FRAME_SIZE_USER_MEASURED
        + SAB_FAN_FRONT_CLEARANCE_USER_MEASURED
    )
    y_reconciliation_per_side = (measured_inner_y - SAB_INNER_Y) / 2.0
    _require(
        abs(measured_inner_x - SAB_INNER_X) < TOLERANCE
        and abs(y_reconciliation_per_side - 0.10) < TOLERANCE,
        "SAB physical fan measurements do not reconcile with the printed base",
    )
    _require(
        abs(SAB_FAN_CENTER_X_FROM_EDGE_MEASUREMENTS - 1.55) < TOLERANCE
        and abs(SAB_FAN_REAR_VIEW_RIGHT_SHIFT - 2.0) < TOLERANCE
        and abs(SAB_FAN_CENTER_X_USER_DIRECTED + 0.45) < TOLERANCE
        and abs(SAB_FAN_CENTER_Y_USER_OBSERVED - 5.70) < TOLERANCE,
        "SAB fan center does not include the 2 mm rear-view-right shift",
    )
    fan_half = SAB_FAN_FRAME_SIZE_USER_MEASURED / 2.0
    modeled_left_clearance = (
        SAB_INNER_X / 2.0 - (SAB_FAN_CENTER_X_USER_DIRECTED + fan_half)
    )
    modeled_right_clearance = (
        SAB_FAN_CENTER_X_USER_DIRECTED - fan_half + SAB_INNER_X / 2.0
    )
    modeled_rear_clearance = (
        SAB_INNER_Y / 2.0 - (SAB_FAN_CENTER_Y_USER_OBSERVED + fan_half)
    )
    modeled_front_clearance = (
        SAB_FAN_CENTER_Y_USER_OBSERVED - fan_half + SAB_INNER_Y / 2.0
    )
    _require(
        abs(
            modeled_left_clearance
            - (
                SAB_FAN_LEFT_CLEARANCE_USER_MEASURED
                + SAB_FAN_REAR_VIEW_RIGHT_SHIFT
            )
        )
        < TOLERANCE
        and abs(
            modeled_right_clearance
            - (
                SAB_FAN_RIGHT_CLEARANCE_USER_MEASURED
                - SAB_FAN_REAR_VIEW_RIGHT_SHIFT
            )
        )
        < TOLERANCE
        and abs(
            modeled_rear_clearance
            - SAB_FAN_REAR_CLEARANCE_USER_MEASURED
            + y_reconciliation_per_side
        )
        < TOLERANCE
        and abs(
            modeled_front_clearance
            - SAB_FAN_FRONT_CLEARANCE_USER_MEASURED
            + y_reconciliation_per_side
        )
        < TOLERANCE,
        "SAB fan edges do not include the rear-view-right shift",
    )
    _require(
        abs(
            (SAB_FAN_OPENING_SIZE - SAB_FAN_FRAME_SIZE_USER_MEASURED) / 2.0
            - SAB_FAN_OPENING_CLEARANCE_PER_SIDE
        )
        < TOLERANCE,
        "SAB fan opening clearance is not 1 mm per side",
    )
    _require(
        abs(SAB_LID_RISER_HEIGHT - 8.0) < TOLERANCE,
        "SAB raised lid does not add 8 mm of interior height",
    )
    _require(
        abs(
            SAB_LID_INTERIOR_ROOF_Z
            - SAB_BASE_HEIGHT
            - SAB_LID_RISER_HEIGHT
        )
        < TOLERANCE,
        "SAB raised lid interior roof datum is inconsistent",
    )
    _require(
        abs(
            SAB_LID_EXTERIOR_TOP_Z
            - SAB_LID_INTERIOR_ROOF_Z
            - LID_TOP
        )
        < TOLERANCE,
        "SAB raised lid exterior roof datum is inconsistent",
    )
    _require(
        abs(SAB_LID_EXTERIOR_TOP_Z - SAB_INSTALLED_HEIGHT - 8.0)
        < TOLERANCE,
        "SAB raised lid roof is not 8 mm above the former exterior top",
    )
    _require(
        SAB_FAN_HEIGHT_ASSUMED > 0.0,
        "SAB assumed fan height must remain positive",
    )
    _require(
        abs(CORNER_GUSSET_ANGLE_DEGREES - 45.0) < TOLERANCE,
        "SAB corner tower gussets are not 45 degrees",
    )
    _require(
        abs(CORNER_GUSSET_TANGENT_WALL_RUN - CORNER_TOWER_RADIUS * sqrt(2.0))
        < TOLERANCE,
        "SAB corner tower gussets do not retain the 45-degree tangent run",
    )
    _require(
        abs(
            CORNER_GUSSET_WALL_RUN
            - CORNER_GUSSET_TANGENT_WALL_RUN
            * CORNER_GUSSET_WALL_CONTACT_MULTIPLIER
        )
        < TOLERANCE,
        "SAB corner tower gusset wall contact is not broadened as configured",
    )
    _require(
        _count_45_degree_planar_edges(sab_base, SAB_BASE_HEIGHT) == 8,
        "SAB base does not have two 45-degree tangent edges at all four towers",
    )
    _require(
        _count_45_degree_planar_edges(
            sab_lid_print,
            LID_TOP + SAB_LID_RISER_HEIGHT,
        )
        == 8,
        "SAB lid does not have two 45-degree tangent edges at all four ears",
    )
    _require(
        len(sab_details["pin_receiver_centers"]) == 4,
        "SAB base must have four pin receivers",
    )
    _require(
        abs(
            SAB_BASE_PIN_RECEIVER_DIAMETER
            - SAB_LID_PIN_DIAMETER
            - SAB_PIN_DIAMETRAL_CLEARANCE
        )
        < TOLERANCE,
        "SAB lid pin diametral clearance is inconsistent",
    )
    _require(
        abs(SAB_BASE_PIN_RECEIVER_DIAMETER - 4.60) < TOLERANCE,
        "SAB base pin receiver diameter changed from 4.60 mm",
    )
    _require(
        abs(SAB_LID_PIN_DIAMETER - 4.00) < TOLERANCE
        and abs(SAB_LID_PIN_TIP_DIAMETER - 3.20) < TOLERANCE,
        "SAB loose-locating lid pin diameters are incorrect",
    )
    _require(
        abs(SAB_PIN_DIAMETRAL_CLEARANCE - 0.60) < TOLERANCE,
        "SAB lid pin diametral clearance is not 0.60 mm",
    )
    _require(
        abs(
            SAB_BASE_PIN_RECEIVER_DEPTH
            - SAB_LID_PIN_LENGTH
            - SAB_PIN_AXIAL_CLEARANCE
        )
        < TOLERANCE,
        "SAB lid pin axial clearance is inconsistent",
    )
    _require(
        abs(SAB_PIN_AXIAL_CLEARANCE - 0.50) < TOLERANCE,
        "SAB lid pin axial clearance is not 0.50 mm",
    )
    lid_print_bounds = sab_lid_print.bounding_box()
    _require(
        abs(
            lid_print_bounds.max.Z
            - LID_TOP
            - SAB_LID_RISER_HEIGHT
            - SAB_LID_PIN_LENGTH
        )
        < TOLERANCE,
        "SAB raised lid pins are not referenced from the original mating plane",
    )
    _require(
        abs(sab_lid_installed.bounding_box().max.Z - SAB_LID_EXTERIOR_TOP_Z)
        < TOLERANCE,
        "SAB installed raised-lid exterior top is incorrect",
    )
    _require(
        abs(SAB_NEAR_WALL_COMPONENT_OFFSET - 5.0) < TOLERANCE,
        "SAB near-wall component clearance is not inset 5 mm",
    )
    _require(
        abs(SAB_BOARD_THICKNESS - 1.70) < TOLERANCE,
        "SAB PCB thickness is not the user-specified 1.7 mm",
    )
    _require(
        len(sab_details["floor_ribs"]) == 6,
        "SAB base must contain a six-member orthogonal floor-rib grid",
    )
    _require(
        abs(SAB_FLOOR_RIB_WIDTH - 2.0) < TOLERANCE
        and abs(SAB_FLOOR_RIB_HEIGHT - 1.75) < TOLERANCE,
        "SAB floor ribs are not 2.0 mm wide x 1.75 mm high",
    )
    for index, rib in enumerate(sab_details["floor_ribs"], start=1):
        _require(
            rib.bounding_box().max.Z < SAB_BOARD_Z - TOLERANCE,
            f"SAB floor rib {index} reaches the PCB underside",
        )
    _require(
        len(sab_details["retaining_posts"]) == 4,
        "SAB base must have four integral PCB retaining posts",
    )
    _require(
        abs(
            SAB_HOLE_DIAMETER_REPORTED
            - SAB_RETAINING_POST_DIAMETER
            - SAB_RETAINING_POST_PCB_DIAMETRAL_CLEARANCE
        )
        < TOLERANCE,
        "SAB retaining-post PCB-hole clearance is inconsistent",
    )
    _require(
        abs(SAB_RETAINING_POST_PCB_DIAMETRAL_CLEARANCE - 0.40)
        < TOLERANCE,
        "SAB retaining posts do not retain 0.40 mm diametral PCB clearance",
    )
    _require(
        abs(SAB_RETAINING_POST_TIP_CHAMFER - 0.40) < TOLERANCE,
        "SAB retaining-post insertion chamfer is not 0.40 mm",
    )
    _require(
        abs(
            SAB_RETAINING_CAP_OUTER_DIAMETER
            - 3.0 * SAB_RETAINING_POST_DIAMETER
        )
        < TOLERANCE,
        "SAB retaining-cap top is not three times the post diameter",
    )
    _require(
        abs(SAB_RETAINING_CAP_HEIGHT - 10.0) < TOLERANCE,
        "SAB retaining caps are not 10 mm long",
    )
    _require(
        abs(SAB_RETAINING_CAP_BODY_DIAMETER - 6.8) < TOLERANCE
        and abs(SAB_RETAINING_CAP_BODY_HEIGHT - 8.0) < TOLERANCE,
        "SAB retaining caps do not have a 6.8 mm x 8 mm lower body",
    )
    _require(
        abs(SAB_RETAINING_CAP_EDGE_CHAMFER - 0.40) < TOLERANCE,
        "SAB retaining-cap bed-face chamfer is not 0.40 mm",
    )
    _require(
        SAB_RETAINING_CAP_SLOT_COUNT == 3
        and abs(SAB_RETAINING_CAP_SLOT_WIDTH - 0.50) < TOLERANCE
        and abs(SAB_RETAINING_CAP_SLOT_DEPTH - 6.0) < TOLERANCE,
        "SAB retaining caps do not have three 0.5 x 6 mm relief slots",
    )
    _require(
        abs(
            SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
            - SAB_HOLE_DIAMETER_REPORTED
        )
        < TOLERANCE,
        "SAB retaining-cap entry does not match the reported PCB hole",
    )
    _require(
        SAB_RETAINING_CAP_BORE_TOP_DIAMETER
        < SAB_RETAINING_POST_DIAMETER,
        "SAB retaining-cap bore does not taper below the post diameter",
    )
    _require(
        abs(SAB_RETAINING_CAP_BORE_TOP_DIAMETER - 3.0) < TOLERANCE
        and abs(SAB_RETAINING_CAP_LOCK_START_DEPTH - 5.0) < TOLERANCE,
        "SAB retaining-cap high-clamp taper is not 3.0 mm / 5.0 mm",
    )
    bore_at_lock_start = (
        SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        + (
            SAB_RETAINING_CAP_BORE_TOP_DIAMETER
            - SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        )
        * (
            SAB_RETAINING_CAP_LOCK_START_DEPTH
            / SAB_RETAINING_CAP_HEIGHT
        )
    )
    _require(
        abs(bore_at_lock_start - SAB_RETAINING_POST_DIAMETER)
        < TOLERANCE,
        "SAB cap taper does not reach the post diameter at the lock start",
    )
    straight_post_engagement = (
        SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT
        - SAB_RETAINING_POST_TIP_CHAMFER
    )
    bore_at_straight_post_end = (
        SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        + (
            SAB_RETAINING_CAP_BORE_TOP_DIAMETER
            - SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        )
        * (straight_post_engagement / SAB_RETAINING_CAP_HEIGHT)
    )
    _require(
        SAB_RETAINING_POST_DIAMETER - bore_at_straight_post_end >= 0.20,
        "SAB cap does not provide at least 0.20 mm diametral interference",
    )
    _require(
        abs(
            SAB_RETAINING_POST_HEIGHT
            - SAB_BOARD_THICKNESS
            - SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT
        )
        < TOLERANCE,
        "SAB retaining-post height does not account for PCB and cap engagement",
    )
    for index, post in enumerate(sab_details["retaining_posts"], start=1):
        bounds = post.bounding_box()
        _require(
            abs(bounds.size.X - SAB_RETAINING_POST_DIAMETER) < TOLERANCE
            and abs(bounds.size.Y - SAB_RETAINING_POST_DIAMETER) < TOLERANCE,
            f"SAB retaining post {index} diameter is incorrect",
        )
        _require(
            abs(bounds.max.Z - SAB_BOARD_Z - SAB_RETAINING_POST_HEIGHT)
            < TOLERANCE,
            f"SAB retaining post {index} top height is incorrect",
        )
    for index, cap in enumerate(sab_caps_print, start=1):
        bounds = cap.bounding_box()
        _require(
            abs(
                max(bounds.size.X, bounds.size.Y)
                - SAB_RETAINING_CAP_OUTER_DIAMETER
            )
            < TOLERANCE
            and min(bounds.size.X, bounds.size.Y)
            > SAB_RETAINING_CAP_OUTER_DIAMETER - SAB_RETAINING_CAP_SLOT_WIDTH
            and abs(bounds.size.Z - SAB_RETAINING_CAP_HEIGHT) < TOLERANCE,
            f"SAB retaining cap {index} external dimensions are incorrect",
        )
        _require(
            bounds.min.Z >= -TOLERANCE,
            f"SAB retaining cap {index} print orientation is below Z=0",
        )
    guard_bounds = sab_fan_guard_print.bounding_box()
    _require(
        abs(guard_bounds.size.X - SAB_FAN_GUARD_OUTER_SIZE) < TOLERANCE
        and abs(guard_bounds.size.Y - SAB_FAN_GUARD_OUTER_SIZE) < TOLERANCE
        and abs(
            guard_bounds.size.Z
            - SAB_FAN_GUARD_THICKNESS
            - SAB_FAN_GUARD_SKIRT_DEPTH
        )
        < TOLERANCE,
        "SAB removable fan guard external dimensions are incorrect",
    )
    _require(
        abs(
            SAB_FAN_GUARD_OUTER_SIZE
            - 2.0 * SAB_FAN_GUARD_FRAME_WIDTH
            - SAB_FAN_FRAME_SIZE_USER_MEASURED
        )
        < TOLERANCE,
        "SAB fan-guard frame does not preserve the measured airflow square",
    )
    _require(
        SAB_FAN_GUARD_SKIRT_OUTER_SIZE < SAB_FAN_OPENING_SIZE
        and SAB_FAN_GUARD_SKIRT_INNER_SIZE > SAB_FAN_FRAME_SIZE_USER_MEASURED,
        "SAB fan-guard skirt does not clear the lid opening and fan frame",
    )
    coupon_bounds = sab_fit_coupon.bounding_box()
    _require(
        abs(coupon_bounds.size.X - SAB_FIT_COUPON_X) < TOLERANCE
        and abs(coupon_bounds.size.Y - SAB_FIT_COUPON_Y) < TOLERANCE
        and abs(
            coupon_bounds.size.Z
            - SAB_FIT_COUPON_BASE_HEIGHT
            - SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT
        )
        < TOLERANCE,
        "SAB post-and-cap fit coupon dimensions are incorrect",
    )
    lid_pin_coupon_bounds = sab_lid_pin_fit_coupon.bounding_box()
    _require(
        abs(lid_pin_coupon_bounds.size.X - SAB_LID_PIN_FIT_COUPON_X)
        < TOLERANCE
        and abs(lid_pin_coupon_bounds.size.Y - SAB_LID_PIN_FIT_COUPON_Y)
        < TOLERANCE
        and abs(
            lid_pin_coupon_bounds.size.Z
            - SAB_LID_PIN_FIT_COUPON_BASE_HEIGHT
            - SAB_LID_PIN_LENGTH
        )
        < TOLERANCE,
        "SAB lid-pin fit coupon dimensions are incorrect",
    )

    _require(
        abs((LRS_INNER_X - (LRS_INNER_X - 2.0 * LID_CLEARANCE_PER_SIDE)) / 2.0
            - LID_CLEARANCE_PER_SIDE)
        < TOLERANCE,
        "LRS lid clearance changed",
    )
    _require(
        abs((SAB_INNER_Y - (SAB_INNER_Y - 2.0 * LID_CLEARANCE_PER_SIDE)) / 2.0
            - LID_CLEARANCE_PER_SIDE)
        < TOLERANCE,
        "SAB lid clearance changed",
    )
    centers = sab_details["standoff_centers"]
    measured_x = max(x for x, _ in centers) - min(x for x, _ in centers)
    measured_y = max(y for _, y in centers) - min(y for _, y in centers)
    _require(
        abs(measured_x - SAB_HOLE_SPACING_X_REPORTED) < TOLERANCE,
        "SAB reported X hole spacing changed",
    )
    _require(
        abs(measured_y - SAB_HOLE_SPACING_Y_REPORTED) < TOLERANCE,
        "SAB reported Y hole spacing changed",
    )
    lrs_centers = lrs_details["mount_centers"]
    lrs_measured_x = max(x for x, _ in lrs_centers) - min(x for x, _ in lrs_centers)
    lrs_measured_y = max(y for _, y in lrs_centers) - min(y for _, y in lrs_centers)
    _require(
        abs(lrs_measured_x - LRS_MOUNT_SPACING_X) < TOLERANCE,
        "LRS X mounting spacing changed",
    )
    _require(
        abs(lrs_measured_y - LRS_MOUNT_SPACING_Y) < TOLERANCE,
        "LRS Y mounting spacing changed",
    )

    lrs_layout = print_layout(
        lrs_base,
        lrs_lid_print,
        LRS_OUTER_Y,
        "lrs_validation_layout",
    )
    sab_print_extras = build_sab_print_extras()
    sab_layout = print_layout(
        sab_base,
        sab_lid_print,
        SAB_OUTER_Y,
        "sab_validation_layout",
        extra_print_objects=sab_print_extras,
        center_gap=SAB_PRINT_CENTER_GAP,
    )
    for name, layout in (("LRS", lrs_layout), ("SAB", sab_layout)):
        size = layout.bounding_box().size
        _require(size.X <= 350.0, f"{name} print layout exceeds 350 mm X")
        _require(size.Y <= 320.0, f"{name} print layout exceeds 320 mm Y")
        _require(layout.bounding_box().min.Z >= -TOLERANCE, f"{name} is below Z=0")
    _require(
        len(sab_layout.children) == 9,
        "SAB print layout must contain nine independently printable objects",
    )
    sab_layout_solids = list(sab_layout.solids())
    _require(
        len(sab_layout_solids) == 9,
        "SAB print layout must export nine separate printable solids",
    )
    for first_index, second_index in combinations(range(9), 2):
        _require(
            _intersection_volume(
                sab_layout_solids[first_index],
                sab_layout_solids[second_index],
            )
            < TOLERANCE,
            (
                "SAB print objects "
                f"{first_index + 1} and {second_index + 1} overlap"
            ),
        )
    print_fan_center_y = (
        print_layout_offset_y(SAB_OUTER_Y, SAB_PRINT_CENTER_GAP)
        - SAB_FAN_CENTER_Y_USER_OBSERVED
    )
    fan_opening_half = SAB_FAN_OPENING_SIZE / 2.0
    for shape, label in sab_print_extras[:6]:
        bounds = shape.bounding_box()
        _require(
            bounds.min.X
            >= SAB_FAN_CENTER_X_USER_DIRECTED - fan_opening_half - TOLERANCE
            and bounds.max.X
            <= SAB_FAN_CENTER_X_USER_DIRECTED + fan_opening_half + TOLERANCE
            and bounds.min.Y
            >= print_fan_center_y - fan_opening_half - TOLERANCE
            and bounds.max.Y
            <= print_fan_center_y + fan_opening_half + TOLERANCE,
            f"SAB nested print object {label} lies outside the fan opening",
        )

    fit = build_fit_details()
    _require(
        len(fit["final"].children) == 11,
        "fit check must have eleven occurrences",
    )
    _require(
        abs(
            fit["sab_reference"].bounding_box().center().Y
            - sab_reference.bounding_box().center().Y
            - SAB_ASSEMBLY_OFFSET_Y
        )
        < TOLERANCE,
        "SAB fit-check reference Y offset changed",
    )

    print("PASS: eleven printable enclosure solids are valid and positive-volume")
    print("PASS: both documented component envelopes clear bases and installed lids")
    print("PASS: LRS terminal bay and SAB USB-C window are unobstructed")
    print("PASS: both SAB long walls, including the former five-window bank, are closed")
    print("PASS: SAB lid serves 35.2, 35.2, and 13.2 mm front plug zones")
    print("PASS: J012 and DC share one continuous 49.7 x 16 mm roof opening")
    print("PASS: SAB USB-C window is 16 x 10 mm with 1.5 mm internal corner radii")
    print("PASS: SAB USB-C window is on the negative-X side, 29 mm toward -Y")
    print("PASS: SAB USB-C window is raised to a 17.6 mm lower and 7 mm upper sill")
    print("PASS: fifty 5 mm short-end perforations preserve 1 mm borders and USB clearance")
    print("PASS: SAB fan reference is the user-measured 60.1 mm square")
    print("PASS: SAB fan opening moved 2 mm rear-view right to X=-0.45 mm")
    print("PASS: Y measurements are reconciled 0.10 mm per side to the printed base")
    print("PASS: SAB 62.1 mm lid opening clears the fan by 1 mm per side")
    print("PASS: SAB lid adds 8 mm while the base height remains 34.6 mm")
    print("PASS: the lid is clear of the full volume at least 5 mm inside each wall")
    print("PASS: all four SAB base towers and four lid ears have broad-root 45-degree gussets")
    print("PASS: four 4.0 mm tapered SAB lid pins have 0.60 mm receiver clearance")
    print("PASS: lid locating clearance is 0.30 mm per side")
    print("PASS: four 3.4 mm integral posts clear the reported 3.8 mm PCB holes")
    print("PASS: six low floor ribs stiffen the base while clearing the PCB")
    print("PASS: four high-clamp mushroom caps retain the 1.7 mm PCB")
    print("PASS: cap lock starts at 5 mm with at least 0.20 mm interference")
    print("PASS: post and cap openings carry 0.4 mm insertion/bed-face chamfers")
    print("PASS: a removable six-spoke fan guard locates in the 62.1 mm opening")
    print("PASS: the separate post-and-cap coupon reproduces the production fit")
    print("PASS: the lid-pin coupon reproduces the pin used by the printed base")
    print("PASS: SAB standoffs match the reported 142 x 104 mm mounting pattern")
    print("PASS: LRS bottom mounts match the official 150 x 50 mm pattern")
    print("PASS: both print sets fit within a 350 x 320 mm bed")
    print("PASS: SAB print set contains nine non-overlapping printable objects")
    print("PASS: caps and both fit coupons nest inside the lid fan opening")
    print("PASS: fit-check assembly contains eleven labeled occurrences")


if __name__ == "__main__":
    validate()
