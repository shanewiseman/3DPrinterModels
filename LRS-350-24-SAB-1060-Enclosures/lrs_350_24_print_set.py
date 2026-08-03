"""Print layout for the Mean Well LRS-350-24 enclosure and fit coupon."""

from enclosure_geometry import (
    LRS_OUTER_Y,
    build_lrs_base,
    build_lrs_print_extras,
    build_lrs_lid_print,
    print_layout,
)


def gen_step():
    return print_layout(
        build_lrs_base(),
        build_lrs_lid_print(),
        LRS_OUTER_Y,
        "lrs_350_24_enclosure_print_set",
        extra_print_objects=build_lrs_print_extras(),
    )
