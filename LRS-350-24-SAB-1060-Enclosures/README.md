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
- `sab_1060_print_set.step` - nine print objects: base, exterior-face-down lid,
  four separate top-face-down PCB retaining caps, a removable fan guard, and a
  post-and-cap fit coupon plus a lid-pin-to-base-receiver fit coupon.
- `enclosure_fit_check.step` - review assembly with both installed lids and
  simplified equipment envelopes; do not print this file.
- `enclosure_geometry.py` - authoritative parameters and geometry.
- `validate_enclosures.py` - fit, access, validity, and bed-size checks.
- `cad_brief.md` and `reference/SOURCES.md` - design contract and provenance.

## Important pre-print measurement

Measure the SAB-1060 mounting-hole rectangle on the physical board. The model
uses a provisional 142 x 104 mm pattern with 3.8 mm board holes because Dayton
does not publish that datum. PCB thickness is the user-specified 1.7 mm. The
fan frame uses the user-measured 60.1 x 60.1 mm square. From the rear view,
its measured edge clearances are rear 24.5 mm, front 35.9 mm, left 47.6 mm,
and right 50.7 mm. Rear-view left maps to +X, placing the fan center at
X=+1.55 mm and Y=+5.70 mm from those measurements. The latest physical-fit
instruction moves the fan opening, fan reference, and removable guard 2 mm
toward rear-view right (global -X), giving the final center X=-0.45 mm and
Y=+5.70 mm. Verify
the provisional 14 mm fan height and the 28.6 mm PCB-bottom-to-fan-top height.
The 62.1 mm lid opening has 1 mm clearance around the measured frame. The
base exterior height remains Z=34.6 mm; the replacement lid raises its
interior roof by 8 mm to Z=42.6 mm and its exterior roof to Z=45.6 mm. The
measured fan top remains at Z=37.6 mm, leaving 5 mm below the roof underside.
The removable fan guard raises the installed outside height to 47.2 mm.
The dedicated USB-C opening follows the user-observed physical orientation:
the negative-X short side, with its center 29 mm toward -Y. Verify that
along-wall center and the intended plug shell against the physical board
before a production print.
The lid now serves three front Mini-Fit Jr. plug zones with two physical roof
openings. J013 retains a separate 35.2 x 16 mm opening. J012 and the DC input
share one continuous 49.7 x 16 mm opening, removing the former 1.3 mm divider
while preserving their 35.2 and 13.2 mm access envelopes. The widths add
1.6 mm clearance per side beyond the original 32, 32, and 10 mm sizes while
retaining the 16 mm front-to-back depth. Their provisional centers are
X=-44.0, +29.5, and +55.0 mm at Y=-50.5 mm, scaled from Dayton's official
top-view guide. Check those centers against the populated board and
cable-latch envelopes before printing.

## Hardware and assembly

- Four M3 lid screws and four heat-set inserts for the LRS enclosure.
- The SAB lid uses four integral tapered pins in matching blind base receivers.
  Each 3.2 mm lead-in tip expands to a 4.0 mm locating land inside the unchanged
  4.6 mm receiver, providing 0.60 mm diametral clearance (0.30 mm per side).
  The pins center the lid without gripping it; they are not a retention feature.
- The SAB replacement lid is an 8 mm raised hood. Its base-mating rim, plug,
  and four pin positions are unchanged, so it remains compatible with the
  already-printed base. The roof is clear across the full volume beginning
  5 mm inward from every inside wall.
- Both long base walls are now closed, including the former bank of five cable
  windows. Printing the closed-wall revision requires a new base; an earlier
  base still mates with the lid but retains its old openings.
- Both short base walls use a 5 mm circular ventilation grid. The positive-X
  wall has 28 perforations; the USB-C wall has 22, with conflicting holes
  omitted to preserve at least 1 mm around the inlet. Every perforation also
  remains at least 1 mm above the interior floor and below the wall top.
- The SAB enclosure reinforces all four base towers and all four matching lid
  ears with filled, broad-root wall gussets that retain a 45-degree tangent at
  each circular boss.
- The SAB PCB rests on four 9 mm-diameter standoffs. Integral 3.4 mm posts pass
  through the reported 3.8 mm PCB holes with 0.40 mm diametral clearance. Each
  post has a 0.4 mm insertion chamfer.
- Six shallow 2.0 x 1.75 mm floor ribs tie the standoff rows and columns into
  an orthogonal grid below the PCB without entering its clearance envelope.
- Four separate 10.2 mm-head x 10 mm-long push-on mushroom caps seat against
  the 1.7 mm PCB. Their lower 8 mm bodies are reduced to 6.8 mm diameter for
  component clearance. Each cap has a 3.8-to-3.0 mm tapered bore and three
  0.5 x 6 mm axial relief slots. The taper begins gripping the 3.4 mm post at
  5.0 mm depth, then develops about 0.21 mm nominal diametral interference at
  the end of the straight post while retaining 8.0 mm total engagement. A
  0.4 mm bed-face lead-in mitigates elephant foot.
- The separate six-spoke fan guard has a 64.1 mm square frame and a shallow
  locating skirt. The skirt leaves 0.2 mm clearance per side in the 62.1 mm
  lid opening and 0.3 mm clearance per side around the measured 60.1 mm fan.
- Four M4 fasteners for the LRS-350-24's official 150 x 50 mm bottom pattern;
  obey Mean Well's maximum screw-entry depth shown in the mechanical drawing.
- Press the four PCB caps down evenly until they contact the board; do not
  force a cap farther if the board begins to flex.
- Add mains-rated strain relief, ferrules, a suitable fuse/switch arrangement,
  and protective earth bonding to the Mean Well metal chassis.

## Printing notes

- The LRS print set has two separated objects. The SAB print set has nine:
  base, lid, four individual retaining caps, removable fan guard, and fit
  coupons for both the PCB post/cap and lid pin/base receiver.
- The SAB lid prints exterior-face-down with all four locating pins pointing
  upward; no pin support is required. Lower the installed lid evenly so the
  four tapered tips enter their receivers together without forcing them.
- The four PCB caps and both fit coupons are nested in the lid's fan opening. The
  caps print top-face-down; their flared openings and widening bores need no
  internal support. Print the two coupons first: test one production cap on the
  post coupon, then turn the male pin coupon over and test it in one receiver
  on the already-printed base before committing to the replacement lid.
- The raised lid prints exterior-face-down. Its 8 mm perimeter hood, plug, and
  pins grow upward from the bed without roof supports.
- The fan guard prints outer-face-down beside the enclosure, with its shallow
  locating skirt upward, and requires no support.
- Recommended structural profile: five wall loops, 25-35% gyroid infill,
  0.16-0.20 mm layers, and a 6-8 mm brim on the large base and lid. No supports
  are intended for any SAB print object.
- The SAB lid includes one 35.2 x 16 mm J013 opening and one continuous
  49.7 x 16 mm opening shared by J012 and DC. Because the lid prints
  exterior-face-down, these openings require no internal support.
- The negative-X short wall includes one 16 x 10 mm USB-C plug window, biased
  29 mm toward -Y, with 1.5 mm internal corner radii. The complete opening is
  raised so its bottom edge is 17.6 mm above the exterior floor and its top
  edge is 7 mm below the base rim. The 16 mm top bridge does not need support
  under normal bridge settings.
- The 5 mm circular short-wall perforations print without support; keep normal
  outer-wall cooling enabled so their upper arcs remain clean.
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

The validator checks solid validity, reference-envelope clearance, the two
physical front roof openings serving three plug zones, closed long walls, the
dedicated USB-C window, retained wall structure,
fan-frame clearance, raised-roof clearance, lid clearance, provisional standoff pattern,
integral chamfered PCB posts, floor ribs, four compliant mushroom caps, fan
guard clearance, both fit-coupon geometries, non-overlapping labeled assembly
structure, and 350 x 320 mm print-layout bounds.
