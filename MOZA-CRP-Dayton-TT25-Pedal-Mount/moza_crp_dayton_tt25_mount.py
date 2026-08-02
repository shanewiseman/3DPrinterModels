"""Perpendicular fork mount for a Dayton TT25 on an original MOZA CRP pedal.

Installed coordinate convention:
- The pedal pivot axis is global X, centered at XYZ=(0, 0, 0).
- The pedal's broad side plane is YZ; the assumed pedal width is along X.
- The TT25 carrier face is XZ, making it 90 degrees to the pedal side plane.
- The TT25 center is at XYZ=(0, -26, 65), behind and above the pivot.
"""

from __future__ import annotations

from math import sqrt

from build123d import (
    Axis,
    BuildSketch,
    Circle,
    Color,
    Cylinder,
    Location,
    Locations,
    Mode,
    Plane,
    RegularPolygon,
    extrude,
    make_hull,
)


# Dayton Audio TT25-8/-16 dimensions from the manufacturer drawing/STEP.
TT25_BODY_DIAMETER = 87.0
TT25_REAR_BULGE_DIAMETER = 67.0
TT25_RELIEF_DIAMETER = 70.5
TT25_REAR_COVER_RELIEF_DIAMETER = 82.0
TT25_REAR_COVER_RELIEF_DEPTH = 1.7
TT25_OVERALL_ENVELOPE = 104.5
TT25_MOUNTING_HOLE_DIAMETER = 3.5
TT25_HOLDER_HOLE_DIAMETER = 3.8

# Exact bare-puck hole centers transformed from the official STEP before the
# requested 180-degree installed-Z rotation. The second coordinate becomes
# installed global Z relative to PUCK_CENTER_Z.
TT25_SOURCE_MOUNTING_HOLE_POSITIONS = (
    (10.0, 47.550505),
    (-10.0, 47.050505),
    (36.179945, -32.435506),
    (45.746932, -14.864998),
    (-46.179945, -15.114998),
    (-35.746932, -32.185506),
)

# Rotating the physical puck 180 degrees about installed global Z mirrors the
# slightly asymmetric manufacturer pattern in X. Rotate the carrier holes with
# it so the six lug centers and their diameters remain an exact match.
TT25_ROTATION_ABOUT_INSTALLED_Z_DEGREES = 180.0
TT25_MOUNTING_HOLE_POSITIONS = tuple(
    (-x, local_z) for x, local_z in TT25_SOURCE_MOUNTING_HOLE_POSITIONS
)

# Perpendicular puck carrier.
HOLDER_OUTER_DIAMETER = 106.0
HOLDER_THICKNESS = 8.5
PUCK_CENTER_Y = -26.0
PUCK_CENTER_Z = 65.0
CABLE_PASS_THROUGH_DIAMETER = 10.0
CABLE_PASS_THROUGH_CENTER_X = (
    TT25_MOUNTING_HOLE_POSITIONS[2][0]
    + TT25_MOUNTING_HOLE_POSITIONS[5][0]
) / 2.0
CABLE_PASS_THROUGH_CENTER_Z = PUCK_CENTER_Z - (
    HOLDER_OUTER_DIAMETER + TT25_RELIEF_DIAMETER
) / 4.0

# Two-arm pedal yoke. The 20 mm pedal width remains an explicit first-fit
# assumption because MOZA does not publish this exposed pivot stack dimension.
PEDAL_MOUNT_WIDTH_ASSUMED = 20.0
PEDAL_SIDE_CLEARANCE = 0.6
FORK_INNER_SPAN = PEDAL_MOUNT_WIDTH_ASSUMED + PEDAL_SIDE_CLEARANCE
FORK_ARM_THICKNESS = 4.5
FORK_PIVOT_BOSS_DIAMETER = 33.0
FORK_LEVER_PAD_DIAMETER = 20.0
# The lever pads meet only the carrier's front side. Their rear extent reaches
# PUCK_CENTER_Y but never crosses the puck-facing rear surface.
FORK_LEVER_JOIN_Y = PUCK_CENTER_Y + FORK_LEVER_PAD_DIAMETER / 2.0
FORK_LEVER_JOIN_Z = 20.0
PEDAL_PIVOT_CLEARANCE_DIAMETER = 8.6

# Reversible captured-M8 receivers on both arms. Each local boss is thickened
# so 4.0 mm of printed material remains between its hex pocket and the pedal.
PIVOT_HEX_NOMINAL_AF = 13.0
PIVOT_HEX_POCKET_AF = 13.4
PIVOT_HEX_POCKET_DEPTH = 6.8
PIVOT_NUT_SUPPORT_FLOOR = 4.0
PIVOT_NUT_BOSS_EXTRA = (
    PIVOT_HEX_POCKET_DEPTH
    + PIVOT_NUT_SUPPORT_FLOOR
    - FORK_ARM_THICKNESS
)

# Captive M3 nuts retain the TT25 without self-tapping into plastic.
PUCK_NUT_POCKET_AF = 5.8
PUCK_NUT_POCKET_DEPTH = 2.7
BOOLEAN_OVERSHOOT = 0.25

HOLDER_COLOR = Color(0.08, 0.10, 0.13)


def _hex_circumradius(across_flats: float) -> float:
    return across_flats / sqrt(3.0)


def _single_solid(shape_or_shapes, feature_name: str):
    solids = list(shape_or_shapes.solids())
    if len(solids) != 1:
        raise RuntimeError(
            f"{feature_name} expected one solid but produced {len(solids)}"
        )
    return solids[0]


def _cylinder_x(radius: float, x_min: float, x_max: float, y=0.0, z=0.0):
    """Create a cylinder on global X with explicit endpoint coordinates."""
    return (
        Cylinder(radius=radius, height=x_max - x_min)
        .rotate(Axis.Y, 90.0)
        .moved(Location(((x_min + x_max) / 2.0, y, z)))
    )


def _cylinder_y(radius: float, y_min: float, y_max: float, x=0.0, z=0.0):
    """Create a cylinder on global Y with explicit endpoint coordinates."""
    return (
        Cylinder(radius=radius, height=y_max - y_min)
        .rotate(Axis.X, -90.0)
        .moved(Location((x, (y_min + y_max) / 2.0, z)))
    )


def _hex_prism_x(across_flats: float, x_min: float, depth: float):
    with BuildSketch(Plane.YZ) as hex_profile:
        RegularPolygon(
            radius=_hex_circumradius(across_flats),
            side_count=6,
            rotation=30.0,
        )
    return extrude(hex_profile.sketch, amount=depth).moved(
        Location((x_min, 0.0, 0.0))
    )


def _hex_prisms_y(centers_xz, across_flats: float, y_front: float, depth: float):
    """Cut hex pockets from a positive-Y face inward along negative Y."""
    with BuildSketch(Plane.XZ) as hex_profiles:
        with Locations(*centers_xz):
            RegularPolygon(
                radius=_hex_circumradius(across_flats),
                side_count=6,
                rotation=30.0,
            )
    return extrude(hex_profiles.sketch, amount=depth).moved(
        Location((0.0, y_front, 0.0))
    )


def _build_ring_blank():
    ring_hole_positions = tuple(
        (x, PUCK_CENTER_Z + local_z)
        for x, local_z in TT25_MOUNTING_HOLE_POSITIONS
    )
    with BuildSketch(Plane.XZ) as ring_profile:
        with Locations((0.0, PUCK_CENTER_Z)):
            Circle(HOLDER_OUTER_DIAMETER / 2.0)
            Circle(TT25_RELIEF_DIAMETER / 2.0, mode=Mode.SUBTRACT)
        with Locations(
            (CABLE_PASS_THROUGH_CENTER_X, CABLE_PASS_THROUGH_CENTER_Z)
        ):
            Circle(CABLE_PASS_THROUGH_DIAMETER / 2.0, mode=Mode.SUBTRACT)
        with Locations(*ring_hole_positions):
            Circle(TT25_HOLDER_HOLE_DIAMETER / 2.0, mode=Mode.SUBTRACT)

    # Plane.XZ extrudes along -Y. Moving its raw -8.5..0 body centers it on
    # PUCK_CENTER_Y without altering the installed X/Z datums.
    ring = extrude(ring_profile.sketch, amount=HOLDER_THICKNESS).moved(
        Location((0.0, PUCK_CENTER_Y + HOLDER_THICKNESS / 2.0, 0.0))
    )
    return _single_solid(ring, "perpendicular puck ring")


def _build_fork_arm(x_min: float):
    with BuildSketch(Plane.YZ) as arm_profile:
        Circle(FORK_PIVOT_BOSS_DIAMETER / 2.0)
        with Locations((FORK_LEVER_JOIN_Y, FORK_LEVER_JOIN_Z)):
            Circle(FORK_LEVER_PAD_DIAMETER / 2.0)
        make_hull()
        Circle(PEDAL_PIVOT_CLEARANCE_DIAMETER / 2.0, mode=Mode.SUBTRACT)
    arm = extrude(arm_profile.sketch, amount=FORK_ARM_THICKNESS).moved(
        Location((x_min, 0.0, 0.0))
    )
    return _single_solid(arm, "fork arm")


def build_holder_details():
    """Build the one-piece perpendicular ring, lever, and two-arm yoke."""
    half_inner_span = FORK_INNER_SPAN / 2.0
    left_arm_x_min = -half_inner_span - FORK_ARM_THICKNESS
    right_arm_x_min = half_inner_span

    ring_blank = _build_ring_blank()
    left_arm = _build_fork_arm(left_arm_x_min)
    right_arm = _build_fork_arm(right_arm_x_min)

    left_arm_outer_x = left_arm_x_min
    right_arm_outer_x = right_arm_x_min + FORK_ARM_THICKNESS
    left_outer_x = left_arm_outer_x - PIVOT_NUT_BOSS_EXTRA
    right_outer_x = right_arm_outer_x + PIVOT_NUT_BOSS_EXTRA

    left_receiver_boss = _cylinder_x(
        FORK_PIVOT_BOSS_DIAMETER / 2.0,
        left_outer_x,
        left_arm_outer_x,
    )
    right_receiver_boss = _cylinder_x(
        FORK_PIVOT_BOSS_DIAMETER / 2.0,
        right_arm_outer_x,
        right_outer_x,
    )

    holder_blank = _single_solid(
        ring_blank.fuse(left_arm)
        .fuse(right_arm)
        .fuse(left_receiver_boss)
        .fuse(right_receiver_boss),
        "fused perpendicular holder",
    )

    pivot_x_min = left_outer_x - BOOLEAN_OVERSHOOT
    pivot_x_max = right_outer_x + BOOLEAN_OVERSHOOT
    pivot_bore = _cylinder_x(
        PEDAL_PIVOT_CLEARANCE_DIAMETER / 2.0,
        pivot_x_min,
        pivot_x_max,
    )

    left_hex_pocket = _hex_prism_x(
        PIVOT_HEX_POCKET_AF,
        left_outer_x - BOOLEAN_OVERSHOOT,
        PIVOT_HEX_POCKET_DEPTH + BOOLEAN_OVERSHOOT,
    )
    right_hex_pocket = _hex_prism_x(
        PIVOT_HEX_POCKET_AF,
        right_outer_x - PIVOT_HEX_POCKET_DEPTH,
        PIVOT_HEX_POCKET_DEPTH + BOOLEAN_OVERSHOOT,
    )

    ring_front_y = PUCK_CENTER_Y + HOLDER_THICKNESS / 2.0
    ring_back_y = PUCK_CENTER_Y - HOLDER_THICKNESS / 2.0
    ring_hole_positions = tuple(
        (x, PUCK_CENTER_Z + local_z)
        for x, local_z in TT25_MOUNTING_HOLE_POSITIONS
    )
    # The reversed puck seats its opposite lug face against the carrier's
    # negative-Y side. M3 screws enter from the outward logo side and remain
    # captured by these pockets on the carrier's positive-Y face.
    puck_nut_pockets = _hex_prisms_y(
        ring_hole_positions,
        PUCK_NUT_POCKET_AF,
        ring_front_y + BOOLEAN_OVERSHOOT,
        PUCK_NUT_POCKET_DEPTH + BOOLEAN_OVERSHOOT,
    )
    rear_cover_relief = _cylinder_y(
        TT25_REAR_COVER_RELIEF_DIAMETER / 2.0,
        ring_back_y - BOOLEAN_OVERSHOOT,
        ring_back_y + TT25_REAR_COVER_RELIEF_DEPTH,
        z=PUCK_CENTER_Z,
    )

    holder = _single_solid(
        holder_blank.cut(pivot_bore)
        .cut(left_hex_pocket)
        .cut(right_hex_pocket)
        .cut(puck_nut_pockets)
        .cut(rear_cover_relief),
        "finished perpendicular yoke holder",
    )
    holder.label = "moza_crp_dayton_tt25_perpendicular_yoke_holder"
    holder.color = HOLDER_COLOR

    return {
        "holder": holder,
        "holder_blank": holder_blank,
        "ring_blank": ring_blank,
        "left_arm": left_arm,
        "right_arm": right_arm,
        "left_receiver_boss": left_receiver_boss,
        "right_receiver_boss": right_receiver_boss,
        "pivot_bore": pivot_bore,
        "left_hex_pocket": left_hex_pocket,
        "right_hex_pocket": right_hex_pocket,
        "puck_nut_pockets": puck_nut_pockets,
        "rear_cover_relief": rear_cover_relief,
        "left_outer_x": left_outer_x,
        "left_arm_outer_x": left_arm_outer_x,
        "left_inner_x": -half_inner_span,
        "right_inner_x": half_inner_span,
        "right_arm_outer_x": right_arm_outer_x,
        "right_outer_x": right_outer_x,
        "ring_front_y": ring_front_y,
        "ring_back_y": ring_back_y,
    }


def gen_step():
    return build_holder_details()["holder"]
