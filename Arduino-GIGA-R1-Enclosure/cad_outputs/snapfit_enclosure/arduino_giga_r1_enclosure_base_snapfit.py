"""Generate the snap-fit Arduino GIGA R1 enclosure base."""

from cad_outputs.snapfit_enclosure.snapfit_geometry import make_base_snapfit


def gen_step():
    return make_base_snapfit()

