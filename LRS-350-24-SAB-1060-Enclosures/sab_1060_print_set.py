"""Nine-object print layout for the Dayton Audio SAB-1060 enclosure."""

from enclosure_geometry import (
    SAB_OUTER_Y,
    SAB_PRINT_CENTER_GAP,
    build_sab_base,
    build_sab_lid_print,
    build_sab_print_extras,
    print_layout,
)


def gen_step():
    return print_layout(
        build_sab_base(),
        build_sab_lid_print(),
        SAB_OUTER_Y,
        "sab_1060_enclosure_print_set",
        extra_print_objects=build_sab_print_extras(),
        center_gap=SAB_PRINT_CENTER_GAP,
    )
