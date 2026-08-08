"""All printable chessboard pieces in a separated nine-plate master layout.

The exported STEP is a labeled assembly intended for Bambu Studio's
multi-object workflow. Playing quarters are single-color structural bodies;
their 32 glue-in dark square inlays are arranged on two separate print plates.
Each perimeter rail stays grouped with its four flush inset notation bodies so
the rail and glyphs can receive different filament assignments. No virtual
build-plate solids are exported. Every printable object lies flat on Z=0 and
is grouped under a suggested 256 x 256 mm plate module.
"""

from __future__ import annotations

from build123d import Axis, Location
from cadpy.assembly import AssemblyHelper, label_shape

from chessboard_geometry import (
    DARK_COLOR,
    LIGHT_COLOR,
    PERIMETER_COLOR,
    QUARTER_ROLES,
    make_corner_cap,
    make_loose_dark_square_inlay,
    make_quarter_light_body_for_print,
    make_rail_print_assembly,
    make_seam_bridge,
)


VIRTUAL_PLATE_SIZE = 256.0
VIRTUAL_PLATE_PITCH = 285.0
DARK_INLAY_PITCH = 61.6  # 59.6 mm tile plus 2.0 mm object spacing.
RAIL_ROW_PITCH = 40.0  # 35 mm rail width plus 5 mm object spacing.

# Plate centers are source datums only. They separate the modules in the
# master STEP and are not exported as physical plate geometry.
PLATE_CENTERS = {
    "plate_01_quarter_sw": (0.0, 0.0),
    "plate_02_quarter_se": (VIRTUAL_PLATE_PITCH, 0.0),
    "plate_03_quarter_nw": (2.0 * VIRTUAL_PLATE_PITCH, 0.0),
    "plate_04_quarter_ne": (3.0 * VIRTUAL_PLATE_PITCH, 0.0),
    "plate_05_horizontal_rails": (4.0 * VIRTUAL_PLATE_PITCH, 0.0),
    "plate_06_vertical_rails": (0.0, -VIRTUAL_PLATE_PITCH),
    "plate_07_dark_inlays_01_16": (VIRTUAL_PLATE_PITCH, -VIRTUAL_PLATE_PITCH),
    "plate_08_dark_inlays_17_32": (2.0 * VIRTUAL_PLATE_PITCH, -VIRTUAL_PLATE_PITCH),
    "plate_09_bridges_and_caps": (3.0 * VIRTUAL_PLATE_PITCH, -VIRTUAL_PLATE_PITCH),
}


def _place_on_virtual_plate(
    shape,
    plate_name: str,
    local_x: float,
    local_y: float,
    *,
    rotation_z: float = 0.0,
):
    """Rotate, center, and bed a component at one virtual-plate coordinate."""

    if rotation_z:
        shape = shape.rotate(Axis.Z, rotation_z)
    bounds = shape.bounding_box()
    center_x = (bounds.min.X + bounds.max.X) / 2.0
    center_y = (bounds.min.Y + bounds.max.Y) / 2.0
    plate_x, plate_y = PLATE_CENTERS[plate_name]
    return shape.moved(
        Location(
            (
                plate_x + local_x - center_x,
                plate_y + local_y - center_y,
                -bounds.min.Z,
            )
        )
    )


def _quarter_plate_groups():
    groups = {}
    for index, role in enumerate(QUARTER_ROLES, start=1):
        plate_name = f"plate_{index:02d}_quarter_{role}"
        quarter = _place_on_virtual_plate(
            make_quarter_light_body_for_print(role),
            plate_name,
            0.0,
            0.0,
        )
        groups[plate_name] = [
            label_shape(quarter, "playing_surface_body", role, color=LIGHT_COLOR)
        ]
    return groups


def _rail_plate_groups():
    groups = {
        "plate_05_horizontal_rails": [],
        "plate_06_vertical_rails": [],
    }
    horizontal_names = ("bottom_ad", "bottom_eh", "top_ad", "top_eh")
    vertical_names = ("left_14", "left_58", "right_14", "right_58")
    row_positions = (
        -1.5 * RAIL_ROW_PITCH,
        -0.5 * RAIL_ROW_PITCH,
        0.5 * RAIL_ROW_PITCH,
        1.5 * RAIL_ROW_PITCH,
    )

    for name, row_y in zip(horizontal_names, row_positions):
        rail = _place_on_virtual_plate(
            make_rail_print_assembly(name),
            "plate_05_horizontal_rails",
            0.0,
            row_y,
        )
        groups["plate_05_horizontal_rails"].append(
            label_shape(rail, "multicolor_rail", name)
        )

    for name, row_y in zip(vertical_names, row_positions):
        rail = _place_on_virtual_plate(
            make_rail_print_assembly(name),
            "plate_06_vertical_rails",
            0.0,
            row_y,
            rotation_z=90.0,
        )
        groups["plate_06_vertical_rails"].append(
            label_shape(rail, "multicolor_rail", name)
        )

    return groups


def _dark_inlay_plate_groups():
    groups = {
        "plate_07_dark_inlays_01_16": [],
        "plate_08_dark_inlays_17_32": [],
    }
    grid_positions = (
        -1.5 * DARK_INLAY_PITCH,
        -0.5 * DARK_INLAY_PITCH,
        0.5 * DARK_INLAY_PITCH,
        1.5 * DARK_INLAY_PITCH,
    )
    instance = 1
    for plate_name in groups:
        for row_y in grid_positions:
            for column_x in grid_positions:
                inlay = _place_on_virtual_plate(
                    make_loose_dark_square_inlay(),
                    plate_name,
                    column_x,
                    row_y,
                )
                groups[plate_name].append(
                    label_shape(
                        inlay,
                        "dark_square_inlay",
                        f"{instance:02d}",
                        color=DARK_COLOR,
                    )
                )
                instance += 1
    return groups


def _bridge_and_cap_plate_group():
    plate_name = "plate_09_bridges_and_caps"
    children = []
    bridge_x_positions = (-82.5, -27.5, 27.5, 82.5)
    instance = 1
    for row_y in (-42.5, -17.5):
        for column_x in bridge_x_positions:
            bridge = _place_on_virtual_plate(
                make_seam_bridge(),
                plate_name,
                column_x,
                row_y,
            )
            children.append(
                label_shape(
                    bridge,
                    "seam_bridge",
                    f"{instance:02d}",
                    color=PERIMETER_COLOR,
                )
            )
            instance += 1

    for instance, column_x in enumerate((-45.0, -15.0, 15.0, 45.0), start=1):
        cap = _place_on_virtual_plate(
            make_corner_cap(),
            plate_name,
            column_x,
            45.0,
        )
        children.append(
            label_shape(
                cap,
                "corner_cap",
                f"{instance:02d}",
                color=PERIMETER_COLOR,
            )
        )
    return {plate_name: children}


def make_print_kit_plate_groups():
    """Return nine groups containing 56 objects and 88 colored leaf solids."""

    groups = {}
    for source in (
        _quarter_plate_groups(),
        _rail_plate_groups(),
        _dark_inlay_plate_groups(),
        _bridge_and_cap_plate_group(),
    ):
        groups.update(source)
    return groups


def make_separated_print_kit():
    assembly = AssemblyHelper("fide_60mm_chessboard_separated_print_kit")
    for plate_name, children in make_print_kit_plate_groups().items():
        assembly.add_module(plate_name, children)
    return assembly.build()


def gen_step():
    return make_separated_print_kit()
