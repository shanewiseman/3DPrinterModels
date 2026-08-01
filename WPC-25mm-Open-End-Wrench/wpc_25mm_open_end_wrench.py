"""Parametric two-color 25 mm open-end wrench for FDM prototyping.

Coordinate convention:
- XY is the wrench profile.
- +Z is the 25 mm extrusion direction.
- The nominal bolt center is at XY=(0, 0).
- The jaw opens toward +X and the handle extends toward -X.
- Z=0..5 mm is the secondary-color build-plate layer.
"""

from __future__ import annotations

from math import cos, radians, sin

from build123d import (
    Align,
    Box,
    BuildSketch,
    Circle,
    Color,
    Compound,
    FontStyle,
    Location,
    Locations,
    Mode,
    Plane,
    Rectangle,
    Text,
    add,
    extrude,
    fillet,
    make_hull,
)


# User-controlled dimensions.
NOMINAL_FASTENER_AF = 25.0
JAW_CLEARANCE = 0.4
JAW_OPENING = NOMINAL_FASTENER_AF + JAW_CLEARANCE
PROFILE_DEPTH = 25.0
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

# Two-color split and photo-inspired logo inlay.
SECONDARY_LAYER_THICKNESS = 5.0
LOGO_INLAY_DEPTH = 0.8
LOGO_NECK_SEARCH_MIN_X = -60.0
LOGO_NECK_SEARCH_MAX_X = HEAD_REAR_DATUM_X
LOGO_CENTER_X = -49.7
LOGO_CENTER_Y = 0.0
LOGO_REFERENCE_OUTER_RADIUS = 15.5
LOGO_OUTER_RADIUS = 12.5
LOGO_SCALE = LOGO_OUTER_RADIUS / LOGO_REFERENCE_OUTER_RADIUS
LOGO_OUTER_RING_WIDTH = 0.75 * LOGO_SCALE
LOGO_INNER_RING_RADIUS = 10.8 * LOGO_SCALE
LOGO_INNER_RING_WIDTH = 0.60 * LOGO_SCALE
LOGO_TOP_TEXT_RADIUS = 13.25 * LOGO_SCALE
LOGO_BOTTOM_TEXT_RADIUS = 13.15 * LOGO_SCALE
LOGO_EDGE_CLEARANCE = 1.0
BOOLEAN_OVERSHOOT = 0.2

PRIMARY_COLOR = Color(0.18, 0.22, 0.28)
SECONDARY_COLOR = Color(0.95, 0.55, 0.08)
SERIF_FONT = "DejaVu Serif"
SANS_FONT = "DejaVu Sans"


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


def _arc_text(
    text: str,
    radius: float,
    start_angle: float,
    end_angle: float,
    font_size: float,
    bottom_arc: bool = False,
):
    """Add individually rotated characters to the active BuildSketch."""
    if len(text) < 2:
        angles = [start_angle]
    else:
        angles = [
            start_angle + (end_angle - start_angle) * index / (len(text) - 1)
            for index in range(len(text))
        ]

    for character, angle in zip(text, angles):
        if character == " ":
            continue
        x = LOGO_CENTER_X + radius * cos(radians(angle))
        y = LOGO_CENTER_Y + radius * sin(radians(angle))
        rotation = angle + 90.0 if bottom_arc else angle - 90.0
        with Locations((x, y)):
            Text(
                character,
                font_size=font_size,
                font=SERIF_FONT,
                font_style=FontStyle.BOLD,
                rotation=rotation,
            )


def _logo_profile():
    """Printable vector interpretation of the supplied Wiseman logo image."""
    with BuildSketch(Plane.XY) as logo:
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y)):
            Circle(LOGO_OUTER_RADIUS)
            Circle(LOGO_OUTER_RADIUS - LOGO_OUTER_RING_WIDTH, mode=Mode.SUBTRACT)
            Circle(LOGO_INNER_RING_RADIUS)
            Circle(LOGO_INNER_RING_RADIUS - LOGO_INNER_RING_WIDTH, mode=Mode.SUBTRACT)

        _arc_text(
            "WISEMAN PRECISION",
            LOGO_TOP_TEXT_RADIUS,
            156.0,
            24.0,
            2.15 * LOGO_SCALE,
        )
        _arc_text(
            "CARTRIDGES",
            LOGO_BOTTOM_TEXT_RADIUS,
            204.0,
            336.0,
            2.05 * LOGO_SCALE,
            bottom_arc=True,
        )

        # Separator dots from the reference artwork.
        for angle in (192.0, 348.0):
            with Locations(
                (
                    LOGO_CENTER_X + LOGO_TOP_TEXT_RADIUS * cos(radians(angle)),
                    LOGO_CENTER_Y + LOGO_TOP_TEXT_RADIUS * sin(radians(angle)),
                )
            ):
                Circle(0.55 * LOGO_SCALE)

        # Central stacked monogram and compact location/established details.
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y + 3.7 * LOGO_SCALE)):
            Text(
                "W",
                font_size=8.0 * LOGO_SCALE,
                font=SERIF_FONT,
                font_style=FontStyle.BOLD,
            )
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y - 1.0 * LOGO_SCALE)):
            Text(
                "PC",
                font_size=6.2 * LOGO_SCALE,
                font=SERIF_FONT,
            )
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y - 5.2 * LOGO_SCALE)):
            Text(
                "ACTON, MA",
                font_size=1.35 * LOGO_SCALE,
                font=SANS_FONT,
                font_style=FontStyle.BOLD,
            )
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y - 6.4 * LOGO_SCALE)):
            Rectangle(11.5 * LOGO_SCALE, 0.30 * LOGO_SCALE)
        with Locations((LOGO_CENTER_X, LOGO_CENTER_Y - 7.6 * LOGO_SCALE)):
            Text(
                "EST. 2026",
                font_size=1.25 * LOGO_SCALE,
                font=SANS_FONT,
                font_style=FontStyle.BOLD,
            )
    return logo.sketch


def _slice_box(z_min: float, z_max: float):
    """Oversized centered box spanning the requested Z interval."""
    return Box(220.0, 100.0, z_max - z_min).moved(
        Location((-45.0, 0.0, (z_min + z_max) / 2.0))
    )


def _labeled_logo_compound(logo_intersection):
    logo_solids = list(logo_intersection.solids())
    if not logo_solids:
        raise RuntimeError("Logo profile did not intersect the wrench palm")
    for index, solid in enumerate(logo_solids, start=1):
        solid.label = f"logo_inlay_{index:02d}"
        solid.color = SECONDARY_COLOR
    return Compound(
        children=logo_solids,
        label="wiseman_precision_logo_inlay",
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
    """Return the labeled color bodies plus validation intermediates."""
    full_body = _round_external_edges(_unfilleted_body())

    secondary_layer = _single_solid(
        full_body.intersect(
            _slice_box(-BOOLEAN_OVERSHOOT, SECONDARY_LAYER_THICKNESS)
        ),
        "secondary layer",
    )
    primary_blank = _single_solid(
        full_body.intersect(
            _slice_box(SECONDARY_LAYER_THICKNESS, PROFILE_DEPTH + BOOLEAN_OVERSHOOT)
        ),
        "primary layer",
    )

    logo_prism = extrude(
        _logo_profile(),
        amount=LOGO_INLAY_DEPTH + BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, PROFILE_DEPTH - LOGO_INLAY_DEPTH)))
    logo_intersection = primary_blank.intersect(logo_prism)
    primary_body = _single_solid(primary_blank.cut(logo_prism), "primary logo pocket")

    primary_body.label = "primary_wrench_body"
    primary_body.color = PRIMARY_COLOR
    secondary_layer.label = "secondary_5mm_surface_layer"
    secondary_layer.color = SECONDARY_COLOR
    logo_inlay = _labeled_logo_compound(logo_intersection)

    final = Compound(
        children=[primary_body, secondary_layer, logo_inlay],
        label="wpc_25mm_open_end_wrench_two_color",
    )

    return {
        "final": final,
        "full_body": full_body,
        "primary_body": primary_body,
        "secondary_layer": secondary_layer,
        "logo_inlay": logo_inlay,
        "logo_prism": logo_prism,
    }


def gen_step():
    return build_wrench_details()["final"]
