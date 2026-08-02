# MOZA CRP Dayton TT25 Perpendicular Yoke Mount

Parametric STEP-first holder that places a Dayton Audio TT25-8 tactile puck 90 degrees to the side plane of an original MOZA CRP pedal. A short reinforced lever joins the puck carrier to two arms that straddle the upper pedal pivot.

## Files

- `moza_crp_dayton_tt25_mount.py` / `.step` — printable one-piece perpendicular yoke.
- `moza_crp_dayton_tt25_fit_check.py` / `.step` — installed assembly with the official TT25, assumed pedal-pivot envelope, M8 nut, and socket-head bolt.
- `validate_mount.py` — deterministic geometry and interference checks.
- `cad_brief.md` — dimensions, coordinate convention, assumptions, and validation targets.
- `reference/dayton_tt25-8_and-16.step` — unmodified official Dayton reference STEP.
- `snapshots/` — reviewed CAD renders.

## Design

- Puck face: XZ plane, exactly 90 degrees to the pedal's assumed YZ side plane.
- Puck center: 65 mm above and 26 mm behind the pedal pivot.
- Carrier: 106 mm outside diameter × 8.5 mm thick.
- TT25 relief: 70.5 mm through opening plus an 82.0 mm × 1.7 mm shallow rear-cover seat.
- Puck orientation: rotated 180 degrees about installed Z, with the Dayton logo facing outward (negative Y) and the opposite lug faces seated directly on the carrier.
- Puck attachment: six exact, rotation-matched manufacturer-pattern 3.8 mm holes with pedal-side M3 nut traps.
- Yoke: two 4.5 mm arms with a 20.6 mm clear span around an assumed 20.0 mm pedal mount.
- Pivot: 8.6 mm M8 clearance through both arms.
- Reversible receivers: matching 13.4 mm across-flats pockets on both arms, each 6.8 mm deep with a 4.0 mm printed support floor.
- Reference hardware: standard M8 nut and M8 × 40 socket-head bolt.
- Wire routing: enclosed 10 mm round pass-through at the bottom of the carrier, aligned to the midpoint of the lower TT25 screw pair and located between the yoke arms. It retains approximately 3.9 mm of material to both ring boundaries and at least 5.1 mm to either arm.

## Installation

Remove the original upper pivot bolt and washers. Place the two printed fork arms on opposite sides of the pedal pivot, insert the M8 nut into either external hex pocket, and pass the bolt through the opposite receiver, pedal pivot, and captured nut. The socket head nests in the unused receiver, so the hardware direction is reversible. Confirm the pedal still moves freely before attaching the TT25.

The modeled 20 mm pedal width and M8 × 40 bolt are first-fit references. Measure the actual width across the pivot and select a bolt that fully engages the 6.5 mm nut without projecting into moving components. Match or exceed the original bolt's strength grade. The puck reversal does not change this M8 pivot stack; the reduced fastener is the TT25's M3 mounting screw.

## Hardware

- 6× M3 × 18 screws. The reversed 8.5 mm TT25 lug plus 8.5 mm carrier stack is 17.0 mm to the outer nut face, leaving approximately 1.0 mm tip projection.
- 6× M3 standard nuts.
- 1× M8 standard hex nut, 13 mm across flats and approximately 6.5 mm thick.
- 1× appropriately graded M8 socket-head bolt; M8 × 40 is shown in the fit check.

## Printing

- Rotate the part in the slicer so the broad puck-carrier face lies on the bed.
- Enable tree/organic supports beneath the elevated fork and pivot bosses.
- Prefer ASA/ABS, PA, PA-CF, or PET-CF. PETG is suitable for a first prototype; avoid PLA for long-term vibration service.
- Start with 0.20 mm layers, 6 walls, 6 top/bottom layers, and 45-60% gyroid or cubic infill.
- Apply a 100% infill modifier around both pivot bosses and the lever-to-carrier junctions.

## First-fit checks

Before installation, measure the pedal pivot width, verify M8 hardware, and compare the measurement with the 20.6 mm yoke span. Check that neither arm binds the pedal, the puck clears the frame throughout pedal travel, and the cable cannot contact a moving linkage. Retighten after a short vibration test and recalibrate the pedal if its sensor reading changes.

This is a prototype accessory, not a MOZA- or Dayton-certified part. No structural FEA or fatigue certification has been performed.
