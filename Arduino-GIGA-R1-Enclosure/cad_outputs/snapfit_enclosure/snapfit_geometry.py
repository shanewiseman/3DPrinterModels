"""Shared source geometry for the Arduino GIGA R1 snap-fit enclosure."""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Color,
    Compound,
    Location,
    Plane,
    Polygon,
    Solid,
    Text,
    extrude,
    import_step,
)


MODEL_DIR = Path(__file__).resolve().parent
BASE_SOURCE = MODEL_DIR / "arduino_giga_r1_enclosure_base_original.step"
LID_SOURCE = MODEL_DIR / "arduino_giga_r1_enclosure_lid_wall_removed_original.step"

# Imported mating envelope in the original assembled coordinates.
BASE_X_MAX = 56.0
BASE_Y_MIN = -30.67
BASE_Y_MAX = 30.67
BASE_ORIGINAL_WALL_THICKNESS = 2.2
BASE_INNER_X_MAX = BASE_X_MAX - BASE_ORIGINAL_WALL_THICKNESS
BASE_INNER_Y_MIN = BASE_Y_MIN + BASE_ORIGINAL_WALL_THICKNESS
BASE_INNER_Y_MAX = BASE_Y_MAX - BASE_ORIGINAL_WALL_THICKNESS
LID_INNER_X_MAX = 56.4
LID_INNER_Y_MIN = -31.07
LID_INNER_Y_MAX = 31.07

# Match the lid's main top thickness to the verified 2.2 mm base floor while
# preserving the lid underside and every mating/snap datum.
BASE_BOTTOM_THICKNESS = 2.2
ORIGINAL_LID_TOP_Z_MIN = 19.4
ORIGINAL_LID_TOP_Z_MAX = 20.0
ORIGINAL_LID_TOP_THICKNESS = ORIGINAL_LID_TOP_Z_MAX - ORIGINAL_LID_TOP_Z_MIN
LID_TOP_THICKNESS = BASE_BOTTOM_THICKNESS
LID_TOP_THICKENING = LID_TOP_THICKNESS - ORIGINAL_LID_TOP_THICKNESS
LID_EXTERIOR_FACE_Z = ORIGINAL_LID_TOP_Z_MAX + LID_TOP_THICKENING
GEOMETRY_TOLERANCE = 1e-6

# Snap feature locations: rear is the complete X-max short wall. Matching
# long-wall pairs are placed on both Y-min and Y-max sides.
REAR_TAB_Y_CENTERS = (-15.0, 15.0)
FRONT_TAB_X_CENTERS = (-30.0, 30.0)
OPPOSITE_SIDE_TAB_X_CENTERS = FRONT_TAB_X_CENTERS

# Double the thickness of the three upper receiver rails inward, retaining the
# original outside envelope and every external lid/skirt clearance. The pocket
# reaches the midpoint of the new 4.4 mm rail, leaving a full 2.2 mm inner rib.
BASE_RECEIVER_RAIL_THICKNESS = BASE_ORIGINAL_WALL_THICKNESS * 2.0
BASE_RECEIVER_RAIL_EXTENSION = (
    BASE_RECEIVER_RAIL_THICKNESS - BASE_ORIGINAL_WALL_THICKNESS
)
BASE_WALL_Z_MAX = 18.0
RECEIVER_RAIL_Z_MIN = 15.6
RECEIVER_RAIL_Z_MAX = BASE_WALL_Z_MAX
RECEIVER_RAIL_POCKET_DEPTH = BASE_RECEIVER_RAIL_THICKNESS / 2.0

# Lid lug geometry. The triangular section creates a lead-in ramp and a flat
# retaining shoulder at TAB_Z_MAX. Lengthen its projection so the tip retains
# the existing 0.5 mm depth clearance to the new pocket's inner face.
TAB_WIDTH = 9.0
TAB_Z_MIN = 16.2
TAB_Z_MAX = 17.4
TAB_ROOT_OVERLAP = 0.1
LID_TO_BASE_SIDE_CLEARANCE = LID_INNER_X_MAX - BASE_X_MAX
TAB_DEPTH_CLEARANCE = 0.5
TAB_PROJECTION = (
    LID_TO_BASE_SIDE_CLEARANCE
    + RECEIVER_RAIL_POCKET_DEPTH
    - TAB_DEPTH_CLEARANCE
)
SNAP_ROOT_FILLET_RADIUS = 0.6
SNAP_ROOT_EDGE_Z_WINDOW = 0.2

# Base pockets are closed on all sides, with lateral and vertical clearance.
POCKET_WIDTH = 10.0
POCKET_Z_MIN = 16.0
POCKET_Z_MAX = 17.6
POCKET_OUTER_OVERSHOOT = 0.2
REAR_POCKET_INWARD_DEPTH = RECEIVER_RAIL_POCKET_DEPTH
FRONT_POCKET_INWARD_DEPTH = RECEIVER_RAIL_POCKET_DEPTH
OPPOSITE_SIDE_POCKET_INWARD_DEPTH = RECEIVER_RAIL_POCKET_DEPTH

# Flush second-color inlay on the outward lid face. The selected center occupies
# the uninterrupted top region between the existing lid cutouts.
LOGO_TEXT = "Giga R1"
LOGO_FONT_SIZE = 8.0
LOGO_CENTER_X = -5.0
LOGO_CENTER_Y = 0.0
LOGO_DEPTH = 0.4
LOGO_Z_MIN = LID_EXTERIOR_FACE_Z - LOGO_DEPTH
LOGO_CUTTER_OVERSHOOT = 0.2
LID_BODY_COLOR = Color(0.12, 0.48, 0.72)
LOGO_COLOR = Color(0.96, 0.96, 0.92)

# GPIO access-slot registration from Arduino's ABX00063 PCB.PcbDoc. The board
# outline origin below is the lower-left corner of the 4000 x 2100 mil nominal
# board envelope. The lid/enclosure XY origin is the board-envelope center.
MM_PER_MIL = 0.0254
GIGA_BOARD_X_MIN_MIL = 1590.5507
GIGA_BOARD_Y_MIN_MIL = 1590.5507
GIGA_BOARD_CENTER_X_MM = 50.8
GIGA_BOARD_CENTER_Y_MM = 26.67

# Each custom through-hole socket body is nominally 2.54 mm beyond the outside
# pin centers (1.27 mm at each end). Add 1.5 mm access/print clearance around
# that body envelope so no lid material overhangs a socket opening.
GPIO_HEADER_BODY_OVERHANG = 1.27
GPIO_ACCESS_CLEARANCE = 1.5
GPIO_FACING_EDGE_CLEARANCE = 1.0
GPIO_SLOT_CORNER_RADIUS = 1.5
GPIO_MINIMUM_WEB = 3.0
GPIO_ANALOG_REAR_ELBOW_OVERLAP = 3.0

# Absolute pad-center limits in the official Altium board coordinates (mils).
# JANALOG is the Y-min 1x24 row; JDIGITAL is the Y-max 1x26 row; JSIDE is the
# X-max 2x18 row carrying D22-D53.
ANALOG_PIN_X_MIL = (2691.5602, 5191.5603)
ANALOG_PIN_Y_MIL = 1691.0502
DIGITAL_PIN_X_MIL = (2331.5581, 4991.5581)
DIGITAL_PIN_Y_MIL = 3591.0493
REAR_PIN_X_MIL = (5290.5502, 5390.5502)
REAR_PIN_Y_MIL = (1890.4976, 3590.4976)

# Existing lid apertures are filled before the board-registered apertures are
# cut. These are exact bounds recovered from the source top face.
ORIGINAL_ANALOG_SLOT_BOUNDS = (-31.2, 48.8, -25.7, -20.3)
ORIGINAL_DIGITAL_SLOT_BOUNDS = (-30.2, 47.8, 20.3, 25.7)
GPIO_SLOT_FILL_OVERLAP = 0.05
GPIO_SLOT_CUT_OVERSHOOT = 0.1


def _board_x_mil_to_lid_mm(value: float) -> float:
    return (
        (value - GIGA_BOARD_X_MIN_MIL) * MM_PER_MIL
        - GIGA_BOARD_CENTER_X_MM
    )


def _board_y_mil_to_lid_mm(value: float) -> float:
    return (
        (value - GIGA_BOARD_Y_MIN_MIL) * MM_PER_MIL
        - GIGA_BOARD_CENTER_Y_MM
    )


def _slot_bounds_from_pin_span(
    x_pin_mil: tuple[float, float] | float,
    y_pin_mil: tuple[float, float] | float,
    x_min_clearance: float = GPIO_ACCESS_CLEARANCE,
    x_max_clearance: float = GPIO_ACCESS_CLEARANCE,
    y_min_clearance: float = GPIO_ACCESS_CLEARANCE,
    y_max_clearance: float = GPIO_ACCESS_CLEARANCE,
) -> tuple[float, float, float, float]:
    x_values = x_pin_mil if isinstance(x_pin_mil, tuple) else (x_pin_mil,) * 2
    y_values = y_pin_mil if isinstance(y_pin_mil, tuple) else (y_pin_mil,) * 2
    return (
        _board_x_mil_to_lid_mm(min(x_values))
        - GPIO_HEADER_BODY_OVERHANG
        - x_min_clearance,
        _board_x_mil_to_lid_mm(max(x_values))
        + GPIO_HEADER_BODY_OVERHANG
        + x_max_clearance,
        _board_y_mil_to_lid_mm(min(y_values))
        - GPIO_HEADER_BODY_OVERHANG
        - y_min_clearance,
        _board_y_mil_to_lid_mm(max(y_values))
        + GPIO_HEADER_BODY_OVERHANG
        + y_max_clearance,
    )


ANALOG_SLOT_BOUNDS = _slot_bounds_from_pin_span(ANALOG_PIN_X_MIL, ANALOG_PIN_Y_MIL)
DIGITAL_SLOT_BOUNDS = _slot_bounds_from_pin_span(
    DIGITAL_PIN_X_MIL,
    DIGITAL_PIN_Y_MIL,
    x_max_clearance=GPIO_FACING_EDGE_CLEARANCE,
)
_rear_slot_envelope = _slot_bounds_from_pin_span(
    REAR_PIN_X_MIL,
    REAR_PIN_Y_MIL,
    x_min_clearance=GPIO_FACING_EDGE_CLEARANCE,
)
REAR_SLOT_BOUNDS = (
    _rear_slot_envelope[0],
    _rear_slot_envelope[1],
    ANALOG_SLOT_BOUNDS[3] - GPIO_ANALOG_REAR_ELBOW_OVERLAP,
    _rear_slot_envelope[3],
)
GPIO_SLOT_BOUNDS = {
    "analog_ymin": ANALOG_SLOT_BOUNDS,
    "digital_ymax": DIGITAL_SLOT_BOUNDS,
    "d22_d53_rear_xmax": REAR_SLOT_BOUNDS,
}


def _load_single_solid(path: Path, expected_label: str) -> Solid:
    imported = import_step(path)
    solids = imported.solids()
    if len(solids) != 1:
        raise ValueError(f"Expected one solid in {path.name}, found {len(solids)}")
    solid = solids[0]
    if not solid.is_valid:
        raise ValueError(f"Imported solid is invalid: {path.name}")
    solid.label = expected_label
    return solid


def _rear_lug(y_center: float) -> Solid:
    root_x = LID_INNER_X_MAX + TAB_ROOT_OVERLAP
    tip_x = LID_INNER_X_MAX - TAB_PROJECTION
    profile = Plane.XZ * Polygon(
        (root_x, TAB_Z_MIN),
        (tip_x, TAB_Z_MAX),
        (root_x, TAB_Z_MAX),
    )
    lug = extrude(profile, amount=TAB_WIDTH / 2.0, both=True)
    return lug.moved(Location((0.0, y_center, 0.0)))


def _front_lug(x_center: float) -> Solid:
    root_y = LID_INNER_Y_MIN - TAB_ROOT_OVERLAP
    tip_y = LID_INNER_Y_MIN + TAB_PROJECTION
    profile = Plane.YZ * Polygon(
        (root_y, TAB_Z_MIN),
        (tip_y, TAB_Z_MAX),
        (root_y, TAB_Z_MAX),
    )
    lug = extrude(profile, amount=TAB_WIDTH / 2.0, both=True)
    return lug.moved(Location((x_center, 0.0, 0.0)))


def _opposite_side_lug(x_center: float) -> Solid:
    root_y = LID_INNER_Y_MAX + TAB_ROOT_OVERLAP
    tip_y = LID_INNER_Y_MAX - TAB_PROJECTION
    profile = Plane.YZ * Polygon(
        (root_y, TAB_Z_MIN),
        (tip_y, TAB_Z_MAX),
        (root_y, TAB_Z_MAX),
    )
    lug = extrude(profile, amount=TAB_WIDTH / 2.0, both=True)
    return lug.moved(Location((x_center, 0.0, 0.0)))


def _thicken_lid_top(lid: Solid) -> Solid:
    top_faces = []
    for face in lid.faces():
        bounds = face.bounding_box()
        if (
            abs(bounds.min.Z - ORIGINAL_LID_TOP_Z_MAX) <= GEOMETRY_TOLERANCE
            and abs(bounds.max.Z - ORIGINAL_LID_TOP_Z_MAX) <= GEOMETRY_TOLERANCE
        ):
            top_faces.append(face)
    if len(top_faces) != 1:
        raise ValueError(f"Expected one lid top face, found {len(top_faces)}")

    top_extension = extrude(
        top_faces[0],
        amount=LID_TOP_THICKENING,
        dir=(0.0, 0.0, 1.0),
    )
    thickened = lid.fuse(top_extension)
    if len(thickened.solids()) != 1 or not thickened.is_valid:
        raise ValueError("Lid top thickening did not produce one valid solid")
    return thickened


def _top_plate_box(
    bounds: tuple[float, float, float, float],
    xy_overlap: float,
    z_overshoot: float,
    corner_radius: float = 0.0,
) -> Solid:
    x_min, x_max, y_min, y_max = bounds
    prism = Box(
        x_max - x_min + 2.0 * xy_overlap,
        y_max - y_min + 2.0 * xy_overlap,
        LID_TOP_THICKNESS + 2.0 * z_overshoot,
        align=(Align.MIN, Align.MIN, Align.MIN),
    )
    if corner_radius > 0.0:
        vertical_edges = []
        for edge in prism.edges():
            edge_bounds = edge.bounding_box()
            if (
                abs(
                    edge_bounds.max.Z
                    - edge_bounds.min.Z
                    - (LID_TOP_THICKNESS + 2.0 * z_overshoot)
                )
                <= GEOMETRY_TOLERANCE
            ):
                vertical_edges.append(edge)
        if len(vertical_edges) != 4:
            raise ValueError(
                f"Expected four vertical GPIO-slot cutter edges, found "
                f"{len(vertical_edges)}"
            )
        prism = prism.fillet(corner_radius, vertical_edges)

    return prism.moved(
        Location(
            (
                x_min - xy_overlap,
                y_min - xy_overlap,
                ORIGINAL_LID_TOP_Z_MIN - z_overshoot,
            )
        )
    )


def _register_gpio_access_slots(lid: Solid) -> Solid:
    old_slot_fillers = [
        _top_plate_box(
            bounds,
            xy_overlap=GPIO_SLOT_FILL_OVERLAP,
            z_overshoot=0.0,
        )
        for bounds in (
            ORIGINAL_ANALOG_SLOT_BOUNDS,
            ORIGINAL_DIGITAL_SLOT_BOUNDS,
        )
    ]
    restored = lid.fuse(*old_slot_fillers)
    if len(restored.solids()) != 1 or not restored.is_valid:
        raise ValueError("GPIO slot restoration did not produce one valid solid")

    registered_cutters = [
        _top_plate_box(
            bounds,
            xy_overlap=0.0,
            z_overshoot=GPIO_SLOT_CUT_OVERSHOOT,
            corner_radius=GPIO_SLOT_CORNER_RADIUS,
        )
        for bounds in GPIO_SLOT_BOUNDS.values()
    ]
    registered = restored.cut(*registered_cutters)
    if len(registered.solids()) != 1 or not registered.is_valid:
        raise ValueError("GPIO slot registration did not produce one valid solid")
    return registered


def _fillet_snap_lug_roots(lid: Solid) -> Solid:
    root_edges = []
    for edge in lid.edges():
        bounds = edge.bounding_box()
        span_x = bounds.max.X - bounds.min.X
        span_y = bounds.max.Y - bounds.min.Y
        span_z = bounds.max.Z - bounds.min.Z
        is_width_edge = abs(edge.length - TAB_WIDTH) <= GEOMETRY_TOLERANCE
        is_root_height = (
            TAB_Z_MIN < bounds.min.Z < TAB_Z_MIN + SNAP_ROOT_EDGE_Z_WINDOW
            and span_z <= GEOMETRY_TOLERANCE
        )
        is_rear_root = (
            abs(bounds.min.X - LID_INNER_X_MAX) <= GEOMETRY_TOLERANCE
            and span_y >= TAB_WIDTH - GEOMETRY_TOLERANCE
        )
        is_side_root = (
            (
                abs(bounds.min.Y - LID_INNER_Y_MIN) <= GEOMETRY_TOLERANCE
                or abs(bounds.min.Y - LID_INNER_Y_MAX) <= GEOMETRY_TOLERANCE
            )
            and span_x >= TAB_WIDTH - GEOMETRY_TOLERANCE
        )
        if is_width_edge and is_root_height and (is_rear_root or is_side_root):
            root_edges.append(edge)

    if len(root_edges) != 6:
        raise ValueError(f"Expected six snap-lug root edges, found {len(root_edges)}")
    filleted = lid.fillet(SNAP_ROOT_FILLET_RADIUS, root_edges)
    if len(filleted.solids()) != 1 or not filleted.is_valid:
        raise ValueError("Snap-lug root filleting did not produce one valid solid")
    return filleted


def _make_logo_part(depth: float) -> Compound | Solid:
    text_profile = Text(LOGO_TEXT, font_size=LOGO_FONT_SIZE)
    return extrude(text_profile, amount=depth).moved(
        Location((LOGO_CENTER_X, LOGO_CENTER_Y, LOGO_Z_MIN))
    )


def _make_lid_snapfit_solid() -> Solid:
    lid = _load_single_solid(LID_SOURCE, "arduino_giga_r1_enclosure_lid_source")
    lid = _thicken_lid_top(lid)
    lid = _register_gpio_access_slots(lid)
    lugs = [*(_rear_lug(y) for y in REAR_TAB_Y_CENTERS)]
    lugs.extend(_front_lug(x) for x in FRONT_TAB_X_CENTERS)
    lugs.extend(_opposite_side_lug(x) for x in OPPOSITE_SIDE_TAB_X_CENTERS)
    revised = lid.fuse(*lugs)
    if len(revised.solids()) != 1 or not revised.is_valid:
        raise ValueError("Lid snap-lug fusion did not produce one valid solid")
    revised = _fillet_snap_lug_roots(revised)
    revised.label = "arduino_giga_r1_enclosure_lid_snapfit_body"
    return revised


def make_lid_snapfit_components() -> tuple[Solid, Compound]:
    lid = _make_lid_snapfit_solid()
    logo_insert = _make_logo_part(LOGO_DEPTH)
    logo_cutter = _make_logo_part(LOGO_DEPTH + LOGO_CUTTER_OVERSHOOT)
    lid_body = lid.cut(*logo_cutter.solids())
    if len(lid_body.solids()) != 1 or not lid_body.is_valid:
        raise ValueError("Logo recess did not produce one valid lid-body solid")

    lid_body.label = "lid_snapfit_body"
    lid_body.color = LID_BODY_COLOR
    logo_solids = []
    for index, solid in enumerate(logo_insert.solids(), start=1):
        solid.label = f"giga_r1_logo:{index}"
        solid.color = LOGO_COLOR
        logo_solids.append(solid)
    logo = Compound(children=logo_solids, label="giga_r1_logo")
    logo.color = LOGO_COLOR
    return lid_body, logo


def make_lid_snapfit() -> Compound:
    lid_body, logo = make_lid_snapfit_components()
    return Compound(
        children=[lid_body, logo],
        label="arduino_giga_r1_enclosure_lid_snapfit_two_color",
    )


def _rear_pocket(y_center: float) -> Solid:
    cutter_depth = REAR_POCKET_INWARD_DEPTH + POCKET_OUTER_OVERSHOOT
    cutter = Box(
        cutter_depth,
        POCKET_WIDTH,
        POCKET_Z_MAX - POCKET_Z_MIN,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    )
    return cutter.moved(
        Location(
            (
                BASE_X_MAX - REAR_POCKET_INWARD_DEPTH,
                y_center,
                POCKET_Z_MIN,
            )
        )
    )


def _front_pocket(x_center: float) -> Solid:
    cutter_depth = FRONT_POCKET_INWARD_DEPTH + POCKET_OUTER_OVERSHOOT
    cutter = Box(
        POCKET_WIDTH,
        cutter_depth,
        POCKET_Z_MAX - POCKET_Z_MIN,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    return cutter.moved(
        Location(
            (
                x_center,
                BASE_Y_MIN - POCKET_OUTER_OVERSHOOT,
                POCKET_Z_MIN,
            )
        )
    )


def _opposite_side_pocket(x_center: float) -> Solid:
    cutter_depth = OPPOSITE_SIDE_POCKET_INWARD_DEPTH + POCKET_OUTER_OVERSHOOT
    cutter = Box(
        POCKET_WIDTH,
        cutter_depth,
        POCKET_Z_MAX - POCKET_Z_MIN,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    return cutter.moved(
        Location(
            (
                x_center,
                BASE_Y_MAX - OPPOSITE_SIDE_POCKET_INWARD_DEPTH,
                POCKET_Z_MIN,
            )
        )
    )


def _receiver_rail_extensions() -> list[Solid]:
    rail_height = RECEIVER_RAIL_Z_MAX - RECEIVER_RAIL_Z_MIN

    rear_rail = Box(
        BASE_RECEIVER_RAIL_EXTENSION,
        BASE_Y_MAX - BASE_Y_MIN,
        rail_height,
        align=(Align.MIN, Align.CENTER, Align.MIN),
    ).moved(
        Location(
            (
                BASE_INNER_X_MAX - BASE_RECEIVER_RAIL_EXTENSION,
                0.0,
                RECEIVER_RAIL_Z_MIN,
            )
        )
    )

    side_length = BASE_X_MAX * 2.0
    y_min_rail = Box(
        side_length,
        BASE_RECEIVER_RAIL_EXTENSION,
        rail_height,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    ).moved(Location((0.0, BASE_INNER_Y_MIN, RECEIVER_RAIL_Z_MIN)))
    y_max_rail = Box(
        side_length,
        BASE_RECEIVER_RAIL_EXTENSION,
        rail_height,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    ).moved(
        Location(
            (
                0.0,
                BASE_INNER_Y_MAX - BASE_RECEIVER_RAIL_EXTENSION,
                RECEIVER_RAIL_Z_MIN,
            )
        )
    )
    return [rear_rail, y_min_rail, y_max_rail]


def make_base_snapfit() -> Solid:
    base = _load_single_solid(BASE_SOURCE, "arduino_giga_r1_enclosure_base_source")
    reinforced = base.fuse(*_receiver_rail_extensions())
    if len(reinforced.solids()) != 1 or not reinforced.is_valid:
        raise ValueError("Receiver-rail thickening did not produce one valid solid")

    pockets = [*(_rear_pocket(y) for y in REAR_TAB_Y_CENTERS)]
    pockets.extend(_front_pocket(x) for x in FRONT_TAB_X_CENTERS)
    pockets.extend(_opposite_side_pocket(x) for x in OPPOSITE_SIDE_TAB_X_CENTERS)
    revised = reinforced.cut(*pockets)
    if len(revised.solids()) != 1 or not revised.is_valid:
        raise ValueError("Base pocket subtraction did not produce one valid solid")
    revised.label = "arduino_giga_r1_enclosure_base_snapfit"
    return revised
