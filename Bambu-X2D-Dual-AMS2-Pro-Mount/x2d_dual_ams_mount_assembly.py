"""Assembled STEP entry point for the provisional X2D dual AMS mount."""

from __future__ import annotations

from cadpy.assembly import AssemblyHelper

from x2d_dual_ams_mount_geometry import (
    BRACKET_Y_CENTERS,
    make_geometry_details,
    side_name,
)


def build_assembly_details():
    details = make_geometry_details()
    assembly = AssemblyHelper("bambu_x2d_dual_ams2pro_fully_printed_mount")

    # Published/provisional reference geometry is included so the installed
    # relationship and door keep-out are reviewable in the assembled STEP.
    x2d = details["x2d_reference"]
    assembly.add(x2d["body"], "bambu_x2d_published_envelope")
    assembly.add(x2d["glass"], "x2d_provisional_top_glass")
    assembly.add(x2d["door_closed"], "x2d_provisional_front_door_closed")
    assembly.add(x2d["door_open"], "x2d_provisional_front_door_open_keepout")

    for side in (-1, 1):
        role = side_name(side)
        assembly.add(details["shelves"][side], f"{role}_printed_shelf")
        for y in BRACKET_Y_CENTERS:
            position = "front" if y < 0.0 else "rear"
            assembly.add(
                details["brackets"][(side, y)],
                f"{role}_{position}_printed_triangle_bracket",
            )
            assembly.add(
                details["side_pads"][(side, y)],
                f"{role}_{position}_printed_side_pad",
            )
            assembly.add(
                details["bracket_hardware"][(side, y)],
                f"{role}_{position}_bracket_hardware",
            )
        assembly.add(
            details["ams_references"][side]["compound"],
            f"{role}_ams2pro_simplified_reference",
        )

    for beam in ("front", "rear"):
        assembly.add(
            details["bridge_segments"][(beam, -1)],
            f"{beam}_bridge_left_printed_half",
        )
        assembly.add(
            details["bridge_segments"][(beam, 1)],
            f"{beam}_bridge_right_printed_half",
        )
        assembly.add(
            details["bridge_center_hardware"][beam],
            f"{beam}_bridge_center_hardware",
        )
        for side in (-1, 1):
            assembly.add(
                details["bridge_end_hardware"][(beam, side)],
                f"{side_name(side)}_{beam}_bridge_end_hardware",
            )

    final = assembly.build()
    final.label = "bambu_x2d_dual_ams2pro_fully_printed_mount_assembly"
    return {"final": final, **details}


def gen_step():
    return build_assembly_details()["final"]
