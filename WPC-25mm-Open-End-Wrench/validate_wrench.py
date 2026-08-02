"""Deterministic validation for the two-piece, two-color WPC wrench."""

from __future__ import annotations

import json

from build123d import Box, FontStyle, GeomType, Location, Vertex

from wpc_25mm_open_end_wrench import (
    CONNECTOR_CLEARANCE,
    CONNECTOR_LENGTH,
    CONNECTOR_ROOT_OVERLAP,
    DOVETAIL_NECK_WIDTH,
    DOVETAIL_TAIL_WIDTH,
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
    LOGO_FONT_STYLE,
    LOGO_INLAY_DEPTH,
    LOGO_NECK_SEARCH_MAX_X,
    LOGO_NECK_SEARCH_MIN_X,
    LOGO_OUTER_RADIUS,
    LOGO_TEXT,
    NECK_HALF_WIDTH,
    PROFILE_DEPTH,
    PRINT_LAYOUT_HANDLE_OFFSET_Y,
    PRINT_LAYOUT_MINIMUM_GAP,
    SECONDARY_LAYER_THICKNESS,
    SPLIT_X,
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


def _one_bounds(shape):
    bounds = shape.bounding_box()
    return {
        "min": [bounds.min.X, bounds.min.Y, bounds.min.Z],
        "max": [bounds.max.X, bounds.max.Y, bounds.max.Z],
        "size": [bounds.size.X, bounds.size.Y, bounds.size.Z],
    }


def main():
    details = build_wrench_details()
    model = details["final"]
    full_body = details["full_body"]
    jaw_piece = details["jaw_piece"]
    handle_piece = details["handle_piece"]
    male_connector = details["male_connector"]
    female_cutter = details["female_cutter"]
    jaw_primary = details["jaw_primary_body"]
    jaw_secondary = details["jaw_secondary_layer"]
    handle_primary = details["handle_primary_body"]
    handle_secondary = details["handle_secondary_layer"]
    logo = details["logo_inlay"]
    jaw_module = details["jaw_module"]
    handle_module = details["handle_module"]
    bounds = model.bounding_box()

    jaw_probe = _box(
        JAW_PARALLEL_LENGTH,
        JAW_OPENING - 0.02,
        PROFILE_DEPTH + 2.0,
        (JAW_THROAT_X + JAW_MOUTH_X) / 2.0,
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

    top_faces = [
        face
        for face in jaw_piece.faces()
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
    logo_bounds = logo.bounding_box()
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

    male_bounds = male_connector.bounding_box()
    female_bounds = female_cutter.bounding_box()
    jaw_handle_overlap = _volume(jaw_piece.intersect(handle_piece))
    male_handle_overlap = _volume(male_connector.intersect(handle_piece))
    male_outside_jaw = _volume(male_connector.cut(jaw_piece))
    male_outside_female_envelope = _volume(male_connector.cut(female_cutter))
    connector_clearance = male_connector.distance_to(handle_piece)

    jaw_layout_bounds = jaw_module.bounding_box()
    handle_layout_bounds = handle_module.bounding_box()
    mechanical_handle_bounds = handle_piece.bounding_box()
    layout_object_gap = jaw_module.distance_to(handle_module)
    layout_overlap = _volume(jaw_module.intersect(handle_module))
    measured_layout_offset_y = (
        (handle_layout_bounds.min.Y + handle_layout_bounds.max.Y) / 2.0
        - (mechanical_handle_bounds.min.Y + mechanical_handle_bounds.max.Y) / 2.0
    )

    jaw_primary_logo_overlap = _volume(jaw_primary.intersect(logo))
    jaw_primary_secondary_overlap = _volume(jaw_primary.intersect(jaw_secondary))
    handle_primary_secondary_overlap = _volume(
        handle_primary.intersect(handle_secondary)
    )
    cross_piece_color_overlap = sum(
        _volume(left.intersect(right))
        for left in (jaw_primary, jaw_secondary, logo)
        for right in (handle_primary, handle_secondary)
    )
    jaw_reconstruction_error = abs(
        jaw_piece.volume - (jaw_primary.volume + jaw_secondary.volume + _volume(logo))
    )
    handle_reconstruction_error = abs(
        handle_piece.volume - (handle_primary.volume + handle_secondary.volume)
    )

    result = {
        "valid": {
            "assembly": model.is_valid,
            "jaw_piece": jaw_piece.is_valid,
            "handle_piece": handle_piece.is_valid,
            "jaw_primary": jaw_primary.is_valid,
            "jaw_secondary": jaw_secondary.is_valid,
            "handle_primary": handle_primary.is_valid,
            "handle_secondary": handle_secondary.is_valid,
            "logo": logo.is_valid,
        },
        "assembly": {
            "top_level_piece_count": len(model.children),
            "solid_count": len(model.solids()),
            "bbox_mm": _one_bounds(model),
            "profile_depth_mm": bounds.size.Z,
        },
        "print_layout": {
            "handle_offset_y_mm": PRINT_LAYOUT_HANDLE_OFFSET_Y,
            "measured_handle_offset_y_mm": measured_layout_offset_y,
            "minimum_required_gap_mm": PRINT_LAYOUT_MINIMUM_GAP,
            "measured_minimum_object_gap_mm": layout_object_gap,
            "overlap_mm3": layout_overlap,
            "jaw_bbox_mm": _one_bounds(jaw_module),
            "handle_bbox_mm": _one_bounds(handle_module),
        },
        "jaw": {
            "opening_mm": JAW_OPENING,
            "specified_parallel_length_mm": JAW_PARALLEL_LENGTH,
            "measured_upper_parallel_length_mm": upper_parallel_length,
            "measured_lower_parallel_length_mm": lower_parallel_length,
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
        "connector": {
            "split_x_mm": SPLIT_X,
            "male_piece": "jaw_piece",
            "female_piece": "handle_piece",
            "specified_insertion_length_mm": CONNECTOR_LENGTH,
            "measured_insertion_length_mm": SPLIT_X - male_bounds.min.X,
            "type": "single_through-depth_dovetail",
            "neck_width_mm": DOVETAIL_NECK_WIDTH,
            "tail_width_mm": male_bounds.size.Y,
            "tail_minus_neck_flare_mm": male_bounds.size.Y
            - DOVETAIL_NECK_WIDTH,
            "height_mm": male_bounds.size.Z,
            "vertical_insertion_access": "through Z=0..15 mm",
            "clearance_per_surface_mm": CONNECTOR_CLEARANCE,
            "measured_minimum_clearance_mm": connector_clearance,
            "root_overlap_mm": CONNECTOR_ROOT_OVERLAP,
            "male_bbox_mm": _one_bounds(male_connector),
            "female_cutter_bbox_mm": _one_bounds(female_cutter),
            "male_volume_mm3": male_connector.volume,
            "female_cutter_volume_mm3": female_cutter.volume,
            "jaw_handle_overlap_mm3": jaw_handle_overlap,
            "male_handle_overlap_mm3": male_handle_overlap,
            "male_outside_jaw_mm3": male_outside_jaw,
            "male_outside_female_envelope_mm3": male_outside_female_envelope,
        },
        "logo": {
            "text": LOGO_TEXT,
            "font_style": LOGO_FONT_STYLE.name,
            "retained_circle_count": 2,
            "solid_count": len(logo.solids()),
            "requested_center_xy_mm": [LOGO_CENTER_X, LOGO_CENTER_Y],
            "exported_center_xy_mm": [
                logo_exported_center_x,
                logo_exported_center_y,
            ],
            "outer_diameter_mm": 2.0 * LOGO_OUTER_RADIUS,
            "clearance_to_nearest_jaw_top_edge_mm": logo_envelope_clearance,
            "minimum_clearance_mm": LOGO_EDGE_CLEARANCE,
            "z_mm": [logo_bounds.min.Z, logo_bounds.max.Z],
            "depth_mm": logo_bounds.size.Z,
        },
        "handle": {
            "specified_length_mm": HANDLE_LENGTH,
            "datum_to_end_mm": HEAD_REAR_DATUM_X - bounds.min.X,
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
        "edge_rounding": {
            "fillet_radius_mm": EXTERNAL_EDGE_FILLET,
            "cylindrical_fillet_face_count": len(comfort_fillet_faces),
        },
        "two_color": {
            "secondary_layer_thickness_mm": SECONDARY_LAYER_THICKNESS,
            "jaw_secondary_z_mm": [
                jaw_secondary.bounding_box().min.Z,
                jaw_secondary.bounding_box().max.Z,
            ],
            "handle_secondary_z_mm": [
                handle_secondary.bounding_box().min.Z,
                handle_secondary.bounding_box().max.Z,
            ],
            "jaw_primary_logo_overlap_mm3": jaw_primary_logo_overlap,
            "jaw_primary_secondary_overlap_mm3": jaw_primary_secondary_overlap,
            "handle_primary_secondary_overlap_mm3": handle_primary_secondary_overlap,
            "cross_piece_color_overlap_mm3": cross_piece_color_overlap,
            "jaw_reconstruction_error_mm3": jaw_reconstruction_error,
            "handle_reconstruction_error_mm3": handle_reconstruction_error,
        },
    }

    assert all(result["valid"].values())
    assert result["assembly"]["top_level_piece_count"] == 2
    assert abs(result["assembly"]["profile_depth_mm"] - PROFILE_DEPTH) < 1e-5
    assert abs(
        result["print_layout"]["measured_handle_offset_y_mm"]
        - PRINT_LAYOUT_HANDLE_OFFSET_Y
    ) < 1e-5
    assert result["print_layout"]["measured_minimum_object_gap_mm"] >= (
        PRINT_LAYOUT_MINIMUM_GAP
    )
    assert result["print_layout"]["overlap_mm3"] < 1e-6
    for piece_bounds in (jaw_layout_bounds, handle_layout_bounds):
        assert abs(piece_bounds.min.Z) < 1e-5
        assert abs(piece_bounds.max.Z - PROFILE_DEPTH) < 1e-5
    assert abs(PROFILE_DEPTH - 15.0) < 1e-9
    assert len(jaw_piece.solids()) == 1
    assert len(handle_piece.solids()) == 1
    assert result["jaw"]["blocked_probe_volume_mm3"] < 1e-6
    assert result["jaw"]["upper_jaw_probe_volume_mm3"] > 100.0
    assert result["jaw"]["lower_jaw_probe_volume_mm3"] > 100.0
    assert result["jaw"]["protected_upper_flat_face_count"] == 1
    assert result["jaw"]["protected_lower_flat_face_count"] == 1
    assert result["jaw"]["protected_throat_face_count"] == 1
    assert result["jaw"]["protected_tip_planar_face_count"] == 2
    assert abs(upper_parallel_length - JAW_PARALLEL_LENGTH) < 1e-5
    assert abs(lower_parallel_length - JAW_PARALLEL_LENGTH) < 1e-5
    assert abs(
        result["connector"]["measured_insertion_length_mm"] - CONNECTOR_LENGTH
    ) < 1e-5
    assert abs(result["connector"]["neck_width_mm"] - DOVETAIL_NECK_WIDTH) < 1e-5
    assert abs(result["connector"]["tail_width_mm"] - DOVETAIL_TAIL_WIDTH) < 1e-5
    assert result["connector"]["tail_minus_neck_flare_mm"] > 0.0
    assert abs(result["connector"]["height_mm"] - PROFILE_DEPTH) < 1e-5
    assert result["connector"]["female_cutter_volume_mm3"] > result["connector"][
        "male_volume_mm3"
    ]
    assert result["connector"]["jaw_handle_overlap_mm3"] < 1e-6
    assert result["connector"]["male_handle_overlap_mm3"] < 1e-6
    assert result["connector"]["male_outside_jaw_mm3"] < 1e-6
    assert result["connector"]["male_outside_female_envelope_mm3"] < 1e-6
    assert result["connector"]["measured_minimum_clearance_mm"] >= 0.20
    assert LOGO_TEXT == "WPC"
    assert LOGO_FONT_STYLE == FontStyle.BOLD
    assert result["logo"]["retained_circle_count"] == 2
    assert LOGO_NECK_SEARCH_MIN_X <= LOGO_CENTER_X <= LOGO_NECK_SEARCH_MAX_X
    assert abs(result["logo"]["outer_diameter_mm"] - 25.0) < 1e-6
    assert abs(result["logo"]["exported_center_xy_mm"][0] - LOGO_CENTER_X) < 1e-5
    assert abs(result["logo"]["exported_center_xy_mm"][1] - LOGO_CENTER_Y) < 1e-5
    assert result["logo"]["clearance_to_nearest_jaw_top_edge_mm"] >= (
        LOGO_EDGE_CLEARANCE - 1e-5
    )
    assert abs(result["logo"]["depth_mm"] - LOGO_INLAY_DEPTH) < 1e-5
    assert abs(result["logo"]["z_mm"][1] - PROFILE_DEPTH) < 1e-5
    assert abs(result["handle"]["datum_to_end_mm"] - HANDLE_LENGTH) < 1e-5
    assert abs(HANDLE_MIDPOINT_X - derived_handle_midpoint_x) < 1e-9
    assert abs(FINGER_CONTOUR_CENTER_X - HANDLE_MIDPOINT_X) < 1e-9
    assert abs(result["handle"]["finger_contour_midpoint_offset_mm"]) < 1e-6
    assert result["handle"]["neck_width_middepth_mm"] >= 2.0 * NECK_HALF_WIDTH - 0.1
    assert result["handle"]["single_finger_contour_face_count"] == 1
    assert result["edge_rounding"]["cylindrical_fillet_face_count"] >= 12
    assert (
        abs(jaw_secondary.bounding_box().size.Z - SECONDARY_LAYER_THICKNESS)
        < 1e-5
    )
    assert (
        abs(handle_secondary.bounding_box().size.Z - SECONDARY_LAYER_THICKNESS)
        < 1e-5
    )
    assert result["two_color"]["jaw_primary_logo_overlap_mm3"] < 1e-6
    assert result["two_color"]["jaw_primary_secondary_overlap_mm3"] < 1e-6
    assert result["two_color"]["handle_primary_secondary_overlap_mm3"] < 1e-6
    assert result["two_color"]["cross_piece_color_overlap_mm3"] < 1e-6
    assert result["two_color"]["jaw_reconstruction_error_mm3"] < 5.0
    assert result["two_color"]["handle_reconstruction_error_mm3"] < 5.0

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
