"""Installed-pose yoke fit check with official Dayton TT25 geometry."""

from __future__ import annotations

from build123d import Color, Compound, Location, import_step
from cadpy.assembly import AssemblyHelper

from moza_crp_dayton_tt25_mount import (
    BOOLEAN_OVERSHOOT,
    CRP2_ATTACHMENT_WIDTH,
    CRP2_INTERNAL_HEX_AF,
    FORK_INNER_SPAN,
    HOLDER_THICKNESS,
    PUCK_CENTER_Y,
    PUCK_CENTER_Z,
    PIVOT_HEX_POCKET_AF,
    PIVOT_HEX_POCKET_DEPTH,
    TT25_ROTATION_ABOUT_INSTALLED_Z_DEGREES,
    _cylinder_x,
    _hex_prism_x,
    _single_solid,
    build_holder_details,
)


TT25_REFERENCE_STEP = "reference/dayton_tt25-8_and-16.step"
# The original logo-inward arrangement used the source front datum at Y=1.5.
# Reversing the puck seats the printed carrier against the opposite faces of
# the 8.5 mm mounting lugs, whose official STEP rear datum is Y=12.9.
TT25_SOURCE_LOGO_SIDE_LUG_PLANE_Y = 4.4
TT25_SOURCE_REVERSED_MOUNT_PLANE_Y = 12.9
TT25_MOUNTING_LUG_THICKNESS = (
    TT25_SOURCE_REVERSED_MOUNT_PLANE_Y
    - TT25_SOURCE_LOGO_SIDE_LUG_PLANE_Y
)

# With the opposite lug face seated directly against the 8.5 mm carrier, the
# distance from the screw-head bearing face to the outer face of a captured
# nut is 17.0 mm. M3 x 18 gives 1.0 mm of controlled tip projection.
PUCK_M3_STACK_TO_NUT_OUTER_FACE = (
    TT25_MOUNTING_LUG_THICKNESS + HOLDER_THICKNESS
)
PUCK_M3_RECOMMENDED_LENGTH = 18.0

# M6 reference hardware. Threads are omitted from the BREP; the nut has a
# physical clearance bore so the fit-check contains no false solid overlap.
M6_BOLT_NOMINAL_DIAMETER = 6.0
M6_BOLT_CLEARANCE_DIAMETER = 6.4
M6_BOLT_LENGTH = 25.0
M6_BOLT_HEAD_DIAMETER = 10.0
M6_BOLT_HEAD_HEIGHT = 6.0
M6_BOLT_SOCKET_AF = 5.0
M6_BOLT_SOCKET_DEPTH = 3.5
M6_NUT_AF = 10.0
M6_NUT_THICKNESS = 5.0


def build_pivot_hardware(holder_details):
    """Build reversible M6 hardware on the yoke's global-X pivot."""
    left_outer_x = holder_details["left_outer_x"]
    right_outer_x = holder_details["right_outer_x"]

    nut_x_min = left_outer_x + 0.15
    nut_x_max = nut_x_min + M6_NUT_THICKNESS
    nut_blank = _hex_prism_x(M6_NUT_AF, nut_x_min, M6_NUT_THICKNESS)
    nut_bore = _cylinder_x(
        M6_BOLT_CLEARANCE_DIAMETER / 2.0,
        nut_x_min - BOOLEAN_OVERSHOOT,
        nut_x_max + BOOLEAN_OVERSHOOT,
    )
    pivot_nut = _single_solid(
        nut_blank.cut(nut_bore),
        "M6 captured nut",
    )
    pivot_nut.label = "m6_captured_hex_nut_reference_threads_omitted"
    pivot_nut.color = Color(0.62, 0.64, 0.67)

    # The socket head nests in the opposite receiver. A second bored reference
    # nut proves that this same pocket can accept the nut if hardware direction
    # is reversed, but is intentionally omitted from the installed assembly.
    right_test_nut_x_max = right_outer_x - 0.15
    right_test_nut_x_min = right_test_nut_x_max - M6_NUT_THICKNESS
    right_test_nut_blank = _hex_prism_x(
        M6_NUT_AF,
        right_test_nut_x_min,
        M6_NUT_THICKNESS,
    )
    right_test_nut_bore = _cylinder_x(
        M6_BOLT_CLEARANCE_DIAMETER / 2.0,
        right_test_nut_x_min - BOOLEAN_OVERSHOOT,
        right_test_nut_x_max + BOOLEAN_OVERSHOOT,
    )
    right_receiver_test_nut = _single_solid(
        right_test_nut_blank.cut(right_test_nut_bore),
        "right-receiver M6 test nut",
    )
    right_receiver_test_nut.label = "m6_right_receiver_test_nut"

    head_inner_x = right_outer_x - PIVOT_HEX_POCKET_DEPTH
    head_outer_x = head_inner_x + M6_BOLT_HEAD_HEIGHT
    shaft_end_x = head_inner_x - M6_BOLT_LENGTH
    bolt_shaft = _cylinder_x(
        M6_BOLT_NOMINAL_DIAMETER / 2.0,
        shaft_end_x,
        head_inner_x + BOOLEAN_OVERSHOOT,
    )
    bolt_head = _cylinder_x(
        M6_BOLT_HEAD_DIAMETER / 2.0,
        head_inner_x,
        head_outer_x,
    )
    socket = _hex_prism_x(
        M6_BOLT_SOCKET_AF,
        head_outer_x - M6_BOLT_SOCKET_DEPTH,
        M6_BOLT_SOCKET_DEPTH + BOOLEAN_OVERSHOOT,
    )
    pivot_bolt = _single_solid(
        bolt_head.fuse(bolt_shaft).cut(socket),
        "M6 socket-head pivot bolt",
    )
    pivot_bolt.label = "m6x25_socket_head_yoke_bolt_reference_threads_omitted"
    pivot_bolt.color = Color(0.34, 0.36, 0.39)

    return {
        "pivot_nut": pivot_nut,
        "right_receiver_test_nut": right_receiver_test_nut,
        "pivot_bolt": pivot_bolt,
        "nut_x_min": nut_x_min,
        "nut_x_max": nut_x_max,
        "right_test_nut_x_min": right_test_nut_x_min,
        "right_test_nut_x_max": right_test_nut_x_max,
        "bolt_shaft_x_min": shaft_end_x,
        "bolt_shaft_x_max": head_inner_x,
    }


def build_fit_details():
    holder_details = build_holder_details()
    holder = holder_details["holder"]
    holder.color = Color(0.12, 0.28, 0.52)

    imported = import_step(TT25_REFERENCE_STEP)
    if len(imported.children) < 1:
        raise RuntimeError("Official TT25 STEP did not expose the bare-puck child")

    # Native Dayton geometry is already broad in XZ. The X rotation maps the
    # extracted hole pattern into installed X/Z. The requested second 180
    # degree turn about installed Z points the logo outward. Seat the opposite
    # lug faces on the carrier's negative-Y side; this avoids burying the lugs
    # in the carrier and removes the former front-datum offset from the M3
    # screw stack. The carrier pattern is rotated identically so all six
    # manufacturer lug centers remain aligned.
    ring_back_y = holder_details["ring_back_y"]
    puck_location = Location(
        (
            0.0,
            ring_back_y - TT25_SOURCE_REVERSED_MOUNT_PLANE_Y,
            PUCK_CENTER_Z,
        ),
        (180.0, 0.0, TT25_ROTATION_ABOUT_INSTALLED_Z_DEGREES),
    )
    placed_puck_solids = []
    for index, source_solid in enumerate(imported.children[0].solids(), start=1):
        placed_solid = source_solid.moved(puck_location)
        placed_solid.label = f"dayton_tt25_8_body_{index:02d}"
        placed_solid.color = Color(0.12, 0.14, 0.17)
        placed_puck_solids.append(placed_solid)
    bare_puck = Compound(
        children=placed_puck_solids,
        label="dayton_tt25_8_reference",
        color=Color(0.12, 0.14, 0.17),
    )

    # The reference envelope uses the user's measured CRP2 attachment width
    # and 10 mm across-flats internal hex. The through hex is conservative
    # until its actual axial depth and center-hole details are measured.
    pedal_reference = _cylinder_x(
        12.0,
        -CRP2_ATTACHMENT_WIDTH / 2.0,
        CRP2_ATTACHMENT_WIDTH / 2.0,
    ).cut(
        _hex_prism_x(
            CRP2_INTERNAL_HEX_AF,
            -FORK_INNER_SPAN / 2.0,
            FORK_INNER_SPAN,
        )
    )
    pedal_reference = _single_solid(pedal_reference, "pedal pivot reference")
    pedal_reference.label = "measured_8mm_crp2_hex_attachment_reference"
    pedal_reference.color = Color(0.28, 0.30, 0.34)

    hardware = build_pivot_hardware(holder_details)
    pivot_nut = hardware["pivot_nut"]
    right_receiver_test_nut = hardware["right_receiver_test_nut"]
    pivot_bolt = hardware["pivot_bolt"]

    assembly = AssemblyHelper("moza_crp_tt25_perpendicular_yoke_fit_check")
    holder_occurrence = assembly.add(holder, "printed_perpendicular_yoke")
    puck_occurrence = assembly.add(bare_puck, "dayton_tt25_8")
    pedal_occurrence = assembly.add(pedal_reference, "measured_crp2_attachment")
    nut_occurrence = assembly.add(pivot_nut, "m6_captured_nut")
    bolt_occurrence = assembly.add(pivot_bolt, "m6_yoke_bolt")
    final = assembly.build()

    return {
        "final": final,
        "holder": holder,
        "holder_details": holder_details,
        "bare_puck": bare_puck,
        "pedal_reference": pedal_reference,
        "pivot_nut": pivot_nut,
        "right_receiver_test_nut": right_receiver_test_nut,
        "pivot_bolt": pivot_bolt,
        "hardware": hardware,
        "holder_occurrence": holder_occurrence,
        "puck_occurrence": puck_occurrence,
        "pedal_occurrence": pedal_occurrence,
        "nut_occurrence": nut_occurrence,
        "bolt_occurrence": bolt_occurrence,
    }


def gen_step():
    return build_fit_details()["final"]
