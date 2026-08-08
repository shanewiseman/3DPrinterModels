"""Deterministic checks for the eight-panel chessboard variant."""

from __future__ import annotations

import json
import re
from pathlib import Path
from tempfile import TemporaryDirectory

from build123d import Compound, Location, export_stl

from chessboard_geometry import (
    FACE_INLAY_THICKNESS,
    OUTER_SIZE,
    PANEL_BASE_THICKNESS,
    PLAYING_SIZE,
    PLAYING_SURFACE_Z,
    RAIL_SPECS,
    SQUARE_SIZE,
    _corner_placements,
    make_corner_cap,
    make_rail_details,
    make_seam_bridge,
)
from eight_panel_geometry import (
    CHECKER_VERTEX_RELIEF_SIZE,
    EIGHT_PANEL_ROLES,
    PANEL_HEIGHT,
    PANEL_M3_CLEARANCE_DIAMETER,
    PANEL_NUT_ENTRY_WIDTH,
    PANEL_NUT_POCKET_ACROSS_FLATS,
    PANEL_WIDTH,
    make_eight_panel_details,
    panel_assembly_location,
)
from validate_stl_watertightness import _mesh_edge_counts
from eight_panel_print_kit import (
    PANEL_LOCAL_X,
    PLATE_CENTERS,
    VIRTUAL_PLATE_SIZE,
    make_eight_panel_print_kit_groups,
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


def _bbox_xy_overlap(first, second) -> bool:
    a = first.bounding_box()
    b = second.bounding_box()
    overlap_x = min(a.max.X, b.max.X) - max(a.min.X, b.min.X)
    overlap_y = min(a.max.Y, b.max.Y) - max(a.min.Y, b.min.Y)
    return overlap_x > TOLERANCE and overlap_y > TOLERANCE


def main():
    _close(PANEL_WIDTH, 120.0, "panel nominal width")
    _close(PANEL_HEIGHT, 240.0, "panel nominal height")
    _close(PANEL_NUT_ENTRY_WIDTH, 6.1, "panel nut entry width")
    _close(PANEL_M3_CLEARANCE_DIAMETER, 3.6, "panel screw passage diameter")
    _close(PANEL_NUT_POCKET_ACROSS_FLATS, 5.8, "panel hex pocket across flats")
    _close(CHECKER_VERTEX_RELIEF_SIZE, 0.2, "checker vertex mesh relief")
    _close(PLAYING_SIZE, 480.0, "playing area")
    _close(OUTER_SIZE, 520.0, "outer board footprint")
    if len(EIGHT_PANEL_ROLES) != 8:
        raise AssertionError("Eight-panel role inventory is not eight")

    details_by_name = {}
    panel_report = {}
    panel_step_product_names = {}
    with TemporaryDirectory(prefix="eight-panel-mesh-check-") as temp_directory:
        mesh_root = Path(temp_directory)
        for name in EIGHT_PANEL_ROLES:
            details = make_eight_panel_details(name)
            details_by_name[name] = details
            body = details["light_body"]
            dark = details["dark_inlays"]
            bounds = body.bounding_box()
            if bounds.size.X > 124.01 or bounds.size.Y > 244.01:
                raise AssertionError(f"Panel {name} exceeds 124 x 244 mm envelope")
            _close(bounds.min.Z, 0.0, f"panel {name} build plane")
            _close(bounds.max.Z, PLAYING_SURFACE_Z, f"panel {name} playing height")
            if len(body.solids()) != 1 or not body.is_valid:
                raise AssertionError(f"Panel {name} is not one valid solid")

            mesh_path = mesh_root / f"{name}.stl"
            export_stl(
                body,
                mesh_path,
                tolerance=0.02,
                angular_tolerance=0.05,
            )
            triangle_count, mesh_edges = _mesh_edge_counts(mesh_path)
            nonmanifold_edges = {
                edge: count for edge, count in mesh_edges.items() if count != 2
            }
            if nonmanifold_edges:
                raise AssertionError(
                    f"Panel {name} mesh contains {len(nonmanifold_edges)} "
                    "non-manifold edges"
                )

            if len(dark.solids()) != 4:
                raise AssertionError(f"Panel {name} does not contain four dark tiles")
            _close(
                _intersection_volume(body, dark),
                0.0,
                f"panel {name} body/dark overlap",
                1e-3,
            )
            for index, tile in enumerate(dark.solids(), start=1):
                tile_bounds = tile.bounding_box()
                _close(tile_bounds.size.X, SQUARE_SIZE, f"{name} tile {index} X")
                _close(tile_bounds.size.Y, SQUARE_SIZE, f"{name} tile {index} Y")
                _close(
                    tile_bounds.size.Z,
                    FACE_INLAY_THICKNESS,
                    f"{name} tile {index} Z",
                )
                _close(
                    tile_bounds.min.Z,
                    PANEL_BASE_THICKNESS,
                    f"{name} tile {index} seat",
                )
            panel_report[name] = {
                "bbox_mm": [bounds.size.X, bounds.size.Y, bounds.size.Z],
                "edges": details["edge_plan"],
                "dark_tiles": len(dark.solids()),
                "mesh_triangles": triangle_count,
                "mesh_nonmanifold_edges": len(nonmanifold_edges),
            }

    for name in EIGHT_PANEL_ROLES:
        expected_name = f"panel_{name}_light_body"
        step_path = Path(f"{expected_name}.step")
        step_text = step_path.read_text(encoding="utf-8")
        product_match = re.search(
            r"#\d+\s*=\s*PRODUCT\(\s*'([^']*)'",
            step_text,
            flags=re.MULTILINE,
        )
        if product_match is None:
            raise AssertionError(f"No STEP PRODUCT name found in {step_path}")
        product_name = product_match.group(1)
        if product_name != expected_name:
            raise AssertionError(
                f"{step_path} top-level product is {product_name!r}, "
                f"expected {expected_name!r}"
            )
        if "=>[" in step_text:
            raise AssertionError(
                f"{step_path} contains an unnamed OpenCascade occurrence"
            )
        panel_step_product_names[name] = product_name

    placed_bodies = {
        name: details_by_name[name]["light_body"].moved(panel_assembly_location(name))
        for name in EIGHT_PANEL_ROLES
    }
    rows = ("south", "north")
    columns = ("ab", "cd", "ef", "gh")
    interface_checks = 0
    for row in rows:
        for west_column, east_column in zip(
            columns[:-1], columns[1:], strict=True
        ):
            west = placed_bodies[f"{row}_{west_column}"]
            east = placed_bodies[f"{row}_{east_column}"]
            _close(
                _intersection_volume(west, east),
                0.0,
                f"{row} {west_column}/{east_column} interference",
                1e-3,
            )
            _close(
                west.distance_to(east),
                0.0,
                f"{row} {west_column}/{east_column} contact",
                1e-3,
            )
            interface_checks += 1
    for column in columns:
        south = placed_bodies[f"south_{column}"]
        north = placed_bodies[f"north_{column}"]
        _close(
            _intersection_volume(south, north),
            0.0,
            f"{column} south/north interference",
            1e-3,
        )
        _close(
            south.distance_to(north),
            0.0,
            f"{column} south/north contact",
            1e-3,
        )
        interface_checks += 1

    rail_details = {name: make_rail_details(name) for name in RAIL_SPECS}
    rail_contacts = (
        ("bottom_ad", "south_ab"),
        ("bottom_ad", "south_cd"),
        ("bottom_eh", "south_ef"),
        ("bottom_eh", "south_gh"),
        ("top_ad", "north_ab"),
        ("top_ad", "north_cd"),
        ("top_eh", "north_ef"),
        ("top_eh", "north_gh"),
        ("left_14", "south_ab"),
        ("left_58", "north_ab"),
        ("right_14", "south_gh"),
        ("right_58", "north_gh"),
    )
    for rail_name, panel_name in rail_contacts:
        rail = rail_details[rail_name]["body"]
        panel = placed_bodies[panel_name]
        _close(
            _intersection_volume(rail, panel),
            0.0,
            f"{rail_name}/{panel_name} interference",
            1e-3,
        )
        _close(
            rail.distance_to(panel),
            0.0,
            f"{rail_name}/{panel_name} contact",
            1e-3,
        )

    assembly_children = []
    for name in EIGHT_PANEL_ROLES:
        location = panel_assembly_location(name)
        assembly_children.extend(
            (
                details_by_name[name]["light_body"].moved(location),
                details_by_name[name]["dark_inlays"].moved(location),
            )
        )
    for details in rail_details.values():
        assembly_children.extend((details["body"], details["notation_inlays"]))
    corner = make_corner_cap()
    assembly_children.extend(
        corner.moved(location) for location in _corner_placements().values()
    )
    bridge = make_seam_bridge()
    assembly_children.extend(
        bridge.moved(Location((seam_x, y_position, 0.0)))
        for seam_x in (-120.0, 0.0, 120.0)
        for y_position in (-180.0, -60.0, 60.0, 180.0)
    )
    assembly_children.extend(
        bridge.moved(Location((x_position, 0.0, 0.0), (0.0, 0.0, 90.0)))
        for x_position in (-180.0, -60.0, 60.0, 180.0)
    )
    full = Compound(children=assembly_children)
    full_bounds = full.bounding_box()
    _close(full_bounds.size.X, OUTER_SIZE, "assembled width")
    _close(full_bounds.size.Y, OUTER_SIZE, "assembled depth")
    if len(full.solids()) != 100:
        raise AssertionError(
            f"Expected 100 assembled leaf solids, found {len(full.solids())}"
        )

    groups = make_eight_panel_print_kit_groups()
    if tuple(groups) != tuple(PLATE_CENTERS):
        raise AssertionError("Print-kit group order does not match plate datums")
    if len(groups) != 13:
        raise AssertionError(f"Expected 13 print plates, found {len(groups)}")

    panel_clear_widths = {}
    component_count = 0
    for plate_name, components in groups.items():
        center_x, center_y = PLATE_CENTERS[plate_name]
        min_x = center_x - VIRTUAL_PLATE_SIZE / 2.0
        max_x = center_x + VIRTUAL_PLATE_SIZE / 2.0
        min_y = center_y - VIRTUAL_PLATE_SIZE / 2.0
        max_y = center_y + VIRTUAL_PLATE_SIZE / 2.0
        for component in components:
            bounds = component.bounding_box()
            _close(bounds.min.Z, 0.0, f"{component.label} bed position")
            if (
                bounds.min.X < min_x - TOLERANCE
                or bounds.max.X > max_x + TOLERANCE
                or bounds.min.Y < min_y - TOLERANCE
                or bounds.max.Y > max_y + TOLERANCE
            ):
                raise AssertionError(f"{component.label} exceeds {plate_name}")
            if plate_name.startswith("plate_0") and "_panel_" in plate_name:
                clear_width = max_x - bounds.max.X
                if clear_width < 120.0 - TOLERANCE:
                    raise AssertionError(
                        f"{component.label} leaves only {clear_width} mm for tower"
                    )
                panel_clear_widths[plate_name] = clear_width
            component_count += 1
        for index, first in enumerate(components):
            for second in components[index + 1 :]:
                if _bbox_xy_overlap(first, second):
                    raise AssertionError(
                        f"Overlapping print footprints on {plate_name}: "
                        f"{first.label} / {second.label}"
                    )

    if component_count != 68:
        raise AssertionError(f"Expected 68 printable objects, found {component_count}")
    print_kit_solid_count = sum(
        len(component.solids())
        for components in groups.values()
        for component in components
    )
    if print_kit_solid_count != 100:
        raise AssertionError("Print-kit leaf-solid count is incorrect")

    report = {
        "assembled_bbox_mm": [
            full_bounds.size.X,
            full_bounds.size.Y,
            full_bounds.size.Z,
        ],
        "assembled_leaf_solids": len(full.solids()),
        "interface_checks": interface_checks,
        "panel_clear_width_mm": panel_clear_widths,
        "panel_local_x_mm": PANEL_LOCAL_X,
        "panel_step_product_names": panel_step_product_names,
        "panels": panel_report,
        "print_kit_components": component_count,
        "print_kit_leaf_solids": print_kit_solid_count,
        "print_kit_plates": len(groups),
        "rail_contact_checks": len(rail_contacts),
        "rail_count": len(RAIL_SPECS),
        "status": "passed",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
