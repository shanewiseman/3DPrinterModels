# LRS-350-24 and SAB-1060 Enclosures

This project contains two coordinated but physically separate ventilated
enclosures:

1. Mean Well LRS-350-24 base and screw-retained lid.
2. Dayton Audio SAB-1060 base and friction-retained lid.

Separate housings keep mains wiring segregated from the low-voltage amplifier,
avoid a long enclosure that would exceed many printer beds, and let each device
retain independent airflow and service access.

## Files

- `lrs_350_24_print_set.step` - two print objects: base and exterior-face-down
  lid.
- `sab_1060_print_set.step` - six print objects: base, exterior-face-down lid,
  and four separate top-face-down PCB retaining caps.
- `enclosure_fit_check.step` - review assembly with both installed lids and
  simplified equipment envelopes; do not print this file.
- `enclosure_geometry.py` - authoritative parameters and geometry.
- `validate_enclosures.py` - fit, access, validity, and bed-size checks.
- `cad_brief.md` and `reference/SOURCES.md` - design contract and provenance.

## Important pre-print measurement

Measure the SAB-1060 mounting-hole rectangle on the physical board. The model
uses a provisional 142 x 104 mm pattern with 3.8 mm board holes because Dayton
does not publish that datum. PCB thickness is the user-specified 1.7 mm. The
fan frame uses the user-measured 60.5 x 60.5 mm
square, centered on X and biased 7 mm toward the +Y rear. Verify
the provisional 14 mm fan height and the 28.6 mm PCB-bottom-to-fan-top height.
The 62.5 mm lid opening has 1 mm clearance around the measured frame and places
the fan top flush with the 37.6 mm enclosure top.
The dedicated USB-C opening follows the user-observed physical orientation:
the negative-X short side, with its center 29 mm toward -Y. Verify that
along-wall center and the intended plug shell against the physical board
before a production print.

## Hardware and assembly

- Four M3 lid screws and four heat-set inserts for the LRS enclosure.
- The SAB lid uses four integral tapered pins in matching blind base receivers.
  Each 3.6 mm lead-in tip expands to a 4.6 mm clamping land matching the 4.6 mm
  receiver for a nominal line-to-line friction fit; lid screws and
  external-tower inserts are not required.
- The SAB enclosure reinforces all four base towers and all four matching lid
  ears with filled, broad-root wall gussets that retain a 45-degree tangent at
  each circular boss.
- The SAB PCB rests on four 9 mm-diameter standoffs. Integral 3.4 mm posts pass
  through the reported 3.8 mm PCB holes with 0.40 mm diametral clearance.
- Four separate 10.2 mm-diameter x 10 mm-long push-on caps seat against the
  1.7 mm PCB. Each cap has a 3.8-to-3.3 mm tapered bore and reaches its nominal
  locking diameter after 8.0 mm of engagement. The cap diameter is exactly
  three times the 3.4 mm post diameter.
- Four M4 fasteners for the LRS-350-24's official 150 x 50 mm bottom pattern;
  obey Mean Well's maximum screw-entry depth shown in the mechanical drawing.
- Press the four PCB caps down evenly until they contact the board; do not
  force a cap farther if the board begins to flex.
- Add mains-rated strain relief, ferrules, a suitable fuse/switch arrangement,
  and protective earth bonding to the Mean Well metal chassis.

## Printing notes

- The LRS print set has two separated objects. The SAB print set has six:
  base, lid, and four individual retaining caps.
- The SAB lid prints exterior-face-down with all four locating pins pointing
  upward; no pin support is required. Press the installed lid down evenly so
  the four tapered tips enter their receivers together.
- The four PCB caps print top-face-down between the base and lid. Their bores
  widen upward in print orientation, so they require no internal support.
- Use at least four perimeters and 30% infill around towers and standoffs.
- The SAB base has only 22 mm horizontal bridges over its five cable exits;
  enable normal bridge cooling rather than adding support inside those bays.
- The negative-X short wall includes one 16 x 10 mm USB-C plug window, biased
  29 mm toward -Y, with 1.5 mm internal corner radii. It retains a
  7 mm lower sill and a 17.6 mm upper rail, so it does not need support under
  normal bridge settings.
- PETG is acceptable for fit prototypes. For a warm operating enclosure,
  prefer a tougher, higher-temperature material such as ASA, ABS, or PA.
- Do not bridge over or intentionally block the LRS fan, lid slots, or side
  vents. Confirm fan direction before permanent installation.

## Safety boundary

The LRS-350-24 exposes hazardous mains voltage at its terminal block. This CAD
model is a mechanical cover, not a certified electrical enclosure. Final
wiring, grounding, flame resistance, clearances, strain relief, ventilation,
and local-code compliance must be reviewed by a qualified person before the
assembly is energized.

## Regeneration and validation

Run the STEP generators with the repository CAD environment, then execute:

```sh
python validate_enclosures.py
```

The validator checks solid validity, reference-envelope clearance, the five
reinforced cable exits, the dedicated USB-C window, retained wall structure,
fan-frame clearance and flush top, lid clearance, provisional standoff pattern,
integral PCB posts, four separate tapered-bore caps, labeled assembly structure,
and 350 x 320 mm print-layout bounds.
