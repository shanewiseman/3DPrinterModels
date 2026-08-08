"""Check that binary STL meshes have exactly two triangles per mesh edge."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import struct
import sys


DEFAULT_PATHS = tuple(
    Path("meshes") / f"rail_{name}_body.stl"
    for name in (
        "bottom_ad",
        "bottom_eh",
        "top_ad",
        "top_eh",
        "left_14",
        "left_58",
        "right_14",
        "right_58",
    )
)
VERTEX_DECIMALS = 5


def _mesh_edge_counts(path: Path) -> tuple[int, Counter]:
    data = path.read_bytes()
    if len(data) < 84:
        raise AssertionError(f"{path}: file is too short to be a binary STL")
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    expected_size = 84 + triangle_count * 50
    if len(data) != expected_size:
        raise AssertionError(
            f"{path}: expected {expected_size} bytes for {triangle_count} triangles, "
            f"got {len(data)}"
        )

    edge_counts: Counter = Counter()
    for index in range(triangle_count):
        record = struct.unpack_from("<12fH", data, 84 + index * 50)
        vertices = [
            tuple(round(value, VERTEX_DECIMALS) for value in record[offset : offset + 3])
            for offset in (3, 6, 9)
        ]
        edge_counts.update(
            tuple(sorted((vertices[first], vertices[second])))
            for first, second in ((0, 1), (1, 2), (2, 0))
        )
    return triangle_count, edge_counts


def main() -> None:
    paths = tuple(Path(argument) for argument in sys.argv[1:]) or DEFAULT_PATHS
    failures = []
    for path in paths:
        triangle_count, edge_counts = _mesh_edge_counts(path)
        nonmanifold = {edge: count for edge, count in edge_counts.items() if count != 2}
        print(
            f"{path}: triangles={triangle_count}, unique_edges={len(edge_counts)}, "
            f"nonmanifold_edges={len(nonmanifold)}"
        )
        if nonmanifold:
            multiplicities = Counter(nonmanifold.values())
            failures.append((path, multiplicities))

    if failures:
        details = ", ".join(f"{path}: {dict(counts)}" for path, counts in failures)
        raise AssertionError(f"Non-watertight STL meshes: {details}")


if __name__ == "__main__":
    main()
