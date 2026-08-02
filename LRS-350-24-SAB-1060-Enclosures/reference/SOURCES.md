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
    fan. That estimate was superseded by the user's 60.5 mm physical square
    measurement and direction to center it on X. Dayton does not publish a
    dimensioned fan drawing.
  - Dayton does not publish a connector-location drawing. The model's earlier
    photo-derived long-edge USB placement was superseded by the user's physical
    observation: the port belongs on the negative-X short side. Its along-wall
    bias is now user-directed toward -Y.
- Dayton Audio, `SAB-1060 Quick Start Guide`:
  <https://www.daytonaudio.com/images/resources/325-510--dayton-audio-sab-1060-quick-start-guide.pdf>
  - Used for the connector map: two speaker-output headers, DC power, USB-C,
    fan power, control header, sync switch, and status LEDs.

## Provisional measurement requiring physical verification

- PCB thickness is modeled from the user's 1.7 mm physical dimension.
- The four SAB-1060 mounting holes are modeled as 3.8 mm diameter on a
  142 x 104 mm rectangle. This value is reported by a reseller and is not
  dimensioned in Dayton's public drawing.
- The fan frame is modeled from the user's 60.5 x 60.5 mm measurement and is
  centered on the board X axis with the user's observed 7 mm rearward Y bias.
  Its 14 mm height remains provisional; verify that height and the
  PCB-bottom-to-fan-top height against the physical assembly.
- The USB-C opening is provisionally 16 x 10 mm on the negative-X short side,
  centered 29 mm toward -Y. Verify the receptacle center and the
  intended cable's molded plug envelope against the physical board.
- Verify both center-to-center distances and hole diameter on the actual board
  before a production print. The 3.4 mm printed posts intentionally leave
  0.40 mm diametral clearance in the reported holes. Update the named constants in
  `enclosure_geometry.py` if the physical board differs.

## Search misses and resulting design choice

- No public manufacturer STEP model or fully dimensioned SAB-1060 connector
  location drawing was found.
- The enclosure therefore routes most pre-connected wiring through five
  reinforced cable bays on one long side. USB-C alone receives a compact,
  explicitly provisional opening on the user-directed short side.
