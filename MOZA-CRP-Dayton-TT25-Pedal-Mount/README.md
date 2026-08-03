# MOZA CRP2 Dayton TT25 Perpendicular Yoke Mount

Parametric STEP-first holder that places a Dayton Audio TT25-8 tactile puck 90 degrees to the side plane of a MOZA CRP2 pedal. A short reinforced lever joins the puck carrier to two arms that straddle the measured 8 mm attachment point.

## Files

- `moza_crp_dayton_tt25_mount.py` / `.step` — printable one-piece perpendicular yoke.
- `moza_crp_dayton_tt25_m6_insert.py` / `.step` — separate keyed M6 nut insert and fit-test object.
- `moza_crp_dayton_tt25_pedal_mount_fit_fixture.py` / `.step` — separate, lower-material partial-ring yoke containing the complete arms, levers, pivot receivers, and ring-junction lobes joined by a clipped section of the production ring.
- `moza_crp_dayton_tt25_print_set.py` / `.step` — holder and insert as two separate, bed-set objects.
- `moza_crp_dayton_tt25_fit_check.py` / `.step` — installed assembly with the official TT25, measured CRP2 attachment envelope, M6 nut, and socket-head bolt.
- `validate_mount.py` — deterministic geometry and interference checks.
- `cad_brief.md` — dimensions, coordinate convention, assumptions, and validation targets.
- `reference/dayton_tt25-8_and-16.step` — unmodified official Dayton reference STEP.
- `snapshots/` — reviewed CAD renders.

## Design

- Puck face: XZ plane, exactly 90 degrees to the pedal's installed YZ side plane.
- Puck center: 65 mm above and 26 mm behind the pedal pivot.
- Carrier: 106 mm outside diameter × 8.5 mm thick.
- TT25 relief: 70.5 mm through opening plus an 82.0 mm × 1.7 mm shallow rear-cover seat.
- Puck orientation: rotated 180 degrees about installed Z, with the Dayton logo facing outward (negative Y) and the opposite lug faces seated directly on the carrier.
- Puck attachment: six exact, rotation-matched manufacturer-pattern 3.8 mm holes with pedal-side M3 nut traps.
- Measured CRP2 interface: 8.0 mm attachment width with a 10.0 mm across-flats internal hex.
- Yoke: two 4.5 mm arms with an 8.6 mm clear span, leaving 0.3 mm nominal clearance on each side of the measured attachment.
- Pedal clearance: the former Ø33 mm circular pivot profiles are flattened into 20 mm-deep D-shaped bosses. The pedal-side face is 10 mm from the bolt center at Y=+10 mm, and the opposite pivot-frame face is Y=-10 mm, 20 mm from that pedal-back datum. The M6 bolt axis remains unchanged.
- Arm-to-ring reinforcement: each arm terminates in a smooth 28 mm lobe centered at Y=-15.5, Z=20 mm. The lobes stop 0.75 mm short of the puck-facing carrier surface and retain approximately 508/525 mm³ of arm-to-ring overlap after relief cuts, roughly 2.4× the former junction contact.
- Pivot: 6.6 mm M6 clearance through both arms.
- Reversible receivers: matching 10.4 mm across-flats M6 nut pockets on both arms, each 5.2 mm deep with a 4.0 mm printed support floor.
- Reference hardware: standard M6 nut and M6 × 25 socket-head bolt.
- Keyed insert: 9.6 mm across-flats × 7.6 mm pilot for the measured 10 mm hex, an 18 mm diameter × 7 mm flange, a 10.4 mm M6 nut pocket, and a 6.6 mm through bore. The insert prints as a separate object.
- Wire routing: enclosed 10 mm round pass-through at the bottom of the carrier, aligned to the midpoint of the lower TT25 screw pair. The narrower CRP2 yoke requires shallow 0.92/0.48 mm reliefs in the adjacent arms; at least 3.58 mm local arm thickness remains, and the hole retains approximately 3.9 mm to both ring boundaries.

## Installation

Remove the original attachment bolt and washers. Place the two printed fork arms around the 8 mm CRP2 attachment, insert the M6 nut into either external arm pocket, and pass the bolt through the opposite receiver, pedal attachment, and captured nut. The socket head nests in the unused receiver, so the hardware direction is reversible. Confirm the pedal still moves freely before attaching the TT25.

The optional keyed insert is a separate fit/retention accessory. Its pilot checks the measured 10 mm internal hex while its external flange accepts the same M6 nut used by the arms. Because the CRP2 hex depth and center opening were not measured, verify that the 7.6 mm pilot seats fully and that the 18 mm flange has exterior clearance before loading it.

For a lower-material fit check, print `moza_crp_dayton_tt25_pedal_mount_fit_fixture.step`. It contains the complete production yoke from the D-shaped pivot receivers through the reinforced lever profiles and 28 mm ring-junction lobes. A narrow, exact section of the production carrier ring remains around the lower lobe junctions, connecting the arms into one rigid object and preserving the real 8.6 mm fork spacing. The rest of the 106 mm Dayton ring is omitted. The fixture is arranged with the retained ring face on the build plate and may require support beneath the elevated pivot arms. Use the intended M6 hardware to verify the fork gap, flat-face clearance, bolt alignment, nut-pocket access, lever clearance, and lobe position. The fixture is not a load-bearing substitute for the complete holder.

The M6 × 25 bolt is the modeled reference for the revised stack. Select a bolt that fully engages the 5 mm nut without projecting into moving components, and match or exceed the original bolt's strength grade.

## Hardware

- 6× M3 × 18 screws. The reversed 8.5 mm TT25 lug plus 8.5 mm carrier stack is 17.0 mm to the outer nut face, leaving approximately 1.0 mm tip projection.
- 6× M3 standard nuts.
- 1× M6 standard hex nut, 10 mm across flats and approximately 5 mm thick.
- 1× appropriately graded M6 socket-head bolt; M6 × 25 is shown in the fit check.

## Printing

- Use the two-object print-set STEP for the pre-arranged holder and insert, or rotate the standalone holder so the broad puck-carrier face lies on the bed.
- Print the insert pilot-down; its nut pocket opens upward and requires no internal support.
- Enable tree/organic supports beneath the elevated fork and pivot bosses.
- Prefer ASA/ABS, PA, PA-CF, or PET-CF. PETG is suitable for a first prototype; avoid PLA for long-term vibration service.
- Start with 0.20 mm layers, 6 walls, 6 top/bottom layers, and 45-60% gyroid or cubic infill.
- Apply a 100% infill modifier around both pivot bosses and the lever-to-carrier junctions.

## First-fit checks

Before installation, verify the 8.0 mm attachment width, 10.0 mm internal hex, M6 hardware, and the 8.6 mm yoke span. The new D-shaped pivot uses the supplied rough dimensions, so also verify that the Y=+10 mm flat seats without touching the pedal body and that the 20 mm flat-to-outer-frame depth is sufficient. Test the insert separately before applying clamp load. Check that neither arm binds the pedal, the puck clears the frame throughout pedal travel, and the cable cannot contact a moving linkage. Retighten after a short vibration test and recalibrate the pedal if its sensor reading changes.

This is a prototype accessory, not a MOZA- or Dayton-certified part. No structural FEA or fatigue certification has been performed.
