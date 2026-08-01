"""Deterministic validation for the two-color WPC 25 mm wrench."""

from __future__ import annotations

import json

from build123d import Box, GeomType, Location

from wpc_25mm_open_end_wrench import (
    FINGER_CONTOUR_RADIUS,
    HANDLE_LENGTH,
    HEAD_REAR_DATUM_X,
    JAW_OPENING,
    JAW_THROAT_X,
    LOGO_INLAY_DEPTH,
    NECK_HALF_WIDTH,
    PROFILE_DEPTH,
    SECONDARY_LAYER_THICKNESS,
    build_wrench_details,
)


def _box(size_x, size_y, size_z, center_x, center_y, center_z):
    return Box(size_x, size_y, size_z).moved(
        Location((center_x, center_y, center_z))
    )


def _volume(shape_or_shapes):
    if shape_or_shapes is None:
        return 0.0
    return sum(solid.volume for solid in shape_or_shapes.solids())


def main():
    details = build_wrench_details()
    model = details["final"]
    full_body = details["full_body"]
    primary = details["primary_body"]
    secondary_layer = details["secondary_layer"]
    logo = details["logo_inlay"]
    bounds = model.bounding_box()

    jaw_probe_x_min = JAW_THROAT_X
    jaw_probe_x_max = 40.0
    jaw_probe = _box(
        jaw_probe_x_max - jaw_probe_x_min,
        JAW_OPENING - 0.02,
        PROFILE_DEPTH + 2.0,
        (jaw_probe_x_min + jaw_probe_x_max) / 2.0,
        0.0,
        PROFILE_DEPTH / 2.0,
    )

    jaw_material_probe_width = 3.0
    upper_probe = _box(
        16.0,
        jaw_material_probe_width,
        PROFILE_DEPTH - 4.0,
        18.0,
        JAW_OPENING / 2.0 + jaw_material_probe_width / 2.0 + 0.2,
        PROFILE_DEPTH / 2.0,
    )
    lower_probe = _box(
        16.0,
        jaw_material_probe_width,
        PROFILE_DEPTH - 4.0,
        18.0,
        -(JAW_OPENING / 2.0 + jaw_material_probe_width / 2.0 + 0.2),
        PROFILE_DEPTH / 2.0,
    )

    neck_slice_x = HEAD_REAR_DATUM_X - 5.0
    neck_slice_dx = 0.1
    neck_slice_dz = 1.0
    neck_probe = _box(
        neck_slice_dx,
        100.0,
        neck_slice_dz,
        neck_slice_x,
        0.0,
        PROFILE_DEPTH / 2.0,
    )
    neck_width = _volume(full_body.intersect(neck_probe)) / (
        neck_slice_dx * neck_slice_dz
    )

    primary_bounds = primary.bounding_box()
    layer_bounds = secondary_layer.bounding_box()
    logo_bounds = logo.bounding_box()
    finger_faces = [
        face
        for face in full_body.faces()
        if face.geom_type == GeomType.CYLINDER
        and abs(getattr(face, "radius", -1.0) - FINGER_CONTOUR_RADIUS) < 1e-4
    ]

    primary_logo_overlap = _volume(primary.intersect(logo))
    primary_layer_overlap = _volume(primary.intersect(secondary_layer))
    logo_layer_overlap = _volume(logo.intersect(secondary_layer))
    component_volume = primary.volume + secondary_layer.volume + _volume(logo)

    result = {
        "valid": {
            "model": model.is_valid,
            "primary": primary.is_valid,
            "secondary_layer": secondary_layer.is_valid,
            "logo": logo.is_valid,
        },
        "solid_counts": {
            "model": len(model.solids()),
            "primary": len(primary.solids()),
            "secondary_layer": len(secondary_layer.solids()),
            "logo": len(logo.solids()),
        },
        "bbox_mm": {
            "min": [bounds.min.X, bounds.min.Y, bounds.min.Z],
            "max": [bounds.max.X, bounds.max.Y, bounds.max.Z],
            "size": [bounds.size.X, bounds.size.Y, bounds.size.Z],
        },
        "profile_depth_mm": bounds.size.Z,
        "jaw": {
            "opening_mm": JAW_OPENING,
            "blocked_probe_volume_mm3": _volume(full_body.intersect(jaw_probe)),
            "upper_jaw_probe_volume_mm3": _volume(full_body.intersect(upper_probe)),
            "lower_jaw_probe_volume_mm3": _volume(full_body.intersect(lower_probe)),
        },
        "handle": {
            "specified_length_mm": HANDLE_LENGTH,
            "datum_to_end_mm": HEAD_REAR_DATUM_X - bounds.min.X,
            "neck_width_middepth_mm": neck_width,
            "single_finger_contour_face_count": len(finger_faces),
            "finger_contour_radius_mm": FINGER_CONTOUR_RADIUS,
        },
        "two_color": {
            "secondary_layer_z_mm": [layer_bounds.min.Z, layer_bounds.max.Z],
            "secondary_layer_thickness_mm": layer_bounds.size.Z,
            "primary_z_mm": [primary_bounds.min.Z, primary_bounds.max.Z],
            "logo_z_mm": [logo_bounds.min.Z, logo_bounds.max.Z],
            "logo_depth_mm": logo_bounds.size.Z,
            "logo_solid_count": len(logo.solids()),
            "primary_logo_overlap_mm3": primary_logo_overlap,
            "primary_layer_overlap_mm3": primary_layer_overlap,
            "logo_layer_overlap_mm3": logo_layer_overlap,
            "volume_reconstruction_error_mm3": abs(full_body.volume - component_volume),
        },
    }

    assert all(result["valid"].values())
    assert result["solid_counts"]["primary"] == 1
    assert result["solid_counts"]["secondary_layer"] == 1
    assert result["solid_counts"]["logo"] > 10
    assert abs(result["profile_depth_mm"] - PROFILE_DEPTH) < 1e-5
    assert result["jaw"]["blocked_probe_volume_mm3"] < 1e-6
    assert result["jaw"]["upper_jaw_probe_volume_mm3"] > 100.0
    assert result["jaw"]["lower_jaw_probe_volume_mm3"] > 100.0
    assert abs(result["handle"]["datum_to_end_mm"] - HANDLE_LENGTH) < 1e-5
    assert result["handle"]["neck_width_middepth_mm"] >= 2.0 * NECK_HALF_WIDTH - 0.1
    assert result["handle"]["single_finger_contour_face_count"] == 1
    assert abs(
        result["two_color"]["secondary_layer_thickness_mm"]
        - SECONDARY_LAYER_THICKNESS
    ) < 1e-5
    assert abs(result["two_color"]["logo_depth_mm"] - LOGO_INLAY_DEPTH) < 1e-5
    assert abs(result["two_color"]["logo_z_mm"][1] - PROFILE_DEPTH) < 1e-5
    assert result["two_color"]["primary_logo_overlap_mm3"] < 1e-6
    assert result["two_color"]["primary_layer_overlap_mm3"] < 1e-6
    assert result["two_color"]["logo_layer_overlap_mm3"] < 1e-6
    # Multi-solid BREP splitting accumulates sub-tenth-mm3 boolean tolerance.
    assert result["two_color"]["volume_reconstruction_error_mm3"] < 0.2

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
