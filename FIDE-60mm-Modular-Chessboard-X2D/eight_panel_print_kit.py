"""Complete eight-panel chessboard print kit in thirteen virtual X2D plates.

Each 120 x 240 mm playing panel occupies the left side of its own 256 mm
virtual plate, leaving the right side available for slicer-generated supports
and a prime tower.  Virtual plates are assembly datums only; no plate solids
are exported.
"""

from __future__ import annotations

from build123d import Axis, Location
from cadpy.assembly import AssemblyHelper, label_shape

from chessboard_geometry import (
    DARK_COLOR,
    LIGHT_COLOR,
    PERIMETER_COLOR,
    make_corner_cap,
    make_loose_dark_square_inlay,
    make_rail_print_assembly,
    make_seam_bridge,
)
from eight_panel_geometry import (
    EIGHT_PANEL_ROLES,
    make_eight_panel_body_for_print,
)


VIRTUAL_PLATE_SIZE = 256.0
VIRTUAL_PLATE_PITCH = 285.0
PANEL_LOCAL_X = -60.0
DARK_INLAY_PITCH = 61.6
RAIL_ROW_PITCH = 40.0


PLATE_CENTERS = {
    "plate_01_panel_south_ab": (0.0, 0.0),
    "plate_02_panel_south_cd": (VIRTUAL_PLATE_PITCH, 0.0),
    "plate_03_panel_south_ef": (2.0 * VIRTUAL_PLATE_PITCH, 0.0),
    "plate_04_panel_south_gh": (3.0 * VIRTUAL_PLATE_PITCH, 0.0),
    "plate_05_panel_north_ab": (0.0, -VIRTUAL_PLATE_PITCH),
    "plate_06_panel_north_cd": (VIRTUAL_PLATE_PITCH, -VIRTUAL_PLATE_PITCH),
    "plate_07_panel_north_ef": (2.0 * VIRTUAL_PLATE_PITCH, -VIRTUAL_PLATE_PITCH),
    "plate_08_panel_north_gh": (3.0 * VIRTUAL_PLATE_PITCH, -VIRTUAL_PLATE_PITCH),
    "plate_09_horizontal_rails": (0.0, -2.0 * VIRTUAL_PLATE_PITCH),
    "plate_10_vertical_rails": (VIRTUAL_PLATE_PITCH, -2.0 * VIRTUAL_PLATE_PITCH),
    "plate_11_dark_inlays_01_16": (2.0 * VIRTUAL_PLATE_PITCH, -2.0 * VIRTUAL_PLATE_PITCH),
    "plate_12_dark_inlays_17_32": (3.0 * VIRTUAL_PLATE_PITCH, -2.0 * VIRTUAL_PLATE_PITCH),
    "plate_13_bridges_and_caps": (4.0 * VIRTUAL_PLATE_PITCH, -2.0 * VIRTUAL_PLATE_PITCH),
}


def _place_on_virtual_plate(
    shape,
    plate_name: str,
    local_x: float,
    local_y: float,
    *,
    rotation_z: float = 0.0,
):
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


def _panel_plate_groups():
    groups = {}
    for index, name in enumerate(EIGHT_PANEL_ROLES, start=1):
        plate_name = f"plate_{index:02d}_panel_{name}"
        panel = _place_on_virtual_plate(
            make_eight_panel_body_for_print(name),
            plate_name,
            PANEL_LOCAL_X,
            0.0,
        )
        groups[plate_name] = [
            label_shape(panel, "playing_surface_body", name, color=LIGHT_COLOR)
        ]
    return groups


def _rail_plate_groups():
    groups = {
        "plate_09_horizontal_rails": [],
        "plate_10_vertical_rails": [],
    }
    horizontal_names = ("bottom_ad", "bottom_eh", "top_ad", "top_eh")
    vertical_names = ("left_14", "left_58", "right_14", "right_58")
    row_positions = (
        -1.5 * RAIL_ROW_PITCH,
        -0.5 * RAIL_ROW_PITCH,
        0.5 * RAIL_ROW_PITCH,
        1.5 * RAIL_ROW_PITCH,
    )
    for name, row_y in zip(horizontal_names, row_positions, strict=True):
        rail = _place_on_virtual_plate(
            make_rail_print_assembly(name),
            "plate_09_horizontal_rails",
            0.0,
            row_y,
        )
        groups["plate_09_horizontal_rails"].append(
            label_shape(rail, "multicolor_rail", name)
        )
    for name, row_y in zip(vertical_names, row_positions, strict=True):
        rail = _place_on_virtual_plate(
            make_rail_print_assembly(name),
            "plate_10_vertical_rails",
            0.0,
            row_y,
            rotation_z=90.0,
        )
        groups["plate_10_vertical_rails"].append(
            label_shape(rail, "multicolor_rail", name)
        )
    return groups


def _dark_inlay_plate_groups():
    groups = {
        "plate_11_dark_inlays_01_16": [],
        "plate_12_dark_inlays_17_32": [],
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
    plate_name = "plate_13_bridges_and_caps"
    children = []
    bridge_x_positions = (-82.5, -27.5, 27.5, 82.5)
    instance = 1
    for row_y in (-67.5, -42.5, -17.5, 7.5):
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
            47.5,
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


def make_eight_panel_print_kit_groups():
    groups = {}
    for source in (
        _panel_plate_groups(),
        _rail_plate_groups(),
        _dark_inlay_plate_groups(),
        _bridge_and_cap_plate_group(),
    ):
        groups.update(source)
    return groups


def make_eight_panel_print_kit():
    assembly = AssemblyHelper("fide_60mm_eight_panel_chessboard_print_kit")
    for plate_name, children in make_eight_panel_print_kit_groups().items():
        assembly.add_module(plate_name, children)
    return assembly.build()


def gen_step():
    return make_eight_panel_print_kit()
