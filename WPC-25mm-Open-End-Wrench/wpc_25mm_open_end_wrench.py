"""Parametric two-piece, two-color 25 mm open-end wrench for FDM prototyping.

Coordinate convention:
- XY is the wrench profile.
- +Z is the 15 mm extrusion direction.
- The nominal bolt center is at XY=(0, 0).
- The jaw opens toward +X and the handle extends toward -X.
- Z=0..5 mm is the secondary-color build-plate layer.
"""

from __future__ import annotations

from build123d import (
    Align,
    Box,
    BuildSketch,
    Circle,
    Color,
    Compound,
    FontStyle,
    Kind,
    Location,
    Locations,
    Mode,
    Plane,
    Polygon,
    Rectangle,
    Text,
    add,
    extrude,
    fillet,
    make_hull,
    offset,
)
from cadpy.assembly import AssemblyHelper


# User-controlled dimensions.
NOMINAL_FASTENER_AF = 25.0
JAW_CLEARANCE = 0.4
JAW_OPENING = NOMINAL_FASTENER_AF + JAW_CLEARANCE
PROFILE_DEPTH = 15.0
HANDLE_LENGTH = 4.0 * 25.4

# Head and jaw geometry.
HEAD_RADIUS = 27.0
HEAD_REAR_DATUM_X = -HEAD_RADIUS
JAW_THROAT_X = -2.0
JAW_PARALLEL_LENGTH = 30.0
JAW_TIP_CENTER_Y = 18.0
JAW_TIP_RADIUS = 9.0
JAW_MOUTH_X = JAW_THROAT_X + JAW_PARALLEL_LENGTH
JAW_TIP_CENTER_X = JAW_MOUTH_X - JAW_TIP_RADIUS
JAW_CUT_END_X = JAW_MOUTH_X + 5.0

# Strength-oriented neck and ergonomic handle geometry.
NECK_CENTER_X = -24.0
NECK_HALF_WIDTH = 14.0
FOREGRIP_CENTER_X = -45.0
FOREGRIP_HALF_WIDTH = 15.0
PALM_CENTER_X = -80.0
PALM_HALF_WIDTH = 18.0
HANDLE_END_X = HEAD_REAR_DATUM_X - HANDLE_LENGTH
HANDLE_END_RADIUS = 14.0
HANDLE_END_CENTER_X = HANDLE_END_X + HANDLE_END_RADIUS
FINGER_CONTOUR_RADIUS = 210.0
HANDLE_MIDPOINT_X = (HANDLE_END_X + HEAD_REAR_DATUM_X) / 2.0
FINGER_CONTOUR_CENTER_X = HANDLE_MIDPOINT_X
FINGER_CONTOUR_CENTER_Y = -224.0
EXTERNAL_EDGE_FILLET = 2.0
EDGE_CLASSIFICATION_TOLERANCE = 1e-5

# Two-piece split, single sliding dovetail, and slicer-ready print layout.
SPLIT_X = -64.0
CONNECTOR_LENGTH = 12.0
DOVETAIL_NECK_WIDTH = 10.0
DOVETAIL_TAIL_WIDTH = 18.0
CONNECTOR_CLEARANCE = 0.25
CONNECTOR_ROOT_OVERLAP = 0.5
PRINT_LAYOUT_HANDLE_OFFSET_Y = 50.0
PRINT_LAYOUT_MINIMUM_GAP = 5.0

# Two-color split and photo-inspired logo inlay.
SECONDARY_LAYER_THICKNESS = 5.0
LOGO_INLAY_DEPTH = 0.8
LOGO_NECK_SEARCH_MIN_X = -60.0
LOGO_NECK_SEARCH_MAX_X = HEAD_REAR_DATUM_X
LOGO_CENTER_X = -49.7
LOGO_CENTER_Y = 0.0
LOGO_OUTER_RADIUS = 12.5
LOGO_OUTER_RING_WIDTH = 0.60
LOGO_INNER_RING_RADIUS = 8.70
LOGO_INNER_RING_WIDTH = 0.50
LOGO_TEXT = "WPC"
LOGO_TEXT_SIZE = 6.0
LOGO_FONT_STYLE = FontStyle.BOLD
LOGO_EDGE_CLEARANCE = 1.0
BOOLEAN_OVERSHOOT = 0.2

PRIMARY_COLOR = Color(0.18, 0.22, 0.28)
SECONDARY_COLOR = Color(0.95, 0.55, 0.08)
SERIF_FONT = "DejaVu Serif"


def _head_profile():
    """Convex, rounded head with robust material around both jaw tips."""
    with BuildSketch() as head:
        Circle(HEAD_RADIUS)
        with Locations(
            (JAW_TIP_CENTER_X, JAW_TIP_CENTER_Y),
            (JAW_TIP_CENTER_X, -JAW_TIP_CENTER_Y),
        ):
            Circle(JAW_TIP_RADIUS)
        make_hull()
    return head.sketch


def _handle_profile():
    """Tangent-hulled grip with one shallow continuous finger curve."""
    with BuildSketch() as handle:
        with Locations((NECK_CENTER_X, 0.0)):
            Circle(NECK_HALF_WIDTH)
        with Locations((FOREGRIP_CENTER_X, 0.0)):
            Circle(FOREGRIP_HALF_WIDTH)
        with Locations((PALM_CENTER_X, 0.0)):
            Circle(PALM_HALF_WIDTH)
        with Locations((HANDLE_END_CENTER_X, 0.0)):
            Circle(HANDLE_END_RADIUS)
        make_hull()

        # A large-radius cutter makes one subtle ergonomic concavity.
        with Locations((FINGER_CONTOUR_CENTER_X, FINGER_CONTOUR_CENTER_Y)):
            Circle(FINGER_CONTOUR_RADIUS, mode=Mode.SUBTRACT)
    return handle.sketch


def _jaw_cutter_profile():
    """Parallel-flat jaw opening with a semicircular, low-stress throat."""
    with BuildSketch() as jaw:
        with Locations((JAW_THROAT_X, 0.0)):
            Circle(JAW_OPENING / 2.0)
            Rectangle(
                JAW_CUT_END_X - JAW_THROAT_X,
                JAW_OPENING,
                align=(Align.MIN, Align.CENTER),
            )
    return jaw.sketch


def _unfilleted_body():
    head = _head_profile()
    handle = _handle_profile()
    jaw = _jaw_cutter_profile()

    with BuildSketch() as profile:
        add(head)
        add(handle)
        add(jaw, mode=Mode.SUBTRACT)

    body = extrude(profile.sketch, amount=PROFILE_DEPTH)
    body.label = "wpc_25mm_open_end_wrench_blank"
    return body


def _is_jaw_inlet_edge(edge, body_max_x: float):
    """Protect the jaw flats, throat, and complete open tip faces from fillets."""
    bounds = edge.bounding_box()
    tolerance = EDGE_CLASSIFICATION_TOLERANCE
    jaw_half_gap = JAW_OPENING / 2.0

    on_upper_flat = (
        bounds.min.X >= JAW_THROAT_X - tolerance
        and abs(bounds.min.Y - jaw_half_gap) <= tolerance
        and abs(bounds.max.Y - jaw_half_gap) <= tolerance
    )
    on_lower_flat = (
        bounds.min.X >= JAW_THROAT_X - tolerance
        and abs(bounds.min.Y + jaw_half_gap) <= tolerance
        and abs(bounds.max.Y + jaw_half_gap) <= tolerance
    )
    on_throat = (
        edge.geom_type.name == "CIRCLE"
        and abs(bounds.min.X - (JAW_THROAT_X - jaw_half_gap)) <= tolerance
        and abs(bounds.max.X - JAW_THROAT_X) <= tolerance
        and abs(bounds.min.Y + jaw_half_gap) <= tolerance
        and abs(bounds.max.Y - jaw_half_gap) <= tolerance
    )
    on_open_tip = (
        abs(bounds.min.X - body_max_x) <= tolerance
        and abs(bounds.max.X - body_max_x) <= tolerance
    )
    return on_upper_flat or on_lower_flat or on_throat or on_open_tip


def _round_external_edges(body):
    """Round every exposed sharp edge except the bolt-entry interface."""
    body_max_x = body.bounding_box().max.X
    selected = [
        edge
        for edge in body.edges()
        if not _is_jaw_inlet_edge(edge, body_max_x)
    ]

    if not selected:
        raise RuntimeError("No external edges were found for comfort fillets")
    rounded = fillet(selected, radius=EXTERNAL_EDGE_FILLET)
    rounded.label = body.label
    return rounded


def _logo_profile():
    """Simplified bold WPC monogram retained inside two concentric rings."""
    with BuildSketch(Plane.XY) as logo:
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y)):
            Circle(LOGO_OUTER_RADIUS)
            Circle(LOGO_OUTER_RADIUS - LOGO_OUTER_RING_WIDTH, mode=Mode.SUBTRACT)
            Circle(LOGO_INNER_RING_RADIUS)
            Circle(LOGO_INNER_RING_RADIUS - LOGO_INNER_RING_WIDTH, mode=Mode.SUBTRACT)
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y)):
            Text(
                LOGO_TEXT,
                font_size=LOGO_TEXT_SIZE,
                font=SERIF_FONT,
                font_style=LOGO_FONT_STYLE,
            )
    return logo.sketch


def _x_slice_box(x_min: float, x_max: float):
    """Oversized box spanning an X partition and the complete wrench depth."""
    return Box(
        x_max - x_min,
        100.0,
        PROFILE_DEPTH + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(
        Location(
            (
                (x_min + x_max) / 2.0,
                0.0,
                PROFILE_DEPTH / 2.0,
            )
        )
    )


def _dovetail_connector(clearance: float = 0.0, through_cutter: bool = False):
    """Single plan-view dovetail, narrow at the jaw and flared in the handle."""
    root_x = SPLIT_X + CONNECTOR_ROOT_OVERLAP
    tail_x = SPLIT_X - CONNECTOR_LENGTH
    neck_half_width = DOVETAIL_NECK_WIDTH / 2.0
    tail_half_width = DOVETAIL_TAIL_WIDTH / 2.0

    with BuildSketch(Plane.XY) as dovetail:
        Polygon(
            (root_x, -neck_half_width),
            (root_x, neck_half_width),
            (tail_x, tail_half_width),
            (tail_x, -tail_half_width),
        )
        if clearance > 0.0:
            offset(amount=clearance, kind=Kind.INTERSECTION)
    z_min = -BOOLEAN_OVERSHOOT if through_cutter else 0.0
    z_max = (
        PROFILE_DEPTH + BOOLEAN_OVERSHOOT
        if through_cutter
        else PROFILE_DEPTH
    )
    connector = extrude(dovetail.sketch, amount=z_max - z_min).moved(
        Location((0.0, 0.0, z_min))
    )
    return _single_solid(connector, "dovetail connector")


def _split_mechanical_body(full_body):
    """Create two mating solids with one male dovetail on the jaw section."""
    jaw_partition = _single_solid(
        full_body.intersect(_x_slice_box(SPLIT_X, JAW_MOUTH_X + 10.0)),
        "jaw partition",
    )
    handle_partition = _single_solid(
        full_body.intersect(_x_slice_box(HANDLE_END_X - 10.0, SPLIT_X)),
        "handle partition",
    )
    male_connector = _dovetail_connector()
    female_cutter = _dovetail_connector(
        CONNECTOR_CLEARANCE,
        through_cutter=True,
    )
    jaw_piece = _single_solid(
        jaw_partition.fuse(male_connector),
        "jaw piece with male connector",
    )
    handle_piece = _single_solid(
        handle_partition.cut(female_cutter),
        "handle piece with female connector",
    )
    jaw_piece.label = "jaw_piece_mechanical_body"
    handle_piece.label = "handle_piece_mechanical_body"
    male_connector.label = "male_single_dovetail"
    female_cutter.label = "female_single_dovetail_socket_clearance"
    return jaw_piece, handle_piece, male_connector, female_cutter


def _slice_box(z_min: float, z_max: float):
    """Oversized centered box spanning the requested Z interval."""
    return Box(220.0, 100.0, z_max - z_min).moved(
        Location((-45.0, 0.0, (z_min + z_max) / 2.0))
    )


def _labeled_logo_compound(logo_intersection):
    logo_solids = list(logo_intersection.solids())
    if not logo_solids:
        raise RuntimeError("Logo profile did not intersect the jaw-side neck")
    for index, solid in enumerate(logo_solids, start=1):
        solid.label = f"logo_inlay_{index:02d}"
        solid.color = SECONDARY_COLOR
    return Compound(
        children=logo_solids,
        label="bold_wpc_two_circle_logo_inlay",
        color=SECONDARY_COLOR,
    )


def _single_solid(shape_or_shapes, feature_name: str):
    solids = list(shape_or_shapes.solids())
    if len(solids) != 1:
        raise RuntimeError(
            f"{feature_name} expected one solid but produced {len(solids)}"
        )
    return solids[0]


def build_wrench_details():
    """Return two keyed mechanical pieces with labeled multi-color bodies."""
    full_body = _round_external_edges(_unfilleted_body())
    jaw_piece, handle_piece, male_connector, female_cutter = (
        _split_mechanical_body(full_body)
    )

    jaw_secondary_layer = _single_solid(
        jaw_piece.intersect(
            _slice_box(-BOOLEAN_OVERSHOOT, SECONDARY_LAYER_THICKNESS)
        ),
        "jaw secondary layer",
    )
    jaw_primary_blank = _single_solid(
        jaw_piece.intersect(
            _slice_box(SECONDARY_LAYER_THICKNESS, PROFILE_DEPTH + BOOLEAN_OVERSHOOT)
        ),
        "jaw primary layer",
    )
    handle_secondary_layer = _single_solid(
        handle_piece.intersect(
            _slice_box(-BOOLEAN_OVERSHOOT, SECONDARY_LAYER_THICKNESS)
        ),
        "handle secondary layer",
    )
    handle_primary_body = _single_solid(
        handle_piece.intersect(
            _slice_box(SECONDARY_LAYER_THICKNESS, PROFILE_DEPTH + BOOLEAN_OVERSHOOT)
        ),
        "handle primary layer",
    )

    logo_prism = extrude(
        _logo_profile(),
        amount=LOGO_INLAY_DEPTH + BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, PROFILE_DEPTH - LOGO_INLAY_DEPTH)))
    logo_intersection = jaw_primary_blank.intersect(logo_prism)
    jaw_primary_body = _single_solid(
        jaw_primary_blank.cut(logo_prism),
        "jaw primary logo pocket",
    )

    jaw_primary_body.label = "jaw_piece_primary_body"
    jaw_primary_body.color = PRIMARY_COLOR
    jaw_secondary_layer.label = "jaw_piece_secondary_5mm_layer"
    jaw_secondary_layer.color = SECONDARY_COLOR
    handle_primary_body.label = "handle_piece_primary_body"
    handle_primary_body.color = PRIMARY_COLOR
    handle_secondary_layer.label = "handle_piece_secondary_5mm_layer"
    handle_secondary_layer.color = SECONDARY_COLOR
    logo_inlay = _labeled_logo_compound(logo_intersection)

    # Export the two modules in a print layout rather than their mated pose.
    # Both remain broad-face-down at Z=0; the handle moves only in +Y.
    handle_layout_location = Location((0.0, PRINT_LAYOUT_HANDLE_OFFSET_Y, 0.0))
    handle_primary_layout = handle_primary_body.moved(handle_layout_location)
    handle_secondary_layout = handle_secondary_layer.moved(handle_layout_location)
    handle_primary_layout.label = "handle_piece_primary_body"
    handle_primary_layout.color = PRIMARY_COLOR
    handle_secondary_layout.label = "handle_piece_secondary_5mm_layer"
    handle_secondary_layout.color = SECONDARY_COLOR

    assembly = AssemblyHelper("wpc_25mm_open_end_wrench_two_object_print_layout")
    jaw_module = assembly.add_module(
        "jaw_piece",
        [jaw_primary_body, jaw_secondary_layer, logo_inlay],
    )
    handle_module = assembly.add_module(
        "handle_piece",
        [handle_primary_layout, handle_secondary_layout],
    )
    final = assembly.build()

    return {
        "final": final,
        "full_body": full_body,
        "jaw_piece": jaw_piece,
        "handle_piece": handle_piece,
        "male_connector": male_connector,
        "female_cutter": female_cutter,
        "jaw_primary_body": jaw_primary_body,
        "jaw_secondary_layer": jaw_secondary_layer,
        "handle_primary_body": handle_primary_body,
        "handle_secondary_layer": handle_secondary_layer,
        "handle_primary_layout": handle_primary_layout,
        "handle_secondary_layout": handle_secondary_layout,
        "logo_inlay": logo_inlay,
        "logo_prism": logo_prism,
        "jaw_module": jaw_module,
        "handle_module": handle_module,
    }


def gen_step():
    return build_wrench_details()["final"]
