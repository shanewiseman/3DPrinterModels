"""Printable keyed CRP2 M6 nut insert and fit-test coupon.

The hex pilot is intentionally undersized from the measured 10.0 mm CRP2
opening. The larger flange carries the same M6 nut pocket used in both yoke
arms without trying to wrap a printed sleeve around a nominal 10 mm nut.
"""

from __future__ import annotations

from build123d import (
    BuildSketch,
    Color,
    Cylinder,
    Location,
    Plane,
    RegularPolygon,
    extrude,
)

from moza_crp_dayton_tt25_mount import (
    BOOLEAN_OVERSHOOT,
    CRP2_ATTACHMENT_WIDTH,
    CRP2_INTERNAL_HEX_AF,
    PEDAL_PIVOT_CLEARANCE_DIAMETER,
    PIVOT_HEX_NOMINAL_AF,
    PIVOT_HEX_POCKET_AF,
    PIVOT_HEX_POCKET_DEPTH,
    _hex_circumradius,
    _single_solid,
)


INSERT_PILOT_AF = 9.6
INSERT_PILOT_LENGTH = CRP2_ATTACHMENT_WIDTH - 0.4
INSERT_FLANGE_DIAMETER = 18.0
INSERT_FLANGE_THICKNESS = 7.0
INSERT_NUT_SUPPORT_FLOOR = INSERT_FLANGE_THICKNESS - PIVOT_HEX_POCKET_DEPTH
INSERT_TOTAL_HEIGHT = INSERT_PILOT_LENGTH + INSERT_FLANGE_THICKNESS
INSERT_TEST_NUT_THICKNESS = 5.0

INSERT_COLOR = Color(0.80, 0.34, 0.10)


def build_insert_details():
    """Build a pilot-down insert that prints without support."""
    with BuildSketch(Plane.XY) as pilot_profile:
        RegularPolygon(
            radius=_hex_circumradius(INSERT_PILOT_AF),
            side_count=6,
            rotation=30.0,
        )
    pilot = extrude(pilot_profile.sketch, amount=INSERT_PILOT_LENGTH)

    flange = Cylinder(
        radius=INSERT_FLANGE_DIAMETER / 2.0,
        height=INSERT_FLANGE_THICKNESS,
    ).moved(
        Location(
            (
                0.0,
                0.0,
                INSERT_PILOT_LENGTH + INSERT_FLANGE_THICKNESS / 2.0,
            )
        )
    )

    insert_blank = _single_solid(
        pilot.fuse(flange),
        "keyed M6 nut insert blank",
    )

    bore = Cylinder(
        radius=PEDAL_PIVOT_CLEARANCE_DIAMETER / 2.0,
        height=INSERT_TOTAL_HEIGHT + 2.0 * BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, INSERT_TOTAL_HEIGHT / 2.0)))

    with BuildSketch(Plane.XY) as nut_profile:
        RegularPolygon(
            radius=_hex_circumradius(PIVOT_HEX_POCKET_AF),
            side_count=6,
            rotation=30.0,
        )
    nut_pocket_z_min = INSERT_TOTAL_HEIGHT - PIVOT_HEX_POCKET_DEPTH
    nut_pocket = extrude(
        nut_profile.sketch,
        amount=PIVOT_HEX_POCKET_DEPTH + BOOLEAN_OVERSHOOT,
    ).moved(Location((0.0, 0.0, nut_pocket_z_min)))

    with BuildSketch(Plane.XY) as measured_hex_profile:
        RegularPolygon(
            radius=_hex_circumradius(CRP2_INTERNAL_HEX_AF),
            side_count=6,
            rotation=30.0,
        )
    measured_hex_envelope = extrude(
        measured_hex_profile.sketch,
        amount=CRP2_ATTACHMENT_WIDTH,
    )

    with BuildSketch(Plane.XY) as test_nut_profile:
        RegularPolygon(
            radius=_hex_circumradius(PIVOT_HEX_NOMINAL_AF),
            side_count=6,
            rotation=30.0,
        )
    test_nut = extrude(
        test_nut_profile.sketch,
        amount=INSERT_TEST_NUT_THICKNESS,
    ).moved(Location((0.0, 0.0, nut_pocket_z_min + 0.1)))

    insert = _single_solid(
        insert_blank.cut(bore).cut(nut_pocket),
        "finished keyed M6 nut insert",
    )
    insert.label = "crp2_10mm_hex_keyed_m6_nut_insert"
    insert.color = INSERT_COLOR

    return {
        "insert": insert,
        "insert_blank": insert_blank,
        "pilot": pilot,
        "flange": flange,
        "bore": bore,
        "nut_pocket": nut_pocket,
        "measured_hex_envelope": measured_hex_envelope,
        "test_nut": test_nut,
        "nut_pocket_z_min": nut_pocket_z_min,
        "measured_crp2_hex_af": CRP2_INTERNAL_HEX_AF,
    }


def gen_step():
    return build_insert_details()["insert"]
