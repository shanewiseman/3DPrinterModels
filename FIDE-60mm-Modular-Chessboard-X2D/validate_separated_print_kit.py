"""Deterministic validation for the separated Bambu Studio print kit."""

from __future__ import annotations

import json

from build123d import Compound

from separated_print_kit import (
    PLATE_CENTERS,
    VIRTUAL_PLATE_SIZE,
    make_print_kit_plate_groups,
    make_separated_print_kit,
)


EXPECTED_PLATES = 9
EXPECTED_COMPONENTS = 56
EXPECTED_SOLIDS = 88
EXPECTED_COUNTS = {
    "playing_surface_body": 4,
    "multicolor_rail": 8,
    "dark_square_inlay": 32,
    "seam_bridge": 8,
    "corner_cap": 4,
}
EXPECTED_SOLIDS_PER_COMPONENT = {
    "playing_surface_body": 1,
    "multicolor_rail": 5,
    "dark_square_inlay": 1,
    "seam_bridge": 1,
    "corner_cap": 1,
}
TOLERANCE = 1e-6


def _close(actual: float, expected: float, label: str, tolerance: float = TOLERANCE):
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def _bbox_xy_overlap(first, second) -> bool:
    a = first.bounding_box()
    b = second.bounding_box()
    overlap_x = min(a.max.X, b.max.X) - max(a.min.X, b.min.X)
    overlap_y = min(a.max.Y, b.max.Y) - max(a.min.Y, b.min.Y)
    return overlap_x > TOLERANCE and overlap_y > TOLERANCE


def main():
    groups = make_print_kit_plate_groups()
    if len(groups) != EXPECTED_PLATES:
        raise AssertionError(f"Expected {EXPECTED_PLATES} plate groups, got {len(groups)}")
    if tuple(groups) != tuple(PLATE_CENTERS):
        raise AssertionError("Plate group order does not match PLATE_CENTERS")

    inventory = {key: 0 for key in EXPECTED_COUNTS}
    all_components = []
    plate_report = {}

    for plate_name, components in groups.items():
        plate_center_x, plate_center_y = PLATE_CENTERS[plate_name]
        plate_min_x = plate_center_x - VIRTUAL_PLATE_SIZE / 2.0
        plate_max_x = plate_center_x + VIRTUAL_PLATE_SIZE / 2.0
        plate_min_y = plate_center_y - VIRTUAL_PLATE_SIZE / 2.0
        plate_max_y = plate_center_y + VIRTUAL_PLATE_SIZE / 2.0

        for component in components:
            bounds = component.bounding_box()
            _close(bounds.min.Z, 0.0, f"{component.label} build-plane position")
            if bounds.min.X < plate_min_x - TOLERANCE or bounds.max.X > plate_max_x + TOLERANCE:
                raise AssertionError(f"{component.label} exceeds {plate_name} in X")
            if bounds.min.Y < plate_min_y - TOLERANCE or bounds.max.Y > plate_max_y + TOLERANCE:
                raise AssertionError(f"{component.label} exceeds {plate_name} in Y")
            prefix = str(component.label).split(":")[0]
            if prefix not in inventory:
                raise AssertionError(f"Unexpected component label: {component.label}")
            solid_count = len(component.solids())
            expected_solid_count = EXPECTED_SOLIDS_PER_COMPONENT[prefix]
            if solid_count != expected_solid_count:
                raise AssertionError(
                    f"{component.label}: expected {expected_solid_count} solids, "
                    f"got {solid_count}"
                )
            if prefix == "dark_square_inlay":
                _close(bounds.size.X, 59.6, f"{component.label} width")
                _close(bounds.size.Y, 59.6, f"{component.label} depth")
                _close(bounds.size.Z, 1.6, f"{component.label} thickness")
            elif prefix == "multicolor_rail":
                child_labels = [str(child.label).split(":")[0] for child in component.children]
                if child_labels != ["perimeter_body", "notation_inlays"]:
                    raise AssertionError(
                        f"{component.label}: unexpected rail part hierarchy {child_labels}"
                    )
                body_part, notation_part = component.children
                if len(body_part.solids()) != 1 or len(notation_part.solids()) != 4:
                    raise AssertionError(
                        f"{component.label}: rail must contain one body and four glyphs"
                    )
                if body_part.color == notation_part.color:
                    raise AssertionError(
                        f"{component.label}: rail body and notation colors are identical"
                    )
            inventory[prefix] += 1
            all_components.append(component)

        for first_index, first in enumerate(components):
            for second in components[first_index + 1 :]:
                if _bbox_xy_overlap(first, second):
                    raise AssertionError(
                        f"Overlapping print footprints on {plate_name}: "
                        f"{first.label} / {second.label}"
                    )

        group_bounds = Compound(children=components).bounding_box()
        plate_report[plate_name] = {
            "components": len(components),
            "solids": sum(len(component.solids()) for component in components),
            "footprint_mm": [group_bounds.size.X, group_bounds.size.Y],
            "height_mm": group_bounds.size.Z,
        }

    if inventory != EXPECTED_COUNTS:
        raise AssertionError(f"Inventory mismatch: expected {EXPECTED_COUNTS}, got {inventory}")
    if len(all_components) != EXPECTED_COMPONENTS:
        raise AssertionError(
            f"Expected {EXPECTED_COMPONENTS} separated components, got {len(all_components)}"
        )

    assembly = make_separated_print_kit()
    if len(assembly.children) != EXPECTED_PLATES:
        raise AssertionError("Separated STEP root does not contain nine plate modules")
    if len(assembly.solids()) != EXPECTED_SOLIDS:
        raise AssertionError("Separated STEP does not contain 88 leaf solids")

    bounds = assembly.bounding_box()
    report = {
        "assembly_bbox_mm": [bounds.size.X, bounds.size.Y, bounds.size.Z],
        "components": len(all_components),
        "leaf_solids": len(assembly.solids()),
        "inventory": inventory,
        "plate_groups": plate_report,
        "status": "passed",
        "virtual_plate_size_mm": VIRTUAL_PLATE_SIZE,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
