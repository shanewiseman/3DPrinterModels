"""Generate the snap-fit Arduino GIGA R1 enclosure lid."""

from cad_outputs.snapfit_enclosure.snapfit_geometry import make_lid_snapfit


def gen_step():
    return make_lid_snapfit()

