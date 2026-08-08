"""Deterministic geometry checks for the centered-pair X2D dual-AMS mount."""

from __future__ import annotations

from math import isclose

from x2d_dual_ams_mount_assembly import build_assembly_details
from x2d_dual_ams_mount_geometry import (
    AMS_CENTER_X,
    AMS_FOOT_HEIGHT,
    AMS_FOOT_SIZE_X,
    AMS_FOOT_SIZE_Y,
    AMS_FOOT_SPACING_X,
    AMS_FOOT_SPACING_Y,
    AMS_PAIR_GAP,
    AMS_WIDTH,
    BRACKET_CHORD,
    BRACKET_Y_CENTERS,
    BRIDGE_CENTER_BOLT_Y_OFFSETS,
    BRIDGE_CENTER_BOSS_HALF_WIDTH,
    BRIDGE_CENTER_BOSS_HEIGHT,
    BRIDGE_DEPTH,
    BRIDGE_TOP_Z,
    BRIDGE_Y_CENTERS,
    M4_BUTTON_HEAD_DIAMETER,
    M4_BUTTON_HEAD_HEIGHT,
    M4_CLEARANCE_DIAMETER,
    M4_NUT_AF,
    PRINT_PART_LIMIT,
    SHELF_DEPTH,
    SHELF_OUTBOARD_MARGIN,
    SHELF_SPAN,
    X2D_GLASS_DEPTH,
    X2D_GLASS_WIDTH,
    _cylinder_x,
    _cylinder_z,
    ams_center_x,
    bracket_screw_xs,
    bridge_end_bolt_positions,
)


TOL = 1.0e-5
VOLUME_TOL = 1.0e-4


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS  {message}")


def close(a: float, b: float, tolerance: float = TOL) -> bool:
    return isclose(a, b, abs_tol=tolerance, rel_tol=0.0)


def overlap_volume(a, b) -> float:
    intersection = a & b
    return 0.0 if intersection is None else intersection.volume


def contains_xy(container, item, tolerance: float = TOL) -> bool:
    outer = container.bounding_box()
    inner = item.bounding_box()
    return (
        inner.min.X >= outer.min.X - tolerance
        and inner.max.X <= outer.max.X + tolerance
        and inner.min.Y >= outer.min.Y - tolerance
        and inner.max.Y <= outer.max.Y + tolerance
    )


def main() -> None:
    details = build_assembly_details()
    print_parts = details["print_parts"]

    check(len(print_parts) == 14, "assembly contains 14 individually printable ASA structural parts")
    for name, shape in print_parts.items():
        size = shape.bounding_box().size
        check(shape.is_valid, f"{name} is a valid B-rep")
        check(len(shape.solids()) == 1, f"{name} is one connected solid")
        check(
            max(size.X, size.Y, size.Z) <= PRINT_PART_LIMIT + TOL,
            f"{name} fits the 252 mm single-part envelope",
        )

    left_ams = details["ams_references"][-1]
    right_ams = details["ams_references"][1]
    left_box = left_ams["compound"].bounding_box()
    right_box = right_ams["compound"].bounding_box()
    check(close(ams_center_x(-1), -AMS_CENTER_X), "left AMS center is at X=-198.7 mm")
    check(close(ams_center_x(1), AMS_CENTER_X), "right AMS center is at X=+198.7 mm")
    check(close(right_box.min.X - left_box.max.X, AMS_PAIR_GAP), "AMS body-to-body gap is 25.4 mm")
    check(close(left_box.min.X + right_box.max.X, 0.0), "combined AMS pair is centered on the X2D top centerline")
    check(close(left_box.size.X, AMS_WIDTH), "left AMS reference retains the 372 mm published width")
    check(close(right_box.size.X, AMS_WIDTH), "right AMS reference retains the 372 mm published width")

    glass = details["x2d_reference"]["glass"]
    check(close(glass.bounding_box().size.X, X2D_GLASS_WIDTH), "provisional top glass reference is 350 mm wide")
    check(close(glass.bounding_box().size.Y, X2D_GLASS_DEPTH), "provisional top glass reference is 340 mm deep")

    for side in (-1, 1):
        shelf = details["shelves"][side]
        shelf_box = shelf.bounding_box()
        ams_box = details["ams_references"][side]["compound"].bounding_box()
        if side < 0:
            outboard_margin = ams_box.min.X - shelf_box.min.X
        else:
            outboard_margin = shelf_box.max.X - ams_box.max.X
        check(close(shelf_box.size.X, SHELF_SPAN), f"{side:+d} shelf is {SHELF_SPAN:.1f} mm outboard")
        check(close(shelf_box.size.Y, SHELF_DEPTH), f"{side:+d} shelf is 252 mm deep")
        check(
            close(outboard_margin, SHELF_OUTBOARD_MARGIN),
            f"{side:+d} shelf extends exactly 25.4 mm beyond its AMS outer face",
        )
        check(close(shelf_box.max.Z, 0.0), f"{side:+d} shelf support face remains at Z=0")

        feet = details["ams_references"][side]["feet"]
        check(len(feet) == 4, f"{side:+d} AMS reference has four provisional feet")
        for foot in feet:
            box = foot.bounding_box()
            check(close(box.min.Z, 0.0), f"{foot.label} remains at the original top datum")
            check(close(box.max.Z, AMS_FOOT_HEIGHT), f"{foot.label} retains the provisional 4 mm foot height")
            check(close(box.size.X, AMS_FOOT_SIZE_X), f"{foot.label} uses the provisional 24 mm foot width")
            check(close(box.size.Y, AMS_FOOT_SIZE_Y), f"{foot.label} uses the provisional 20 mm foot depth")
            if abs(box.center().X) < X2D_GLASS_WIDTH / 2.0:
                check(contains_xy(glass, foot), f"{foot.label} is fully supported on the modeled X2D top")
            else:
                check(contains_xy(shelf, foot), f"{foot.label} is fully supported by its outboard shelf")

    check(close(AMS_FOOT_SPACING_X, 320.0), "provisional AMS foot spacing is 320 mm side-to-side")
    check(close(AMS_FOOT_SPACING_Y, 220.0), "provisional AMS foot spacing is 220 mm front-to-back")
    check(close(BRACKET_CHORD, 25.4), "triangle bracket outer chord is exactly 1 inch (25.4 mm)")
    check(close(M4_CLEARANCE_DIAMETER, 4.5), "M4 through-hole allowance is 4.5 mm")
    check(close(M4_BUTTON_HEAD_DIAMETER, 8.2), "M4 button-head envelope is 8.2 mm")
    check(close(M4_NUT_AF, 7.4), "captive M4 nut allowance is 7.4 mm across flats")

    # Bracket fastener paths remain fully open through the shelf and bracket.
    for side in (-1, 1):
        for y in BRACKET_Y_CENTERS:
            shelf = details["shelves"][side]
            bracket = details["brackets"][(side, y)]
            hardware = details["bracket_hardware"][(side, y)]
            for x in bracket_screw_xs(side):
                probe = _cylinder_z(M4_CLEARANCE_DIAMETER / 2.0, -32.0, 1.0, x, y)
                check(overlap_volume(shelf, probe) <= VOLUME_TOL, f"shelf M4 bracket hole is open at x={x:.1f}, y={y:.1f}")
                check(overlap_volume(bracket, probe) <= VOLUME_TOL, f"bracket M4 hole is open at x={x:.1f}, y={y:.1f}")
                # Material at the old 8.2 mm counterbore radius must now run
                # continuously to the shelf top around each 4.5 mm hole.
                annulus_probe = _cylinder_z(0.25, -2.0, 0.0, x + 3.2, y)
                check(
                    close(overlap_volume(shelf, annulus_probe), annulus_probe.volume),
                    f"shelf bracket hole has no head recess at x={x:.1f}, y={y:.1f}",
                )
            check(
                close(hardware.bounding_box().max.Z, M4_BUTTON_HEAD_HEIGHT),
                f"bracket button heads at y={y:.1f} stand above the shelf",
            )
            check(
                overlap_volume(shelf, hardware) <= VOLUME_TOL,
                f"bracket hardware at y={y:.1f} clears the plain shelf holes",
            )

    # Low tie lands align to their shelf holes and keep heads below Z=3 mm.
    for beam in ("front", "rear"):
        beam_y = BRIDGE_Y_CENTERS[0] if beam == "front" else BRIDGE_Y_CENTERS[1]
        for side in (-1, 1):
            shelf = details["shelves"][side]
            tie = details["bridge_segments"][(beam, side)]
            for x, y in bridge_end_bolt_positions(side, beam_y):
                clearance = _cylinder_z(M4_CLEARANCE_DIAMETER / 2.0, -13.0, 4.0, x, y)
                head = _cylinder_z(
                    M4_BUTTON_HEAD_DIAMETER / 2.0,
                    BRIDGE_TOP_Z - M4_BUTTON_HEAD_HEIGHT,
                    BRIDGE_TOP_Z + 1.0,
                    x,
                    y,
                )
                check(overlap_volume(shelf, clearance) <= VOLUME_TOL, f"{beam}/{side:+d} shelf tie hole is open")
                check(overlap_volume(tie, clearance) <= VOLUME_TOL, f"{beam}/{side:+d} printed tie hole is open")
                check(overlap_volume(tie, head) <= VOLUME_TOL, f"{beam}/{side:+d} tie button-head recess is open")

        left = details["bridge_segments"][(beam, -1)]
        right = details["bridge_segments"][(beam, 1)]
        check(overlap_volume(left, right) <= VOLUME_TOL, f"{beam} center bosses assemble without interference")
        center_z = BRIDGE_CENTER_BOSS_HEIGHT / 2.0
        for offset in BRIDGE_CENTER_BOLT_Y_OFFSETS:
            probe = _cylinder_x(
                M4_CLEARANCE_DIAMETER / 2.0,
                -BRIDGE_CENTER_BOSS_HALF_WIDTH - 1.0,
                BRIDGE_CENTER_BOSS_HALF_WIDTH + 1.0,
                beam_y + offset,
                center_z,
            )
            check(overlap_volume(left, probe) <= VOLUME_TOL, f"{beam} left center-boss M4 hole is open at Y offset {offset:+.0f}")
            check(overlap_volume(right, probe) <= VOLUME_TOL, f"{beam} right center-boss M4 hole is open at Y offset {offset:+.0f}")

    check(close(BRIDGE_DEPTH, 50.0), "each low-profile tie is 50 mm front-to-back")
    check(close(BRIDGE_TOP_Z, 3.0), "planar tie spans remain at or below Z=3 mm")
    check(close(BRIDGE_CENTER_BOSS_HALF_WIDTH, 9.0), "each center boss stays inside its half of the 25.4 mm AMS gap")

    door_closed = details["x2d_reference"]["door_closed"]
    door_open = details["x2d_reference"]["door_open"]
    body = details["x2d_reference"]["body"]
    for tie in details["bridge_segments"].values():
        check(overlap_volume(tie, glass) <= VOLUME_TOL, f"{tie.label} does not penetrate the modeled top glass")
        check(overlap_volume(tie, door_closed) <= VOLUME_TOL, f"{tie.label} clears the closed front door")
        check(overlap_volume(tie, door_open) <= VOLUME_TOL, f"{tie.label} clears the modeled open-door sweep")
        for side in (-1, 1):
            ams = details["ams_references"][side]
            for envelope in (ams["lower"], ams["lid"], *ams["feet"]):
                check(overlap_volume(tie, envelope) <= VOLUME_TOL, f"{tie.label} clears {envelope.label}")

    non_contact_parts = [
        *details["shelves"].values(),
        *details["brackets"].values(),
        *details["bridge_segments"].values(),
    ]
    for part in non_contact_parts:
        check(overlap_volume(part, body) <= VOLUME_TOL, f"{part.label} does not penetrate the X2D envelope")

    final_box = details["final"].bounding_box()
    print(
        "ASSEMBLY_BOUNDS "
        f"{final_box.size.X:.3f} x {final_box.size.Y:.3f} x {final_box.size.Z:.3f} mm"
    )
    print("VALIDATION COMPLETE")


if __name__ == "__main__":
    main()
