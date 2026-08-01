# WPC 25 mm Open-End Wrench

Parametric STEP-first, multi-material model of a printable open-end wrench for a nominal 25 mm across-flats hex fastener.

## Primary files

- `wpc_25mm_open_end_wrench.py` — build123d parametric source.
- `wpc_25mm_open_end_wrench.step` — generated, validated CAD part.
- `validate_wrench.py` — deterministic geometry checks.
- `cad_brief.md` — dimensions, assumptions, and validation intent.
- `snapshots/` — CAD review packet and final rendered views.

## Key dimensions

- Jaw opening: 25.4 mm, including 0.4 mm total first-print clearance.
- Part thickness: 25.0 mm.
- Handle length: 101.6 mm (4.000 in) from the rear head datum to the handle end.
- Overall envelope: approximately 166.6 × 54.0 × 25.0 mm.
- Measured reinforced neck width: 29.22 mm at the validation section.
- Finger grip: one shallow continuous R210 lower-edge contour.
- Secondary-color build-plate layer: complete Z=0..5 mm volume.
- Logo: 31 mm photo-inspired Wiseman Precision design, flush-inlaid 0.8 mm into the top face as a separate secondary-color body.

## Color-body structure

- `primary_wrench_body` — Z=5..25 mm primary body with the logo pocket removed.
- `secondary_5mm_surface_layer` — the complete bottom 5 mm of the wrench.
- `wiseman_precision_logo_inlay` — flush secondary-color logo solids at Z=24.2..25 mm.

## Regenerate and validate

Run from this directory with the CAD skill environment available:

```bash
python /path/to/cad/scripts/step wpc_25mm_open_end_wrench.py
PYTHONPATH=. python validate_wrench.py
```

## Use limitation

This is a conceptual/light-duty FDM tool. It has not been FEA-tested, torque-rated, or safety-certified. Real strength depends heavily on material, print orientation, walls, infill, layer adhesion, material bonding across the 5 mm color interface, and fastener condition.
