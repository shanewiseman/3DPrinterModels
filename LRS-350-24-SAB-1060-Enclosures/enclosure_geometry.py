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
LID_RISER_SEAT_BRIDGE_HEIGHT = 0.40
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
SAB_FLOOR_RIB_WIDTH = 2.0
SAB_FLOOR_RIB_HEIGHT = 1.75
SAB_RETAINING_POST_DIAMETER = 3.4
SAB_RETAINING_POST_TIP_CHAMFER = 0.4
SAB_RETAINING_POST_PCB_DIAMETRAL_CLEARANCE = (
    SAB_HOLE_DIAMETER_REPORTED - SAB_RETAINING_POST_DIAMETER
)
SAB_RETAINING_CAP_OUTER_DIAMETER = 3.0 * SAB_RETAINING_POST_DIAMETER
SAB_RETAINING_CAP_BODY_DIAMETER = 6.8
SAB_RETAINING_CAP_BODY_HEIGHT = 8.0
SAB_RETAINING_CAP_HEIGHT = 10.0
SAB_RETAINING_CAP_EDGE_CHAMFER = 0.4
SAB_RETAINING_CAP_COMPONENT_CLEARANCE = 0.5
SAB_RETAINING_CAP_BORE_ENTRY_DIAMETER = SAB_HOLE_DIAMETER_REPORTED
SAB_RETAINING_CAP_BORE_TOP_DIAMETER = 3.0
SAB_RETAINING_CAP_SLOT_COUNT = 3
SAB_RETAINING_CAP_SLOT_WIDTH = 0.5
SAB_RETAINING_CAP_SLOT_DEPTH = 6.0
SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT = 8.0
SAB_RETAINING_CAP_LOCK_START_DEPTH = (
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
SAB_PRINT_CENTER_GAP = 8.0
# Free-sliding locating fit revised from the user's physical test of the
# already-printed base. The pins now center the lid but are not intended to
# retain it. The unchanged 4.6 mm receiver leaves 0.60 mm diametral clearance.
SAB_LID_PIN_DIAMETER = 4.0
SAB_LID_PIN_LENGTH = 5.5
SAB_LID_PIN_TIP_DIAMETER = 3.2
SAB_LID_PIN_TIP_LENGTH = 0.8
SAB_BASE_PIN_RECEIVER_DIAMETER = 4.6
SAB_BASE_PIN_RECEIVER_DEPTH = 6.0
SAB_PIN_DIAMETRAL_CLEARANCE = (
    SAB_BASE_PIN_RECEIVER_DIAMETER - SAB_LID_PIN_DIAMETER
)
SAB_PIN_AXIAL_CLEARANCE = SAB_BASE_PIN_RECEIVER_DEPTH - SAB_LID_PIN_LENGTH
SAB_FAN_FRAME_SIZE_USER_MEASURED = 60.1
SAB_FAN_HEIGHT_ASSUMED = 14.0
# Physical clearances are referenced while looking at the enclosure from the
# rear: viewer-left is +X, viewer-right is -X, rear is +Y, and front is -Y.
SAB_FAN_REAR_CLEARANCE_USER_MEASURED = 24.5
SAB_FAN_FRONT_CLEARANCE_USER_MEASURED = 35.9
SAB_FAN_LEFT_CLEARANCE_USER_MEASURED = 47.6
SAB_FAN_RIGHT_CLEARANCE_USER_MEASURED = 50.7
SAB_FAN_CENTER_X_FROM_EDGE_MEASUREMENTS = (
    SAB_FAN_RIGHT_CLEARANCE_USER_MEASURED
    - SAB_FAN_LEFT_CLEARANCE_USER_MEASURED
) / 2.0
# Rear-view right is global -X. The user's latest physical alignment moves the
# complete fan opening/reference/guard 2 mm toward rear-view right.
SAB_FAN_REAR_VIEW_RIGHT_SHIFT = 2.0
SAB_FAN_CENTER_X_USER_DIRECTED = (
    SAB_FAN_CENTER_X_FROM_EDGE_MEASUREMENTS
    - SAB_FAN_REAR_VIEW_RIGHT_SHIFT
)
SAB_FAN_CENTER_Y_USER_OBSERVED = (
    SAB_FAN_FRONT_CLEARANCE_USER_MEASURED
    - SAB_FAN_REAR_CLEARANCE_USER_MEASURED
) / 2.0
SAB_FAN_OPENING_CLEARANCE_PER_SIDE = 1.0
SAB_FAN_OPENING_SIZE = (
    SAB_FAN_FRAME_SIZE_USER_MEASURED
    + 2.0 * SAB_FAN_OPENING_CLEARANCE_PER_SIDE
)
SAB_FAN_GUARD_OUTER_SIZE = SAB_FAN_OPENING_SIZE + 2.0
SAB_FAN_GUARD_FRAME_WIDTH = 2.0
SAB_FAN_GUARD_THICKNESS = 1.6
SAB_FAN_GUARD_SPOKE_WIDTH = 2.0
SAB_FAN_GUARD_HUB_DIAMETER = 12.0
SAB_FAN_GUARD_SKIRT_DEPTH = 1.2
SAB_FAN_GUARD_SKIRT_OUTER_SIZE = SAB_FAN_OPENING_SIZE - 0.4
SAB_FAN_GUARD_SKIRT_INNER_SIZE = SAB_FAN_FRAME_SIZE_USER_MEASURED + 0.6
SAB_PRINT_GUARD_GAP = 8.0
SAB_FIT_COUPON_X = 14.0
SAB_FIT_COUPON_Y = 10.0
SAB_FIT_COUPON_BASE_HEIGHT = 2.0
SAB_FIT_COUPON_CENTER_X = 23.0
SAB_LID_PIN_FIT_COUPON_X = 14.0
SAB_LID_PIN_FIT_COUPON_Y = 10.0
SAB_LID_PIN_FIT_COUPON_BASE_HEIGHT = 2.0
SAB_LID_PIN_FIT_COUPON_CENTER_X = -23.0
SAB_INSTALLED_HEIGHT = SAB_BOARD_Z + SAB_HEIGHT
SAB_BASE_HEIGHT = SAB_INSTALLED_HEIGHT - LID_TOP
SAB_LID_RISER_HEIGHT = 8.0
SAB_LID_INTERIOR_ROOF_Z = SAB_BASE_HEIGHT + SAB_LID_RISER_HEIGHT
SAB_LID_EXTERIOR_TOP_Z = SAB_LID_INTERIOR_ROOF_Z + LID_TOP
SAB_NEAR_WALL_COMPONENT_OFFSET = 5.0
# Roof access above the three front (-Y) Mini-Fit Jr. plug groups. X centers
# are scaled from Dayton's official top-view wiring-guide image using the
# reported 142 mm mounting-hole spacing. The original user-supplied widths
# were 32, 32, and 10 mm. Each side now carries 1.6 mm of extra X clearance
# for the photo-derived center uncertainty; the 16 mm Y depth is unchanged.
SAB_FRONT_CONNECTOR_OPENING_COUNT = 3
SAB_FRONT_CONNECTOR_OPENING_CENTER_XS = (-44.0, 29.5, 55.0)
SAB_FRONT_CONNECTOR_OPENING_WIDTHS = (35.2, 35.2, 13.2)
SAB_FRONT_CONNECTOR_OPENING_DEPTH = 16.0
SAB_FRONT_CONNECTOR_OPENING_CENTER_Y = -50.5
SAB_FRONT_CONNECTOR_JOINED_OPENING_MIN_X = (
    SAB_FRONT_CONNECTOR_OPENING_CENTER_XS[1]
    - SAB_FRONT_CONNECTOR_OPENING_WIDTHS[1] / 2.0
)
SAB_FRONT_CONNECTOR_JOINED_OPENING_MAX_X = (
    SAB_FRONT_CONNECTOR_OPENING_CENTER_XS[2]
    + SAB_FRONT_CONNECTOR_OPENING_WIDTHS[2] / 2.0
)
SAB_FRONT_CONNECTOR_JOINED_OPENING_WIDTH = (
    SAB_FRONT_CONNECTOR_JOINED_OPENING_MAX_X
    - SAB_FRONT_CONNECTOR_JOINED_OPENING_MIN_X
)
SAB_FRONT_CONNECTOR_JOINED_OPENING_CENTER_X = (
    SAB_FRONT_CONNECTOR_JOINED_OPENING_MIN_X
    + SAB_FRONT_CONNECTOR_JOINED_OPENING_MAX_X
) / 2.0
SAB_USB_PORT_CENTER_Y_USER_DIRECTED = -29.0
SAB_USB_PORT_WIDTH = 16.0
SAB_USB_PORT_CORNER_RADIUS = 1.5
SAB_USB_PORT_HEIGHT = 10.0
SAB_USB_PORT_TOP_RAIL_HEIGHT = 7.0
SAB_USB_PORT_BOTTOM = (
    SAB_BASE_HEIGHT - SAB_USB_PORT_HEIGHT - SAB_USB_PORT_TOP_RAIL_HEIGHT
)
SAB_USB_CONNECTOR_WIDTH_ASSUMED = 9.0
SAB_USB_CONNECTOR_DEPTH_ASSUMED = 8.0
SAB_USB_CONNECTOR_HEIGHT_ASSUMED = 4.0
SAB_USB_CONNECTOR_BOTTOM_ASSUMED = (
    SAB_USB_PORT_BOTTOM
    + (SAB_USB_PORT_HEIGHT - SAB_USB_CONNECTOR_HEIGHT_ASSUMED) / 2.0
)
# Circular ventilation perforations through both short (global X-normal) base
# walls. The lowest row remains 1 mm above the interior floor, the upper row
# remains over 1 mm below the wall top, and the end columns stay clear of the
# broad corner gussets. Conflicting holes are omitted around the USB-C inlet.
SAB_SHORT_END_PERFORATION_DIAMETER = 5.0
SAB_SHORT_END_PERFORATION_Y_CENTERS = (
    -39.0,
    -26.0,
    -13.0,
    0.0,
    13.0,
    26.0,
    39.0,
)
SAB_SHORT_END_PERFORATION_Z_CENTERS = (6.5, 14.5, 22.5, 30.5)
SAB_SHORT_END_PERFORATION_MIN_BORDER = 1.0
SAB_SHORT_END_PERFORATION_USB_CLEARANCE = 1.0

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


def _circular_prism_x(
    diameter: float,
    depth: float,
    center_x: float,
    center_y: float,
    center_z: float,
):
    """Create a circular prism centered on and normal to global X."""
    return Cylinder(
        radius=diameter / 2.0,
        height=depth,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).rotate(Axis.Y, 90.0).moved(
        Location((center_x, center_y, center_z))
    )


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


def _sab_front_connector_opening_specs():
    return tuple(
        zip(
            SAB_FRONT_CONNECTOR_OPENING_CENTER_XS,
            SAB_FRONT_CONNECTOR_OPENING_WIDTHS,
        )
    )


def _sab_front_connector_cut_specs():
    """Two physical roof cuts serving the three front connector zones."""
    return (
        (
            SAB_FRONT_CONNECTOR_OPENING_CENTER_XS[0],
            SAB_FRONT_CONNECTOR_OPENING_WIDTHS[0],
        ),
        (
            SAB_FRONT_CONNECTOR_JOINED_OPENING_CENTER_X,
            SAB_FRONT_CONNECTOR_JOINED_OPENING_WIDTH,
        ),
    )


def _sab_short_end_perforation_specs():
    radius = SAB_SHORT_END_PERFORATION_DIAMETER / 2.0
    usb_min_y = SAB_USB_PORT_CENTER_Y_USER_DIRECTED - SAB_USB_PORT_WIDTH / 2.0
    usb_max_y = SAB_USB_PORT_CENTER_Y_USER_DIRECTED + SAB_USB_PORT_WIDTH / 2.0
    usb_min_z = SAB_USB_PORT_BOTTOM
    usb_max_z = SAB_USB_PORT_BOTTOM + SAB_USB_PORT_HEIGHT
    specs = []
    for wall_x in (-SAB_OUTER_X / 2.0, SAB_OUTER_X / 2.0):
        for center_z in SAB_SHORT_END_PERFORATION_Z_CENTERS:
            for center_y in SAB_SHORT_END_PERFORATION_Y_CENTERS:
                if wall_x < 0.0:
                    y_clear = (
                        center_y + radius
                        <= usb_min_y - SAB_SHORT_END_PERFORATION_USB_CLEARANCE
                        or center_y - radius
                        >= usb_max_y + SAB_SHORT_END_PERFORATION_USB_CLEARANCE
                    )
                    z_clear = (
                        center_z + radius
                        <= usb_min_z - SAB_SHORT_END_PERFORATION_USB_CLEARANCE
                        or center_z - radius
                        >= usb_max_z + SAB_SHORT_END_PERFORATION_USB_CLEARANCE
                    )
                    if not (y_clear or z_clear):
                        continue
                specs.append((wall_x, center_y, center_z))
    return tuple(specs)


def _sab_retaining_post(
    center_x: float,
    center_y: float,
    bottom_z: float,
    height: float,
):
    """Create a 3.4 mm post with a 0.4 mm conical insertion chamfer."""
    shaft_height = height - SAB_RETAINING_POST_TIP_CHAMFER
    shaft = Cylinder(
        radius=SAB_RETAINING_POST_DIAMETER / 2.0,
        height=shaft_height + 0.20,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, center_y, bottom_z - 0.20)))
    tip = Cone(
        bottom_radius=SAB_RETAINING_POST_DIAMETER / 2.0,
        top_radius=(
            SAB_RETAINING_POST_DIAMETER / 2.0
            - SAB_RETAINING_POST_TIP_CHAMFER
        ),
        height=SAB_RETAINING_POST_TIP_CHAMFER,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, center_y, bottom_z + shaft_height)))
    return _fuse_all((shaft, tip), "chamfered SAB retaining post")


def _sab_floor_ribs():
    """Low orthogonal ribs that stiffen the floor below the PCB envelope."""
    rib_bottom = FLOOR - 0.20
    rib_height = SAB_FLOOR_RIB_HEIGHT + 0.20
    ribs = []
    for y in (-SAB_HOLE_SPACING_Y_REPORTED / 2.0, 0.0,
              SAB_HOLE_SPACING_Y_REPORTED / 2.0):
        ribs.append(
            _box(
                SAB_HOLE_SPACING_X_REPORTED,
                SAB_FLOOR_RIB_WIDTH,
                rib_height,
            ).moved(Location((0.0, y, rib_bottom)))
        )
    for x in (-SAB_HOLE_SPACING_X_REPORTED / 2.0, 0.0,
              SAB_HOLE_SPACING_X_REPORTED / 2.0):
        ribs.append(
            _box(
                SAB_FLOOR_RIB_WIDTH,
                SAB_HOLE_SPACING_Y_REPORTED,
                rib_height,
            ).moved(Location((x, 0.0, rib_bottom)))
        )
    return tuple(ribs)


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


def _lid_pin(center_x: float, center_y: float, pin_base_z: float):
    straight_length = SAB_LID_PIN_LENGTH - SAB_LID_PIN_TIP_LENGTH
    stem = Cylinder(
        radius=SAB_LID_PIN_DIAMETER / 2.0,
        height=straight_length + 0.20,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, center_y, pin_base_z - 0.20)))
    tip = Cone(
        bottom_radius=SAB_LID_PIN_DIAMETER / 2.0,
        top_radius=SAB_LID_PIN_TIP_DIAMETER / 2.0,
        height=SAB_LID_PIN_TIP_LENGTH,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, center_y, pin_base_z + straight_length)))
    return _fuse_all((stem, tip), "tapered lid locating pin")


def _lid_corner_pins(
    outer_x: float,
    outer_y: float,
    pin_base_z: float,
):
    return tuple(
        _lid_pin(x, y, pin_base_z)
        for x, y in _tower_centers(outer_x, outer_y)
    )


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
    lid_riser_height: float = 0.0,
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

    lid_parts = [plate]
    mating_plane_z = LID_TOP + lid_riser_height
    if lid_riser_height > 0.0:
        riser_bottom_z = LID_TOP - 0.20
        riser_outer = _box(
            outer_x,
            outer_y,
            lid_riser_height + 0.20,
        ).moved(Location((0.0, 0.0, riser_bottom_z)))
        riser_inner = _box(
            outer_x - 2.0 * WALL,
            outer_y - 2.0 * WALL,
            lid_riser_height + 2.0 * BOOLEAN_OVERSHOOT,
        ).moved(
            Location(
                (
                    0.0,
                    0.0,
                    riser_bottom_z - BOOLEAN_OVERSHOOT,
                )
            )
        )
        riser_frame = _single_solid(
            riser_outer.cut(riser_inner),
            f"{label} raised perimeter hood",
        )
        riser_columns = tuple(
            Cylinder(
                radius=CORNER_TOWER_RADIUS,
                height=lid_riser_height + 0.20,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).moved(Location((x, y, riser_bottom_z)))
            for x, y in _tower_centers(outer_x, outer_y)
        )
        riser_gussets = (
            tuple(
                gusset.moved(Location((0.0, 0.0, riser_bottom_z)))
                for gusset in _corner_tower_gussets(
                    outer_x,
                    outer_y,
                    lid_riser_height + 0.20,
                )
            )
            if reinforce_corner_towers
            else ()
        )
        lid_parts.extend((riser_frame, *riser_columns, *riser_gussets))

    plug_outer_x = outer_x - 2.0 * WALL - 2.0 * LID_CLEARANCE_PER_SIDE
    plug_outer_y = outer_y - 2.0 * WALL - 2.0 * LID_CLEARANCE_PER_SIDE
    plug_inner_x = plug_outer_x - 2.0 * LID_PLUG_WALL
    plug_inner_y = plug_outer_y - 2.0 * LID_PLUG_WALL
    if lid_riser_height > 0.0:
        seat_bridge_outer = _box(
            outer_x - 2.0 * WALL + 0.40,
            outer_y - 2.0 * WALL + 0.40,
            LID_RISER_SEAT_BRIDGE_HEIGHT,
        ).moved(
            Location(
                (
                    0.0,
                    0.0,
                    mating_plane_z - LID_RISER_SEAT_BRIDGE_HEIGHT,
                )
            )
        )
        seat_bridge_inner = _box(
            plug_inner_x,
            plug_inner_y,
            LID_RISER_SEAT_BRIDGE_HEIGHT + 2.0 * BOOLEAN_OVERSHOOT,
        ).moved(
            Location(
                (
                    0.0,
                    0.0,
                    mating_plane_z
                    - LID_RISER_SEAT_BRIDGE_HEIGHT
                    - BOOLEAN_OVERSHOOT,
                )
            )
        )
        seat_bridge = _single_solid(
            seat_bridge_outer.cut(seat_bridge_inner),
            f"{label} raised hood seating ledge",
        )
        lid_parts.append(seat_bridge)
    plug_outer = _box(
        plug_outer_x,
        plug_outer_y,
        LID_PLUG_DEPTH + 0.20,
    ).moved(Location((0.0, 0.0, mating_plane_z - 0.20)))
    plug_inner = _box(
        plug_inner_x,
        plug_inner_y,
        LID_PLUG_DEPTH + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, mating_plane_z - 0.20)))
    plug_frame = _single_solid(plug_outer.cut(plug_inner), f"{label} lid plug")
    lid_parts.append(plug_frame)
    lid = _fuse_all(lid_parts, f"{label} complete lid")

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
            (
                lid,
                *_lid_corner_pins(
                    outer_x,
                    outer_y,
                    mating_plane_z,
                ),
            ),
            f"{label} lid with integral locating pins",
        )
    lid.label = f"{label}_lid_print_exterior_face_down"
    lid.color = LID_COLOR
    return lid


def assembled_lid(
    lid_print,
    base_height: float,
    lid_riser_height: float = 0.0,
):
    """Flip a print-oriented lid into its installed pose above the base."""
    return lid_print.rotate(Axis.X, 180.0).moved(
        Location(
            (
                0.0,
                0.0,
                base_height + LID_TOP + lid_riser_height,
            )
        )
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

    # The former five-window long-wall cable bank is intentionally closed.
    # Cable service now passes vertically through three lid openings directly
    # above the front connector groups; the USB-C side window remains.
    cable_x_positions = ()
    access_cutters = ()

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
    short_end_perforation_specs = _sab_short_end_perforation_specs()
    short_end_perforation_cutters = tuple(
        _circular_prism_x(
            SAB_SHORT_END_PERFORATION_DIAMETER,
            2.0 * WALL + 2.0,
            wall_x,
            center_y,
            center_z,
        )
        for wall_x, center_y, center_z in short_end_perforation_specs
    )

    shell = _cut_all(
        blank,
        (usb_port_cutter, *short_end_perforation_cutters),
        "SAB closed long walls, short-end perforations, and USB-C access",
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
        _sab_retaining_post(
            x,
            y,
            SAB_BOARD_Z,
            SAB_RETAINING_POST_HEIGHT,
        )
        for x, y in standoff_centers
    ]
    floor_ribs = _sab_floor_ribs()
    base = _fuse_all(
        (shell, *floor_ribs, *standoffs, *retaining_posts),
        "SAB ribbed base, standoffs, and integral PCB retaining posts",
    )
    base = _cut_base_pin_receivers(
        base,
        SAB_OUTER_X,
        SAB_OUTER_Y,
        SAB_BASE_HEIGHT,
    )
    base.label = "sab_1060_base"
    base.color = ENCLOSURE_COLOR

    access_probes = ()
    usb_access_probe = _rounded_rect_prism_x(
        SAB_USB_PORT_WIDTH - 1.0,
        SAB_USB_PORT_HEIGHT - 1.0,
        SAB_USB_PORT_CORNER_RADIUS - 0.5,
        10.0,
        -SAB_OUTER_X / 2.0,
        SAB_USB_PORT_CENTER_Y_USER_DIRECTED,
        SAB_USB_PORT_BOTTOM + 0.5,
    )
    short_end_perforation_probes = tuple(
        _circular_prism_x(
            SAB_SHORT_END_PERFORATION_DIAMETER - 0.5,
            2.0 * WALL + 1.0,
            wall_x,
            center_y,
            center_z,
        )
        for wall_x, center_y, center_z in short_end_perforation_specs
    )
    closed_wall_probes = (
        _box(20.0, 4.0, 6.0).moved(
            Location((0.0, -SAB_OUTER_Y / 2.0, SAB_BASE_HEIGHT / 2.0))
        ),
        _box(20.0, 4.0, 6.0).moved(
            Location((0.0, SAB_OUTER_Y / 2.0, SAB_BASE_HEIGHT / 2.0))
        ),
    )
    return {
        "base": base,
        "access_cutters": tuple(access_cutters),
        "access_probes": access_probes,
        "usb_port_cutter": usb_port_cutter,
        "usb_access_probe": usb_access_probe,
        "short_end_perforation_specs": short_end_perforation_specs,
        "short_end_perforation_cutters": short_end_perforation_cutters,
        "short_end_perforation_probes": short_end_perforation_probes,
        "closed_wall_probes": closed_wall_probes,
        "cable_x_positions": cable_x_positions,
        "standoff_centers": standoff_centers,
        "floor_ribs": floor_ribs,
        "retaining_posts": tuple(retaining_posts),
        "pin_receiver_centers": _tower_centers(SAB_OUTER_X, SAB_OUTER_Y),
    }


def build_sab_base():
    return build_sab_base_details()["base"]


def build_sab_retaining_cap_installed():
    """Compliant mushroom cap, authored with its board face at Z=0."""
    body = Cylinder(
        radius=SAB_RETAINING_CAP_BODY_DIAMETER / 2.0,
        height=SAB_RETAINING_CAP_BODY_HEIGHT + 0.20,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    head_bottom = SAB_RETAINING_CAP_BODY_HEIGHT - 0.20
    head_straight_height = (
        SAB_RETAINING_CAP_HEIGHT
        - SAB_RETAINING_CAP_EDGE_CHAMFER
        - head_bottom
    )
    head = Cylinder(
        radius=SAB_RETAINING_CAP_OUTER_DIAMETER / 2.0,
        height=head_straight_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, head_bottom)))
    head_chamfer = Cone(
        bottom_radius=SAB_RETAINING_CAP_OUTER_DIAMETER / 2.0,
        top_radius=(
            SAB_RETAINING_CAP_OUTER_DIAMETER / 2.0
            - SAB_RETAINING_CAP_EDGE_CHAMFER
        ),
        height=SAB_RETAINING_CAP_EDGE_CHAMFER,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(
        Location(
            (
                0.0,
                0.0,
                SAB_RETAINING_CAP_HEIGHT
                - SAB_RETAINING_CAP_EDGE_CHAMFER,
            )
        )
    )
    blank = _fuse_all(
        (body, head, head_chamfer),
        "SAB mushroom PCB retaining cap blank",
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

    # The print-bed opening is flared by 0.4 mm to compensate for first-layer
    # elephant foot and provide a positive lead-in without moving the lock
    # point deeper in the main 3.8-to-3.0 mm taper.
    chamfer_start_z = (
        SAB_RETAINING_CAP_HEIGHT - SAB_RETAINING_CAP_EDGE_CHAMFER
    )
    main_radius_at_chamfer = (
        entry_radius + radius_slope * chamfer_start_z
    )
    chamfer_slope = 1.0
    bore_chamfer = Cone(
        bottom_radius=main_radius_at_chamfer,
        top_radius=(
            main_radius_at_chamfer
            + chamfer_slope
            * (SAB_RETAINING_CAP_EDGE_CHAMFER + BOOLEAN_OVERSHOOT)
        ),
        height=SAB_RETAINING_CAP_EDGE_CHAMFER + BOOLEAN_OVERSHOOT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((0.0, 0.0, chamfer_start_z)))

    # Three narrow radial slots connect to the bore over the upper 6 mm. The
    # uncut 4 mm board-side ring and shorter fingers increase spring force while
    # keeping the cap a single printable collet-like object.
    slot_bottom = SAB_RETAINING_CAP_HEIGHT - SAB_RETAINING_CAP_SLOT_DEPTH
    slot_inner_radius = SAB_RETAINING_CAP_BORE_TOP_DIAMETER / 2.0 - 0.15
    slot_outer_radius = SAB_RETAINING_CAP_OUTER_DIAMETER / 2.0 + 0.50
    slot_length = slot_outer_radius - slot_inner_radius
    slot_center_x = (slot_outer_radius + slot_inner_radius) / 2.0
    slot_blank = _box(
        slot_length,
        SAB_RETAINING_CAP_SLOT_WIDTH,
        SAB_RETAINING_CAP_SLOT_DEPTH + BOOLEAN_OVERSHOOT,
    ).moved(Location((slot_center_x, 0.0, slot_bottom)))
    relief_slots = tuple(
        slot_blank.rotate(
            Axis.Z,
            index * 360.0 / SAB_RETAINING_CAP_SLOT_COUNT,
        )
        for index in range(SAB_RETAINING_CAP_SLOT_COUNT)
    )
    cap = _cut_all(
        blank,
        (bore, bore_chamfer, *relief_slots),
        "SAB compliant tapered-bore PCB retaining cap",
    )
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
    for index, (x, y) in enumerate(
        (
            (-pitch / 2.0, -pitch / 2.0),
            (pitch / 2.0, -pitch / 2.0),
            (-pitch / 2.0, pitch / 2.0),
            (pitch / 2.0, pitch / 2.0),
        )
    ):
        cap = build_sab_retaining_cap_print().moved(Location((x, y, 0.0)))
        cap.label = f"sab_1060_pcb_retaining_cap_{index + 1}_print"
        caps.append(cap)
    return tuple(caps)


def build_sab_fan_guard_installed_local():
    """Build a removable guard with a shallow skirt locating in the lid cutout."""
    outer = _box(
        SAB_FAN_GUARD_OUTER_SIZE,
        SAB_FAN_GUARD_OUTER_SIZE,
        SAB_FAN_GUARD_THICKNESS,
    )
    inner_size = SAB_FAN_GUARD_OUTER_SIZE - 2.0 * SAB_FAN_GUARD_FRAME_WIDTH
    inner = _box(
        inner_size,
        inner_size,
        SAB_FAN_GUARD_THICKNESS + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, -BOOLEAN_OVERSHOOT)))
    frame = _single_solid(outer.cut(inner), "SAB fan guard outer frame")

    spoke_length = SAB_FAN_GUARD_OUTER_SIZE * 1.5
    spoke_blanks = tuple(
        _box(
            spoke_length,
            SAB_FAN_GUARD_SPOKE_WIDTH,
            SAB_FAN_GUARD_THICKNESS,
        ).rotate(Axis.Z, angle)
        for angle in (0.0, 60.0, 120.0)
    )
    hub = Cylinder(
        radius=SAB_FAN_GUARD_HUB_DIAMETER / 2.0,
        height=SAB_FAN_GUARD_THICKNESS,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    spoke_field = _fuse_all(
        (*spoke_blanks, hub),
        "SAB fan guard radial spoke field",
    )
    clipped_spokes = _single_solid(
        spoke_field.intersect(outer),
        "SAB fan guard clipped radial spokes",
    )

    skirt_outer = _box(
        SAB_FAN_GUARD_SKIRT_OUTER_SIZE,
        SAB_FAN_GUARD_SKIRT_OUTER_SIZE,
        SAB_FAN_GUARD_SKIRT_DEPTH + 0.20,
    ).moved(Location((0.0, 0.0, -SAB_FAN_GUARD_SKIRT_DEPTH)))
    skirt_inner = _box(
        SAB_FAN_GUARD_SKIRT_INNER_SIZE,
        SAB_FAN_GUARD_SKIRT_INNER_SIZE,
        SAB_FAN_GUARD_SKIRT_DEPTH + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(
        Location(
            (
                0.0,
                0.0,
                -SAB_FAN_GUARD_SKIRT_DEPTH - BOOLEAN_OVERSHOOT,
            )
        )
    )
    skirt = _single_solid(
        skirt_outer.cut(skirt_inner),
        "SAB fan guard locating skirt",
    )
    guard = _fuse_all(
        (frame, clipped_spokes, skirt),
        "SAB removable fan guard",
    )
    guard.label = "sab_1060_fan_guard_installed"
    guard.color = LID_COLOR
    return guard


def build_sab_fan_guard_print():
    """Orient the guard outer-face-down with the locating skirt upward."""
    guard = build_sab_fan_guard_installed_local().rotate(
        Axis.X,
        180.0,
    ).moved(Location((0.0, 0.0, SAB_FAN_GUARD_THICKNESS)))
    guard.label = "sab_1060_fan_guard_print_outer_face_down"
    guard.color = LID_COLOR
    return guard


def build_sab_fan_guard_installed():
    guard = build_sab_fan_guard_installed_local().moved(
        Location(
            (
                SAB_FAN_CENTER_X_USER_DIRECTED,
                SAB_FAN_CENTER_Y_USER_OBSERVED,
                SAB_LID_EXTERIOR_TOP_Z,
            )
        )
    )
    guard.label = "sab_1060_fan_guard_installed"
    guard.color = LID_COLOR
    return guard


def build_sab_post_fit_coupon():
    """Small bed-side post coupon used with one production retaining cap."""
    coupon_base = _box(
        SAB_FIT_COUPON_X,
        SAB_FIT_COUPON_Y,
        SAB_FIT_COUPON_BASE_HEIGHT,
    )
    test_post = _sab_retaining_post(
        0.0,
        0.0,
        SAB_FIT_COUPON_BASE_HEIGHT,
        SAB_RETAINING_CAP_NOMINAL_ENGAGEMENT,
    )
    coupon = _fuse_all(
        (coupon_base, test_post),
        "SAB post and retaining-cap fit coupon",
    )
    coupon.label = "sab_1060_post_and_cap_fit_coupon"
    coupon.color = ENCLOSURE_COLOR
    return coupon


def build_sab_lid_pin_fit_coupon():
    """Male pin coupon for direct testing in an already-printed base receiver."""
    coupon_base = _box(
        SAB_LID_PIN_FIT_COUPON_X,
        SAB_LID_PIN_FIT_COUPON_Y,
        SAB_LID_PIN_FIT_COUPON_BASE_HEIGHT,
    )
    test_pin = _lid_pin(
        0.0,
        0.0,
        SAB_LID_PIN_FIT_COUPON_BASE_HEIGHT,
    )
    coupon = _fuse_all(
        (coupon_base, test_pin),
        "SAB lid-pin-to-base-receiver fit coupon",
    )
    coupon.label = "sab_1060_lid_pin_fit_coupon"
    coupon.color = LID_COLOR
    return coupon


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
        lid_riser_height=SAB_LID_RISER_HEIGHT,
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
    front_connector_openings = tuple(
        _box(
            width,
            SAB_FRONT_CONNECTOR_OPENING_DEPTH,
            LID_TOP + 2.0 * BOOLEAN_OVERSHOOT,
        ).moved(
            Location(
                (
                    center_x,
                    # The print lid flips about X for installation. Author the
                    # installed front (-Y) openings at positive print Y.
                    -SAB_FRONT_CONNECTOR_OPENING_CENTER_Y,
                    -BOOLEAN_OVERSHOOT,
                )
            )
        )
        for center_x, width in _sab_front_connector_cut_specs()
    )
    lid = _cut_all(
        lid,
        (fan_opening, *front_connector_openings),
        "SAB fan and front connector lid openings",
    )
    lid.label = "sab_1060_lid_print_8mm_raised_hood"
    lid.color = LID_COLOR
    return lid


def build_sab_front_connector_access_probes_installed():
    """Inset probes proving all three installed plug zones are unobstructed."""
    return tuple(
        _box(
            width - 0.5,
            SAB_FRONT_CONNECTOR_OPENING_DEPTH - 0.5,
            LID_TOP + 2.0 * BOOLEAN_OVERSHOOT,
        ).moved(
            Location(
                (
                    center_x,
                    SAB_FRONT_CONNECTOR_OPENING_CENTER_Y,
                    SAB_LID_INTERIOR_ROOF_Z - BOOLEAN_OVERSHOOT,
                )
            )
        )
        for center_x, width in _sab_front_connector_opening_specs()
    )


def build_sab_front_connector_joined_access_probe_installed():
    """Inset probe proving the J012 and DC zones form one continuous opening."""
    return _box(
        SAB_FRONT_CONNECTOR_JOINED_OPENING_WIDTH - 0.5,
        SAB_FRONT_CONNECTOR_OPENING_DEPTH - 0.5,
        LID_TOP + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(
        Location(
            (
                SAB_FRONT_CONNECTOR_JOINED_OPENING_CENTER_X,
                SAB_FRONT_CONNECTOR_OPENING_CENTER_Y,
                SAB_LID_INTERIOR_ROOF_Z - BOOLEAN_OVERSHOOT,
            )
        )
    )


def build_sab_near_wall_component_clearance_probe():
    """Volume at least 5 mm inside every wall, from plug depth to roof."""
    probe_bottom_z = SAB_BASE_HEIGHT - LID_PLUG_DEPTH
    probe = _box(
        SAB_INNER_X - 2.0 * SAB_NEAR_WALL_COMPONENT_OFFSET,
        SAB_INNER_Y - 2.0 * SAB_NEAR_WALL_COMPONENT_OFFSET,
        SAB_LID_INTERIOR_ROOF_Z - probe_bottom_z,
    ).moved(Location((0.0, 0.0, probe_bottom_z)))
    probe.label = "sab_1060_5mm_inset_lid_clearance_probe"
    return probe


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
    # central fan footprint is removed so the explicit fan can occupy it below
    # the replacement lid's raised roof and airflow opening.
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
    fan.label = "user_measured_60_1mm_sab_1060_fan_reference"
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
                SAB_USB_CONNECTOR_BOTTOM_ASSUMED,
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


def build_sab_print_extras():
    """Nest caps/coupons in the lid opening and place the guard beside it."""
    lid_center_y = print_layout_offset_y(
        SAB_OUTER_Y,
        SAB_PRINT_CENTER_GAP,
    )
    print_fan_center_y = lid_center_y - SAB_FAN_CENTER_Y_USER_OBSERVED

    objects = []
    for index, cap in enumerate(build_sab_retaining_caps_print(), start=1):
        placed_cap = cap.moved(
            Location(
                (
                    SAB_FAN_CENTER_X_USER_DIRECTED,
                    print_fan_center_y,
                    0.0,
                )
            )
        )
        objects.append((placed_cap, f"pcb_retaining_cap_{index}"))

    coupon = build_sab_post_fit_coupon().moved(
        Location(
            (
                SAB_FAN_CENTER_X_USER_DIRECTED + SAB_FIT_COUPON_CENTER_X,
                print_fan_center_y,
                0.0,
            )
        )
    )
    objects.append((coupon, "post_and_cap_fit_coupon"))

    pin_coupon = build_sab_lid_pin_fit_coupon().moved(
        Location(
            (
                SAB_FAN_CENTER_X_USER_DIRECTED
                + SAB_LID_PIN_FIT_COUPON_CENTER_X,
                print_fan_center_y,
                0.0,
            )
        )
    )
    objects.append((pin_coupon, "lid_pin_to_base_receiver_fit_coupon"))

    enclosure_footprint_half_x = (
        SAB_OUTER_X / 2.0 + CORNER_TOWER_OUTSET + CORNER_TOWER_RADIUS
    )
    guard_center_x = (
        enclosure_footprint_half_x
        + SAB_PRINT_GUARD_GAP
        + SAB_FAN_GUARD_OUTER_SIZE / 2.0
    )
    guard = build_sab_fan_guard_print().moved(
        Location((guard_center_x, 0.0, 0.0))
    )
    objects.append((guard, "removable_fan_guard"))
    return tuple(objects)
