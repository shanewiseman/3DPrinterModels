"""Parametric geometry for the provisional X2D dual AMS 2 Pro mount.

Coordinate convention
---------------------
Origin: center of the published X2D top envelope.
X: printer left (-) to right (+).
Y: printer front (-) to rear (+).
Z: upward; the provisional X2D top and AMS support faces are Z=0.

Published product envelopes are exact to their cited specifications. The X2D
rim, glass, door, and AMS foot details are documented first-pass assumptions
that must be replaced with physical measurements before production printing.
"""

from __future__ import annotations

from math import cos, hypot, radians, sin, sqrt

from build123d import (
    Align,
    Axis,
    Box,
    BuildSketch,
    Color,
    Compound,
    Cylinder,
    Location,
    Locations,
    Plane,
    Polygon,
    RegularPolygon,
    extrude,
)


# ---------------------------------------------------------------------------
# Published envelopes and provisional mating assumptions
# ---------------------------------------------------------------------------

X2D_WIDTH = 392.0
X2D_DEPTH = 406.0
X2D_HEIGHT = 478.0
X2D_TOP_Z = 0.0

# Provisional top details. These remain labeled reference geometry.
X2D_GLASS_WIDTH = 350.0
X2D_GLASS_DEPTH = 340.0
X2D_GLASS_THICKNESS = 4.0
X2D_DOOR_WIDTH = 360.0
X2D_DOOR_HEIGHT = 400.0
X2D_DOOR_THICKNESS = 5.0
X2D_DOOR_TOP_Z = -25.0
X2D_DOOR_CLOSED_Y = -X2D_DEPTH / 2.0 - X2D_DOOR_THICKNESS / 2.0
X2D_DOOR_HINGE_X = -X2D_DOOR_WIDTH / 2.0
X2D_DOOR_OPEN_ANGLE_DEGREES = -105.0

AMS_WIDTH = 372.0
AMS_DEPTH = 280.0
AMS_HEIGHT = 226.0
AMS_EMPTY_MASS_KG = 2.5

# Provisional foot pattern; intentionally conspicuous in source and labels.
AMS_FOOT_SPACING_X = 320.0
AMS_FOOT_SPACING_Y = 220.0
AMS_FOOT_SIZE_X = 24.0
AMS_FOOT_SIZE_Y = 20.0
AMS_FOOT_HEIGHT = 4.0

SHELF_DEPTH = 252.0
SHELF_THICKNESS = 6.0
SHELF_RIB_DEPTH = 6.0
SHELF_TO_PRINTER_GAP = 3.0
AMS_PAIR_GAP = 25.4
SHELF_OUTBOARD_MARGIN = 25.4

PRINTER_SIDE_X = X2D_WIDTH / 2.0
SHELF_ROOT_X = PRINTER_SIDE_X + SHELF_TO_PRINTER_GAP
AMS_CENTER_X = (AMS_WIDTH + AMS_PAIR_GAP) / 2.0
AMS_PAIR_OUTER_X = AMS_CENTER_X + AMS_WIDTH / 2.0
SHELF_OUTER_X = AMS_PAIR_OUTER_X + SHELF_OUTBOARD_MARGIN
SHELF_SPAN = SHELF_OUTER_X - SHELF_ROOT_X

# A 50 mm bridge receiver at +/-101 ends exactly at the 252 mm shelf edges.
BRACKET_Y_CENTERS = (-101.0, 101.0)
BRACKET_THICKNESS = 12.0
BRACKET_CHORD = 25.4
BRACKET_WEB = 10.0
BRACKET_WEB_CELLS = ((0.18, 0.43), (0.43, 0.68), (0.68, 0.88))
BRACKET_TOP_Z = -SHELF_THICKNESS
BRACKET_DROP = 246.0
BRACKET_BOTTOM_Z = BRACKET_TOP_Z - BRACKET_DROP

M4_CLEARANCE_DIAMETER = 4.5
M4_BUTTON_HEAD_DIAMETER = 8.2
M4_BUTTON_HEAD_HEIGHT = 2.4
M4_NUT_AF = 7.4
M4_NUT_THICKNESS = 3.8
BRACKET_SCREW_OFFSETS = (30.0, 80.0, 130.0, 180.0)

# The centered AMS pair leaves no room for a tall beam under either body. Two
# 3 mm planar truss ties therefore run between the provisional foot rows. Their
# narrow center bosses rise only within the 25.4 mm inter-AMS gap.
BRIDGE_Y_CENTERS = (-70.0, 70.0)
BRIDGE_DEPTH = 50.0
BRIDGE_HEIGHT = 3.0
BRIDGE_BOTTOM_Z = 0.0
BRIDGE_TOP_Z = BRIDGE_BOTTOM_Z + BRIDGE_HEIGHT
BRIDGE_FRAME_WIDTH = 8.0
BRIDGE_WEB = 8.0
BRIDGE_END_OVERLAP = 50.0
BRIDGE_HALF_OUTER_X = SHELF_ROOT_X + BRIDGE_END_OVERLAP
BRIDGE_CENTER_BOSS_HALF_WIDTH = 9.0
BRIDGE_CENTER_BOSS_HEIGHT = 25.4
BRIDGE_CENTER_BOLT_Y_OFFSETS = (-14.0, 0.0, 14.0)
BRIDGE_END_BOLT_LOCAL_XY = ((15.0, -12.0), (30.0, 12.0), (45.0, -12.0))

SIDE_PAD_THICKNESS = SHELF_TO_PRINTER_GAP
SIDE_PAD_DEPTH = 30.0
SIDE_PAD_HEIGHT = 120.0
SIDE_PAD_CENTER_Z = -130.0

PRINT_PART_LIMIT = 252.0
BOOLEAN_OVERSHOOT = 1.0


# Colors are intentionally distinct for assembly review.
SHELF_COLOR = Color(0.12, 0.28, 0.52)
BRACKET_COLOR = Color(0.90, 0.34, 0.07)
BRIDGE_COLOR = Color(0.10, 0.50, 0.30)
PAD_COLOR = Color(0.38, 0.20, 0.52)
HARDWARE_COLOR = Color(0.55, 0.58, 0.62)
PRINTER_COLOR = Color(0.22, 0.24, 0.27, 0.22)
GLASS_COLOR = Color(0.24, 0.50, 0.72, 0.28)
DOOR_COLOR = Color(0.78, 0.12, 0.10, 0.20)
AMS_COLOR = Color(0.64, 0.67, 0.72, 0.55)
AMS_LID_COLOR = Color(0.78, 0.81, 0.86, 0.48)


def _box_at(x_min, x_max, y_min, y_max, z_min, z_max):
    """Axis-aligned box from explicit extrema."""
    return Box(
        x_max - x_min,
        y_max - y_min,
        z_max - z_min,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).moved(Location((x_min, y_min, z_min)))


def _cylinder_z(radius, z_min, z_max, x=0.0, y=0.0):
    return Cylinder(
        radius=radius,
        height=z_max - z_min,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((x, y, z_min)))


def _cylinder_x(radius, x_min, x_max, y=0.0, z=0.0):
    return (
        Cylinder(radius=radius, height=x_max - x_min)
        .rotate(Axis.Y, 90.0)
        .moved(Location(((x_min + x_max) / 2.0, y, z)))
    )


def _hex_prism_z(across_flats, height, x, y, bottom_z):
    circumradius = across_flats / sqrt(3.0)
    points = tuple(
        (
            x + circumradius * cos(radians(30.0 + 60.0 * index)),
            y + circumradius * sin(radians(30.0 + 60.0 * index)),
        )
        for index in range(6)
    )
    with BuildSketch(Plane.XY) as profile:
        Polygon(*points)
    return extrude(profile.sketch, amount=height).moved(
        Location((0.0, 0.0, bottom_z))
    )


def _hex_prism_x(across_flats, depth, x_min, y, z):
    with BuildSketch(Plane.YZ) as profile:
        with Locations((y, z)):
            RegularPolygon(
                radius=across_flats / sqrt(3.0),
                side_count=6,
                rotation=30.0,
            )
    return extrude(profile.sketch, amount=depth).moved(Location((x_min, 0.0, 0.0)))


def _member_xz(x1, z1, x2, z2, width, y_center, thickness):
    """Rectangular structural member in the XZ plane, extruded along Y."""
    dx = x2 - x1
    dz = z2 - z1
    length = hypot(dx, dz)
    if length <= 0.0:
        raise ValueError("Member endpoints must differ")
    px = -dz / length * width / 2.0
    pz = dx / length * width / 2.0
    points = (
        (x1 + px, z1 + pz),
        (x2 + px, z2 + pz),
        (x2 - px, z2 - pz),
        (x1 - px, z1 - pz),
    )
    with BuildSketch(Plane.XZ) as profile:
        Polygon(*points)
    # Plane.XZ raw extrusion occupies Y=-thickness..0.
    return extrude(profile.sketch, amount=thickness).moved(
        Location((0.0, y_center + thickness / 2.0, 0.0))
    )


def _member_xy(x1, y1, x2, y2, width, z_min, z_max):
    """Rectangular structural member in XY, extruded upward from z_min."""
    dx = x2 - x1
    dy = y2 - y1
    length = hypot(dx, dy)
    if length <= 0.0:
        raise ValueError("Member endpoints must differ")
    px = -dy / length * width / 2.0
    py = dx / length * width / 2.0
    points = (
        (x1 + px, y1 + py),
        (x2 + px, y2 + py),
        (x2 - px, y2 - py),
        (x1 - px, y1 - py),
    )
    with BuildSketch(Plane.XY) as profile:
        Polygon(*points)
    return extrude(profile.sketch, amount=z_max - z_min).moved(
        Location((0.0, 0.0, z_min))
    )


def _fuse_all(shapes):
    items = list(shapes)
    if not items:
        raise ValueError("At least one shape is required")
    result = items[0]
    for shape in items[1:]:
        result = result.fuse(shape)
    solids = list(result.solids())
    if len(solids) != 1:
        raise RuntimeError(f"Expected one fused solid, found {len(solids)}")
    return solids[0]


def _cut_all(shape, tools):
    result = shape
    for tool in tools:
        result = result.cut(tool)
    solids = list(result.solids())
    if len(solids) != 1:
        raise RuntimeError(f"Expected one cut solid, found {len(solids)}")
    return solids[0]


def side_name(side):
    return "right" if side > 0 else "left"


def shelf_root_x(side):
    return side * SHELF_ROOT_X


def shelf_outer_x(side):
    return side * SHELF_OUTER_X


def shelf_x_bounds(side):
    return tuple(sorted((shelf_root_x(side), shelf_outer_x(side))))


def ams_center_x(side):
    return side * AMS_CENTER_X


def bracket_screw_xs(side):
    return tuple(shelf_root_x(side) + side * offset for offset in BRACKET_SCREW_OFFSETS)


def bridge_end_bolt_positions(side, beam_y):
    """Three vertical M4 positions in each 50 mm shelf-overlap land."""
    root = shelf_root_x(side)
    return tuple(
        (root + side * dx, beam_y + dy)
        for dx, dy in BRIDGE_END_BOLT_LOCAL_XY
    )


def make_shelf(side):
    """Create one 211.1 x 252 mm shelf with ribs and low tie-bolt lands."""
    x_min, x_max = shelf_x_bounds(side)
    y_min = -SHELF_DEPTH / 2.0
    y_max = SHELF_DEPTH / 2.0
    parts = [
        _box_at(x_min, x_max, y_min, y_max, -SHELF_THICKNESS, 0.0),
        _box_at(x_min, x_max, y_min, y_min + 12.0, -12.0, -SHELF_THICKNESS),
        _box_at(x_min, x_max, y_max - 12.0, y_max, -12.0, -SHELF_THICKNESS),
    ]
    inner = shelf_root_x(side)
    outer = shelf_outer_x(side)
    for fraction in (0.24, 0.50, 0.76):
        x = inner + side * SHELF_SPAN * fraction
        parts.append(_box_at(x - 5.0, x + 5.0, y_min, y_max, -12.0, -6.0))
    for y in (-62.0, 0.0, 62.0):
        parts.append(_box_at(x_min, x_max, y - 5.0, y + 5.0, -12.0, -6.0))

    shelf = _fuse_all(parts)
    cuts = []
    for y in BRACKET_Y_CENTERS:
        for x in bracket_screw_xs(side):
            cuts.append(_cylinder_z(M4_CLEARANCE_DIAMETER / 2.0, -32.5, 1.0, x, y))
    # Keep the bracket fastener paths as plain M4 clearance holes. The
    # button-head screws intentionally remain proud of the shelf top so this
    # face has no large, shallow counterbores to bridge during printing.
    # Three vertical M4 tie bolts per end land. Nuts load from the shelf
    # underside; the tie itself contains the flush button-head recesses.
    for beam_y in BRIDGE_Y_CENTERS:
        for x, y in bridge_end_bolt_positions(side, beam_y):
            cuts.append(_cylinder_z(M4_CLEARANCE_DIAMETER / 2.0, -13.0, 4.0, x, y))
            cuts.append(_hex_prism_z(M4_NUT_AF, 4.0, x, y, -6.1))
    shelf = _cut_all(shelf, cuts)
    shelf.label = f"{side_name(side)}_211p1x252mm_shelf_plain_m4_bracket_holes"
    shelf.color = SHELF_COLOR
    return shelf


def make_bracket_frame_members(side, y_center):
    """Return the top, printer-side, and diagonal perimeter members."""
    root = shelf_root_x(side)
    outer = shelf_outer_x(side)
    x_min, x_max = sorted((root, outer))
    top = BRACKET_TOP_Z
    bottom = BRACKET_BOTTOM_Z

    top_chord = _box_at(
        x_min,
        x_max,
        y_center - BRACKET_THICKNESS / 2.0,
        y_center + BRACKET_THICKNESS / 2.0,
        top - BRACKET_CHORD,
        top,
    )
    printer_chord = _box_at(
        min(root, root + side * BRACKET_CHORD),
        max(root, root + side * BRACKET_CHORD),
        y_center - BRACKET_THICKNESS / 2.0,
        y_center + BRACKET_THICKNESS / 2.0,
        bottom,
        top,
    )
    diagonal_start = (
        root + side * BRACKET_CHORD / 2.0,
        bottom + BRACKET_CHORD / 2.0,
    )
    diagonal_end = (
        outer - side * BRACKET_CHORD / 2.0,
        top - BRACKET_CHORD / 2.0,
    )
    diagonal_chord = _member_xz(
        *diagonal_start,
        *diagonal_end,
        BRACKET_CHORD,
        y_center,
        BRACKET_THICKNESS,
    )
    return top_chord, printer_chord, diagonal_chord


def bracket_web_point(side, fraction, on_top):
    """Locate a web endpoint on the centerline of its perimeter chord."""
    root = shelf_root_x(side)
    outer = shelf_outer_x(side)
    x = root + side * SHELF_SPAN * fraction
    if on_top:
        return x, BRACKET_TOP_Z - BRACKET_CHORD / 2.0

    diagonal_start = (
        root + side * BRACKET_CHORD / 2.0,
        BRACKET_BOTTOM_Z + BRACKET_CHORD / 2.0,
    )
    diagonal_end = (
        outer - side * BRACKET_CHORD / 2.0,
        BRACKET_TOP_Z - BRACKET_CHORD / 2.0,
    )
    diagonal_fraction = (x - diagonal_start[0]) / (
        diagonal_end[0] - diagonal_start[0]
    )
    z = diagonal_start[1] + diagonal_fraction * (
        diagonal_end[1] - diagonal_start[1]
    )
    return x, z


def make_bracket_web_members(side, y_center):
    """Return six truss webs with deliberate centerline frame engagement."""
    parts = []
    for a, b in BRACKET_WEB_CELLS:
        parts.append(
            _member_xz(
                *bracket_web_point(side, a, True),
                *bracket_web_point(side, b, False),
                BRACKET_WEB,
                y_center,
                BRACKET_THICKNESS,
            )
        )
        parts.append(
            _member_xz(
                *bracket_web_point(side, a, False),
                *bracket_web_point(side, b, True),
                BRACKET_WEB,
                y_center,
                BRACKET_THICKNESS,
            )
        )
    return tuple(parts)


def make_bracket(side, y_center):
    """One right-triangle bracket with 25.4 mm outer chords and truss webs."""
    root = shelf_root_x(side)
    top = BRACKET_TOP_Z
    parts = [
        *make_bracket_frame_members(side, y_center),
        *make_bracket_web_members(side, y_center),
    ]

    bracket = _fuse_all(parts)
    cuts = []
    nut_bottom = top - BRACKET_CHORD + 2.4
    for x in bracket_screw_xs(side):
        cuts.append(_cylinder_z(M4_CLEARANCE_DIAMETER / 2.0, top - BRACKET_CHORD - 1.0, 1.0, x, y_center))
        cuts.append(_hex_prism_z(M4_NUT_AF, M4_NUT_THICKNESS, x, y_center, nut_bottom))
        if y_center < 0.0:
            entry_y_min = y_center - BRACKET_THICKNESS / 2.0 - 1.0
            entry_y_max = y_center
        else:
            entry_y_min = y_center
            entry_y_max = y_center + BRACKET_THICKNESS / 2.0 + 1.0
        cuts.append(
            _box_at(
                x - M4_NUT_AF / 2.0,
                x + M4_NUT_AF / 2.0,
                entry_y_min,
                entry_y_max,
                nut_bottom,
                nut_bottom + M4_NUT_THICKNESS,
            )
        )
    bracket = _cut_all(bracket, cuts)
    position = "front" if y_center < 0.0 else "rear"
    bracket.label = f"{side_name(side)}_{position}_trussed_triangle_bracket"
    bracket.color = BRACKET_COLOR
    return bracket


def _planar_bridge_truss(x_min, x_max, beam_y):
    """Low-profile XY truss that stays below the provisional AMS underside."""
    y_min = beam_y - BRIDGE_DEPTH / 2.0
    y_max = beam_y + BRIDGE_DEPTH / 2.0
    z_min = BRIDGE_BOTTOM_Z
    z_max = BRIDGE_TOP_Z
    parts = [
        _box_at(x_min, x_max, y_min, y_min + BRIDGE_FRAME_WIDTH, z_min, z_max),
        _box_at(x_min, x_max, y_max - BRIDGE_FRAME_WIDTH, y_max, z_min, z_max),
        _box_at(x_min, x_min + BRIDGE_FRAME_WIDTH, y_min, y_max, z_min, z_max),
        _box_at(x_max - BRIDGE_FRAME_WIDTH, x_max, y_min, y_max, z_min, z_max),
    ]
    length = x_max - x_min
    cell_count = max(3, int(length // 42.0))
    step = length / cell_count
    rail_low = y_min + BRIDGE_FRAME_WIDTH / 2.0
    rail_high = y_max - BRIDGE_FRAME_WIDTH / 2.0
    for index in range(cell_count):
        xa = x_min + index * step
        xb = xa + step
        ya, yb = (rail_low, rail_high) if index % 2 == 0 else (rail_high, rail_low)
        parts.append(_member_xy(xa, ya, xb, yb, BRIDGE_WEB, z_min, z_max))
    envelope = _box_at(x_min, x_max, y_min, y_max, z_min, z_max)
    truss = _fuse_all(parts) & envelope
    solids = list(truss.solids())
    if len(solids) != 1:
        raise RuntimeError(f"Expected one planar truss solid, found {len(solids)}")
    return solids[0]


def make_bridge_segment(beam_name, side):
    """One printable low-profile half-tie with a center M4 joining boss."""
    beam_y = BRIDGE_Y_CENTERS[0] if beam_name == "front" else BRIDGE_Y_CENTERS[1]
    boss_outer_x = side * BRIDGE_CENTER_BOSS_HALF_WIDTH
    root_x = shelf_root_x(side)
    overlap_outer_x = side * BRIDGE_HALF_OUTER_X
    if side < 0:
        main_x_min, main_x_max = root_x, boss_outer_x
        land_x_min, land_x_max = overlap_outer_x, root_x
        boss_x_min, boss_x_max = boss_outer_x, 0.0
    else:
        main_x_min, main_x_max = boss_outer_x, root_x
        land_x_min, land_x_max = root_x, overlap_outer_x
        boss_x_min, boss_x_max = 0.0, boss_outer_x

    truss = _planar_bridge_truss(main_x_min, main_x_max, beam_y)
    land = _box_at(
        min(land_x_min, land_x_max),
        max(land_x_min, land_x_max),
        beam_y - BRIDGE_DEPTH / 2.0,
        beam_y + BRIDGE_DEPTH / 2.0,
        BRIDGE_BOTTOM_Z,
        BRIDGE_TOP_Z,
    )
    boss = _box_at(
        min(boss_x_min, boss_x_max),
        max(boss_x_min, boss_x_max),
        beam_y - BRIDGE_DEPTH / 2.0,
        beam_y + BRIDGE_DEPTH / 2.0,
        BRIDGE_BOTTOM_Z,
        BRIDGE_CENTER_BOSS_HEIGHT,
    )
    segment = _fuse_all((truss, land, boss))
    cuts = []

    # Three flush vertical M4 heads secure the 50 mm shelf overlap.
    for x, y in bridge_end_bolt_positions(side, beam_y):
        cuts.append(_cylinder_z(M4_CLEARANCE_DIAMETER / 2.0, -1.0, 4.0, x, y))
        cuts.append(
            _cylinder_z(
                M4_BUTTON_HEAD_DIAMETER / 2.0,
                BRIDGE_TOP_Z - M4_BUTTON_HEAD_HEIGHT,
                BRIDGE_TOP_Z + 1.0,
                x,
                y,
            )
        )

    # Three transverse M4 screws occupy the narrow gap between AMS bodies.
    center_hole_z = BRIDGE_CENTER_BOSS_HEIGHT / 2.0
    for y_offset in BRIDGE_CENTER_BOLT_Y_OFFSETS:
        y = beam_y + y_offset
        cuts.append(
            _cylinder_x(
                M4_CLEARANCE_DIAMETER / 2.0,
                -BRIDGE_CENTER_BOSS_HALF_WIDTH - 1.0,
                BRIDGE_CENTER_BOSS_HALF_WIDTH + 1.0,
                y,
                center_hole_z,
            )
        )
        if side < 0:
            cuts.append(
                _cylinder_x(
                    M4_BUTTON_HEAD_DIAMETER / 2.0,
                    -BRIDGE_CENTER_BOSS_HALF_WIDTH - 1.0,
                    -BRIDGE_CENTER_BOSS_HALF_WIDTH + M4_BUTTON_HEAD_HEIGHT,
                    y,
                    center_hole_z,
                )
            )
        else:
            cuts.append(
                _hex_prism_x(
                    M4_NUT_AF,
                    4.2,
                    BRIDGE_CENTER_BOSS_HALF_WIDTH - 4.2,
                    y,
                    center_hole_z,
                )
            )

    segment = _cut_all(segment, cuts)
    segment.label = f"{beam_name}_low_profile_tie_{side_name(side)}_half"
    segment.color = BRIDGE_COLOR
    return segment


def make_side_pad(side, y_center):
    """Provisional replaceable ASA pressure-spreading side pad."""
    if side > 0:
        x_min, x_max = PRINTER_SIDE_X, SHELF_ROOT_X
    else:
        x_min, x_max = -SHELF_ROOT_X, -PRINTER_SIDE_X
    pad = _box_at(
        x_min,
        x_max,
        y_center - SIDE_PAD_DEPTH / 2.0,
        y_center + SIDE_PAD_DEPTH / 2.0,
        SIDE_PAD_CENTER_Z - SIDE_PAD_HEIGHT / 2.0,
        SIDE_PAD_CENTER_Z + SIDE_PAD_HEIGHT / 2.0,
    )
    position = "front" if y_center < 0.0 else "rear"
    pad.label = f"{side_name(side)}_{position}_provisional_side_contact_pad"
    pad.color = PAD_COLOR
    return pad


def make_x2d_reference():
    body = _box_at(
        -X2D_WIDTH / 2.0,
        X2D_WIDTH / 2.0,
        -X2D_DEPTH / 2.0,
        X2D_DEPTH / 2.0,
        -X2D_HEIGHT,
        0.0,
    )
    body.label = "bambu_x2d_published_392x406x478_envelope"
    body.color = PRINTER_COLOR
    glass = _box_at(
        -X2D_GLASS_WIDTH / 2.0,
        X2D_GLASS_WIDTH / 2.0,
        -X2D_GLASS_DEPTH / 2.0,
        X2D_GLASS_DEPTH / 2.0,
        -X2D_GLASS_THICKNESS,
        0.0,
    )
    glass.label = "provisional_x2d_top_glass_350x340x4"
    glass.color = GLASS_COLOR

    door_bottom = X2D_DOOR_TOP_Z - X2D_DOOR_HEIGHT
    closed = Box(
        X2D_DOOR_WIDTH,
        X2D_DOOR_THICKNESS,
        X2D_DOOR_HEIGHT,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(Location((X2D_DOOR_HINGE_X, X2D_DOOR_CLOSED_Y, door_bottom)))
    closed.label = "provisional_x2d_front_door_closed"
    closed.color = DOOR_COLOR

    open_door = Box(
        X2D_DOOR_WIDTH,
        X2D_DOOR_THICKNESS,
        X2D_DOOR_HEIGHT,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(
        Location(
            (X2D_DOOR_HINGE_X, X2D_DOOR_CLOSED_Y, door_bottom),
            (0.0, 0.0, X2D_DOOR_OPEN_ANGLE_DEGREES),
        )
    )
    open_door.label = "provisional_x2d_front_door_open_keepout"
    open_door.color = DOOR_COLOR
    return {
        "body": body,
        "glass": glass,
        "door_closed": closed,
        "door_open": open_door,
    }


def make_ams_reference(side):
    """Simplified AMS envelope with visible provisional foot positions."""
    center_x = ams_center_x(side)
    lower = _box_at(
        center_x - AMS_WIDTH / 2.0,
        center_x + AMS_WIDTH / 2.0,
        -AMS_DEPTH / 2.0,
        AMS_DEPTH / 2.0,
        AMS_FOOT_HEIGHT,
        80.0,
    )
    lower.label = f"{side_name(side)}_ams2pro_published_footprint_body"
    lower.color = AMS_COLOR
    lid = _box_at(
        center_x - AMS_WIDTH / 2.0 + 6.0,
        center_x + AMS_WIDTH / 2.0 - 6.0,
        -AMS_DEPTH / 2.0 + 6.0,
        AMS_DEPTH / 2.0 - 6.0,
        80.0,
        AMS_HEIGHT,
    )
    lid.label = f"{side_name(side)}_ams2pro_lid_envelope"
    lid.color = AMS_LID_COLOR
    feet = []
    for dx in (-AMS_FOOT_SPACING_X / 2.0, AMS_FOOT_SPACING_X / 2.0):
        for dy in (-AMS_FOOT_SPACING_Y / 2.0, AMS_FOOT_SPACING_Y / 2.0):
            foot = _box_at(
                center_x + dx - AMS_FOOT_SIZE_X / 2.0,
                center_x + dx + AMS_FOOT_SIZE_X / 2.0,
                dy - AMS_FOOT_SIZE_Y / 2.0,
                dy + AMS_FOOT_SIZE_Y / 2.0,
                0.0,
                AMS_FOOT_HEIGHT,
            )
            foot.label = f"{side_name(side)}_ams2pro_provisional_foot_{len(feet)+1}"
            foot.color = Color(0.12, 0.13, 0.14)
            feet.append(foot)
    compound = Compound(
        children=[lower, lid, *feet],
        label=f"{side_name(side)}_ams2pro_simplified_reference",
        color=AMS_COLOR,
    )
    return {"compound": compound, "lower": lower, "lid": lid, "feet": tuple(feet)}


def make_bracket_hardware(side, y_center):
    """Simplified M4 button-head screws and captive nuts for one bracket."""
    children = []
    nut_bottom = BRACKET_TOP_Z - BRACKET_CHORD + 2.4
    for index, x in enumerate(bracket_screw_xs(side), start=1):
        shaft = _cylinder_z(2.0, nut_bottom, 0.5, x, y_center)
        head = _cylinder_z(
            M4_BUTTON_HEAD_DIAMETER / 2.0 - 0.15,
            0.0,
            M4_BUTTON_HEAD_HEIGHT,
            x,
            y_center,
        )
        bolt = _fuse_all((shaft, head))
        bolt.label = f"m4_button_head_bracket_bolt_{index}"
        bolt.color = HARDWARE_COLOR
        nut = _hex_prism_z(7.0, 3.2, x, y_center, nut_bottom + 0.3)
        nut.label = f"m4_bracket_nut_{index}"
        nut.color = HARDWARE_COLOR
        children.extend((bolt, nut))
    position = "front" if y_center < 0.0 else "rear"
    return Compound(
        children=children,
        label=f"{side_name(side)}_{position}_bracket_m4_hardware",
        color=HARDWARE_COLOR,
    )


def make_bridge_center_hardware(beam_name):
    """Three transverse M4 screws joining one pair of center bosses."""
    beam_y = BRIDGE_Y_CENTERS[0] if beam_name == "front" else BRIDGE_Y_CENTERS[1]
    hole_z = BRIDGE_CENTER_BOSS_HEIGHT / 2.0
    children = []
    for index, y_offset in enumerate(BRIDGE_CENTER_BOLT_Y_OFFSETS, start=1):
        y = beam_y + y_offset
        shaft = _cylinder_x(2.0, -BRIDGE_CENTER_BOSS_HALF_WIDTH, BRIDGE_CENTER_BOSS_HALF_WIDTH - 1.0, y, hole_z)
        head = _cylinder_x(
            M4_BUTTON_HEAD_DIAMETER / 2.0 - 0.15,
            -BRIDGE_CENTER_BOSS_HALF_WIDTH,
            -BRIDGE_CENTER_BOSS_HALF_WIDTH + M4_BUTTON_HEAD_HEIGHT,
            y,
            hole_z,
        )
        bolt = _fuse_all((shaft, head))
        bolt.label = f"m4_button_head_center_tie_bolt_{index}"
        bolt.color = HARDWARE_COLOR
        nut = _hex_prism_x(7.0, 3.2, BRIDGE_CENTER_BOSS_HALF_WIDTH - 3.5, y, hole_z)
        nut.label = f"m4_center_tie_nut_{index}"
        nut.color = HARDWARE_COLOR
        children.extend((bolt, nut))
    return Compound(
        children=children,
        label=f"{beam_name}_center_tie_m4_hardware",
        color=HARDWARE_COLOR,
    )


def make_bridge_end_hardware(beam_name, side):
    """Three vertical M4 screws joining one tie land to its shelf."""
    beam_y = BRIDGE_Y_CENTERS[0] if beam_name == "front" else BRIDGE_Y_CENTERS[1]
    children = []
    nut_bottom = -5.7
    head_bottom = BRIDGE_TOP_Z - M4_BUTTON_HEAD_HEIGHT
    for index, (x, y) in enumerate(bridge_end_bolt_positions(side, beam_y), start=1):
        shaft = _cylinder_z(2.0, nut_bottom, head_bottom + 0.5, x, y)
        head = _cylinder_z(
            M4_BUTTON_HEAD_DIAMETER / 2.0 - 0.15,
            head_bottom,
            BRIDGE_TOP_Z,
            x,
            y,
        )
        bolt = _fuse_all((shaft, head))
        bolt.label = f"m4_button_head_tie_end_bolt_{index}"
        bolt.color = HARDWARE_COLOR
        nut = _hex_prism_z(7.0, 3.2, x, y, nut_bottom + 0.2)
        nut.label = f"m4_tie_end_nut_{index}"
        nut.color = HARDWARE_COLOR
        children.extend((bolt, nut))
    position = "front" if beam_y < 0.0 else "rear"
    return Compound(
        children=children,
        label=f"{side_name(side)}_{position}_tie_end_m4_hardware",
        color=HARDWARE_COLOR,
    )


def make_geometry_details():
    shelves = {side: make_shelf(side) for side in (-1, 1)}
    brackets = {
        (side, y): make_bracket(side, y)
        for side in (-1, 1)
        for y in BRACKET_Y_CENTERS
    }
    bridge_segments = {
        (beam, side): make_bridge_segment(beam, side)
        for beam in ("front", "rear")
        for side in (-1, 1)
    }
    side_pads = {
        (side, y): make_side_pad(side, y)
        for side in (-1, 1)
        for y in BRACKET_Y_CENTERS
    }
    ams_references = {side: make_ams_reference(side) for side in (-1, 1)}
    x2d_reference = make_x2d_reference()
    bracket_hardware = {
        (side, y): make_bracket_hardware(side, y)
        for side in (-1, 1)
        for y in BRACKET_Y_CENTERS
    }
    bridge_center_hardware = {
        beam: make_bridge_center_hardware(beam)
        for beam in ("front", "rear")
    }
    bridge_end_hardware = {
        (beam, side): make_bridge_end_hardware(beam, side)
        for beam in ("front", "rear")
        for side in (-1, 1)
    }

    print_parts = {
        shelves[-1].label: shelves[-1],
        shelves[1].label: shelves[1],
        **{shape.label: shape for shape in brackets.values()},
        **{shape.label: shape for shape in bridge_segments.values()},
        **{shape.label: shape for shape in side_pads.values()},
    }
    return {
        "shelves": shelves,
        "brackets": brackets,
        "bridge_segments": bridge_segments,
        "side_pads": side_pads,
        "ams_references": ams_references,
        "x2d_reference": x2d_reference,
        "bracket_hardware": bracket_hardware,
        "bridge_center_hardware": bridge_center_hardware,
        "bridge_end_hardware": bridge_end_hardware,
        "print_parts": print_parts,
    }


__all__ = [name for name in globals() if name.isupper()] + [
    "make_geometry_details",
    "side_name",
    "shelf_x_bounds",
    "shelf_root_x",
    "shelf_outer_x",
    "ams_center_x",
]
