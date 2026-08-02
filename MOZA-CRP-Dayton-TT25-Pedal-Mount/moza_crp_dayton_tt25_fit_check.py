"""Installed-pose yoke fit check with official Dayton TT25 geometry."""

from __future__ import annotations

from build123d import Color, Compound, Location, import_step
from cadpy.assembly import AssemblyHelper

from moza_crp_dayton_tt25_mount import (
    BOOLEAN_OVERSHOOT,
    FORK_INNER_SPAN,
    HOLDER_THICKNESS,
    PEDAL_MOUNT_WIDTH_ASSUMED,
    PUCK_CENTER_Y,
    PUCK_CENTER_Z,
    PIVOT_HEX_POCKET_AF,
    PIVOT_HEX_POCKET_DEPTH,
    _cylinder_x,
    _hex_prism_x,
    _single_solid,
    build_holder_details,
)


TT25_REFERENCE_STEP = "reference/dayton_tt25-8_and-16.step"
TT25_SOURCE_MOUNT_PLANE_Y = 1.5

# M8 reference hardware. Threads are omitted from the BREP; the nut has a
# physical clearance bore so the fit-check contains no false solid overlap.
M8_BOLT_NOMINAL_DIAMETER = 8.0
M8_BOLT_CLEARANCE_DIAMETER = 8.2
M8_BOLT_LENGTH = 40.0
M8_BOLT_HEAD_DIAMETER = 13.0
M8_BOLT_HEAD_HEIGHT = 8.0
M8_BOLT_SOCKET_AF = 6.0
M8_BOLT_SOCKET_DEPTH = 4.5
M8_NUT_AF = 13.0
M8_NUT_THICKNESS = 6.5


def build_pivot_hardware(holder_details):
    """Build reversible M8 hardware on the yoke's global-X pivot."""
    left_outer_x = holder_details["left_outer_x"]
    right_outer_x = holder_details["right_outer_x"]

    nut_x_min = left_outer_x + 0.15
    nut_x_max = nut_x_min + M8_NUT_THICKNESS
    nut_blank = _hex_prism_x(M8_NUT_AF, nut_x_min, M8_NUT_THICKNESS)
    nut_bore = _cylinder_x(
        M8_BOLT_CLEARANCE_DIAMETER / 2.0,
        nut_x_min - BOOLEAN_OVERSHOOT,
        nut_x_max + BOOLEAN_OVERSHOOT,
    )
    pivot_nut = _single_solid(
        nut_blank.cut(nut_bore),
        "M8 captured nut",
    )
    pivot_nut.label = "m8_captured_hex_nut_reference_threads_omitted"
    pivot_nut.color = Color(0.62, 0.64, 0.67)

    # The socket head nests in the opposite receiver. A second bored reference
    # nut proves that this same pocket can accept the nut if hardware direction
    # is reversed, but is intentionally omitted from the installed assembly.
    right_test_nut_x_max = right_outer_x - 0.15
    right_test_nut_x_min = right_test_nut_x_max - M8_NUT_THICKNESS
    right_test_nut_blank = _hex_prism_x(
        M8_NUT_AF,
        right_test_nut_x_min,
        M8_NUT_THICKNESS,
    )
    right_test_nut_bore = _cylinder_x(
        M8_BOLT_CLEARANCE_DIAMETER / 2.0,
        right_test_nut_x_min - BOOLEAN_OVERSHOOT,
        right_test_nut_x_max + BOOLEAN_OVERSHOOT,
    )
    right_receiver_test_nut = _single_solid(
        right_test_nut_blank.cut(right_test_nut_bore),
        "right-receiver M8 test nut",
    )
    right_receiver_test_nut.label = "m8_right_receiver_test_nut"

    head_inner_x = right_outer_x - PIVOT_HEX_POCKET_DEPTH
    head_outer_x = head_inner_x + M8_BOLT_HEAD_HEIGHT
    shaft_end_x = head_inner_x - M8_BOLT_LENGTH
    bolt_shaft = _cylinder_x(
        M8_BOLT_NOMINAL_DIAMETER / 2.0,
        shaft_end_x,
        head_inner_x + BOOLEAN_OVERSHOOT,
    )
    bolt_head = _cylinder_x(
        M8_BOLT_HEAD_DIAMETER / 2.0,
        head_inner_x,
        head_outer_x,
    )
    socket = _hex_prism_x(
        M8_BOLT_SOCKET_AF,
        head_outer_x - M8_BOLT_SOCKET_DEPTH,
        M8_BOLT_SOCKET_DEPTH + BOOLEAN_OVERSHOOT,
    )
    pivot_bolt = _single_solid(
        bolt_head.fuse(bolt_shaft).cut(socket),
        "M8 socket-head pivot bolt",
    )
    pivot_bolt.label = "m8x40_socket_head_yoke_bolt_reference_threads_omitted"
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

    # Native Dayton geometry is already broad in XZ. Rotating 180 degrees
    # around X maps the extracted hole pattern into the holder's global X/Z
    # coordinates and points the puck body away from the pedal.
    ring_back_y = holder_details["ring_back_y"]
    puck_location = Location(
        (
            0.0,
            ring_back_y + TT25_SOURCE_MOUNT_PLANE_Y,
            PUCK_CENTER_Z,
        ),
        (180.0, 0.0, 0.0),
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

    # A bored cylindrical envelope represents the CRP pivot stack between the
    # fork arms. Its width is an explicit first-fit assumption, not MOZA data.
    pedal_reference = _cylinder_x(
        12.0,
        -PEDAL_MOUNT_WIDTH_ASSUMED / 2.0,
        PEDAL_MOUNT_WIDTH_ASSUMED / 2.0,
    ).cut(
        _cylinder_x(
            M8_BOLT_CLEARANCE_DIAMETER / 2.0,
            -FORK_INNER_SPAN / 2.0,
            FORK_INNER_SPAN / 2.0,
        )
    )
    pedal_reference = _single_solid(pedal_reference, "pedal pivot reference")
    pedal_reference.label = "assumed_20mm_crp_pivot_stack_reference"
    pedal_reference.color = Color(0.28, 0.30, 0.34)

    hardware = build_pivot_hardware(holder_details)
    pivot_nut = hardware["pivot_nut"]
    right_receiver_test_nut = hardware["right_receiver_test_nut"]
    pivot_bolt = hardware["pivot_bolt"]

    assembly = AssemblyHelper("moza_crp_tt25_perpendicular_yoke_fit_check")
    holder_occurrence = assembly.add(holder, "printed_perpendicular_yoke")
    puck_occurrence = assembly.add(bare_puck, "dayton_tt25_8")
    pedal_occurrence = assembly.add(pedal_reference, "assumed_crp_pivot_stack")
    nut_occurrence = assembly.add(pivot_nut, "m8_captured_nut")
    bolt_occurrence = assembly.add(pivot_bolt, "m8_yoke_bolt")
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
