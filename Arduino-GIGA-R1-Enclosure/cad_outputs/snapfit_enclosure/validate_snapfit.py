"""Read-only geometric validation for the snap-fit enclosure deliverables."""

from __future__ import annotations

import json

from build123d import GeomType

from cad_outputs.snapfit_enclosure.snapfit_geometry import (
    BASE_BOTTOM_THICKNESS,
    BASE_RECEIVER_RAIL_THICKNESS,
    FRONT_TAB_X_CENTERS,
    GPIO_MINIMUM_WEB,
    GPIO_ANALOG_REAR_ELBOW_OVERLAP,
    GPIO_SLOT_CORNER_RADIUS,
    GPIO_SLOT_BOUNDS,
    LID_TOP_THICKNESS,
    LOGO_DEPTH,
    LOGO_Z_MIN,
    OPPOSITE_SIDE_TAB_X_CENTERS,
    POCKET_WIDTH,
    POCKET_Z_MAX,
    POCKET_Z_MIN,
    RECEIVER_RAIL_POCKET_DEPTH,
    REAR_TAB_Y_CENTERS,
    SNAP_ROOT_FILLET_RADIUS,
    TAB_WIDTH,
    TAB_DEPTH_CLEARANCE,
    TAB_PROJECTION,
    TAB_Z_MAX,
    TAB_Z_MIN,
    _front_lug,
    _opposite_side_lug,
    _rear_lug,
    _top_plate_box,
    make_base_snapfit,
    make_lid_snapfit_components,
)


def overlap_volume(left, right) -> float:
    overlap = left.intersect(right)
    return 0.0 if overlap is None else overlap.volume


def slot_probe(bounds):
    return _top_plate_box(
        bounds,
        xy_overlap=0.0,
        z_overshoot=0.0,
        corner_radius=GPIO_SLOT_CORNER_RADIUS,
    )


base = make_base_snapfit()
lid_body, logo = make_lid_snapfit_components()
logo_solids = logo.solids()
snap_root_fillet_faces = [
    face
    for face in lid_body.faces()
    if face.geom_type == GeomType.CYLINDER
    and abs(face.radius - SNAP_ROOT_FILLET_RADIUS) < 1e-8
    and 15.8 < face.bounding_box().min.Z < 16.0
    and 16.4 < face.bounding_box().max.Z < 16.5
]
snap_retaining_shoulders = [
    face
    for face in lid_body.faces()
    if face.geom_type == GeomType.PLANE
    and abs(face.bounding_box().min.Z - TAB_Z_MAX) < 1e-8
    and abs(face.bounding_box().max.Z - TAB_Z_MAX) < 1e-8
    and abs(face.area - TAB_WIDTH * TAB_PROJECTION) < 1e-8
]

lugs = [
    *((f"rear_xmax_y{center:g}", _rear_lug(center)) for center in REAR_TAB_Y_CENTERS),
    *((f"side_ymin_x{center:g}", _front_lug(center)) for center in FRONT_TAB_X_CENTERS),
    *(
        (f"side_ymax_x{center:g}", _opposite_side_lug(center))
        for center in OPPOSITE_SIDE_TAB_X_CENTERS
    ),
]

report = {
    "valid": {
        "base": base.is_valid,
        "lid_body": lid_body.is_valid,
        "logo": logo.is_valid,
    },
    "solid_counts": {
        "base": len(base.solids()),
        "lid_body": len(lid_body.solids()),
        "logo": len(logo_solids),
        "snap_lugs": len(lugs),
    },
    "snap_lug_base_overlap_mm3": {
        name: overlap_volume(lug, base) for name, lug in lugs
    },
    "assembled_lid_base_overlap_mm3": overlap_volume(lid_body, base),
    "lid_body_logo_overlap_mm3": sum(
        overlap_volume(lid_body, solid) for solid in logo_solids
    ),
    "gpio_access_slot_bounds_mm": {
        name: {
            "x_min": bounds[0],
            "x_max": bounds[1],
            "y_min": bounds[2],
            "y_max": bounds[3],
        }
        for name, bounds in GPIO_SLOT_BOUNDS.items()
    },
    "gpio_access_slot_blocked_volume_mm3": {
        name: overlap_volume(lid_body, slot_probe(bounds))
        for name, bounds in GPIO_SLOT_BOUNDS.items()
    },
    "gpio_access_slot_corner_radius_mm": GPIO_SLOT_CORNER_RADIUS,
    "digital_to_rear_web_mm": (
        GPIO_SLOT_BOUNDS["d22_d53_rear_xmax"][0]
        - GPIO_SLOT_BOUNDS["digital_ymax"][1]
    ),
    "analog_rear_elbow_overlap_mm": (
        GPIO_SLOT_BOUNDS["analog_ymin"][3]
        - GPIO_SLOT_BOUNDS["d22_d53_rear_xmax"][2]
    ),
    "snap_root_fillets": {
        "count": len(snap_root_fillet_faces),
        "radius_mm": SNAP_ROOT_FILLET_RADIUS,
    },
    "snap_retaining_shoulders": {
        "count": len(snap_retaining_shoulders),
        "area_each_mm2": TAB_WIDTH * TAB_PROJECTION,
    },
    "clearance_mm": {
        "lateral_each_side": (POCKET_WIDTH - TAB_WIDTH) / 2.0,
        "depth_to_inner_receiver_wall": TAB_DEPTH_CLEARANCE,
        "below_lug": TAB_Z_MIN - POCKET_Z_MIN,
        "above_lug": POCKET_Z_MAX - TAB_Z_MAX,
    },
    "thickness_mm": {
        "base_floor": BASE_BOTTOM_THICKNESS,
        "base_receiver_rail": BASE_RECEIVER_RAIL_THICKNESS,
        "receiver_depth_to_rail_center": RECEIVER_RAIL_POCKET_DEPTH,
        "lid_top": LID_TOP_THICKNESS,
        "logo_inlay": LOGO_DEPTH,
    },
    "logo_z_mm": {
        "min": LOGO_Z_MIN,
        "max": logo.bounding_box().max.Z,
        "lid_outward_face": lid_body.bounding_box().max.Z,
    },
}

assert all(report["valid"].values())
assert report["solid_counts"] == {
    "base": 1,
    "lid_body": 1,
    "logo": 7,
    "snap_lugs": 6,
}
assert max(report["snap_lug_base_overlap_mm3"].values()) < 1e-8
assert report["assembled_lid_base_overlap_mm3"] < 1e-8
assert report["lid_body_logo_overlap_mm3"] < 1e-8
assert max(report["gpio_access_slot_blocked_volume_mm3"].values()) < 1e-8
assert report["digital_to_rear_web_mm"] >= GPIO_MINIMUM_WEB
assert abs(
    report["analog_rear_elbow_overlap_mm"] - GPIO_ANALOG_REAR_ELBOW_OVERLAP
) < 1e-8
assert report["snap_root_fillets"] == {
    "count": 6,
    "radius_mm": SNAP_ROOT_FILLET_RADIUS,
}
assert report["snap_retaining_shoulders"] == {
    "count": 6,
    "area_each_mm2": TAB_WIDTH * TAB_PROJECTION,
}
assert abs(report["logo_z_mm"]["max"] - report["logo_z_mm"]["lid_outward_face"]) < 1e-6
assert abs(report["thickness_mm"]["base_floor"] - report["thickness_mm"]["lid_top"]) < 1e-9

print(json.dumps(report, indent=2, sort_keys=True))
