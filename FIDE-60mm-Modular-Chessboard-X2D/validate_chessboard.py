"""Deterministic source-level checks for the modular chessboard geometry."""

from __future__ import annotations

import json
from math import sqrt

from build123d import Location

from chessboard_geometry import (
    ANTI_LIP_DEPTH_CLEARANCE,
    ANTI_LIP_GROOVE_HEIGHT,
    ANTI_LIP_GROOVE_LENGTH,
    ANTI_LIP_KEY_HEIGHT,
    ANTI_LIP_KEY_LENGTH,
    ANTI_LIP_KEY_POSITIONS,
    BRIDGE_LENGTH,
    BRIDGE_THICKNESS,
    BRIDGE_WIDTH,
    CORNER_LOCK_NUT_Y,
    CORNER_LOCK_RAILS,
    CORNER_LOCK_Z,
    CORNER_MITER_CLEARANCE,
    CORNER_RIB_PROJECTION,
    CORNER_RIB_WIDTH,
    CORNER_TENON_CLEARANCE,
    CORNER_TENON_DEPTH,
    CORNER_TENON_HEIGHT,
    DARK_COLOR,
    ELEPHANT_FOOT_RELIEF,
    FACE_INLAY_THICKNESS,
    FIT_LEAD_CHAMFER,
    GROOVE_DEPTH,
    JOIN_CLEARANCE,
    LOOSE_DARK_SQUARE_SIZE,
    M2_CLEARANCE_DIAMETER,
    M2_HEAD_RECESS_DEPTH,
    M2_NUT_ACROSS_FLATS,
    M2_NUT_POCKET_ACROSS_FLATS,
    M2_NUT_POCKET_THICKNESS,
    M2_NUT_THICKNESS,
    M2_SCREW_LENGTH,
    M3_NUT_ACROSS_FLATS,
    M3_NUT_THICKNESS,
    NUT_POCKET_ACROSS_FLATS,
    NUT_POCKET_HEIGHT,
    NUT_POCKET_Z,
    NOTATION_ROTATION_BY_SIDE,
    OUTER_SIZE,
    PANEL_BASE_THICKNESS,
    PERIMETER_RISE,
    PERIMETER_TOP_EDGE_FILLET_RADIUS,
    PERIMETER_TOP_Z,
    PERIMETER_WIDTH,
    PLAYING_SIZE,
    PLAYING_SURFACE_Z,
    QUARTER_ROLES,
    QUARTER_SIZE,
    RAIL_SPECS,
    SCREW_TIP_Z,
    SQUARE_SIZE,
    TONGUE_PROJECTION,
    UNDERSIDE_DEPTH,
    _corner_core_local,
    _corner_placements,
    _corner_tenon_profile_points,
    _cylinder_along_axis,
    _hex_prism_along_axis,
    _polygon_prism,
    _rail_corner_rib,
    make_corner_cap,
    make_full_assembly,
    make_loose_dark_square_inlay,
    make_notation_insert_print_set,
    make_quarter_details,
    make_rail_details,
    make_seam_bridge,
)


TOLERANCE = 1e-4


def _close(actual: float, expected: float, label: str, tolerance: float = TOLERANCE):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def _volume(shape) -> float:
    if shape is None:
        return 0.0
    return sum(solid.volume for solid in shape.solids())


def _intersection_volume(first, second) -> float:
    return _volume(first.intersect(second))


def _radius_face_count(shape, radius: float) -> int:
    return sum(
        1
        for face in shape.faces()
        if getattr(face, "radius", None) is not None
        and abs(face.radius - radius) <= TOLERANCE
    )


def _sloped_face_count(shape) -> int:
    count = 0
    for face in shape.faces():
        if "PLANE" not in str(face.geom_type).upper():
            continue
        normal = face.normal_at()
        components = (abs(normal.X), abs(normal.Y), abs(normal.Z))
        if sum(component > 1e-3 for component in components) >= 2:
            count += 1
    return count


def _quarter_location(role: str):
    return Location(
        (
            -QUARTER_SIZE / 2.0 if role.endswith("w") else QUARTER_SIZE / 2.0,
            -QUARTER_SIZE / 2.0 if role.startswith("s") else QUARTER_SIZE / 2.0,
            0.0,
        )
    )


def main():
    if not 50.0 <= SQUARE_SIZE <= 60.0:
        raise AssertionError("Square size is outside the current FIDE 50-60 mm range")
    _close(PLAYING_SIZE, 480.0, "playing area")
    _close(OUTER_SIZE, 520.0, "outer board size")
    _close(PERIMETER_WIDTH, 20.0, "perimeter width")
    _close(PERIMETER_TOP_Z - PLAYING_SURFACE_Z, PERIMETER_RISE, "raised perimeter")
    _close(PERIMETER_RISE, 10.0, "perimeter rise")
    _close(PLAYING_SURFACE_Z, 9.6, "playing surface height")
    _close(JOIN_CLEARANCE, 0.25, "tongue/groove depth clearance")
    _close(GROOVE_DEPTH - TONGUE_PROJECTION, 0.25, "joinery clearance derivation")
    _close(FIT_LEAD_CHAMFER, 0.5, "fit lead-in chamfer")
    _close(ELEPHANT_FOOT_RELIEF, 0.4, "first-layer relief")
    _close(CORNER_MITER_CLEARANCE, 0.3, "corner miter clearance")
    _close(CORNER_TENON_CLEARANCE, 0.25, "corner mortise clearance")
    _close(CORNER_TENON_DEPTH, 2.5, "corner tenon depth")
    _close(CORNER_TENON_HEIGHT, 5.0, "corner tenon height")
    _close(CORNER_RIB_WIDTH, 14.0, "corner core width")
    _close(ANTI_LIP_DEPTH_CLEARANCE, 0.25, "upper-key depth clearance")
    _close(
        ANTI_LIP_GROOVE_HEIGHT - ANTI_LIP_KEY_HEIGHT,
        0.4,
        "upper-key vertical clearance",
    )
    _close(
        ANTI_LIP_GROOVE_LENGTH - ANTI_LIP_KEY_LENGTH,
        0.4,
        "upper-key lateral clearance",
    )
    if len(ANTI_LIP_KEY_POSITIONS) != 2:
        raise AssertionError("Each internal quarter edge must have two upper keys")

    quarter_details = {}
    quarter_summary = {}
    for role in QUARTER_ROLES:
        details = make_quarter_details(role)
        quarter_details[role] = details
        light = details["light_body"]
        dark = details["dark_inlays"]
        bounds = light.bounding_box()
        if bounds.size.X > 244.01 or bounds.size.Y > 244.01:
            raise AssertionError(f"Quarter {role} exceeds its 244 mm print envelope")
        if bounds.size.X > 256.0 or bounds.size.Y > 256.0:
            raise AssertionError(f"Quarter {role} exceeds the X2D main-nozzle bed")
        _close(bounds.min.Z, 0.0, f"quarter {role} bottom")
        _close(bounds.max.Z, PLAYING_SURFACE_Z, f"quarter {role} top")
        if len(light.solids()) != 1:
            raise AssertionError(f"Quarter {role} light body is not monolithic")
        if len(dark.solids()) != 8:
            raise AssertionError(f"Quarter {role} does not contain eight dark tiles")
        if _sloped_face_count(light) < 8:
            raise AssertionError(f"Quarter {role} is missing fit chamfer faces")
        _close(_intersection_volume(light, dark), 0.0, f"quarter {role} color-body overlap", 1e-3)
        for index, tile in enumerate(dark.solids(), start=1):
            tile_bounds = tile.bounding_box()
            _close(tile_bounds.size.X, SQUARE_SIZE, f"quarter {role} dark tile {index} X")
            _close(tile_bounds.size.Y, SQUARE_SIZE, f"quarter {role} dark tile {index} Y")
            _close(tile_bounds.size.Z, FACE_INLAY_THICKNESS, f"quarter {role} dark tile {index} Z")
            _close(tile_bounds.min.Z, PANEL_BASE_THICKNESS, f"quarter {role} tile seat")
        quarter_summary[role] = {
            "bbox": [bounds.size.X, bounds.size.Y, bounds.size.Z],
            "dark_tiles": len(dark.solids()),
            "edges": details["edge_plan"],
            "upper_keys": 2 * list(details["edge_plan"].values()).count("male"),
            "upper_grooves": 2
            * list(details["edge_plan"].values()).count("female"),
        }

    # Representative assembled interfaces: no positive-volume interference;
    # distance zero confirms the bodies still meet at their intended datums.
    sw = quarter_details["sw"]["light_body"].moved(_quarter_location("sw"))
    se = quarter_details["se"]["light_body"].moved(_quarter_location("se"))
    nw = quarter_details["nw"]["light_body"].moved(_quarter_location("nw"))
    _close(_intersection_volume(sw, se), 0.0, "south row panel interference", 1e-3)
    _close(_intersection_volume(sw, nw), 0.0, "west column panel interference", 1e-3)
    _close(sw.distance_to(se), 0.0, "south row panel contact", 1e-3)
    _close(sw.distance_to(nw), 0.0, "west column panel contact", 1e-3)

    rail_summary = {}
    rail_details = {}
    expected_notation_rotations = {
        "south": 0.0,
        "north": 180.0,
        "west": 180.0,
        "east": 0.0,
    }
    if NOTATION_ROTATION_BY_SIDE != expected_notation_rotations:
        raise AssertionError(
            "Notation rotations must face the east ranks toward White and "
            "the west ranks toward Black"
        )
    for name in RAIL_SPECS:
        details = make_rail_details(name)
        rail_details[name] = details
        body = details["body"]
        inlays = details["notation_inlays"]
        bounds = body.bounding_box()
        if max(bounds.size.X, bounds.size.Y) > 247.1:
            raise AssertionError(f"Rail {name} exceeds its 247.1 mm print envelope")
        if max(bounds.size.X, bounds.size.Y) > 256.0:
            raise AssertionError(f"Rail {name} exceeds the X2D main-nozzle bed")
        if len(body.solids()) != 1:
            raise AssertionError(f"Rail {name} is not monolithic")
        if len(inlays.solids()) != 4:
            raise AssertionError(f"Rail {name} does not contain four glyphs")
        _close(
            details["notation_rotation_deg"],
            expected_notation_rotations[details["spec"].side],
            f"rail {name} notation rotation",
        )
        if _sloped_face_count(body) < 8:
            raise AssertionError(f"Rail {name} is missing fit chamfer faces")
        if _radius_face_count(body, PERIMETER_TOP_EDGE_FILLET_RADIUS) != 2:
            raise AssertionError(
                f"Rail {name} does not have two exposed top-edge fillets"
            )
        _close(bounds.min.Z, -UNDERSIDE_DEPTH, f"rail {name} bottom")
        _close(bounds.max.Z, PERIMETER_TOP_Z, f"rail {name} top")
        _close(_intersection_volume(body, inlays), 0.0, f"rail {name} notation overlap", 1e-3)
        rail_summary[name] = {
            "bbox": [bounds.size.X, bounds.size.Y, bounds.size.Z],
            "glyphs": list(details["spec"].symbols),
            "notation_rotation_deg": details["notation_rotation_deg"],
        }

    bottom_rail = rail_details["bottom_ad"]["body"]
    _close(_intersection_volume(sw, bottom_rail), 0.0, "quarter/perimeter interference", 1e-3)
    _close(sw.distance_to(bottom_rail), 0.0, "quarter/perimeter contact", 1e-3)

    bridge = make_seam_bridge()
    bridge_bounds = bridge.bounding_box()
    _close(bridge_bounds.size.X, BRIDGE_LENGTH, "bridge length")
    _close(bridge_bounds.size.Y, BRIDGE_WIDTH, "bridge width")
    _close(bridge_bounds.size.Z, BRIDGE_THICKNESS, "bridge thickness")
    if len(bridge.solids()) != 1:
        raise AssertionError("Seam bridge is not one solid")

    corner = make_corner_cap()
    corner_bounds = corner.bounding_box()
    _close(corner_bounds.size.X, PERIMETER_WIDTH, "corner width X")
    _close(corner_bounds.size.Y, PERIMETER_WIDTH, "corner width Y")
    if len(corner.solids()) != 1:
        raise AssertionError("Corner cap is not one solid")
    if _radius_face_count(corner, PERIMETER_TOP_EDGE_FILLET_RADIUS) != 2:
        raise AssertionError("Corner cap does not have two exposed top-edge fillets")
    if _sloped_face_count(corner) < 6:
        raise AssertionError("Corner cap is missing fit chamfer faces")
    corner_pairs = {
        "sw": ("bottom_ad", "left_14"),
        "se": ("right_14", "bottom_eh"),
        "ne": ("top_eh", "right_58"),
        "nw": ("left_58", "top_ad"),
    }
    for role, (locking_name, mating_name) in corner_pairs.items():
        locking_rail = rail_details[locking_name]["body"]
        mating_rail = rail_details[mating_name]["body"]
        placed_corner = corner.moved(_corner_placements()[role])
        _close(
            _intersection_volume(locking_rail, mating_rail),
            0.0,
            f"{role} rail/rail interference",
            1e-3,
        )
        _close(
            locking_rail.distance_to(mating_rail),
            0.0,
            f"{role} rail/rail contact",
            1e-3,
        )
        for rail_name, rail in (
            (locking_name, locking_rail),
            (mating_name, mating_rail),
        ):
            _close(
                _intersection_volume(placed_corner, rail),
                0.0,
                f"{role} corner/{rail_name} interference",
                1e-3,
            )

    tenon_probe = _polygon_prism(
        _corner_tenon_profile_points(),
        CORNER_TENON_HEIGHT,
        -UNDERSIDE_DEPTH,
    )
    mortised_core = _corner_core_local("y")
    _close(
        _intersection_volume(tenon_probe, mortised_core),
        0.0,
        "corner tenon/mortise interference",
        1e-3,
    )
    _close(
        tenon_probe.distance_to(mortised_core),
        CORNER_TENON_CLEARANCE / sqrt(2.0),
        "corner tenon/mortise diagonal clearance",
        1e-3,
    )

    sw_corner = corner.moved(_corner_placements()["sw"])

    # Representative southwest M2 corner lock: the top-loaded nut fits its
    # rail-rib pocket and the cross-screw path is clear through cap and rib.
    if "bottom_ad" not in CORNER_LOCK_RAILS:
        raise AssertionError("Southwest corner-lock rail is not configured")
    lock_rib_center_x = -QUARTER_SIZE - CORNER_RIB_PROJECTION / 2.0
    bottom_rib = _rail_corner_rib(RAIL_SPECS["bottom_ad"], -250.0)
    m2_nut = _hex_prism_along_axis(
        M2_NUT_ACROSS_FLATS,
        M2_NUT_THICKNESS,
        "y",
        (
            lock_rib_center_x,
            -250.0 + CORNER_LOCK_NUT_Y,
            CORNER_LOCK_Z,
        ),
    )
    _close(
        _intersection_volume(bottom_rib, m2_nut),
        0.0,
        "M2 nut/rail-rib pocket interference",
        1e-3,
    )
    lock_probe = _cylinder_along_axis(
        M2_CLEARANCE_DIAMETER / 2.0 - 0.08,
        14.0,
        "y",
        (lock_rib_center_x, -253.0, CORNER_LOCK_Z),
    )
    lock_union = sw_corner.fuse(rail_details["bottom_ad"]["body"])
    _close(
        _intersection_volume(lock_union, lock_probe),
        0.0,
        "M2 corner-lock screw-path obstruction",
        1e-3,
    )
    m2_screw_seat = -PERIMETER_WIDTH / 2.0 + M2_HEAD_RECESS_DEPTH
    m2_screw_tip = m2_screw_seat + M2_SCREW_LENGTH
    m2_nut_far_face = CORNER_LOCK_NUT_Y + M2_NUT_POCKET_THICKNESS / 2.0
    if not m2_screw_tip > m2_nut_far_face:
        raise AssertionError("M2 x 12 screw does not pass through the captured nut")

    loose_inlay = make_loose_dark_square_inlay()
    loose_bounds = loose_inlay.bounding_box()
    _close(loose_bounds.size.X, LOOSE_DARK_SQUARE_SIZE, "loose dark inlay X")
    _close(loose_bounds.size.Y, LOOSE_DARK_SQUARE_SIZE, "loose dark inlay Y")
    if not loose_bounds.size.X < SQUARE_SIZE:
        raise AssertionError("Loose inlay has no lateral fit clearance")

    notation_set = make_notation_insert_print_set()
    if len(notation_set.solids()) != 32:
        raise AssertionError("Notation set must contain 32 glyph inserts")

    if NUT_POCKET_ACROSS_FLATS <= M3_NUT_ACROSS_FLATS:
        raise AssertionError("Nut pocket has no across-flats clearance")
    if NUT_POCKET_HEIGHT <= M3_NUT_THICKNESS:
        raise AssertionError("Nut pocket has no thickness clearance")
    if not NUT_POCKET_Z < SCREW_TIP_Z <= PANEL_BASE_THICKNESS:
        raise AssertionError("M3 x 12 screw tip is outside the blind nut region")

    assembly = make_full_assembly()
    bounds = assembly.bounding_box()
    _close(bounds.size.X, OUTER_SIZE, "assembled X envelope")
    _close(bounds.size.Y, OUTER_SIZE, "assembled Y envelope")
    _close(bounds.min.Z, -UNDERSIDE_DEPTH, "assembled bottom")
    _close(bounds.max.Z, PERIMETER_TOP_Z, "assembled top")
    if len(assembly.children) != 24:
        raise AssertionError(f"Expected 24 top-level occurrences, got {len(assembly.children)}")
    if len(assembly.solids()) != 88:
        raise AssertionError(f"Expected 88 assembly solids, got {len(assembly.solids())}")
    if _radius_face_count(assembly, PERIMETER_TOP_EDGE_FILLET_RADIUS) != 24:
        raise AssertionError("Assembly does not contain all 24 exposed border fillets")

    report = {
        "status": "passed",
        "square_mm": SQUARE_SIZE,
        "playing_area_mm": [PLAYING_SIZE, PLAYING_SIZE],
        "outer_envelope_mm": [bounds.size.X, bounds.size.Y, bounds.size.Z],
        "perimeter_rise_mm": PERIMETER_RISE,
        "perimeter_top_edge_fillet": {
            "radius_mm": PERIMETER_TOP_EDGE_FILLET_RADIUS,
            "rounded_edges": 24,
        },
        "fit_refinements": {
            "lead_in_chamfer_mm": FIT_LEAD_CHAMFER,
            "first_layer_relief_mm": ELEPHANT_FOOT_RELIEF,
            "upper_keys_per_internal_edge": len(ANTI_LIP_KEY_POSITIONS),
            "upper_key_depth_clearance_mm": ANTI_LIP_DEPTH_CLEARANCE,
            "corner_miter_clearance_mm": CORNER_MITER_CLEARANCE,
            "corner_tenon_depth_mm": CORNER_TENON_DEPTH,
            "corner_mortise_nominal_clearance_mm": CORNER_TENON_CLEARANCE,
        },
        "join_clearance_mm": JOIN_CLEARANCE,
        "quarters": quarter_summary,
        "rails": rail_summary,
        "hardware": {
            "m3_x_12_screws": 32,
            "m3_nuts": 32,
            "nut_across_flats_clearance_mm": NUT_POCKET_ACROSS_FLATS - M3_NUT_ACROSS_FLATS,
            "nut_thickness_clearance_mm": NUT_POCKET_HEIGHT - M3_NUT_THICKNESS,
            "screw_tip_z_mm": SCREW_TIP_Z,
            "m2_x_12_corner_screws": 4,
            "m2_corner_nuts": 4,
            "m2_nut_across_flats_clearance_mm": M2_NUT_POCKET_ACROSS_FLATS
            - M2_NUT_ACROSS_FLATS,
            "m2_nut_thickness_clearance_mm": M2_NUT_POCKET_THICKNESS
            - M2_NUT_THICKNESS,
        },
        "assembly": {
            "top_level_occurrences": len(assembly.children),
            "solids": len(assembly.solids()),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
