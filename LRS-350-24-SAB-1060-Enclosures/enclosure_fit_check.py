"""Installed fit-check assembly for both independent enclosures."""

from build123d import Location
from cadpy.assembly import AssemblyHelper

from enclosure_geometry import (
    LRS_BASE_HEIGHT,
    SAB_BASE_HEIGHT,
    SAB_LID_RISER_HEIGHT,
    assembled_lid,
    build_lrs_base,
    build_lrs_lid_print,
    build_lrs_reference,
    build_sab_base,
    build_sab_fan_guard_installed,
    build_sab_lid_print,
    build_sab_reference,
    build_sab_retaining_caps_installed,
)


SAB_ASSEMBLY_OFFSET_Y = 150.0


def build_fit_details():
    lrs_base = build_lrs_base()
    lrs_lid = assembled_lid(build_lrs_lid_print(), LRS_BASE_HEIGHT)
    lrs_reference = build_lrs_reference()

    sab_location = Location((0.0, SAB_ASSEMBLY_OFFSET_Y, 0.0))
    sab_base = build_sab_base().moved(sab_location)
    sab_lid = assembled_lid(
        build_sab_lid_print(),
        SAB_BASE_HEIGHT,
        SAB_LID_RISER_HEIGHT,
    ).moved(sab_location)
    sab_reference = build_sab_reference().moved(sab_location)
    sab_caps = tuple(
        cap.moved(sab_location)
        for cap in build_sab_retaining_caps_installed()
    )
    sab_fan_guard = build_sab_fan_guard_installed().moved(sab_location)

    assembly = AssemblyHelper("lrs_350_24_and_sab_1060_fit_check")
    assembly.add(lrs_base, "lrs_350_24_printed_base")
    assembly.add(lrs_reference, "lrs_350_24_reference_envelope")
    assembly.add(lrs_lid, "lrs_350_24_printed_lid")
    assembly.add(sab_base, "sab_1060_printed_base")
    assembly.add(sab_reference, "sab_1060_reference_envelope")
    assembly.add(sab_lid, "sab_1060_printed_lid")
    for index, cap in enumerate(sab_caps, start=1):
        assembly.add(cap, f"sab_1060_pcb_retaining_cap_{index}_installed")
    assembly.add(sab_fan_guard, "sab_1060_removable_fan_guard_installed")
    final = assembly.build()

    return {
        "final": final,
        "lrs_base": lrs_base,
        "lrs_lid": lrs_lid,
        "lrs_reference": lrs_reference,
        "sab_base": sab_base,
        "sab_lid": sab_lid,
        "sab_reference": sab_reference,
        "sab_caps": sab_caps,
        "sab_fan_guard": sab_fan_guard,
    }


def gen_step():
    return build_fit_details()["final"]
