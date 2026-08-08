"""Eight-panel variant of the 60 mm modular X2D chessboard.

The assembled coordinate system matches ``chessboard_geometry``: the board
center is the origin, XY is the playing plane, White is at negative Y, and +Z
is upward.  Each printable playing panel contains two files by four ranks and
is centered locally for slicer import.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from build123d import Compound, Location, RegularPolygon, extrude, chamfer
from cadpy.assembly import AssemblyHelper, label_shape

from chessboard_geometry import (
    ANTI_LIP_GROOVE_DEPTH,
    ANTI_LIP_GROOVE_HEIGHT,
    ANTI_LIP_GROOVE_LENGTH,
    ANTI_LIP_GROOVE_Z,
    ANTI_LIP_KEY_HEIGHT,
    ANTI_LIP_KEY_LENGTH,
    ANTI_LIP_KEY_PROJECTION,
    ANTI_LIP_KEY_Z,
    DARK_COLOR,
    FACE_INLAY_THICKNESS,
    FIT_LEAD_CHAMFER,
    GROOVE_DEPTH,
    GROOVE_HEIGHT,
    GROOVE_Z,
    LIGHT_COLOR,
    NUT_POCKET_HEIGHT,
    NUT_POCKET_Z,
    PANEL_BASE_THICKNESS,
    PERIMETER_COLOR,
    PLAYING_SIZE,
    PLAYING_SURFACE_Z,
    RAIL_SCREW_OFFSET,
    RAIL_SPECS,
    SEAM_SCREW_OFFSET,
    SQUARE_SIZE,
    TONGUE_END_MARGIN,
    TONGUE_HEIGHT,
    TONGUE_PROJECTION,
    TONGUE_Z,
    _box,
    _chamfer_bottom_edges,
    _chamfer_projecting_tip,
    _corner_placements,
    _cut_many,
    _cylinder,
    make_corner_cap,
    make_rail_details,
    make_seam_bridge,
)


PANEL_WIDTH = 2.0 * SQUARE_SIZE
PANEL_HEIGHT = 4.0 * SQUARE_SIZE
PANEL_COLUMNS = ("ab", "cd", "ef", "gh")
PANEL_ROWS = ("south", "north")
PANEL_X_CENTERS = (-180.0, -60.0, 60.0, 180.0)
PANEL_Y_CENTERS = {"south": -120.0, "north": 120.0}

# Panel-only M3 clearances refined from the user's PLA Matte print test.
# Perimeter rails, seam bridges, corner caps, and legacy quarters deliberately
# retain the original shared hardware dimensions in chessboard_geometry.py.
PANEL_M3_CLEARANCE_DIAMETER = 3.6
PANEL_NUT_ENTRY_WIDTH = 6.1
PANEL_NUT_POCKET_ACROSS_FLATS = 5.8
PANEL_NUT_POCKET_MAJOR_RADIUS = PANEL_NUT_POCKET_ACROSS_FLATS / sqrt(3.0)

# Diagonally opposite raised light squares otherwise meet along a zero-width
# vertical edge at the three internal checker vertices in each 2 x 4 panel.
# Some slicer tessellators represent that edge with four incident triangles
# and report it as non-manifold.  This sub-nozzle relief separates those
# diagonal contacts without changing the 60 mm grid pitch or dark-tile seats.
CHECKER_VERTEX_RELIEF_SIZE = 0.2
CHECKER_VERTEX_RELIEF_OVERSHOOT = 0.1


@dataclass(frozen=True)
class EightPanelSpec:
    name: str
    row: str
    column: str
    column_index: int


EIGHT_PANEL_SPECS = {
    f"{row}_{column}": EightPanelSpec(
        f"{row}_{column}", row, column, column_index
    )
    for row in PANEL_ROWS
    for column_index, column in enumerate(PANEL_COLUMNS)
}
EIGHT_PANEL_ROLES = tuple(EIGHT_PANEL_SPECS)


def panel_edge_plan(name: str) -> dict[str, str]:
    """Return male/female/outer intent for one assembled panel."""

    spec = EIGHT_PANEL_SPECS[name]
    return {
        "west": "outer" if spec.column_index == 0 else "female",
        "east": "outer" if spec.column_index == 3 else "male",
        "south": "outer" if spec.row == "south" else "female",
        "north": "male" if spec.row == "south" else "outer",
    }


def panel_assembly_location(name: str) -> Location:
    spec = EIGHT_PANEL_SPECS[name]
    return Location(
        (
            PANEL_X_CENTERS[spec.column_index],
            PANEL_Y_CENTERS[spec.row],
            0.0,
        )
    )


def _rect_edge_feature(
    edge: str,
    *,
    male: bool,
    negative_margin: float = TONGUE_END_MARGIN,
    positive_margin: float = TONGUE_END_MARGIN,
):
    """Make one lower tongue or groove for a 120 x 240 mm panel."""

    half_x = PANEL_WIDTH / 2.0
    half_y = PANEL_HEIGHT / 2.0
    if edge in {"east", "west"}:
        along_min = -half_y + negative_margin
        along_max = half_y - positive_margin
        edge_span = along_max - along_min
        along_center = (along_min + along_max) / 2.0
        if male:
            sign = 1.0 if edge == "east" else -1.0
            center_x = sign * (half_x + TONGUE_PROJECTION / 2.0)
            tongue = _box(
                TONGUE_PROJECTION,
                edge_span,
                TONGUE_HEIGHT,
                center_x,
                along_center,
                TONGUE_Z,
            )
            return _chamfer_projecting_tip(
                tongue,
                edge,
                sign * (half_x + TONGUE_PROJECTION),
            )
        overshoot = 0.2
        sign = 1.0 if edge == "east" else -1.0
        center_x = sign * (half_x - GROOVE_DEPTH / 2.0 + overshoot / 2.0)
        return _box(
            GROOVE_DEPTH + overshoot,
            edge_span,
            GROOVE_HEIGHT,
            center_x,
            along_center,
            GROOVE_Z,
        )

    along_min = -half_x + negative_margin
    along_max = half_x - positive_margin
    edge_span = along_max - along_min
    along_center = (along_min + along_max) / 2.0
    if male:
        sign = 1.0 if edge == "north" else -1.0
        center_y = sign * (half_y + TONGUE_PROJECTION / 2.0)
        tongue = _box(
            edge_span,
            TONGUE_PROJECTION,
            TONGUE_HEIGHT,
            along_center,
            center_y,
            TONGUE_Z,
        )
        return _chamfer_projecting_tip(
            tongue,
            edge,
            sign * (half_y + TONGUE_PROJECTION),
        )
    overshoot = 0.2
    sign = 1.0 if edge == "north" else -1.0
    center_y = sign * (half_y - GROOVE_DEPTH / 2.0 + overshoot / 2.0)
    return _box(
        edge_span,
        GROOVE_DEPTH + overshoot,
        GROOVE_HEIGHT,
        along_center,
        center_y,
        GROOVE_Z,
    )


def _anti_lip_positions(edge: str) -> tuple[float, float]:
    return (-90.0, 90.0) if edge in {"east", "west"} else (-30.0, 30.0)


def _edge_end_margins(spec: EightPanelSpec, edge: str, connection: str):
    """Keep relief at rail ends, but not where one rail spans two panels."""

    if connection == "outer" and edge in {"north", "south"}:
        if spec.column_index % 2 == 0:
            return TONGUE_END_MARGIN, 0.0
        return 0.0, TONGUE_END_MARGIN
    return TONGUE_END_MARGIN, TONGUE_END_MARGIN


def _rect_anti_lip_feature(edge: str, along: float, *, male: bool):
    """Make one concealed upper seam key or its clearance groove."""

    half_x = PANEL_WIDTH / 2.0
    half_y = PANEL_HEIGHT / 2.0
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
        center_x = (
            sign * (half_x + projection / 2.0)
            if male
            else sign * (half_x - ANTI_LIP_GROOVE_DEPTH / 2.0 + 0.1)
        )
        feature = _box(projection, span, height, center_x, along, min_z)
        tip = sign * (half_x + ANTI_LIP_KEY_PROJECTION)
    else:
        center_y = (
            sign * (half_y + projection / 2.0)
            if male
            else sign * (half_y - ANTI_LIP_GROOVE_DEPTH / 2.0 + 0.1)
        )
        feature = _box(span, projection, height, along, center_y, min_z)
        tip = sign * (half_y + ANTI_LIP_KEY_PROJECTION)

    if male:
        return _chamfer_projecting_tip(feature, edge, tip)
    return feature


def _chamfer_panel_fit_openings(body, edge_plan: dict[str, str]):
    """Chamfer internal female seam openings without weakening rail corners."""

    half_x = PANEL_WIDTH / 2.0
    half_y = PANEL_HEIGHT / 2.0
    opening_edges = []
    for edge in body.edges():
        center = edge.center()
        x_side = "east" if center.X > 0.0 else "west"
        y_side = "north" if center.Y > 0.0 else "south"
        on_x_face = (
            abs(abs(center.X) - half_x) < 1e-6
            and abs(center.Y) < half_y - 9.0
            and edge_plan[x_side] == "female"
        )
        on_y_face = (
            abs(abs(center.Y) - half_y) < 1e-6
            and abs(center.X) < half_x - 9.0
            and edge_plan[y_side] == "female"
        )
        if (on_x_face or on_y_face) and 0.45 < center.Z < 7.35:
            opening_edges.append(edge)
    if not opening_edges:
        return body
    return chamfer(opening_edges, length=FIT_LEAD_CHAMFER)


def _panel_nut_positions(edge: str) -> tuple[float, ...]:
    return (-SQUARE_SIZE, SQUARE_SIZE) if edge in {"east", "west"} else (0.0,)


def _rect_nut_trap_cutters(edge: str, along: float, inward_offset: float):
    """Create one side-loaded M3 trap in a rectangular panel edge."""

    half_x = PANEL_WIDTH / 2.0
    half_y = PANEL_HEIGHT / 2.0
    if edge in {"east", "west"}:
        sign = 1.0 if edge == "east" else -1.0
        pocket_x = sign * (half_x - inward_offset)
        pocket_y = along
        hex_profile = RegularPolygon(
            radius=PANEL_NUT_POCKET_MAJOR_RADIUS,
            side_count=6,
            major_radius=True,
            rotation=0.0,
        )
        hex_pocket = extrude(hex_profile, amount=NUT_POCKET_HEIGHT).moved(
            Location((pocket_x, pocket_y, NUT_POCKET_Z))
        )
        channel_min_x = (
            pocket_x - PANEL_NUT_POCKET_MAJOR_RADIUS
            if sign > 0
            else -half_x - 0.3
        )
        channel_max_x = (
            half_x + 0.3
            if sign > 0
            else pocket_x + PANEL_NUT_POCKET_MAJOR_RADIUS
        )
        channel = _box(
            channel_max_x - channel_min_x,
            PANEL_NUT_ENTRY_WIDTH,
            NUT_POCKET_HEIGHT,
            (channel_min_x + channel_max_x) / 2.0,
            pocket_y,
            NUT_POCKET_Z,
        )
    else:
        sign = 1.0 if edge == "north" else -1.0
        pocket_x = along
        pocket_y = sign * (half_y - inward_offset)
        hex_profile = RegularPolygon(
            radius=PANEL_NUT_POCKET_MAJOR_RADIUS,
            side_count=6,
            major_radius=True,
            rotation=30.0,
        )
        hex_pocket = extrude(hex_profile, amount=NUT_POCKET_HEIGHT).moved(
            Location((pocket_x, pocket_y, NUT_POCKET_Z))
        )
        channel_min_y = (
            pocket_y - PANEL_NUT_POCKET_MAJOR_RADIUS
            if sign > 0
            else -half_y - 0.3
        )
        channel_max_y = (
            half_y + 0.3
            if sign > 0
            else pocket_y + PANEL_NUT_POCKET_MAJOR_RADIUS
        )
        channel = _box(
            PANEL_NUT_ENTRY_WIDTH,
            channel_max_y - channel_min_y,
            NUT_POCKET_HEIGHT,
            pocket_x,
            (channel_min_y + channel_max_y) / 2.0,
            NUT_POCKET_Z,
        )

    screw_passage = _cylinder(
        PANEL_M3_CLEARANCE_DIAMETER / 2.0,
        NUT_POCKET_Z + 0.25,
        pocket_x,
        pocket_y,
        -0.1,
    )
    return [hex_pocket, channel, screw_passage]


def make_eight_panel_details(name: str):
    """Return one assembled-position panel body and four exact dark tiles."""

    spec = EIGHT_PANEL_SPECS[name]
    edge_plan = panel_edge_plan(name)
    body = _box(
        PANEL_WIDTH,
        PANEL_HEIGHT,
        PANEL_BASE_THICKNESS,
        0.0,
        0.0,
        0.0,
    )
    body = _chamfer_bottom_edges(body, 0.0)

    light_caps = []
    dark_exact = []
    x_centers = (-SQUARE_SIZE / 2.0, SQUARE_SIZE / 2.0)
    y_centers = (-90.0, -30.0, 30.0, 90.0)
    global_rank_start = 0 if spec.row == "south" else 4
    global_file_start = 2 * spec.column_index
    for file_index, center_x in enumerate(x_centers):
        for rank_index, center_y in enumerate(y_centers):
            global_file = global_file_start + file_index
            global_rank = global_rank_start + rank_index
            is_dark = (global_file + global_rank) % 2 == 0
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
    checker_vertex_cutters = [
        _box(
            CHECKER_VERTEX_RELIEF_SIZE,
            CHECKER_VERTEX_RELIEF_SIZE,
            FACE_INLAY_THICKNESS + 2.0 * CHECKER_VERTEX_RELIEF_OVERSHOOT,
            0.0,
            center_y,
            PANEL_BASE_THICKNESS - CHECKER_VERTEX_RELIEF_OVERSHOOT,
        )
        for center_y in (-SQUARE_SIZE, 0.0, SQUARE_SIZE)
    ]
    body = _cut_many(body, checker_vertex_cutters)
    groove_cutters = []
    for edge, connection in edge_plan.items():
        negative_margin, positive_margin = _edge_end_margins(
            spec, edge, connection
        )
        if connection == "male":
            body = body.fuse(
                _rect_edge_feature(
                    edge,
                    male=True,
                    negative_margin=negative_margin,
                    positive_margin=positive_margin,
                )
            ).clean()
            for along in _anti_lip_positions(edge):
                body = body.fuse(
                    _rect_anti_lip_feature(edge, along, male=True)
                ).clean()
        elif connection == "female":
            groove_cutters.append(
                _rect_edge_feature(
                    edge,
                    male=False,
                    negative_margin=negative_margin,
                    positive_margin=positive_margin,
                )
            )
            for along in _anti_lip_positions(edge):
                groove_cutters.append(
                    _rect_anti_lip_feature(edge, along, male=False)
                )
        else:
            groove_cutters.append(
                _rect_edge_feature(
                    edge,
                    male=False,
                    negative_margin=negative_margin,
                    positive_margin=positive_margin,
                )
            )

    nut_cutters = []
    for edge, connection in edge_plan.items():
        inward_offset = (
            RAIL_SCREW_OFFSET if connection == "outer" else SEAM_SCREW_OFFSET
        )
        for along in _panel_nut_positions(edge):
            nut_cutters.extend(
                _rect_nut_trap_cutters(edge, along, inward_offset)
            )

    body = _cut_many(body, [*groove_cutters, *nut_cutters])
    body = _chamfer_panel_fit_openings(body, edge_plan)
    body = label_shape(body, "playing_panel_body", name, color=LIGHT_COLOR)

    dark_tiles = [
        label_shape(tile, "dark_square", name, index, color=DARK_COLOR)
        for index, tile in enumerate(dark_exact, start=1)
    ]
    dark_compound = Compound(
        children=dark_tiles,
        label=f"dark_square_inlays:{name}",
        color=DARK_COLOR,
    )
    return {
        "spec": spec,
        "edge_plan": edge_plan,
        "light_body": body,
        "dark_inlays": dark_compound,
    }


def make_eight_panel_body_for_print(name: str):
    body = make_eight_panel_details(name)["light_body"]
    bounds = body.bounding_box()
    center_x = (bounds.min.X + bounds.max.X) / 2.0
    center_y = (bounds.min.Y + bounds.max.Y) / 2.0

    # Bake the local centering translation into the standalone part geometry.
    # A non-identity TopLoc_Location exports as an unnamed top-level XCAF
    # occurrence (for example ``=>[0:1:1:2]``), which Bambu Studio then uses
    # as the object name instead of the useful part name below.
    body = body.transformed(offset=(-center_x, -center_y, 0.0))
    return label_shape(body, f"panel_{name}_light_body", color=LIGHT_COLOR)


def make_eight_panel_chessboard_assembly():
    """Build the complete board with eight playing panels and sixteen bridges."""

    assembly = AssemblyHelper("fide_60mm_eight_panel_chessboard_x2d")
    for name in EIGHT_PANEL_ROLES:
        details = make_eight_panel_details(name)
        location = panel_assembly_location(name)
        assembly.add_module(
            f"panel_{name}",
            [
                details["light_body"].moved(location),
                details["dark_inlays"].moved(location),
            ],
        )

    for name in RAIL_SPECS:
        details = make_rail_details(name)
        assembly.add_module(
            f"rail_{name}",
            [details["body"], details["notation_inlays"]],
        )

    for role, location in _corner_placements().items():
        assembly.add(
            make_corner_cap().moved(location),
            "corner_cap",
            role,
            color=PERIMETER_COLOR,
        )

    for seam_x in (-120.0, 0.0, 120.0):
        for y_position in (-180.0, -60.0, 60.0, 180.0):
            assembly.add(
                make_seam_bridge().moved(Location((seam_x, y_position, 0.0))),
                "vertical_seam_bridge",
                int(seam_x),
                int(y_position),
                color=PERIMETER_COLOR,
            )
    for x_position in (-180.0, -60.0, 60.0, 180.0):
        assembly.add(
            make_seam_bridge().moved(
                Location((x_position, 0.0, 0.0), (0.0, 0.0, 90.0))
            ),
            "horizontal_seam_bridge",
            int(x_position),
            color=PERIMETER_COLOR,
        )

    return assembly.build()


__all__ = [
    "EIGHT_PANEL_ROLES",
    "EIGHT_PANEL_SPECS",
    "PANEL_HEIGHT",
    "PANEL_M3_CLEARANCE_DIAMETER",
    "PANEL_NUT_ENTRY_WIDTH",
    "PANEL_NUT_POCKET_ACROSS_FLATS",
    "CHECKER_VERTEX_RELIEF_SIZE",
    "PANEL_WIDTH",
    "make_eight_panel_body_for_print",
    "make_eight_panel_chessboard_assembly",
    "make_eight_panel_details",
    "panel_assembly_location",
    "panel_edge_plan",
]
