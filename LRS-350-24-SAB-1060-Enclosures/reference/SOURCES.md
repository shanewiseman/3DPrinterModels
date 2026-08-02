# Sources and measurement status

## Manufacturer sources

- Mean Well, `LRS-350 Series` specification and mechanical drawing:
  <https://www.meanwell.com/Upload/PDF/LRS-350/LRS-350-SPEC.PDF>
  - Used for the 215 x 115 x 30 mm case envelope, airflow/terminal-end
    orientation, and four-hole 150 x 50 mm bottom M4 mounting pattern.
- Dayton Audio, `SAB-1060 Sim 7.3 Channel Amplifier Board`:
  <https://www.daytonaudio.com/product/2059/sab-1060-sim-7-3-channel-sim-racer-arcade-amplifier-board-10-x-60w>
  - Used for the 152.4 x 114.3 x 28.6 mm overall board-with-fan envelope and
    15-30 VDC operating range.
  - The official orthogonal product photo was initially used to estimate the
    fan. That estimate was superseded by the user's 60.1 mm physical square
    measurement and rear-view edge measurements. Dayton does not publish a
    dimensioned fan drawing.
  - Dayton does not publish a connector-location drawing. The model's earlier
    photo-derived long-edge USB placement was superseded by the user's physical
    observation: the port belongs on the negative-X short side. Its along-wall
    bias is now user-directed toward -Y.
- Dayton Audio, `SAB-1060 Quick Start Guide`:
  <https://www.daytonaudio.com/images/resources/325-510--dayton-audio-sab-1060-quick-start-guide.pdf>
  - Used for the connector map: two speaker-output headers, DC power, USB-C,
    fan power, control header, sync switch, and status LEDs.
  - The embedded orthogonal top-view image is also used to estimate the front
    plug centers. Scaling its connector centers from the reported 142 mm
    mounting-hole span gives provisional enclosure X centers of -44.0 mm for
    J013, +29.5 mm for J012, and +55.0 mm for DC input. The original opening
    dimensions were user-specified at 32 x 16, 32 x 16, and 10 x 16 mm. The
    widths are now 35.2, 35.2, and 13.2 mm to add 1.6 mm photo-placement
    clearance per side; the user-directed 16 mm depth remains unchanged. The
    J012 and DC zones share one continuous 49.7 x 16 mm opening with no divider.

## Provisional measurement requiring physical verification

- PCB thickness is modeled from the user's 1.7 mm physical dimension.
- The four SAB-1060 mounting holes are modeled as 3.8 mm diameter on a
  142 x 104 mm rectangle. This value is reported by a reseller and is not
  dimensioned in Dayton's public drawing.
- The fan frame is modeled from the user's 60.1 x 60.1 mm measurement. Viewed
  from the rear, the user measured rear/front/left/right clearances of
  24.5/35.9/47.6/50.7 mm. Rear-view left is modeled as +X and rear as +Y,
  placing the measurement-derived fan center at X=+1.55 mm and Y=+5.70 mm.
  The latest user instruction overrides X by moving the opening/reference/guard
  2 mm toward rear-view right, producing final X=-0.45 mm. The physical X stack
  exactly matches the 158.4 mm CAD interior; the physical Y stack is 120.5 mm,
  0.2 mm above the fixed 120.3 mm CAD interior, so the model splits that
  discrepancy equally. Its 14 mm height remains provisional; verify that
  height and the PCB-bottom-to-fan-top height against the physical assembly.
- The USB-C opening remains 16 x 10 mm on the negative-X short side, centered
  29 mm toward -Y. The user's physical-access direction moves the entire window
  upward to leave 7 mm between its top edge and the base rim, producing a
  17.6 mm lower sill. Verify the receptacle center and the intended cable's
  molded plug envelope against the physical board. The provisional connector
  envelope is centered vertically in this user-directed opening.
- The replacement SAB lid's 8 mm rise and the 5 mm wall-inset component
  clearance come from the user's physical test of the already-printed base.
  The base height and pin receivers remain unchanged. The later upward USB
  window move changes the negative-X wall and requires a base reprint.
- The three front connector access zones share a provisional installed Y center of
  -50.5 mm. This places their front edge 1.65 mm inside the enclosure's inner
  front wall while covering the official-image plug row. Verify all X/Y centers
  and cable-latch swing space on the populated board.
- The printed base's 4.6 mm receivers produced an overly tight line-to-line
  fit, so the user requested a slight reduction of the replacement lid pins.
  The production pins and matching coupon are now 4.5 mm maximum diameter.
- Verify both center-to-center distances and hole diameter on the actual board
  before a production print. The 3.4 mm printed posts intentionally leave
  0.40 mm diametral clearance in the reported holes. Update the named constants in
  `enclosure_geometry.py` if the physical board differs.

## Search misses and resulting design choice

- No public manufacturer STEP model or fully dimensioned SAB-1060 connector
  location drawing was found.
- The earlier five-window long-wall cable bank is now closed. The replacement
  lid instead uses two rectangular roof openings above the three official-guide
  plug groups; J012 and DC share one opening. USB-C retains its separate, explicitly
  provisional opening on the user-directed short side.

## Print-driven dimensions

- The 6.8 mm mushroom-cap body, three 0.5 x 6 mm relief slots, 0.4 mm lead-ins,
  2.0 x 1.75 mm floor ribs, six-spoke guard, and fit coupon are design choices
  for FDM printability and serviceability; they are not manufacturer datums.
- The male lid-pin coupon reproduces the existing parametric pin exactly so its
  0.10 mm diametral-clearance receiver fit can be checked before printing the
  raised lid.
- Test the coupon in the intended filament and slicer profile before printing
  the full enclosure. Adjust the named fit constants if the production printer
  produces materially different hole or post dimensions.
