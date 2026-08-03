"""Two-object print layout for the CRP2/TT25 holder and M6 nut insert."""

from __future__ import annotations

from build123d import Axis, Location
from cadpy.assembly import AssemblyHelper

from moza_crp_dayton_tt25_m6_insert import build_insert_details
from moza_crp_dayton_tt25_mount import build_holder_details


PRINT_OBJECT_GAP = 4.0


def build_print_set_details():
    holder = build_holder_details()["holder"].rotate(Axis.X, 90.0)
    holder_bbox = holder.bounding_box()
    holder = holder.moved(Location((0.0, 0.0, -holder_bbox.min.Z)))

    insert = build_insert_details()["insert"]
    settled_holder_bbox = holder.bounding_box()
    insert_bbox = insert.bounding_box()
    insert_center_x = (
        settled_holder_bbox.max.X
        + PRINT_OBJECT_GAP
        - insert_bbox.min.X
    )
    insert = insert.moved(Location((insert_center_x, 0.0, 0.0)))

    assembly = AssemblyHelper("moza_crp2_dayton_tt25_m6_print_set")
    holder_occurrence = assembly.add(holder, "perpendicular_yoke_holder")
    insert_occurrence = assembly.add(insert, "keyed_m6_nut_insert")
    final = assembly.build()

    return {
        "final": final,
        "holder": holder,
        "insert": insert,
        "holder_occurrence": holder_occurrence,
        "insert_occurrence": insert_occurrence,
        "object_gap": PRINT_OBJECT_GAP,
    }


def gen_step():
    return build_print_set_details()["final"]
