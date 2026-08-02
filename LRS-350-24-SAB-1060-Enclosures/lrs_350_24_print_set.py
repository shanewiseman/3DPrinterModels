"""Two-object print layout for the Mean Well LRS-350-24 enclosure."""

from enclosure_geometry import (
    LRS_OUTER_Y,
    build_lrs_base,
    build_lrs_lid_print,
    print_layout,
)


def gen_step():
    return print_layout(
        build_lrs_base(),
        build_lrs_lid_print(),
        LRS_OUTER_Y,
        "lrs_350_24_enclosure_print_set",
    )
