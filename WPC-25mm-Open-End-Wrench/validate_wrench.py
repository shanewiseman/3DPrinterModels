"""Deterministic validation for the two-color WPC 25 mm wrench."""

from __future__ import annotations

import json

from build123d import Box, GeomType, Location, Vertex

from wpc_25mm_open_end_wrench import (
    EXTERNAL_EDGE_FILLET,
    FINGER_CONTOUR_CENTER_X,
    FINGER_CONTOUR_RADIUS,
    HANDLE_END_X,
    HANDLE_LENGTH,
    HANDLE_MIDPOINT_X,
    HEAD_REAR_DATUM_X,
    JAW_MOUTH_X,
    JAW_OPENING,
    JAW_PARALLEL_LENGTH,
    JAW_THROAT_X,
    LOGO_CENTER_X,
    LOGO_CENTER_Y,
    LOGO_EDGE_CLEARANCE,
    LOGO_INLAY_DEPTH,
    LOGO_NECK_SEARCH_MAX_X,
    LOGO_NECK_SEARCH_MIN_X,
    LOGO_OUTER_RADIUS,
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
    jaw_probe_x_max = JAW_MOUTH_X
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
    top_faces = [
        face
        for face in full_body.faces()
        if face.geom_type == GeomType.PLANE
        and abs(face.bounding_box().min.Z - PROFILE_DEPTH) < 1e-5
        and abs(face.bounding_box().max.Z - PROFILE_DEPTH) < 1e-5
    ]
    top_face = max(top_faces, key=lambda face: face.area)
    logo_center_vertex = Vertex(LOGO_CENTER_X, LOGO_CENTER_Y, PROFILE_DEPTH)
    logo_center_to_top_edge = min(
        edge.distance_to(logo_center_vertex) for edge in top_face.edges()
    )
    logo_envelope_clearance = logo_center_to_top_edge - LOGO_OUTER_RADIUS
    logo_exported_center_x = (logo_bounds.min.X + logo_bounds.max.X) / 2.0
    logo_exported_center_y = (logo_bounds.min.Y + logo_bounds.max.Y) / 2.0
    finger_faces = [
        face
        for face in full_body.faces()
        if face.geom_type == GeomType.CYLINDER
        and abs(getattr(face, "radius", -1.0) - FINGER_CONTOUR_RADIUS) < 1e-4
    ]
    finger_contour_peak_x = (
        finger_faces[0].axis_of_rotation.position.X if len(finger_faces) == 1 else None
    )
    derived_handle_midpoint_x = (HANDLE_END_X + HEAD_REAR_DATUM_X) / 2.0
    comfort_fillet_faces = [
        face
        for face in full_body.faces()
        if face.geom_type == GeomType.CYLINDER
        and abs((getattr(face, "radius", None) or -1.0) - EXTERNAL_EDGE_FILLET)
        < 1e-4
    ]
    jaw_half_gap = JAW_OPENING / 2.0
    protected_upper_flats = []
    protected_lower_flats = []
    protected_tip_faces = []
    protected_throat_faces = []
    geometry_tolerance = 1e-4
    for face in full_body.faces():
        face_bounds = face.bounding_box()
        if face.geom_type == GeomType.PLANE:
            if (
                abs(face_bounds.min.Y - jaw_half_gap) < geometry_tolerance
                and abs(face_bounds.max.Y - jaw_half_gap) < geometry_tolerance
                and face_bounds.min.X <= JAW_THROAT_X + geometry_tolerance
                and face_bounds.max.X >= bounds.max.X - geometry_tolerance
            ):
                protected_upper_flats.append(face)
            if (
                abs(face_bounds.min.Y + jaw_half_gap) < geometry_tolerance
                and abs(face_bounds.max.Y + jaw_half_gap) < geometry_tolerance
                and face_bounds.min.X <= JAW_THROAT_X + geometry_tolerance
                and face_bounds.max.X >= bounds.max.X - geometry_tolerance
            ):
                protected_lower_flats.append(face)
            if (
                abs(face_bounds.min.X - bounds.max.X) < geometry_tolerance
                and abs(face_bounds.max.X - bounds.max.X) < geometry_tolerance
            ):
                protected_tip_faces.append(face)
        elif (
            face.geom_type == GeomType.CYLINDER
            and abs((getattr(face, "radius", None) or -1.0) - jaw_half_gap)
            < geometry_tolerance
            and abs(face_bounds.min.Z) < geometry_tolerance
            and abs(face_bounds.max.Z - PROFILE_DEPTH) < geometry_tolerance
        ):
            protected_throat_faces.append(face)

    primary_logo_overlap = _volume(primary.intersect(logo))
    primary_layer_overlap = _volume(primary.intersect(secondary_layer))
    logo_layer_overlap = _volume(logo.intersect(secondary_layer))
    component_volume = primary.volume + secondary_layer.volume + _volume(logo)
    volume_reconstruction_error = abs(full_body.volume - component_volume)
    upper_parallel_length = (
        protected_upper_flats[0].bounding_box().max.X
        - protected_upper_flats[0].bounding_box().min.X
        if len(protected_upper_flats) == 1
        else None
    )
    lower_parallel_length = (
        protected_lower_flats[0].bounding_box().max.X
        - protected_lower_flats[0].bounding_box().min.X
        if len(protected_lower_flats) == 1
        else None
    )

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
            "specified_parallel_length_mm": JAW_PARALLEL_LENGTH,
            "measured_upper_parallel_length_mm": upper_parallel_length,
            "measured_lower_parallel_length_mm": lower_parallel_length,
            "mouth_x_mm": bounds.max.X,
            "overall_inlet_depth_mm": bounds.max.X
            - (JAW_THROAT_X - jaw_half_gap),
            "blocked_probe_volume_mm3": _volume(full_body.intersect(jaw_probe)),
            "upper_jaw_probe_volume_mm3": _volume(full_body.intersect(upper_probe)),
            "lower_jaw_probe_volume_mm3": _volume(full_body.intersect(lower_probe)),
            "protected_upper_flat_face_count": len(protected_upper_flats),
            "protected_lower_flat_face_count": len(protected_lower_flats),
            "protected_throat_face_count": len(protected_throat_faces),
            "protected_tip_planar_face_count": len(protected_tip_faces),
        },
        "edge_rounding": {
            "fillet_radius_mm": EXTERNAL_EDGE_FILLET,
            "cylindrical_fillet_face_count": len(comfort_fillet_faces),
        },
        "logo_placement": {
            "neck_search_x_mm": [
                LOGO_NECK_SEARCH_MIN_X,
                LOGO_NECK_SEARCH_MAX_X,
            ],
            "requested_center_xy_mm": [LOGO_CENTER_X, LOGO_CENTER_Y],
            "exported_envelope_center_xy_mm": [
                logo_exported_center_x,
                logo_exported_center_y,
            ],
            "outer_diameter_mm": 2.0 * LOGO_OUTER_RADIUS,
            "center_to_nearest_flat_top_edge_mm": logo_center_to_top_edge,
            "clearance_to_flat_top_edge_mm": logo_envelope_clearance,
            "minimum_clearance_mm": LOGO_EDGE_CLEARANCE,
        },
        "handle": {
            "specified_length_mm": HANDLE_LENGTH,
            "datum_to_end_mm": HEAD_REAR_DATUM_X - bounds.min.X,
            "handle_end_x_mm": HANDLE_END_X,
            "rear_head_datum_x_mm": HEAD_REAR_DATUM_X,
            "derived_midpoint_x_mm": derived_handle_midpoint_x,
            "finger_contour_peak_x_mm": finger_contour_peak_x,
            "finger_contour_midpoint_offset_mm": (
                None
                if finger_contour_peak_x is None
                else finger_contour_peak_x - derived_handle_midpoint_x
            ),
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
            "volume_reconstruction_error_mm3": volume_reconstruction_error,
            "volume_reconstruction_relative_error": (
                volume_reconstruction_error / full_body.volume
            ),
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
    assert result["jaw"]["protected_upper_flat_face_count"] == 1
    assert result["jaw"]["protected_lower_flat_face_count"] == 1
    assert result["jaw"]["protected_throat_face_count"] == 1
    assert result["jaw"]["protected_tip_planar_face_count"] == 2
    assert abs(result["jaw"]["mouth_x_mm"] - JAW_MOUTH_X) < 1e-5
    assert (
        abs(
            result["jaw"]["measured_upper_parallel_length_mm"]
            - JAW_PARALLEL_LENGTH
        )
        < 1e-5
    )
    assert (
        abs(
            result["jaw"]["measured_lower_parallel_length_mm"]
            - JAW_PARALLEL_LENGTH
        )
        < 1e-5
    )
    assert result["edge_rounding"]["cylindrical_fillet_face_count"] >= 12
    assert LOGO_NECK_SEARCH_MIN_X <= LOGO_CENTER_X <= LOGO_NECK_SEARCH_MAX_X
    assert abs(result["logo_placement"]["outer_diameter_mm"] - 25.0) < 1e-6
    assert abs(
        result["logo_placement"]["exported_envelope_center_xy_mm"][0]
        - LOGO_CENTER_X
    ) < 1e-5
    assert abs(
        result["logo_placement"]["exported_envelope_center_xy_mm"][1]
        - LOGO_CENTER_Y
    ) < 1e-5
    assert (
        result["logo_placement"]["clearance_to_flat_top_edge_mm"]
        >= LOGO_EDGE_CLEARANCE - 1e-5
    )
    assert abs(result["handle"]["datum_to_end_mm"] - HANDLE_LENGTH) < 1e-5
    assert abs(HANDLE_MIDPOINT_X - derived_handle_midpoint_x) < 1e-9
    assert abs(FINGER_CONTOUR_CENTER_X - HANDLE_MIDPOINT_X) < 1e-9
    assert abs(result["handle"]["finger_contour_midpoint_offset_mm"]) < 1e-6
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
    # Splitting many filleted faces into color bodies accumulates small BREP tolerance.
    assert result["two_color"]["volume_reconstruction_error_mm3"] < 10.0
    assert result["two_color"]["volume_reconstruction_relative_error"] < 1e-4

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
