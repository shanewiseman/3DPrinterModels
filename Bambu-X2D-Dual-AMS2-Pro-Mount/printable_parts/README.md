# Individual printable STEP files

This directory contains one manufacturing-oriented STEP for each of the 14
printed ASA structural objects in the assembled mount. Printer/AMS reference
envelopes and purchased M4 hardware are intentionally excluded.

Every part is centered on XY and rests on Z=0. Shelves and low ties retain
their flat orientation; brackets are laid on their broad truss face; side pads
are laid on their largest face.

| Quantity | STEP files | Saved bounds (mm) |
| ---: | --- | --- |
| 2 | `left_shelf.step`, `right_shelf.step` | 211.1 × 252 × 12 |
| 4 | `*_bracket.step` | 211.1 × 246 × 12 |
| 4 | `*_tie_*_half.step` | 249 × 50 × 25.4 |
| 4 | `*_side_pad.step` | 120 × 30 × 3 |

The separate source entry points are under `sources/`. Regenerate the files
through the CAD `scripts/step` launcher so their GLB/topology sidecars remain
in sync. One reviewed isometric image per export is stored under `snapshots/`.
