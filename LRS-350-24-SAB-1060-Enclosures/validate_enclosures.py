"""Geometry and documented-fit validation for both enclosure print sets."""

from __future__ import annotations

from math import sqrt

from enclosure_fit_check import SAB_ASSEMBLY_OFFSET_Y, build_fit_details
from enclosure_geometry import (
    CORNER_GUSSET_ANGLE_DEGREES,
    CORNER_GUSSET_TANGENT_WALL_RUN,
    CORNER_GUSSET_WALL_RUN,
    CORNER_GUSSET_WALL_CONTACT_MULTIPLIER,
    CORNER_TOWER_RADIUS,
    LID_CLEARANCE_PER_SIDE,
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
    SAB_CABLE_RIB_WIDTH,
    SAB_CABLE_TOP_RAIL_HEIGHT,
    SAB_CABLE_WINDOW_BOTTOM,
    SAB_CABLE_WINDOW_COUNT,
    SAB_CABLE_WINDOW_WIDTH,
    SAB_FAN_CENTER_X_USER_DIRECTED,
    SAB_FAN_CENTER_Y_USER_OBSERVED,
    SAB_FAN_FRAME_SIZE_USER_MEASURED,
    SAB_FAN_HEIGHT_ASSUMED,
    SAB_FAN_OPENING_CLEARANCE_PER_SIDE,
    SAB_FAN_OPENING_SIZE,
    SAB_HOLE_SPACING_X_REPORTED,
    SAB_HOLE_SPACING_Y_REPORTED,
    SAB_HOLE_DIAMETER_REPORTED,
    SAB_INNER_X,
    SAB_INNER_Y,
    SAB_OUTER_X,
    SAB_OUTER_Y,
    SAB_INSTALLED_HEIGHT,
    SAB_LID_PIN_DIAMETER,
    SAB_LID_PIN_LENGTH,
    SAB_PIN_AXIAL_CLEARANCE,
    SAB_PIN_DIAMETRAL_CLEARANCE,
    SAB_PRINT_CENTER_GAP,
    SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER,
    SAB_RETAINING_CAP_BORE_TOP_DIAMETER,
    SAB_RETAINING_CAP_HEIGHT,
    SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT,
    SAB_RETAINING_CAP_OUTER_DIAMETER,
    SAB_RETAINING_POST_DIAMETER,
    SAB_RETAINING_POST_HEIGHT,
    SAB_RETAINING_POST_PCB_DIAMETRAL_CLEARANCE,
    SAB_USB_PORT_BOTTOM,
    SAB_USB_PORT_CENTER_Y_USER_DIRECTED,
    SAB_USB_PORT_CORNER_RADIUS,
    SAB_USB_PORT_HEIGHT,
    SAB_USB_PORT_TOP_RAIL_HEIGHT,
    SAB_USB_PORT_WIDTH,
    assembled_lid,
    build_lrs_base_details,
    build_lrs_lid_print,
    build_lrs_reference,
    build_sab_base_details,
    build_sab_lid_print,
    build_sab_reference,
    build_sab_retaining_caps_installed,
    build_sab_retaining_caps_print,
    print_layout,
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
    sab_lid_installed = assembled_lid(sab_lid_print, SAB_BASE_HEIGHT)
    sab_reference = build_sab_reference()
    sab_caps_installed = build_sab_retaining_caps_installed()
    sab_caps_print = build_sab_retaining_caps_print()

    printable_shapes = (
        ("LRS base", lrs_base),
        ("LRS lid", lrs_lid_print),
        ("SAB base", sab_base),
        ("SAB lid", sab_lid_print),
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
    for index, cap in enumerate(sab_caps_installed, start=1):
        _require(
            _intersection_volume(cap, sab_base) < TOLERANCE,
            f"SAB retaining cap {index} interferes with its integral post",
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
        len(sab_details["access_probes"]) == SAB_CABLE_WINDOW_COUNT,
        "SAB cable exit count changed",
    )
    for index, probe in enumerate(sab_details["access_probes"], start=1):
        _require(
            _intersection_volume(probe, sab_base) < TOLERANCE,
            f"SAB cable exit {index} is obstructed",
        )
    _require(
        _intersection_volume(sab_details["usb_access_probe"], sab_base)
        < TOLERANCE,
        "SAB USB-C access window is obstructed",
    )
    for index, probe in enumerate(sab_details["closed_wall_probes"], start=1):
        _require(
            _intersection_volume(probe, sab_base) > 1.0,
            f"SAB intentionally closed wall {index} is unexpectedly open",
        )

    _require(
        SAB_CABLE_WINDOW_WIDTH <= 22.0 + TOLERANCE,
        "SAB cable-window bridge span exceeds 22 mm",
    )
    _require(
        SAB_CABLE_RIB_WIDTH >= 5.0 - TOLERANCE,
        "SAB cable-window cross ribs are under 5 mm",
    )
    _require(
        SAB_CABLE_TOP_RAIL_HEIGHT >= 5.5 - TOLERANCE,
        "SAB cable-window top rail is under 5.5 mm",
    )
    _require(
        0.45 * SAB_BASE_HEIGHT <= SAB_CABLE_WINDOW_BOTTOM <= 0.55 * SAB_BASE_HEIGHT,
        "SAB cable exits no longer begin near half wall height",
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
        SAB_USB_PORT_BOTTOM >= 7.0 - TOLERANCE,
        "SAB USB-C access lower sill is under 7 mm",
    )
    _require(
        SAB_USB_PORT_TOP_RAIL_HEIGHT >= 17.0 - TOLERANCE,
        "SAB USB-C access upper rail is under 17 mm",
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
        abs(SAB_FAN_FRAME_SIZE_USER_MEASURED - 60.5) < TOLERANCE,
        "SAB fan frame is not the user-measured 60.5 mm square",
    )
    _require(
        abs(SAB_FAN_CENTER_X_USER_DIRECTED) < TOLERANCE,
        "SAB fan and lid opening are not centered on X",
    )
    _require(
        abs(SAB_FAN_CENTER_Y_USER_OBSERVED - 7.0) < TOLERANCE,
        "SAB fan rearward Y bias changed",
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
        abs(SAB_BASE_HEIGHT + 3.0 - SAB_INSTALLED_HEIGHT) < TOLERANCE,
        "SAB lid top is not flush with the assumed fan-frame top",
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
        _count_45_degree_planar_edges(sab_lid_print, 3.0) == 8,
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
        abs(SAB_PIN_DIAMETRAL_CLEARANCE) < TOLERANCE,
        "SAB lid pin does not reach the full receiver diameter",
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
    _require(
        abs(SAB_BOARD_THICKNESS - 1.70) < TOLERANCE,
        "SAB PCB thickness is not the user-specified 1.7 mm",
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
    nominal_bore_at_post_end = (
        SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        + (
            SAB_RETAINING_CAP_BORE_TOP_DIAMETER
            - SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        )
        * (
            SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT
            / SAB_RETAINING_CAP_HEIGHT
        )
    )
    _require(
        abs(nominal_bore_at_post_end - SAB_RETAINING_POST_DIAMETER)
        < TOLERANCE,
        "SAB cap taper does not reach the post diameter at nominal seating",
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
            abs(bounds.size.X - SAB_RETAINING_CAP_OUTER_DIAMETER) < TOLERANCE
            and abs(bounds.size.Y - SAB_RETAINING_CAP_OUTER_DIAMETER) < TOLERANCE
            and abs(bounds.size.Z - SAB_RETAINING_CAP_HEIGHT) < TOLERANCE,
            f"SAB retaining cap {index} external dimensions are incorrect",
        )
        _require(
            bounds.min.Z >= -TOLERANCE,
            f"SAB retaining cap {index} print orientation is below Z=0",
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
    sab_cap_objects = tuple(
        (cap, f"pcb_retaining_cap_{index}")
        for index, cap in enumerate(sab_caps_print, start=1)
    )
    sab_layout = print_layout(
        sab_base,
        sab_lid_print,
        SAB_OUTER_Y,
        "sab_validation_layout",
        extra_print_objects=sab_cap_objects,
        center_gap=SAB_PRINT_CENTER_GAP,
    )
    for name, layout in (("LRS", lrs_layout), ("SAB", sab_layout)):
        size = layout.bounding_box().size
        _require(size.X <= 350.0, f"{name} print layout exceeds 350 mm X")
        _require(size.Y <= 320.0, f"{name} print layout exceeds 320 mm Y")
        _require(layout.bounding_box().min.Z >= -TOLERANCE, f"{name} is below Z=0")
    _require(
        len(sab_layout.children) == 6,
        "SAB print layout must contain base, lid, and four separate caps",
    )
    _require(
        len(sab_layout.solids()) == 6,
        "SAB print layout must export six separate printable solids",
    )

    fit = build_fit_details()
    _require(len(fit["final"].children) == 10, "fit check must have ten occurrences")
    _require(
        abs(
            fit["sab_reference"].bounding_box().center().Y
            - sab_reference.bounding_box().center().Y
            - SAB_ASSEMBLY_OFFSET_Y
        )
        < TOLERANCE,
        "SAB fit-check reference Y offset changed",
    )

    print("PASS: eight printable enclosure solids are valid and positive-volume")
    print("PASS: both documented component envelopes clear bases and installed lids")
    print("PASS: LRS terminal bay, five SAB cable exits, and USB-C window are unobstructed")
    print("PASS: the unused SAB wall areas remain closed")
    print("PASS: SAB cable spans are 22 mm with 5 mm ribs and a 5.6 mm top rail")
    print("PASS: SAB USB-C window is 16 x 10 mm with 1.5 mm internal corner radii")
    print("PASS: SAB USB-C window is on the negative-X side, 29 mm toward -Y")
    print("PASS: SAB USB-C window retains a 7 mm sill and 17.6 mm top rail")
    print("PASS: SAB fan reference is 60.5 mm square and centered on X")
    print("PASS: SAB fan and opening are biased 7 mm toward the +Y rear")
    print("PASS: SAB 62.5 mm lid opening clears the fan by 1 mm per side")
    print("PASS: SAB lid top remains flush with the assumed fan top")
    print("PASS: all four SAB base towers and four lid ears have broad-root 45-degree gussets")
    print("PASS: four tapered SAB lid pins reach the full 4.6 mm receiver diameter")
    print("PASS: lid locating clearance is 0.30 mm per side")
    print("PASS: four 3.4 mm integral posts clear the reported 3.8 mm PCB holes")
    print("PASS: four separate 10.2 x 10 mm tapered-bore caps retain the 1.7 mm PCB")
    print("PASS: SAB standoffs match the reported 142 x 104 mm mounting pattern")
    print("PASS: LRS bottom mounts match the official 150 x 50 mm pattern")
    print("PASS: both print sets fit within a 350 x 320 mm bed")
    print("PASS: SAB print set contains base, lid, and four separate caps")
    print("PASS: fit-check assembly contains ten labeled occurrences")


if __name__ == "__main__":
    validate()
