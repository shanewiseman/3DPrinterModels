"""Generate a side-by-side, flat-side-down print layout of both enclosure parts."""

from build123d import Color, Location
from cadpy.assembly import AssemblyHelper

from cad_outputs.snapfit_enclosure.snapfit_geometry import (
    LID_EXTERIOR_FACE_Z,
    make_base_snapfit,
    make_lid_snapfit,
)


BASE_WIDTH_X = 112.0
LID_WIDTH_X = 115.2
SIDE_BY_SIDE_GAP = 12.0
X2D_LAYOUT_ROTATION_Z = 90.0

TOTAL_LAYOUT_WIDTH = BASE_WIDTH_X + SIDE_BY_SIDE_GAP + LID_WIDTH_X
LAYOUT_X_MIN = -TOTAL_LAYOUT_WIDTH / 2.0
BASE_LAYOUT_X = LAYOUT_X_MIN + BASE_WIDTH_X / 2.0
LID_LAYOUT_X = LAYOUT_X_MIN + BASE_WIDTH_X + SIDE_BY_SIDE_GAP + LID_WIDTH_X / 2.0


def gen_step():
    base = make_base_snapfit().moved(Location((BASE_LAYOUT_X, 0.0, 0.0)))
    lid = make_lid_snapfit().moved(
        Location((LID_LAYOUT_X, 0.0, LID_EXTERIOR_FACE_Z), (180.0, 0.0, 0.0))
    )
    x2d_plate_rotation = Location((0.0, 0.0, 0.0), (0.0, 0.0, X2D_LAYOUT_ROTATION_Z))
    base = base.moved(x2d_plate_rotation)
    lid = lid.moved(x2d_plate_rotation)

    assembly = AssemblyHelper("arduino_giga_r1_enclosure_snapfit_print_layout")
    assembly.add(base, "base_snapfit_x2d_rotated", color=Color(0.72, 0.78, 0.84))
    assembly.add(lid, "lid_snapfit_two_color_flat_side_down_x2d_rotated")
    return assembly.build()
