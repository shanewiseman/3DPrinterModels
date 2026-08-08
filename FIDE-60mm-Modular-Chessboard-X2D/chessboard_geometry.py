"""Parametric geometry for the 60 mm modular X2D chessboard.

Origin and orientation for the assembled model:

* the board center is (0, 0, 0)
* XY is the playing plane and +Z is up
* White sits at negative Y
* file ``a`` is at negative X and rank ``1`` is at negative Y

Printable quarter and rail helpers retain this geometry but recenter individual
parts for convenient slicer import.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from build123d import (
    Align,
    Axis,
    Box,
    Color,
    Compound,
    Cylinder,
    FontStyle,
    Location,
    RegularPolygon,
    Text,
    chamfer,
    extrude,
    fillet,
)
from cadpy.assembly import AssemblyHelper, label_shape


# FIDE-guideline and board envelope parameters.
SQUARE_SIZE = 60.0
SQUARE_COUNT = 8
PLAYING_SIZE = SQUARE_SIZE * SQUARE_COUNT
QUARTER_SIZE = PLAYING_SIZE / 2.0
PERIMETER_WIDTH = 20.0
OUTER_SIZE = PLAYING_SIZE + 2.0 * PERIMETER_WIDTH

# Structural and color-layer dimensions.
PANEL_BASE_THICKNESS = 8.0
FACE_INLAY_THICKNESS = 1.6
PLAYING_SURFACE_Z = PANEL_BASE_THICKNESS + FACE_INLAY_THICKNESS
PERIMETER_RISE = 10.0
PERIMETER_TOP_Z = PLAYING_SURFACE_Z + PERIMETER_RISE
UNDERSIDE_DEPTH = 8.0

# Printed alignment geometry.
TONGUE_PROJECTION = 4.0
TONGUE_HEIGHT = 2.5
TONGUE_Z = 0.0
TONGUE_END_MARGIN = 4.0
GROOVE_DEPTH = 4.25
GROOVE_HEIGHT = 2.9
GROOVE_Z = -0.1
JOIN_CLEARANCE = GROOVE_DEPTH - TONGUE_PROJECTION
FIT_LEAD_CHAMFER = 0.5
ELEPHANT_FOOT_RELIEF = 0.4

# Concealed upper registration keys prevent a lip at the playing-surface
# seams. Their positions avoid the M3 nut traps at +/-60 mm.
ANTI_LIP_KEY_LENGTH = 20.0
ANTI_LIP_KEY_PROJECTION = 3.0
ANTI_LIP_KEY_HEIGHT = 2.0
ANTI_LIP_KEY_Z = 5.0
ANTI_LIP_KEY_POSITIONS = (-90.0, 90.0)
ANTI_LIP_GROOVE_LENGTH = 20.4
ANTI_LIP_GROOVE_DEPTH = 3.25
ANTI_LIP_GROOVE_HEIGHT = 2.4
ANTI_LIP_GROOVE_Z = 4.8
ANTI_LIP_DEPTH_CLEARANCE = ANTI_LIP_GROOVE_DEPTH - ANTI_LIP_KEY_PROJECTION

# User-provided M3 hardware. Dimensions target a common DIN 934-style nut and
# socket/pan screw head; the README asks the user to test one nut trap first.
M3_CLEARANCE_DIAMETER = 3.4
M3_HEAD_CLEARANCE_DIAMETER = 6.8
M3_HEAD_RECESS_DEPTH = 3.2
M3_SCREW_LENGTH = 12.0
M3_NUT_ACROSS_FLATS = 5.5
M3_NUT_THICKNESS = 2.4
NUT_POCKET_ACROSS_FLATS = 5.72
NUT_POCKET_MAJOR_RADIUS = NUT_POCKET_ACROSS_FLATS / sqrt(3.0)
NUT_POCKET_HEIGHT = 2.8
NUT_POCKET_Z = 4.3
NUT_ENTRY_WIDTH = 5.9
SEAM_SCREW_OFFSET = 15.0
RAIL_SCREW_OFFSET = 10.0
SCREW_SEAT_Z = -UNDERSIDE_DEPTH + M3_HEAD_RECESS_DEPTH
SCREW_TIP_Z = SCREW_SEAT_Z + M3_SCREW_LENGTH

# One M2 x 12 cross-lock retains each corner cap. A top-loaded nut pocket in
# one rail rib per corner avoids heat-set inserts and remains support-free.
M2_CLEARANCE_DIAMETER = 2.4
M2_HEAD_CLEARANCE_DIAMETER = 4.5
M2_HEAD_RECESS_DEPTH = 2.2
M2_SCREW_LENGTH = 12.0
M2_NUT_ACROSS_FLATS = 4.0
M2_NUT_THICKNESS = 1.6
M2_NUT_POCKET_ACROSS_FLATS = 4.25
M2_NUT_POCKET_THICKNESS = 1.9
M2_NUT_ENTRY_WIDTH = 4.95
M2_NUT_INWARD_OFFSET = 2.0
CORNER_LOCK_Z = 4.0

# Bridge, rail, corner, and pad dimensions.
BRIDGE_LENGTH = 50.0
BRIDGE_WIDTH = 20.0
BRIDGE_THICKNESS = UNDERSIDE_DEPTH
RAIL_LENGTH = QUARTER_SIZE
RAIL_FLANGE_DEPTH = 15.0
CORNER_RIB_PROJECTION = 7.0
CORNER_RIB_WIDTH = 9.0
CORNER_RIB_HEIGHT = 16.0
CORNER_SLOT_CLEARANCE = 0.3
CORNER_SLOT_LEAD_DEPTH = 0.8
FELT_RECESS_LENGTH = 30.0
FELT_RECESS_WIDTH = 12.0
FELT_RECESS_DEPTH = 0.8
PERIMETER_TOP_EDGE_FILLET_RADIUS = 2.0

# Flush notation inlays. The pocket is the union of four diagonally shifted
# copies of the insert profile. This provides clearance around outer and inner
# glyph contours without the tiny curved edges produced by a 2D profile offset;
# those edges were imported as open shells by some STEP consumers.
NOTATION_FONT = "DejaVu Sans"
NOTATION_INSERT_FONT_SIZE = 11.0
NOTATION_POCKET_CLEARANCE = 0.18
NOTATION_INLAY_THICKNESS = 1.2
NOTATION_POCKET_DEPTH = 1.4

# Optional separately printed dark-square inlay.
LOOSE_INLAY_CLEARANCE = 0.2
LOOSE_DARK_SQUARE_SIZE = SQUARE_SIZE - 2.0 * LOOSE_INLAY_CLEARANCE

# STEP/display color intent. Actual PLA selections remain slicer-controlled.
LIGHT_COLOR = Color(0.94, 0.86, 0.68)
DARK_COLOR = Color(0.22, 0.09, 0.035)
PERIMETER_COLOR = Color(0.035, 0.035, 0.035)
NOTATION_COLOR = Color(0.96, 0.90, 0.72)
HARDWARE_COLOR = Color(0.35, 0.35, 0.37)


QUARTER_ROLES = ("sw", "se", "nw", "ne")


@dataclass(frozen=True)
class RailSpec:
    name: str
    side: str
    half: str
    symbols: tuple[str, str, str, str]


RAIL_SPECS = {
    "bottom_ad": RailSpec("bottom_ad", "south", "west", tuple("abcd")),
    "bottom_eh": RailSpec("bottom_eh", "south", "east", tuple("efgh")),
    "top_ad": RailSpec("top_ad", "north", "west", tuple("abcd")),
    "top_eh": RailSpec("top_eh", "north", "east", tuple("efgh")),
    "left_14": RailSpec("left_14", "west", "south", tuple("1234")),
    "left_58": RailSpec("left_58", "west", "north", tuple("5678")),
    "right_14": RailSpec("right_14", "east", "south", tuple("1234")),
    "right_58": RailSpec("right_58", "east", "north", tuple("5678")),
}

# These four ribs align with the generic corner cap's cross-lock after its
# four assembly rotations: southwest, southeast, northeast, northwest.
CORNER_LOCK_RAILS = {"bottom_ad", "right_14", "top_eh", "left_58"}


def _box(
    size_x: float,
    size_y: float,
    size_z: float,
    center_x: float,
    center_y: float,
    min_z: float,
):
    return Box(
        size_x,
        size_y,
        size_z,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, center_y, min_z)))


def _cylinder(radius: float, height: float, center_x: float, center_y: float, min_z: float):
    return Cylinder(
        radius=radius,
        height=height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location((center_x, center_y, min_z)))


def _cylinder_along_axis(
    radius: float,
    length: float,
    axis: str,
    center: tuple[float, float, float],
):
    solid = Cylinder(
        radius=radius,
        height=length,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )
    if axis == "x":
        solid = solid.rotate(Axis.Y, 90.0)
    elif axis == "y":
        solid = solid.rotate(Axis.X, 90.0)
    elif axis != "z":
        raise ValueError(f"Unknown cylinder axis: {axis}")
    return solid.moved(Location(center))


def _hex_prism_along_axis(
    across_flats: float,
    thickness: float,
    axis: str,
    center: tuple[float, float, float],
):
    profile = RegularPolygon(
        radius=across_flats / sqrt(3.0),
        side_count=6,
        major_radius=True,
        rotation=0.0,
    )
    solid = extrude(profile, amount=thickness).moved(
        Location((0.0, 0.0, -thickness / 2.0))
    )
    if axis == "x":
        solid = solid.rotate(Axis.Y, 90.0)
    elif axis == "y":
        solid = solid.rotate(Axis.X, 90.0)
    elif axis != "z":
        raise ValueError(f"Unknown hex-prism axis: {axis}")
    return solid.moved(Location(center))


def _chamfer_bottom_edges(shape, bottom_z: float):
    bottom_edges = [
        edge for edge in shape.edges() if abs(edge.center().Z - bottom_z) < 1e-6
    ]
    if not bottom_edges:
        raise ValueError("No build-plane edges found for first-layer relief")
    return chamfer(bottom_edges, length=ELEPHANT_FOOT_RELIEF)


def _chamfer_projecting_tip(shape, edge_name: str, tip_coordinate: float):
    if edge_name in {"east", "west"}:
        tip_edges = [
            edge
            for edge in shape.edges()
            if abs(edge.center().X - tip_coordinate) < 1e-6
        ]
    else:
        tip_edges = [
            edge
            for edge in shape.edges()
            if abs(edge.center().Y - tip_coordinate) < 1e-6
        ]
    if len(tip_edges) != 4:
        raise ValueError(
            f"Expected four leading edges on {edge_name}, found {len(tip_edges)}"
        )
    return chamfer(tip_edges, length=FIT_LEAD_CHAMFER)


def _cut_many(body, cutters):
    # Cutting with a disconnected Compound can preserve the cutter solids in
    # some OCCT/build123d combinations. Sequential booleans are a little more
    # expensive but deterministically return only the intended remainder.
    result = body
    for cutter in cutters:
        result = result.cut(cutter)
    return result.clean()


def _center_xy(shape):
    bounds = shape.bounding_box()
    center_x = (bounds.min.X + bounds.max.X) / 2.0
    center_y = (bounds.min.Y + bounds.max.Y) / 2.0
    return shape.moved(Location((-center_x, -center_y, 0.0)))


def _edge_feature(edge: str, *, male: bool):
    """Return a tongue or groove cutter on one edge of a local quarter."""

    half = QUARTER_SIZE / 2.0
    edge_span = QUARTER_SIZE - 2.0 * TONGUE_END_MARGIN
    if edge in {"east", "west"}:
        if male:
            sign = 1.0 if edge == "east" else -1.0
            center_x = (half + TONGUE_PROJECTION / 2.0) * sign
            tongue = _box(
                TONGUE_PROJECTION,
                edge_span,
                TONGUE_HEIGHT,
                center_x,
                0.0,
                TONGUE_Z,
            )
            return _chamfer_projecting_tip(
                tongue,
                edge,
                sign * (half + TONGUE_PROJECTION),
            )
        overshoot = 0.2
        center_x = (
            half - GROOVE_DEPTH / 2.0 + overshoot / 2.0
        ) * (1.0 if edge == "east" else -1.0)
        return _box(
            GROOVE_DEPTH + overshoot,
            edge_span,
            GROOVE_HEIGHT,
            center_x,
            0.0,
            GROOVE_Z,
        )

    if male:
        sign = 1.0 if edge == "north" else -1.0
        center_y = (half + TONGUE_PROJECTION / 2.0) * sign
        tongue = _box(
            edge_span,
            TONGUE_PROJECTION,
            TONGUE_HEIGHT,
            0.0,
            center_y,
            TONGUE_Z,
        )
        return _chamfer_projecting_tip(
            tongue,
            edge,
            sign * (half + TONGUE_PROJECTION),
        )
    overshoot = 0.2
    center_y = (
        half - GROOVE_DEPTH / 2.0 + overshoot / 2.0
    ) * (1.0 if edge == "north" else -1.0)
    return _box(
        edge_span,
        GROOVE_DEPTH + overshoot,
        GROOVE_HEIGHT,
        0.0,
        center_y,
        GROOVE_Z,
    )


def _anti_lip_feature(edge: str, along: float, *, male: bool):
    """Create one concealed upper key or its clearance groove."""

    half = QUARTER_SIZE / 2.0
    sign = 1.0 if edge in {"east", "north"} else -1.0
    if male:
        projection = ANTI_LIP_KEY_PROJECTION
        span = ANTI_LIP_KEY_LENGTH
        height = ANTI_LIP_KEY_HEIGHT
        min_z = ANTI_LIP_KEY_Z
    else:
        projection = ANTI_LIP_GROOVE_DEPTH + 0.2
        span = ANTI_LIP_GROOVE_LENGTH
        height = ANTI_LIP_GROOVE_HEIGHT
        min_z = ANTI_LIP_GROOVE_Z

    if edge in {"east", "west"}:
        center_x = sign * (half + projection / 2.0) if male else sign * (
            half - ANTI_LIP_GROOVE_DEPTH / 2.0 + 0.1
        )
        feature = _box(
            projection,
            span,
            height,
            center_x,
            along,
            min_z,
        )
        tip = sign * (half + ANTI_LIP_KEY_PROJECTION)
    else:
        center_y = sign * (half + projection / 2.0) if male else sign * (
            half - ANTI_LIP_GROOVE_DEPTH / 2.0 + 0.1
        )
        feature = _box(
            span,
            projection,
            height,
            along,
            center_y,
            min_z,
        )
        tip = sign * (half + ANTI_LIP_KEY_PROJECTION)

    if male:
        return _chamfer_projecting_tip(feature, edge, tip)
    return feature


def _chamfer_quarter_fit_openings(body):
    """Chamfer accessible groove, upper-key, and nut-slot mouth edges."""

    half = QUARTER_SIZE / 2.0
    opening_edges = []
    for edge in body.edges():
        center = edge.center()
        on_x_face = abs(abs(center.X) - half) < 1e-6 and abs(center.Y) < 111.0
        on_y_face = abs(abs(center.Y) - half) < 1e-6 and abs(center.X) < 111.0
        if (on_x_face or on_y_face) and 0.45 < center.Z < 7.35:
            opening_edges.append(edge)
    if not opening_edges:
        raise ValueError("No quarter fit-opening edges found for lead-in chamfers")
    return chamfer(opening_edges, length=FIT_LEAD_CHAMFER)


def _nut_trap_cutters(edge: str, along: float, inward_offset: float):
    """Create a side-loaded vertical M3 nut trap and its screw passage."""

    half = QUARTER_SIZE / 2.0
    if edge in {"east", "west"}:
        sign = 1.0 if edge == "east" else -1.0
        pocket_x = sign * (half - inward_offset)
        pocket_y = along
        hex_profile = RegularPolygon(
            radius=NUT_POCKET_MAJOR_RADIUS,
            side_count=6,
            major_radius=True,
            rotation=0.0,
        )
        hex_pocket = extrude(hex_profile, amount=NUT_POCKET_HEIGHT).moved(
            Location((pocket_x, pocket_y, NUT_POCKET_Z))
        )
        channel_min_x = pocket_x - NUT_POCKET_MAJOR_RADIUS if sign > 0 else -half - 0.3
        channel_max_x = half + 0.3 if sign > 0 else pocket_x + NUT_POCKET_MAJOR_RADIUS
        channel = _box(
            channel_max_x - channel_min_x,
            NUT_ENTRY_WIDTH,
            NUT_POCKET_HEIGHT,
            (channel_min_x + channel_max_x) / 2.0,
            pocket_y,
            NUT_POCKET_Z,
        )
    else:
        sign = 1.0 if edge == "north" else -1.0
        pocket_x = along
        pocket_y = sign * (half - inward_offset)
        hex_profile = RegularPolygon(
            radius=NUT_POCKET_MAJOR_RADIUS,
            side_count=6,
            major_radius=True,
            rotation=30.0,
        )
        hex_pocket = extrude(hex_profile, amount=NUT_POCKET_HEIGHT).moved(
            Location((pocket_x, pocket_y, NUT_POCKET_Z))
        )
        channel_min_y = pocket_y - NUT_POCKET_MAJOR_RADIUS if sign > 0 else -half - 0.3
        channel_max_y = half + 0.3 if sign > 0 else pocket_y + NUT_POCKET_MAJOR_RADIUS
        channel = _box(
            NUT_ENTRY_WIDTH,
            channel_max_y - channel_min_y,
            NUT_POCKET_HEIGHT,
            pocket_x,
            (channel_min_y + channel_max_y) / 2.0,
            NUT_POCKET_Z,
        )

    screw_passage = _cylinder(
        M3_CLEARANCE_DIAMETER / 2.0,
        NUT_POCKET_Z + 0.25,
        pocket_x,
        pocket_y,
        -0.1,
    )
    return [hex_pocket, channel, screw_passage]


def _quarter_edge_plan(role: str):
    if role not in QUARTER_ROLES:
        raise ValueError(f"Unknown quarter role: {role}")

    west_half = role.endswith("w")
    south_half = role.startswith("s")
    return {
        "east" if west_half else "west": "male" if west_half else "female",
        "north" if south_half else "south": "male" if south_half else "female",
        "west" if west_half else "east": "outer",
        "south" if south_half else "north": "outer",
    }


def make_quarter_details(role: str):
    """Return labeled light/dark bodies and joinery metadata for one quarter."""

    edge_plan = _quarter_edge_plan(role)
    body = _box(
        QUARTER_SIZE,
        QUARTER_SIZE,
        PANEL_BASE_THICKNESS,
        0.0,
        0.0,
        0.0,
    )
    body = _chamfer_bottom_edges(body, 0.0)

    light_caps = []
    dark_exact = []
    centers = [
        -QUARTER_SIZE / 2.0 + SQUARE_SIZE / 2.0 + index * SQUARE_SIZE
        for index in range(4)
    ]
    for file_index, center_x in enumerate(centers):
        for rank_index, center_y in enumerate(centers):
            is_dark = (file_index + rank_index) % 2 == 0
            tile = _box(
                SQUARE_SIZE,
                SQUARE_SIZE,
                FACE_INLAY_THICKNESS,
                center_x,
                center_y,
                PANEL_BASE_THICKNESS,
            )
            if is_dark:
                dark_exact.append(tile)
            else:
                # A tiny overlap makes the light cap reliably monolithic with
                # the structural body without changing the top elevation.
                light_caps.append(
                    _box(
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                        FACE_INLAY_THICKNESS + 0.01,
                        center_x,
                        center_y,
                        PANEL_BASE_THICKNESS - 0.01,
                    )
                )

    body = body.fuse(*light_caps).clean()
    groove_cutters = []
    for edge, connection in edge_plan.items():
        if connection == "male":
            body = body.fuse(_edge_feature(edge, male=True)).clean()
            for along in ANTI_LIP_KEY_POSITIONS:
                body = body.fuse(
                    _anti_lip_feature(edge, along, male=True)
                ).clean()
        elif connection == "female":
            groove_cutters.append(_edge_feature(edge, male=False))
            for along in ANTI_LIP_KEY_POSITIONS:
                groove_cutters.append(_anti_lip_feature(edge, along, male=False))
        else:
            groove_cutters.append(_edge_feature(edge, male=False))

    nut_cutters = []
    for edge, connection in edge_plan.items():
        offset = RAIL_SCREW_OFFSET if connection == "outer" else SEAM_SCREW_OFFSET
        for along in (-SQUARE_SIZE, SQUARE_SIZE):
            nut_cutters.extend(_nut_trap_cutters(edge, along, offset))

    body = _cut_many(body, [*groove_cutters, *nut_cutters])
    body = _chamfer_quarter_fit_openings(body)
    body = label_shape(body, "quarter_light_body", role, color=LIGHT_COLOR)

    labeled_dark = []
    for index, tile in enumerate(dark_exact, start=1):
        labeled_dark.append(
            label_shape(tile, "dark_square", role, index, color=DARK_COLOR)
        )
    dark_compound = Compound(
        children=labeled_dark,
        label=f"dark_square_inlays:{role}",
        color=DARK_COLOR,
    )

    return {
        "role": role,
        "edge_plan": edge_plan,
        "light_body": body,
        "dark_inlays": dark_compound,
    }


def make_quarter_print_assembly(role: str):
    details = make_quarter_details(role)
    assembly = AssemblyHelper(f"quarter_{role}_multicolor_print")
    assembly.add(details["light_body"], "light_body", role, color=LIGHT_COLOR)
    assembly.add(details["dark_inlays"], "dark_inlays", role, color=DARK_COLOR)
    return assembly.build()


def make_quarter_light_body_for_print(role: str):
    return label_shape(
        _center_xy(make_quarter_details(role)["light_body"]),
        "quarter_light_body",
        role,
        color=LIGHT_COLOR,
    )


def make_loose_dark_square_inlay():
    return label_shape(
        _box(
            LOOSE_DARK_SQUARE_SIZE,
            LOOSE_DARK_SQUARE_SIZE,
            FACE_INLAY_THICKNESS,
            0.0,
            0.0,
            0.0,
        ),
        "loose_dark_square_inlay",
        color=DARK_COLOR,
    )


def _rail_long_range(spec: RailSpec):
    if spec.half in {"west", "south"}:
        return (-QUARTER_SIZE, 0.0)
    return (0.0, QUARTER_SIZE)


def _rail_text_solid(
    symbol: str,
    *,
    font_size: float,
    rotation: float,
    center_x: float,
    center_y: float,
    min_z: float,
    height: float,
    pocket_clearance: float = 0.0,
):
    profile = Text(
        symbol,
        font_size=font_size,
        font=NOTATION_FONT,
        font_style=FontStyle.BOLD,
        rotation=rotation,
    )
    solid = extrude(profile, amount=height)
    if pocket_clearance:
        shifted = [
            solid.moved(Location((shift_x, shift_y, 0.0)))
            for shift_x, shift_y in (
                (pocket_clearance, pocket_clearance),
                (pocket_clearance, -pocket_clearance),
                (-pocket_clearance, pocket_clearance),
                (-pocket_clearance, -pocket_clearance),
            )
        ]
        solid = solid.fuse(*shifted).clean()
    return solid.moved(Location((center_x, center_y, min_z)))


def _rail_corner_rib(spec: RailSpec, wall_center: float):
    long_min, long_max = _rail_long_range(spec)
    negative_end = spec.half in {"west", "south"}
    if spec.side in {"south", "north"}:
        end = long_min if negative_end else long_max
        center_x = end - CORNER_RIB_PROJECTION / 2.0 if negative_end else end + CORNER_RIB_PROJECTION / 2.0
        rib = _box(
            CORNER_RIB_PROJECTION + 0.1,
            CORNER_RIB_WIDTH,
            CORNER_RIB_HEIGHT + UNDERSIDE_DEPTH,
            center_x,
            wall_center,
            -UNDERSIDE_DEPTH,
        )
        lock_center = (center_x, wall_center, CORNER_LOCK_Z)
        lock_axis = "y"
        inward = 1.0 if spec.side == "south" else -1.0
        nut_center = (
            center_x,
            wall_center + inward * M2_NUT_INWARD_OFFSET,
            CORNER_LOCK_Z,
        )
        channel_center_x, channel_center_y = center_x, nut_center[1]
        channel_size_x, channel_size_y = (
            M2_NUT_ENTRY_WIDTH,
            M2_NUT_POCKET_THICKNESS,
        )
    else:
        end = long_min if negative_end else long_max
        center_y = end - CORNER_RIB_PROJECTION / 2.0 if negative_end else end + CORNER_RIB_PROJECTION / 2.0
        rib = _box(
            CORNER_RIB_WIDTH,
            CORNER_RIB_PROJECTION + 0.1,
            CORNER_RIB_HEIGHT + UNDERSIDE_DEPTH,
            wall_center,
            center_y,
            -UNDERSIDE_DEPTH,
        )
        lock_center = (wall_center, center_y, CORNER_LOCK_Z)
        lock_axis = "x"
        inward = 1.0 if spec.side == "west" else -1.0
        nut_center = (
            wall_center + inward * M2_NUT_INWARD_OFFSET,
            center_y,
            CORNER_LOCK_Z,
        )
        channel_center_x, channel_center_y = nut_center[0], center_y
        channel_size_x, channel_size_y = (
            M2_NUT_POCKET_THICKNESS,
            M2_NUT_ENTRY_WIDTH,
        )

    top_edges = [
        edge
        for edge in rib.edges()
        if abs(edge.center().Z - CORNER_RIB_HEIGHT) < 1e-6
    ]
    rib = chamfer(top_edges, length=FIT_LEAD_CHAMFER)

    if spec.name in CORNER_LOCK_RAILS:
        entry_min_z = CORNER_LOCK_Z - M2_NUT_POCKET_ACROSS_FLATS / 2.0
        entry_height = CORNER_RIB_HEIGHT - entry_min_z + 0.1
        cutters = [
            _cylinder_along_axis(
                M2_CLEARANCE_DIAMETER / 2.0,
                CORNER_RIB_WIDTH + 0.4,
                lock_axis,
                lock_center,
            ),
            _hex_prism_along_axis(
                M2_NUT_POCKET_ACROSS_FLATS,
                M2_NUT_POCKET_THICKNESS,
                lock_axis,
                nut_center,
            ),
            _box(
                channel_size_x,
                channel_size_y,
                entry_height,
                channel_center_x,
                channel_center_y,
                entry_min_z,
            ),
        ]
        rib = _cut_many(rib, cutters)
    return rib


def _fillet_rail_exposed_top_edges(wall, long_length: float):
    """Round the two exposed top edges without softening rail mating seams."""

    top_edges = [
        edge
        for edge in wall.edges()
        if abs(edge.center().Z - PERIMETER_TOP_Z) < 1e-6
        and abs(edge.length - long_length) < 1e-6
    ]
    if len(top_edges) != 2:
        raise ValueError(
            f"Expected two exposed rail top edges, found {len(top_edges)}"
        )
    return fillet(top_edges, radius=PERIMETER_TOP_EDGE_FILLET_RADIUS)


def make_rail_details(name: str):
    """Return one assembled-position rail body and its contrasting glyphs."""

    spec = RAIL_SPECS[name]
    long_min, long_max = _rail_long_range(spec)
    long_center = (long_min + long_max) / 2.0
    long_length = long_max - long_min
    rail_height = PERIMETER_TOP_Z + UNDERSIDE_DEPTH
    overlap = 0.1

    if spec.side == "south":
        wall_center = -(PLAYING_SIZE / 2.0 + PERIMETER_WIDTH / 2.0)
        wall = _box(long_length, PERIMETER_WIDTH, rail_height, long_center, wall_center, -UNDERSIDE_DEPTH)
        flange = _box(long_length, RAIL_FLANGE_DEPTH + overlap, UNDERSIDE_DEPTH, long_center, -PLAYING_SIZE / 2.0 + (RAIL_FLANGE_DEPTH - overlap) / 2.0, -UNDERSIDE_DEPTH)
        tongue = _box(long_length - 2.0 * TONGUE_END_MARGIN, TONGUE_PROJECTION + overlap, TONGUE_HEIGHT, long_center, -PLAYING_SIZE / 2.0 + (TONGUE_PROJECTION - overlap) / 2.0, TONGUE_Z)
        screw_across = -PLAYING_SIZE / 2.0 + RAIL_SCREW_OFFSET
        text_across = wall_center
        text_rotation = 0.0
        tongue_edge = "north"
        tongue_tip = -PLAYING_SIZE / 2.0 + TONGUE_PROJECTION
    elif spec.side == "north":
        wall_center = PLAYING_SIZE / 2.0 + PERIMETER_WIDTH / 2.0
        wall = _box(long_length, PERIMETER_WIDTH, rail_height, long_center, wall_center, -UNDERSIDE_DEPTH)
        flange = _box(long_length, RAIL_FLANGE_DEPTH + overlap, UNDERSIDE_DEPTH, long_center, PLAYING_SIZE / 2.0 - (RAIL_FLANGE_DEPTH - overlap) / 2.0, -UNDERSIDE_DEPTH)
        tongue = _box(long_length - 2.0 * TONGUE_END_MARGIN, TONGUE_PROJECTION + overlap, TONGUE_HEIGHT, long_center, PLAYING_SIZE / 2.0 - (TONGUE_PROJECTION - overlap) / 2.0, TONGUE_Z)
        screw_across = PLAYING_SIZE / 2.0 - RAIL_SCREW_OFFSET
        text_across = wall_center
        text_rotation = 180.0
        tongue_edge = "south"
        tongue_tip = PLAYING_SIZE / 2.0 - TONGUE_PROJECTION
    elif spec.side == "west":
        wall_center = -(PLAYING_SIZE / 2.0 + PERIMETER_WIDTH / 2.0)
        wall = _box(PERIMETER_WIDTH, long_length, rail_height, wall_center, long_center, -UNDERSIDE_DEPTH)
        flange = _box(RAIL_FLANGE_DEPTH + overlap, long_length, UNDERSIDE_DEPTH, -PLAYING_SIZE / 2.0 + (RAIL_FLANGE_DEPTH - overlap) / 2.0, long_center, -UNDERSIDE_DEPTH)
        tongue = _box(TONGUE_PROJECTION + overlap, long_length - 2.0 * TONGUE_END_MARGIN, TONGUE_HEIGHT, -PLAYING_SIZE / 2.0 + (TONGUE_PROJECTION - overlap) / 2.0, long_center, TONGUE_Z)
        screw_across = -PLAYING_SIZE / 2.0 + RAIL_SCREW_OFFSET
        text_across = wall_center
        text_rotation = -90.0
        tongue_edge = "east"
        tongue_tip = -PLAYING_SIZE / 2.0 + TONGUE_PROJECTION
    else:
        wall_center = PLAYING_SIZE / 2.0 + PERIMETER_WIDTH / 2.0
        wall = _box(PERIMETER_WIDTH, long_length, rail_height, wall_center, long_center, -UNDERSIDE_DEPTH)
        flange = _box(RAIL_FLANGE_DEPTH + overlap, long_length, UNDERSIDE_DEPTH, PLAYING_SIZE / 2.0 - (RAIL_FLANGE_DEPTH - overlap) / 2.0, long_center, -UNDERSIDE_DEPTH)
        tongue = _box(TONGUE_PROJECTION + overlap, long_length - 2.0 * TONGUE_END_MARGIN, TONGUE_HEIGHT, PLAYING_SIZE / 2.0 - (TONGUE_PROJECTION - overlap) / 2.0, long_center, TONGUE_Z)
        screw_across = PLAYING_SIZE / 2.0 - RAIL_SCREW_OFFSET
        text_across = wall_center
        text_rotation = 90.0
        tongue_edge = "west"
        tongue_tip = PLAYING_SIZE / 2.0 - TONGUE_PROJECTION

    wall = _fillet_rail_exposed_top_edges(wall, long_length)
    tongue = _chamfer_projecting_tip(tongue, tongue_edge, tongue_tip)
    corner_rib = _rail_corner_rib(spec, wall_center)
    body = wall.fuse(flange, tongue, corner_rib).clean()
    body = _chamfer_bottom_edges(body, -UNDERSIDE_DEPTH)

    screw_positions = (long_min + SQUARE_SIZE, long_min + 3.0 * SQUARE_SIZE)
    cutters = []
    for long_position in screw_positions:
        if spec.side in {"south", "north"}:
            screw_x, screw_y = long_position, screw_across
        else:
            screw_x, screw_y = screw_across, long_position
        cutters.append(
            _cylinder(
                M3_CLEARANCE_DIAMETER / 2.0,
                UNDERSIDE_DEPTH + NUT_POCKET_Z + 0.25,
                screw_x,
                screw_y,
                -UNDERSIDE_DEPTH - 0.1,
            )
        )
        cutters.append(
            _cylinder(
                M3_HEAD_CLEARANCE_DIAMETER / 2.0,
                M3_HEAD_RECESS_DEPTH + 0.2,
                screw_x,
                screw_y,
                -UNDERSIDE_DEPTH - 0.1,
            )
        )

    if spec.side in {"south", "north"}:
        felt_center_x, felt_center_y = long_center, wall_center
        felt_size_x, felt_size_y = FELT_RECESS_LENGTH, FELT_RECESS_WIDTH
    else:
        felt_center_x, felt_center_y = wall_center, long_center
        felt_size_x, felt_size_y = FELT_RECESS_WIDTH, FELT_RECESS_LENGTH
    cutters.append(
        _box(
            felt_size_x,
            felt_size_y,
            FELT_RECESS_DEPTH + 0.1,
            felt_center_x,
            felt_center_y,
            -UNDERSIDE_DEPTH - 0.05,
        )
    )

    inserts = []
    text_positions = [long_min + SQUARE_SIZE / 2.0 + index * SQUARE_SIZE for index in range(4)]
    for symbol, long_position in zip(spec.symbols, text_positions, strict=True):
        if spec.side in {"south", "north"}:
            text_x, text_y = long_position, text_across
        else:
            text_x, text_y = text_across, long_position
        pocket = _rail_text_solid(
            symbol,
            font_size=NOTATION_INSERT_FONT_SIZE,
            rotation=text_rotation,
            center_x=text_x,
            center_y=text_y,
            min_z=PERIMETER_TOP_Z - NOTATION_POCKET_DEPTH,
            height=NOTATION_POCKET_DEPTH + 0.2,
            pocket_clearance=NOTATION_POCKET_CLEARANCE,
        )
        cutters.append(pocket)
        insert = _rail_text_solid(
            symbol,
            font_size=NOTATION_INSERT_FONT_SIZE,
            rotation=text_rotation,
            center_x=text_x,
            center_y=text_y,
            min_z=PERIMETER_TOP_Z - NOTATION_INLAY_THICKNESS,
            height=NOTATION_INLAY_THICKNESS,
        )
        inserts.append(
            label_shape(insert, "notation", name, symbol, color=NOTATION_COLOR)
        )

    body = _cut_many(body, cutters)
    body = label_shape(body, "perimeter_rail", name, color=PERIMETER_COLOR)
    insert_compound = Compound(
        children=inserts,
        label=f"notation_inlays:{name}",
        color=NOTATION_COLOR,
    )
    return {
        "spec": spec,
        "body": body,
        "notation_inlays": insert_compound,
    }


def make_rail_print_assembly(name: str):
    details = make_rail_details(name)
    combined = Compound(children=[details["body"], details["notation_inlays"]])
    bounds = combined.bounding_box()
    move = Location(
        (
            -(bounds.min.X + bounds.max.X) / 2.0,
            -(bounds.min.Y + bounds.max.Y) / 2.0,
            0.0,
        )
    )
    body = details["body"].moved(move)
    inlays = details["notation_inlays"].moved(move)
    assembly = AssemblyHelper(f"rail_{name}_multicolor_print")
    assembly.add(body, "perimeter_body", name, color=PERIMETER_COLOR)
    assembly.add(inlays, "notation_inlays", name, color=NOTATION_COLOR)
    return assembly.build()


def make_rail_body_for_print(name: str):
    return label_shape(
        _center_xy(make_rail_details(name)["body"]),
        "perimeter_rail",
        name,
        color=PERIMETER_COLOR,
    )


def make_seam_bridge():
    body = _box(
        BRIDGE_LENGTH,
        BRIDGE_WIDTH,
        BRIDGE_THICKNESS,
        0.0,
        0.0,
        -UNDERSIDE_DEPTH,
    )
    cutters = []
    for center_x in (-SEAM_SCREW_OFFSET, SEAM_SCREW_OFFSET):
        cutters.append(
            _cylinder(
                M3_CLEARANCE_DIAMETER / 2.0,
                BRIDGE_THICKNESS + 0.2,
                center_x,
                0.0,
                -UNDERSIDE_DEPTH - 0.1,
            )
        )
        cutters.append(
            _cylinder(
                M3_HEAD_CLEARANCE_DIAMETER / 2.0,
                M3_HEAD_RECESS_DEPTH + 0.2,
                center_x,
                0.0,
                -UNDERSIDE_DEPTH - 0.1,
            )
        )
    return label_shape(
        _cut_many(body, cutters),
        "seam_bridge",
        color=PERIMETER_COLOR,
    )


def make_corner_cap():
    """Make the southwest-oriented cap; rotate copies in 90-degree steps."""

    block = _box(
        PERIMETER_WIDTH,
        PERIMETER_WIDTH,
        PERIMETER_TOP_Z + UNDERSIDE_DEPTH,
        0.0,
        0.0,
        -UNDERSIDE_DEPTH,
    )
    outer_top_edges = [
        edge
        for edge in block.edges()
        if abs(edge.center().Z - PERIMETER_TOP_Z) < 1e-6
        and (
            abs(edge.center().X + PERIMETER_WIDTH / 2.0) < 1e-6
            or abs(edge.center().Y + PERIMETER_WIDTH / 2.0) < 1e-6
        )
    ]
    if len(outer_top_edges) != 2:
        raise ValueError(
            f"Expected two exposed corner top edges, found {len(outer_top_edges)}"
        )
    block = fillet(outer_top_edges, radius=PERIMETER_TOP_EDGE_FILLET_RADIUS)
    block = _chamfer_bottom_edges(block, -UNDERSIDE_DEPTH)
    slot_depth = CORNER_RIB_PROJECTION + CORNER_SLOT_CLEARANCE
    slot_width = CORNER_RIB_WIDTH + 2.0 * CORNER_SLOT_CLEARANCE
    slot_height = CORNER_RIB_HEIGHT + CORNER_SLOT_CLEARANCE + UNDERSIDE_DEPTH
    positive_x_slot = _box(
        slot_depth + 0.2,
        slot_width,
        slot_height,
        PERIMETER_WIDTH / 2.0 - slot_depth / 2.0 + 0.1,
        0.0,
        -UNDERSIDE_DEPTH - 0.1,
    )
    positive_y_slot = _box(
        slot_width,
        slot_depth + 0.2,
        slot_height,
        0.0,
        PERIMETER_WIDTH / 2.0 - slot_depth / 2.0 + 0.1,
        -UNDERSIDE_DEPTH - 0.1,
    )
    lead_depth = slot_depth + 2.0 * FIT_LEAD_CHAMFER
    lead_width = slot_width + 2.0 * FIT_LEAD_CHAMFER
    positive_x_lead = _box(
        lead_depth + 0.2,
        lead_width,
        CORNER_SLOT_LEAD_DEPTH + 0.1,
        PERIMETER_WIDTH / 2.0 - lead_depth / 2.0 + 0.1,
        0.0,
        -UNDERSIDE_DEPTH - 0.1,
    )
    positive_y_lead = _box(
        lead_width,
        lead_depth + 0.2,
        CORNER_SLOT_LEAD_DEPTH + 0.1,
        0.0,
        PERIMETER_WIDTH / 2.0 - lead_depth / 2.0 + 0.1,
        -UNDERSIDE_DEPTH - 0.1,
    )
    felt_recess = _box(
        12.0,
        12.0,
        FELT_RECESS_DEPTH + 0.1,
        0.0,
        0.0,
        -UNDERSIDE_DEPTH - 0.05,
    )
    lock_x = PERIMETER_WIDTH / 2.0 - CORNER_RIB_PROJECTION / 2.0
    lock_hole_start = -PERIMETER_WIDTH / 2.0 - 0.1
    lock_hole_end = CORNER_RIB_WIDTH / 2.0 + 0.2
    lock_hole_length = lock_hole_end - lock_hole_start
    lock_clearance = _cylinder_along_axis(
        M2_CLEARANCE_DIAMETER / 2.0,
        lock_hole_length,
        "y",
        (lock_x, (lock_hole_start + lock_hole_end) / 2.0, CORNER_LOCK_Z),
    )
    lock_head_recess = _cylinder_along_axis(
        M2_HEAD_CLEARANCE_DIAMETER / 2.0,
        M2_HEAD_RECESS_DEPTH + 0.2,
        "y",
        (
            lock_x,
            lock_hole_start + (M2_HEAD_RECESS_DEPTH + 0.2) / 2.0,
            CORNER_LOCK_Z,
        ),
    )
    return label_shape(
        _cut_many(
            block,
            [
                positive_x_slot,
                positive_y_slot,
                positive_x_lead,
                positive_y_lead,
                felt_recess,
                lock_clearance,
                lock_head_recess,
            ],
        ),
        "corner_cap",
        color=PERIMETER_COLOR,
    )


def make_notation_insert_print_set():
    rows = (tuple("abcdefgh"), tuple("abcdefgh"), tuple("12345678"), tuple("12345678"))
    children = []
    spacing = 16.0
    for row_index, symbols in enumerate(rows):
        for column_index, symbol in enumerate(symbols):
            center_x = (column_index - 3.5) * spacing
            center_y = (1.5 - row_index) * spacing
            glyph = _rail_text_solid(
                symbol,
                font_size=NOTATION_INSERT_FONT_SIZE,
                rotation=0.0,
                center_x=center_x,
                center_y=center_y,
                min_z=0.0,
                height=NOTATION_INLAY_THICKNESS,
            )
            children.append(
                label_shape(
                    glyph,
                    "notation_insert",
                    row_index + 1,
                    symbol,
                    color=NOTATION_COLOR,
                )
            )
    return Compound(
        children=children,
        label="notation_insert_print_set",
        color=NOTATION_COLOR,
    )


def _quarter_assembly_location(role: str):
    return Location(
        (
            -QUARTER_SIZE / 2.0 if role.endswith("w") else QUARTER_SIZE / 2.0,
            -QUARTER_SIZE / 2.0 if role.startswith("s") else QUARTER_SIZE / 2.0,
            0.0,
        )
    )


def _corner_placements():
    corner_center = PLAYING_SIZE / 2.0 + PERIMETER_WIDTH / 2.0
    return {
        "sw": Location((-corner_center, -corner_center, 0.0), (0.0, 0.0, 0.0)),
        "se": Location((corner_center, -corner_center, 0.0), (0.0, 0.0, 90.0)),
        "ne": Location((corner_center, corner_center, 0.0), (0.0, 0.0, 180.0)),
        "nw": Location((-corner_center, corner_center, 0.0), (0.0, 0.0, 270.0)),
    }


def make_full_assembly():
    assembly = AssemblyHelper("fide_60mm_modular_chessboard_x2d")

    for role in QUARTER_ROLES:
        details = make_quarter_details(role)
        location = _quarter_assembly_location(role)
        light = details["light_body"].moved(location)
        dark = details["dark_inlays"].moved(location)
        assembly.add_module(f"quarter_{role}", [light, dark])

    for name in RAIL_SPECS:
        details = make_rail_details(name)
        assembly.add_module(
            f"rail_{name}",
            [details["body"], details["notation_inlays"]],
        )

    corner = make_corner_cap()
    for role, location in _corner_placements().items():
        placed = corner.moved(location)
        assembly.add(placed, "corner_cap", role, color=PERIMETER_COLOR)

    bridge = make_seam_bridge()
    for y_position in (-3.0 * SQUARE_SIZE, -SQUARE_SIZE, SQUARE_SIZE, 3.0 * SQUARE_SIZE):
        placed = bridge.moved(Location((0.0, y_position, 0.0)))
        assembly.add(placed, "vertical_seam_bridge", int(y_position), color=PERIMETER_COLOR)
    for x_position in (-3.0 * SQUARE_SIZE, -SQUARE_SIZE, SQUARE_SIZE, 3.0 * SQUARE_SIZE):
        placed = bridge.moved(Location((x_position, 0.0, 0.0), (0.0, 0.0, 90.0)))
        assembly.add(placed, "horizontal_seam_bridge", int(x_position), color=PERIMETER_COLOR)

    return assembly.build()
