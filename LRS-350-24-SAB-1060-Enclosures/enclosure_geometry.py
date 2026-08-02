"""Parametric geometry for LRS-350-24 and SAB-1060 protective enclosures.

Coordinate convention:
- millimetres throughout;
- component length on global X, width on global Y, height on global Z;
- base floor rests on Z=0;
- lids are authored exterior-face-down for support-free printing.
"""

from __future__ import annotations

from math import sqrt

from build123d import (
    Align,
    Axis,
    Box,
    BuildSketch,
    Color,
    Compound,
    Cone,
    Cylinder,
    Location,
    Locations,
    Plane,
    Polygon,
    RectangleRounded,
    extrude,
)


BOOLEAN_OVERSHOOT = 0.5

# Shared print and hardware choices.
WALL = 3.0
FLOOR = 3.0
LID_TOP = 3.0
LID_PLUG_DEPTH = 3.0
LID_PLUG_WALL = 2.2
LID_CLEARANCE_PER_SIDE = 0.30
CORNER_TOWER_RADIUS = 5.5
CORNER_TOWER_OUTSET = 2.5
CORNER_GUSSET_ANGLE_DEGREES = 45.0
CORNER_GUSSET_TANGENT_WALL_RUN = CORNER_TOWER_RADIUS * sqrt(2.0)
CORNER_GUSSET_WALL_CONTACT_MULTIPLIER = 2.0
CORNER_GUSSET_WALL_RUN = (
    CORNER_GUSSET_TANGENT_WALL_RUN * CORNER_GUSSET_WALL_CONTACT_MULTIPLIER
)
CORNER_GUSSET_TANGENT_RETAINED_FRACTION = 0.50
M3_LID_CLEARANCE_DIAMETER = 3.4
M3_INSERT_POCKET_DIAMETER = 4.6
M3_INSERT_POCKET_DEPTH = 6.0

# Manufacturer LRS-350 family outline.
LRS_LENGTH = 215.0
LRS_WIDTH = 115.0
LRS_HEIGHT = 30.0
LRS_XY_CLEARANCE_PER_SIDE = 4.0
LRS_INNER_X = LRS_LENGTH + 2.0 * LRS_XY_CLEARANCE_PER_SIDE
LRS_INNER_Y = LRS_WIDTH + 2.0 * LRS_XY_CLEARANCE_PER_SIDE
LRS_OUTER_X = LRS_INNER_X + 2.0 * WALL
LRS_OUTER_Y = LRS_INNER_Y + 2.0 * WALL
LRS_BASE_HEIGHT = 38.0
LRS_COMPONENT_Z = 4.0
LRS_MOUNT_SPACING_X = 150.0
LRS_MOUNT_SPACING_Y = 50.0
LRS_MOUNT_CLEARANCE_DIAMETER = 4.5
LRS_SUPPORT_PAD_RADIUS = 7.0
LRS_SUPPORT_PAD_HEIGHT = LRS_COMPONENT_Z - FLOOR
LRS_TERMINAL_WINDOW_Y = 111.0
LRS_TERMINAL_WINDOW_BOTTOM = 5.0
LRS_TERMINAL_WINDOW_HEIGHT = 29.0

# Dayton SAB-1060 official outline plus measured and provisional fit datums.
SAB_LENGTH = 152.4
SAB_WIDTH = 114.3
SAB_HEIGHT = 28.6
SAB_HOLE_DIAMETER_REPORTED = 3.8
SAB_HOLE_SPACING_X_REPORTED = 142.0
SAB_HOLE_SPACING_Y_REPORTED = 104.0
SAB_XY_CLEARANCE_PER_SIDE = 3.0
SAB_INNER_X = SAB_LENGTH + 2.0 * SAB_XY_CLEARANCE_PER_SIDE
SAB_INNER_Y = SAB_WIDTH + 2.0 * SAB_XY_CLEARANCE_PER_SIDE
SAB_OUTER_X = SAB_INNER_X + 2.0 * WALL
SAB_OUTER_Y = SAB_INNER_Y + 2.0 * WALL
SAB_BOARD_Z = 9.0
SAB_BOARD_THICKNESS = 1.7
SAB_STANDOFF_RADIUS = 4.5
SAB_STANDOFF_HEIGHT = SAB_BOARD_Z - FLOOR
SAB_RETAINING_POST_DIAMETER = 3.4
SAB_RETAINING_POST_PCB_DIAMETRAL_CLEARANCE = (
    SAB_HOLE_DIAMETER_REPORTED - SAB_RETAINING_POST_DIAMETER
)
SAB_RETAINING_CAP_OUTER_DIAMETER = 3.0 * SAB_RETAINING_POST_DIAMETER
SAB_RETAINING_CAP_HEIGHT = 10.0
SAB_RETAINING_CAP_COMPONENT_CLEARANCE = 0.5
SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER = SAB_HOLE_DIAMETER_REPORTED
SAB_RETAINING_CAP_BORE_TOP_DIAMETER = 3.3
SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT = (
    SAB_RETAINING_CAP_HEIGHT
    * (
        SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        - SAB_RETAINING_POST_DIAMETER
    )
    / (
        SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER
        - SAB_RETAINING_CAP_BORE_TOP_DIAMETER
    )
)
SAB_RETAINING_POST_HEIGHT = (
    SAB_BOARD_THICKNESS + SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT
)
SAB_RETAINING_CAP_PRINT_SPACING = 4.0
SAB_PRINT_CENTER_GAP = SAB_RETAINING_CAP_OUTER_DIAMETER + 8.0
# Nominal line-to-line friction fit: the tapered lead-in reaches the full
# receiver diameter at the straight clamping land.
SAB_LID_PIN_DIAMETER = 4.6
SAB_LID_PIN_LENGTH = 5.5
SAB_LID_PIN_TIP_DIAMETER = 3.6
SAB_LID_PIN_TIP_LENGTH = 0.8
SAB_BASE_PIN_RECEIVER_DIAMETER = 4.6
SAB_BASE_PIN_RECEIVER_DEPTH = 6.0
SAB_PIN_DIAMETRAL_CLEARANCE = (
    SAB_BASE_PIN_RECEIVER_DIAMETER - SAB_LID_PIN_DIAMETER
)
SAB_PIN_AXIAL_CLEARANCE = SAB_BASE_PIN_RECEIVER_DEPTH - SAB_LID_PIN_LENGTH
SAB_FAN_FRAME_SIZE_USER_MEASURED = 60.5
SAB_FAN_HEIGHT_ASSUMED = 14.0
SAB_FAN_CENTER_X_USER_DIRECTED = 0.0
SAB_FAN_CENTER_Y_USER_OBSERVED = 7.0
SAB_FAN_OPENING_CLEARANCE_PER_SIDE = 1.0
SAB_FAN_OPENING_SIZE = (
    SAB_FAN_FRAME_SIZE_USER_MEASURED
    + 2.0 * SAB_FAN_OPENING_CLEARANCE_PER_SIDE
)
SAB_INSTALLED_HEIGHT = SAB_BOARD_Z + SAB_HEIGHT
SAB_BASE_HEIGHT = SAB_INSTALLED_HEIGHT - LID_TOP
SAB_CABLE_WINDOW_COUNT = 5
SAB_CABLE_WINDOW_WIDTH = 22.0
SAB_CABLE_WINDOW_HEIGHT = 12.0
SAB_CABLE_WINDOW_BOTTOM = 17.0
SAB_CABLE_RIB_WIDTH = 5.0
SAB_CABLE_WINDOW_TOP = SAB_CABLE_WINDOW_BOTTOM + SAB_CABLE_WINDOW_HEIGHT
SAB_CABLE_TOP_RAIL_HEIGHT = SAB_BASE_HEIGHT - SAB_CABLE_WINDOW_TOP
SAB_USB_PORT_CENTER_Y_USER_DIRECTED = -29.0
SAB_USB_PORT_WIDTH = 16.0
SAB_USB_PORT_HEIGHT = 10.0
SAB_USB_PORT_CORNER_RADIUS = 1.5
SAB_USB_PORT_BOTTOM = 7.0
SAB_USB_PORT_TOP_RAIL_HEIGHT = (
    SAB_BASE_HEIGHT - SAB_USB_PORT_BOTTOM - SAB_USB_PORT_HEIGHT
)
SAB_USB_CONNECTOR_WIDTH_ASSUMED = 9.0
SAB_USB_CONNECTOR_DEPTH_ASSUMED = 8.0
SAB_USB_CONNECTOR_HEIGHT_ASSUMED = 4.0

ENCLOSURE_COLOR = Color(0.10, 0.24, 0.46)
LID_COLOR = Color(0.16, 0.38, 0.68)
PSU_COLOR = Color(0.64, 0.66, 0.68)
BOARD_COLOR = Color(0.05, 0.42, 0.20)
COMPONENT_COLOR = Color(0.14, 0.16, 0.18)


def _box(x: float, y: float, z: float):
    return Box(
        x,
        y,
        z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )


def _rounded_rect_prism_x(
    width: float,
    height: float,
    radius: float,
    depth: float,
    center_x: float,
    center_y: float,
    bottom_z: float,
):
    """Create a rounded-rectangle prism centered on and normal to global X."""
    with BuildSketch(Plane.YZ) as profile:
        with Locations((center_y, bottom_z + height / 2.0)):
            RectangleRounded(width, height, radius)
    prism = extrude(profile.sketch, amount=depth / 2.0, both=True).moved(
        Location((center_x, 0.0, 0.0))
    )
    return _single_solid(prism, "rounded rectangle X prism")


def _single_solid(shape_or_shapes, feature_name: str):
    solids = list(shape_or_shapes.solids())
    if len(solids) != 1:
        raise RuntimeError(
            f"{feature_name} expected one solid but produced {len(solids)}"
        )
    return solids[0]


def _fuse_all(parts, feature_name: str):
    parts = list(parts)
    if not parts:
        raise ValueError(f"{feature_name} did not receive any parts")
    fused = parts[0]
    for part in parts[1:]:
        fused = fused.fuse(part)
    return _single_solid(fused, feature_name)


def _cut_all(blank, cutters, feature_name: str):
    result = blank
    for cutter in cutters:
        result = result.cut(cutter)
    return _single_solid(result, feature_name)


def _tower_centers(outer_x: float, outer_y: float):
    x = outer_x / 2.0 + CORNER_TOWER_OUTSET
    y = outer_y / 2.0 + CORNER_TOWER_OUTSET
    return ((-x, -y), (-x, y), (x, -y), (x, y))


def _sab_standoff_centers():
    return tuple(
        (x, y)
        for y in (
            -SAB_HOLE_SPACING_Y_REPORTED / 2.0,
            SAB_HOLE_SPACING_Y_REPORTED / 2.0,
        )
        for x in (
            -SAB_HOLE_SPACING_X_REPORTED / 2.0,
            SAB_HOLE_SPACING_X_REPORTED / 2.0,
        )
    )


def _corner_tower_gussets(outer_x: float, outer_y: float, height: float):
    """Broad-root gussets that retain a 45-degree tangent at each tower."""
    tangent_offset = CORNER_TOWER_RADIUS / sqrt(2.0)
    gussets = []
    for sign_x in (-1.0, 1.0):
        for sign_y in (-1.0, 1.0):
            corner_x = sign_x * outer_x / 2.0
            corner_y = sign_y * outer_y / 2.0

            horizontal_wall_point = (
                corner_x - sign_x * CORNER_GUSSET_WALL_RUN,
                corner_y,
            )
            horizontal_tangent_wall_point = (
                corner_x - sign_x * CORNER_GUSSET_TANGENT_WALL_RUN,
                corner_y,
            )
            horizontal_tangent_point = (
                corner_x
                + sign_x * (CORNER_TOWER_OUTSET - tangent_offset),
                corner_y
                + sign_y * (CORNER_TOWER_OUTSET + tangent_offset),
            )
            horizontal_shoulder_point = tuple(
                tangent_coordinate
                + (
                    wall_coordinate - tangent_coordinate
                ) * CORNER_GUSSET_TANGENT_RETAINED_FRACTION
                for tangent_coordinate, wall_coordinate in zip(
                    horizontal_tangent_point,
                    horizontal_tangent_wall_point,
                )
            )
            vertical_wall_point = (
                corner_x,
                corner_y - sign_y * CORNER_GUSSET_WALL_RUN,
            )
            vertical_tangent_wall_point = (
                corner_x,
                corner_y - sign_y * CORNER_GUSSET_TANGENT_WALL_RUN,
            )
            vertical_tangent_point = (
                corner_x
                + sign_x * (CORNER_TOWER_OUTSET + tangent_offset),
                corner_y
                + sign_y * (CORNER_TOWER_OUTSET - tangent_offset),
            )
            vertical_shoulder_point = tuple(
                tangent_coordinate
                + (
                    wall_coordinate - tangent_coordinate
                ) * CORNER_GUSSET_TANGENT_RETAINED_FRACTION
                for tangent_coordinate, wall_coordinate in zip(
                    vertical_tangent_point,
                    vertical_tangent_wall_point,
                )
            )

            for points in (
                (
                    horizontal_wall_point,
                    horizontal_shoulder_point,
                    horizontal_tangent_point,
                    (corner_x, corner_y),
                ),
                (
                    vertical_wall_point,
                    vertical_shoulder_point,
                    vertical_tangent_point,
                    (corner_x, corner_y),
                ),
            ):
                with BuildSketch(Plane.XY) as profile:
                    Polygon(*points)
                gussets.append(
                    _single_solid(
                        extrude(profile.sketch, amount=height),
                        "corner tower tangent gusset",
                    )
                )
    return tuple(gussets)


def _base_blank(
    outer_x: float,
    outer_y: float,
    height: float,
    reinforce_corner_towers: bool = False,
):
    outer = _box(outer_x, outer_y, height)
    cavity = _box(
        outer_x - 2.0 * WALL,
        outer_y - 2.0 * WALL,
        height - FLOOR + BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, FLOOR)))
    shell = _single_solid(outer.cut(cavity), "base shell")
    towers = [
        Cylinder(
            radius=CORNER_TOWER_RADIUS,
            height=height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, 0.0)))
        for x, y in _tower_centers(outer_x, outer_y)
    ]
    gussets = (
        _corner_tower_gussets(outer_x, outer_y, height)
        if reinforce_corner_towers
        else ()
    )
    return _fuse_all((shell, *towers, *gussets), "base with corner towers")


def _cut_base_insert_pockets(blank, outer_x: float, outer_y: float, height: float):
    cutters = [
        Cylinder(
            radius=M3_INSERT_POCKET_DIAMETER / 2.0,
            height=M3_INSERT_POCKET_DEPTH + BOOLEAN_OVERSHOOT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, height - M3_INSERT_POCKET_DEPTH)))
        for x, y in _tower_centers(outer_x, outer_y)
    ]
    return _cut_all(blank, cutters, "base insert pockets")


def _cut_base_pin_receivers(blank, outer_x: float, outer_y: float, height: float):
    cutters = [
        Cylinder(
            radius=SAB_BASE_PIN_RECEIVER_DIAMETER / 2.0,
            height=SAB_BASE_PIN_RECEIVER_DEPTH + BOOLEAN_OVERSHOOT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, height - SAB_BASE_PIN_RECEIVER_DEPTH)))
        for x, y in _tower_centers(outer_x, outer_y)
    ]
    return _cut_all(blank, cutters, "base blind pin receivers")


def _lid_corner_pins(outer_x: float, outer_y: float):
    straight_length = SAB_LID_PIN_LENGTH - SAB_LID_PIN_TIP_LENGTH
    pins = []
    for x, y in _tower_centers(outer_x, outer_y):
        stem = Cylinder(
            radius=SAB_LID_PIN_DIAMETER / 2.0,
            height=straight_length + 0.20,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, LID_TOP - 0.20)))
        tip = Cone(
            bottom_radius=SAB_LID_PIN_DIAMETER / 2.0,
            top_radius=SAB_LID_PIN_TIP_DIAMETER / 2.0,
            height=SAB_LID_PIN_TIP_LENGTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, LID_TOP + straight_length)))
        pins.append(_fuse_all((stem, tip), "tapered lid locating pin"))
    return tuple(pins)


def _vent_slot_cutters(
    x_positions,
    y_positions,
    slot_x: float,
    slot_y: float,
    z_height: float,
):
    return [
        _box(slot_x, slot_y, z_height + 2.0 * BOOLEAN_OVERSHOOT).moved(
            Location((x, y, -BOOLEAN_OVERSHOOT))
        )
        for y in y_positions
        for x in x_positions
    ]


def _build_lid_print(
    outer_x: float,
    outer_y: float,
    vent_x_positions,
    vent_y_positions,
    slot_x: float,
    slot_y: float,
    label: str,
    reinforce_corner_towers: bool = False,
    use_corner_pins: bool = False,
):
    plate_parts = [_box(outer_x, outer_y, LID_TOP)]
    plate_parts.extend(
        Cylinder(
            radius=CORNER_TOWER_RADIUS,
            height=LID_TOP,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, 0.0)))
        for x, y in _tower_centers(outer_x, outer_y)
    )
    if reinforce_corner_towers:
        plate_parts.extend(_corner_tower_gussets(outer_x, outer_y, LID_TOP))
    plate = _fuse_all(plate_parts, f"{label} lid plate and ears")

    plug_outer_x = outer_x - 2.0 * WALL - 2.0 * LID_CLEARANCE_PER_SIDE
    plug_outer_y = outer_y - 2.0 * WALL - 2.0 * LID_CLEARANCE_PER_SIDE
    plug_outer = _box(
        plug_outer_x,
        plug_outer_y,
        LID_PLUG_DEPTH + 0.20,
    ).moved(Location((0.0, 0.0, LID_TOP - 0.20)))
    plug_inner = _box(
        plug_outer_x - 2.0 * LID_PLUG_WALL,
        plug_outer_y - 2.0 * LID_PLUG_WALL,
        LID_PLUG_DEPTH + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, LID_TOP - 0.20)))
    plug_frame = _single_solid(plug_outer.cut(plug_inner), f"{label} lid plug")
    lid = _fuse_all((plate, plug_frame), f"{label} complete lid")

    cutters = _vent_slot_cutters(
        vent_x_positions,
        vent_y_positions,
        slot_x,
        slot_y,
        LID_TOP,
    )
    if not use_corner_pins:
        cutters.extend(
            Cylinder(
                radius=M3_LID_CLEARANCE_DIAMETER / 2.0,
                height=LID_TOP + 2.0 * BOOLEAN_OVERSHOOT,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, -BOOLEAN_OVERSHOOT)))
            for x, y in _tower_centers(outer_x, outer_y)
        )
    lid = _cut_all(lid, cutters, f"{label} ventilated lid")
    if use_corner_pins:
        lid = _fuse_all(
            (lid, *_lid_corner_pins(outer_x, outer_y)),
            f"{label} lid with integral locating pins",
        )
    lid.label = f"{label}_lid_print_exterior_face_down"
    lid.color = LID_COLOR
    return lid


def assembled_lid(lid_print, base_height: float):
    """Flip a print-oriented lid into its installed pose above the base."""
    return lid_print.rotate(Axis.X, 180.0).moved(
        Location((0.0, 0.0, base_height + LID_TOP))
    )


def build_lrs_base_details():
    blank = _base_blank(LRS_OUTER_X, LRS_OUTER_Y, LRS_BASE_HEIGHT)

    terminal_window = _box(
        2.0 * WALL + 2.0 * BOOLEAN_OVERSHOOT,
        LRS_TERMINAL_WINDOW_Y,
        LRS_TERMINAL_WINDOW_HEIGHT,
    ).moved(
        Location(
            (
                -LRS_OUTER_X / 2.0 - WALL,
                0.0,
                LRS_TERMINAL_WINDOW_BOTTOM,
            )
        )
    )

    side_vents = []
    for y in (-LRS_OUTER_Y / 2.0 - WALL, LRS_OUTER_Y / 2.0):
        for x in (-76.0, -50.0, -24.0, 2.0, 28.0, 54.0, 80.0):
            side_vents.append(
                _box(18.0, 2.0 * WALL + 2.0, 16.0).moved(
                    Location((x, y, 12.0))
                )
            )

    rear_vents = [
        _box(2.0 * WALL + 2.0, 15.0, 16.0).moved(
            Location((LRS_OUTER_X / 2.0, y, 12.0))
        )
        for y in (-36.0, -12.0, 12.0, 36.0)
    ]

    base = _cut_all(
        blank,
        (terminal_window, *side_vents, *rear_vents),
        "LRS terminal and ventilation openings",
    )
    mount_centers = tuple(
        (x, y)
        for y in (-LRS_MOUNT_SPACING_Y / 2.0, LRS_MOUNT_SPACING_Y / 2.0)
        for x in (-LRS_MOUNT_SPACING_X / 2.0, LRS_MOUNT_SPACING_X / 2.0)
    )
    support_pads = [
        Cylinder(
            radius=LRS_SUPPORT_PAD_RADIUS,
            height=LRS_SUPPORT_PAD_HEIGHT + 0.20,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, FLOOR - 0.20)))
        for x, y in mount_centers
    ]
    base = _fuse_all((base, *support_pads), "LRS base and mounting pads")
    mount_holes = [
        Cylinder(
            radius=LRS_MOUNT_CLEARANCE_DIAMETER / 2.0,
            height=LRS_COMPONENT_Z + 2.0 * BOOLEAN_OVERSHOOT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, -BOOLEAN_OVERSHOOT)))
        for x, y in mount_centers
    ]
    base = _cut_all(base, mount_holes, "LRS M4 bottom mounting holes")
    base = _cut_base_insert_pockets(
        base,
        LRS_OUTER_X,
        LRS_OUTER_Y,
        LRS_BASE_HEIGHT,
    )
    base.label = "lrs_350_24_base"
    base.color = ENCLOSURE_COLOR

    access_probe = _box(
        10.0,
        LRS_TERMINAL_WINDOW_Y - 1.0,
        LRS_TERMINAL_WINDOW_HEIGHT - 1.0,
    ).moved(
        Location(
            (
                -LRS_OUTER_X / 2.0 - 5.0,
                0.0,
                LRS_TERMINAL_WINDOW_BOTTOM + 0.5,
            )
        )
    )
    return {
        "base": base,
        "terminal_window_cutter": terminal_window,
        "terminal_access_probe": access_probe,
        "side_vent_cutters": tuple(side_vents),
        "rear_vent_cutters": tuple(rear_vents),
        "mount_centers": mount_centers,
    }


def build_lrs_base():
    return build_lrs_base_details()["base"]


def build_lrs_lid_print():
    return _build_lid_print(
        LRS_OUTER_X,
        LRS_OUTER_Y,
        (-84.0, -60.0, -36.0, -12.0, 12.0, 36.0, 60.0, 84.0),
        (-42.0, -21.0, 0.0, 21.0, 42.0),
        16.0,
        6.0,
        "lrs_350_24",
    )


def build_lrs_reference():
    reference = _box(LRS_LENGTH, LRS_WIDTH, LRS_HEIGHT).moved(
        Location((0.0, 0.0, LRS_COMPONENT_Z))
    )
    reference.label = "mean_well_lrs_350_24_reference_envelope"
    reference.color = PSU_COLOR
    return reference


def build_sab_base_details():
    blank = _base_blank(
        SAB_OUTER_X,
        SAB_OUTER_Y,
        SAB_BASE_HEIGHT,
        reinforce_corner_towers=True,
    )

    # Only the positive-Y long wall carries cable exits. Five short bays keep
    # each horizontal bridge at 22 mm while leaving 5 mm vertical cross ribs.
    cable_bank_width = (
        SAB_CABLE_WINDOW_COUNT * SAB_CABLE_WINDOW_WIDTH
        + (SAB_CABLE_WINDOW_COUNT - 1) * SAB_CABLE_RIB_WIDTH
    )
    cable_pitch = SAB_CABLE_WINDOW_WIDTH + SAB_CABLE_RIB_WIDTH
    cable_x_positions = tuple(
        -cable_bank_width / 2.0
        + SAB_CABLE_WINDOW_WIDTH / 2.0
        + index * cable_pitch
        for index in range(SAB_CABLE_WINDOW_COUNT)
    )
    access_cutters = [
        _box(
            SAB_CABLE_WINDOW_WIDTH,
            2.0 * WALL + 2.0,
            SAB_CABLE_WINDOW_HEIGHT,
        ).moved(
            Location(
                (
                    x,
                    SAB_OUTER_Y / 2.0,
                    SAB_CABLE_WINDOW_BOTTOM,
                )
            )
        )
        for x in cable_x_positions
    ]

    # User-directed placement: the negative-X short wall, biased 29 mm toward
    # -Y. The along-wall center remains a pre-print measurement.
    usb_port_cutter = _rounded_rect_prism_x(
        SAB_USB_PORT_WIDTH,
        SAB_USB_PORT_HEIGHT,
        SAB_USB_PORT_CORNER_RADIUS,
        2.0 * WALL + 2.0,
        -SAB_OUTER_X / 2.0,
        SAB_USB_PORT_CENTER_Y_USER_DIRECTED,
        SAB_USB_PORT_BOTTOM,
    )

    shell = _cut_all(
        blank,
        (*access_cutters, usb_port_cutter),
        "SAB reinforced cable exits and USB-C access",
    )

    standoff_centers = _sab_standoff_centers()
    standoffs = [
        Cylinder(
            radius=SAB_STANDOFF_RADIUS,
            height=SAB_STANDOFF_HEIGHT + 0.20,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, FLOOR - 0.20)))
        for x, y in standoff_centers
    ]
    retaining_posts = [
        Cylinder(
            radius=SAB_RETAINING_POST_DIAMETER / 2.0,
            height=SAB_RETAINING_POST_HEIGHT + 0.20,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, SAB_BOARD_Z - 0.20)))
        for x, y in standoff_centers
    ]
    base = _fuse_all(
        (shell, *standoffs, *retaining_posts),
        "SAB base, standoffs, and integral PCB retaining posts",
    )
    base = _cut_base_pin_receivers(
        base,
        SAB_OUTER_X,
        SAB_OUTER_Y,
        SAB_BASE_HEIGHT,
    )
    base.label = "sab_1060_base"
    base.color = ENCLOSURE_COLOR

    access_probes = tuple(
        _box(
            SAB_CABLE_WINDOW_WIDTH - 1.0,
            10.0,
            SAB_CABLE_WINDOW_HEIGHT - 1.0,
        ).moved(
            Location(
                (
                    x,
                    SAB_OUTER_Y / 2.0,
                    SAB_CABLE_WINDOW_BOTTOM + 0.5,
                )
            )
        )
        for x in cable_x_positions
    )
    usb_access_probe = _rounded_rect_prism_x(
        SAB_USB_PORT_WIDTH - 1.0,
        SAB_USB_PORT_HEIGHT - 1.0,
        SAB_USB_PORT_CORNER_RADIUS - 0.5,
        10.0,
        -SAB_OUTER_X / 2.0,
        SAB_USB_PORT_CENTER_Y_USER_DIRECTED,
        SAB_USB_PORT_BOTTOM + 0.5,
    )
    closed_wall_probes = (
        _box(20.0, 4.0, 6.0).moved(
            Location((0.0, -SAB_OUTER_Y / 2.0, SAB_CABLE_WINDOW_BOTTOM + 2.0))
        ),
        _box(4.0, 20.0, 6.0).moved(
            Location((-SAB_OUTER_X / 2.0, 0.0, SAB_CABLE_WINDOW_BOTTOM + 2.0))
        ),
        _box(4.0, 20.0, 6.0).moved(
            Location((SAB_OUTER_X / 2.0, 0.0, SAB_CABLE_WINDOW_BOTTOM + 2.0))
        ),
    )
    return {
        "base": base,
        "access_cutters": tuple(access_cutters),
        "access_probes": access_probes,
        "usb_port_cutter": usb_port_cutter,
        "usb_access_probe": usb_access_probe,
        "closed_wall_probes": closed_wall_probes,
        "cable_x_positions": cable_x_positions,
        "standoff_centers": standoff_centers,
        "retaining_posts": tuple(retaining_posts),
        "pin_receiver_centers": _tower_centers(SAB_OUTER_X, SAB_OUTER_Y),
    }


def build_sab_base():
    return build_sab_base_details()["base"]


def build_sab_retaining_cap_installed():
    """Push-on cap with a tapered bore, authored board-contact-face-down."""
    body = Cylinder(
        radius=SAB_RETAINING_CAP_OUTER_DIAMETER / 2.0,
        height=SAB_RETAINING_CAP_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # Overshoot both faces while retaining the exact requested diameters at
    # the cap faces. This avoids coincident boolean faces without changing fit.
    entry_radius = SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER / 2.0
    top_radius = SAB_RETAINING_CAP_BORE_TOP_DIAMETER / 2.0
    radius_slope = (
        top_radius - entry_radius
    ) / SAB_RETAINING_CAP_HEIGHT
    cutter_bottom_radius = entry_radius - radius_slope * BOOLEAN_OVERSHOOT
    cutter_top_radius = top_radius + radius_slope * BOOLEAN_OVERSHOOT
    bore = Cone(
        bottom_radius=cutter_bottom_radius,
        top_radius=cutter_top_radius,
        height=SAB_RETAINING_CAP_HEIGHT + 2.0 * BOOLEAN_OVERSHOOT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, -BOOLEAN_OVERSHOOT)))
    cap = _single_solid(body.cut(bore), "SAB tapered-bore PCB retaining cap")
    cap.label = "sab_1060_pcb_retaining_cap_installed"
    cap.color = LID_COLOR
    return cap


def build_sab_retaining_cap_print():
    """Flip the cap top-face-down so its tapered bore prints support-free."""
    cap = build_sab_retaining_cap_installed().rotate(Axis.X, 180.0).moved(
        Location((0.0, 0.0, SAB_RETAINING_CAP_HEIGHT))
    )
    cap.label = "sab_1060_pcb_retaining_cap_print_top_face_down"
    cap.color = LID_COLOR
    return cap


def build_sab_retaining_caps_installed():
    caps = []
    board_top = SAB_BOARD_Z + SAB_BOARD_THICKNESS
    for index, (x, y) in enumerate(_sab_standoff_centers(), start=1):
        cap = build_sab_retaining_cap_installed().moved(
            Location((x, y, board_top))
        )
        cap.label = f"sab_1060_pcb_retaining_cap_{index}_installed"
        caps.append(cap)
    return tuple(caps)


def build_sab_retaining_caps_print():
    pitch = (
        SAB_RETAINING_CAP_OUTER_DIAMETER
        + SAB_RETAINING_CAP_PRINT_SPACING
    )
    caps = []
    for index in range(4):
        x = (index - 1.5) * pitch
        cap = build_sab_retaining_cap_print().moved(Location((x, 0.0, 0.0)))
        cap.label = f"sab_1060_pcb_retaining_cap_{index + 1}_print"
        caps.append(cap)
    return tuple(caps)


def build_sab_lid_print():
    lid = _build_lid_print(
        SAB_OUTER_X,
        SAB_OUTER_Y,
        (),
        (),
        1.0,
        1.0,
        "sab_1060",
        reinforce_corner_towers=True,
        use_corner_pins=True,
    )
    fan_opening = _box(
        SAB_FAN_OPENING_SIZE,
        SAB_FAN_OPENING_SIZE,
        LID_TOP + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(
        Location(
            (
                SAB_FAN_CENTER_X_USER_DIRECTED,
                # The print-oriented lid is flipped 180 degrees about X for
                # installation, so author the Y offset with the opposite sign.
                -SAB_FAN_CENTER_Y_USER_OBSERVED,
                -BOOLEAN_OVERSHOOT,
            )
        )
    )
    lid = _single_solid(lid.cut(fan_opening), "SAB fan-frame lid opening")
    lid.label = "sab_1060_lid_print_fan_frame_flush"
    lid.color = LID_COLOR
    return lid


def build_sab_reference():
    board = _box(SAB_LENGTH, SAB_WIDTH, SAB_BOARD_THICKNESS).moved(
        Location((0.0, 0.0, SAB_BOARD_Z))
    )
    holes = [
        Cylinder(
            radius=SAB_HOLE_DIAMETER_REPORTED / 2.0,
            height=SAB_BOARD_THICKNESS + 2.0 * BOOLEAN_OVERSHOOT,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(Location((x, y, SAB_BOARD_Z - BOOLEAN_OVERSHOOT)))
        for y in (
            -SAB_HOLE_SPACING_Y_REPORTED / 2.0,
            SAB_HOLE_SPACING_Y_REPORTED / 2.0,
        )
        for x in (
            -SAB_HOLE_SPACING_X_REPORTED / 2.0,
            SAB_HOLE_SPACING_X_REPORTED / 2.0,
        )
    ]
    board = _cut_all(board, holes, "SAB reference mounting holes")
    board.color = BOARD_COLOR

    # The non-fan envelope is deliberately conservative up to Z=32, but its
    # central fan footprint is removed so the explicit flush fan can occupy it.
    non_fan_top_z = 32.0
    component_envelope = _box(
        136.0,
        98.0,
        non_fan_top_z - SAB_BOARD_Z - SAB_BOARD_THICKNESS,
    ).moved(
        Location((0.0, 0.0, SAB_BOARD_Z + SAB_BOARD_THICKNESS))
    )
    fan_relief = _box(
        SAB_FAN_FRAME_SIZE_USER_MEASURED,
        SAB_FAN_FRAME_SIZE_USER_MEASURED,
        non_fan_top_z - SAB_BOARD_Z + BOOLEAN_OVERSHOOT,
    ).moved(
        Location(
            (
                SAB_FAN_CENTER_X_USER_DIRECTED,
                SAB_FAN_CENTER_Y_USER_OBSERVED,
                SAB_BOARD_Z + SAB_BOARD_THICKNESS,
            )
        )
    )
    component_envelope = _single_solid(
        component_envelope.cut(fan_relief),
        "SAB conservative non-fan component envelope",
    )
    cap_reliefs = [
        Cylinder(
            radius=(
                SAB_RETAINING_CAP_OUTER_DIAMETER / 2.0
                + SAB_RETAINING_CAP_COMPONENT_CLEARANCE
            ),
            height=(
                non_fan_top_z
                - SAB_BOARD_Z
                - SAB_BOARD_THICKNESS
                + 2.0 * BOOLEAN_OVERSHOOT
            ),
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).moved(
            Location(
                (
                    x,
                    y,
                    SAB_BOARD_Z
                    + SAB_BOARD_THICKNESS
                    - BOOLEAN_OVERSHOOT,
                )
            )
        )
        for x, y in _sab_standoff_centers()
    ]
    component_envelope = _cut_all(
        component_envelope,
        cap_reliefs,
        "SAB component envelope mounting-zone cap clearances",
    )
    component_envelope.color = COMPONENT_COLOR

    fan = _box(
        SAB_FAN_FRAME_SIZE_USER_MEASURED,
        SAB_FAN_FRAME_SIZE_USER_MEASURED,
        SAB_FAN_HEIGHT_ASSUMED,
    ).moved(
        Location(
            (
                SAB_FAN_CENTER_X_USER_DIRECTED,
                SAB_FAN_CENTER_Y_USER_OBSERVED,
                SAB_INSTALLED_HEIGHT - SAB_FAN_HEIGHT_ASSUMED,
            )
        )
    )
    fan.label = "user_measured_60_5mm_sab_1060_fan_reference"
    fan.color = COMPONENT_COLOR

    usb_connector = _box(
        SAB_USB_CONNECTOR_DEPTH_ASSUMED,
        SAB_USB_CONNECTOR_WIDTH_ASSUMED,
        SAB_USB_CONNECTOR_HEIGHT_ASSUMED,
    ).moved(
        Location(
            (
                -SAB_LENGTH / 2.0,
                SAB_USB_PORT_CENTER_Y_USER_DIRECTED,
                SAB_BOARD_Z,
            )
        )
    )
    usb_connector.label = "assumed_sab_1060_usb_c_connector_reference"
    usb_connector.color = COMPONENT_COLOR

    reference = Compound(
        children=[board, component_envelope, fan, usb_connector],
        label="dayton_sab_1060_reference_envelope",
    )
    return reference


def print_layout_offset_y(outer_y: float, center_gap: float = 8.0):
    footprint_y = outer_y + 2.0 * (
        CORNER_TOWER_OUTSET + CORNER_TOWER_RADIUS
    )
    return (footprint_y + center_gap) / 2.0


def print_layout(
    base,
    lid,
    outer_y: float,
    assembly_name: str,
    extra_print_objects=(),
    center_gap: float = 8.0,
):
    from cadpy.assembly import AssemblyHelper

    offset = print_layout_offset_y(outer_y, center_gap)
    base_placed = base.moved(Location((0.0, -offset, 0.0)))
    lid_placed = lid.moved(Location((0.0, offset, 0.0)))
    assembly = AssemblyHelper(assembly_name)
    assembly.add(base_placed, "base_print_object")
    assembly.add(lid_placed, "lid_print_object_exterior_face_down")
    for shape, label in extra_print_objects:
        assembly.add(shape, label)
    return assembly.build()
