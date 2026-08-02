# WPC 25 mm Open-End Wrench

Parametric STEP-first, two-piece multi-material model of a printable open-end wrench for a nominal 25 mm across-flats hex fastener.

## Primary files

- `wpc_25mm_open_end_wrench.py` — build123d parametric source.
- `wpc_25mm_open_end_wrench.step` — generated, validated CAD part.
- `validate_wrench.py` — deterministic geometry checks.
- `cad_brief.md` — dimensions, assumptions, and validation intent.
- `snapshots/` — CAD review packet and final rendered views.

## Key dimensions

- Jaw opening: 25.4 mm, including 0.4 mm total first-print clearance.
- Parallel jaw section: 30.0 mm from the throat tangent to the mouth.
- Total inlet depth: 42.7 mm including the rounded throat.
- Part thickness: 15.0 mm.
- Handle length: 101.6 mm (4.000 in) from the rear head datum to the handle end.
- Two-object print-layout envelope: approximately 156.6 × 95.0 × 15.0 mm.
- Measured reinforced neck width: 29.22 mm at the validation section.
- Finger grip: one shallow continuous R210 lower-edge contour with its peak at X=-77.8 mm, the exact midpoint of the handle-only span.
- Edge treatment: 2 mm comfort fillets on all exposed sharp edges except the bolt-entry flats, throat, and jaw-tip inlet edges.
- Secondary-color build-plate layer: complete Z=0..5 mm volume.
- Mechanical split: X=-64.0 mm, immediately behind the neck logo in the foregrip-to-palm transition.
- Connector: one 12 mm-long through-depth dovetail on the jaw piece, flaring from a 10 mm neck to an 18 mm tail; the matching handle socket has 0.25 mm clearance per mating surface. The through socket allows vertical assembly after printing.
- Logo: simplified 25 mm design containing only two concentric rings and a centered bold `WPC` monogram. It remains a flush 0.8 mm-deep secondary-color inlay centered at X=-49.7 mm, Y=0.

## Assembly and color-body structure

- `jaw_piece` — jaw/neck module with the male dovetail, primary body, bottom 5 mm secondary layer, and bold WPC/two-ring logo inlay.
- `handle_piece` — ergonomic handle module with the matching female dovetail socket, primary body, and bottom 5 mm secondary layer.
- The two modules are exported as separate slicer-ready objects, both flat at Z=0. The handle is translated +50 mm in Y, leaving a measured gap between it and the jaw module.

## Regenerate and validate

Run from this directory with the CAD skill environment available:

```bash
python /path/to/cad/scripts/step wpc_25mm_open_end_wrench.py
PYTHONPATH=. python validate_wrench.py
```

## Use limitation

This is a conceptual/light-duty FDM tool. It has not been FEA-tested, torque-rated, or safety-certified. Real strength depends heavily on material, print orientation, walls, infill, layer adhesion, material bonding across the 5 mm color interface, and fastener condition.
