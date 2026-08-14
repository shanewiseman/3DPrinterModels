# CAD brief

- Model: Bambu X2D dual AMS 2 Pro top/side mount.
- Task type: new multi-part assembly; first provisional assembled STEP.
- Inputs: user concept sketch `reference/1000020266.jpg`, published product
  dimensions, and future physical measurements.
- Units: millimeters.
- Assembly coordinate convention: origin at the center of the X2D top envelope;
  X left-to-right, Y front-to-back, and +Z upward.
- Product envelopes: X2D 392 × 406 × 478 mm; each AMS 2 Pro
  372 × 280 × 226 mm.
- Printing constraint: all individual printed parts must fit the X2D main-nozzle
  256 × 256 mm XY area. The longest modeled part dimension is 252 mm, with
  final allowance selected from the material and adhesion strategy.
- Assembly concept: mirrored left/right 211.1 × 252 mm outboard support
  shelves, each with front and rear triangular brackets. The AMS units
  themselves are moved inward and arranged side-by-side as a pair centered on
  X=0. Each AMS places its outer foot pair on one printed shelf and its inner
  foot pair directly on the normal X2D top datum.
- AMS pair positioning: 25.4 mm body-to-body gap; centers at X=±198.7 mm;
  combined AMS footprint X=-384.7 to +384.7 mm. This leaves 188.7 mm of AMS
  body beyond each 196 mm printer side rather than placing both AMS units fully
  outboard.
- Shelf outboard sizing: roots remain at X=±199.0 mm, 3 mm clear of the
  provisional printer sides. Outer faces are X=±410.1 mm, exactly 25.4 mm
  beyond the corresponding AMS outer face, yielding a 211.1 mm X span.
- Shelf connection revision: two removable 50 mm-deep × 3 mm-high planar ASA
  truss ties cross the X2D at Y=±70 mm, between the provisional AMS foot rows.
  Their flat spans remain below the provisional 4 mm AMS underside datum. Each
  half has a narrow 9 mm-wide center boss rising to 25.4 mm only inside the
  25.4 mm gap between the AMS bodies; three transverse M4 bolts join each
  center seam. Each half overlaps its shelf by 50 mm and uses three recessed
  vertical M4 bolts with underside captive nuts.
- Payload orientation: both AMS units face global front in coordination with
  the X2D. The 372 mm AMS width is global X and the 280 mm depth is global Y.
- Provisional envelope consequence: the centered AMS pair spans 769.4 mm and
  has a 25.4 mm center gap. Each 211.1 mm outboard shelf supports only the outer
  foot pair; the inner foot pair remains on the X2D top. The AMS envelopes
  overhang the centered 252 mm shelf depth by 14 mm front and rear.
- Shelf implementation: two 211.1 × 252 mm flat plates with 6 mm skins,
  6 mm-deep underside ribs, four bracket lands, and two low-profile tie-overlap
  lands per shelf. No foot rails are needed for the provisional centered foot
  pattern.
- Elevation constraint: connecting the shelves must not change foot support Z
  or raise either AMS. The planar tie spans occupy Z=0–3 mm only between the
  foot rows, below the provisional AMS body underside at Z=4 mm. Center bosses
  rise only inside the clear 25.4 mm gap between AMS envelopes.
- Bracket intent: right triangle with 25.4 mm perimeter chords, internal
  triangular webbing, broad radiused nodes, and a broad-face-down print
  orientation. Every 10 mm inner web endpoint reaches the exact centerline of
  its top or diagonal perimeter chord for deliberate fused engagement.
- Hardware intent: M4 button-head screws and 4.5 mm nominal clearance.
  Bracket-to-shelf fasteners use plain through-holes with heads intentionally
  proud of the shelf top; replaceable captive M4 nuts remain in bracket top
  chords. Recesses remain only where required by the low-profile tie geometry.
- Printer interface: no drilling or permanent modification. The inner AMS feet
  and low-profile ties use the normal X2D top datum in this conceptual revision;
  their exact bearing zones and glass compatibility remain measurement items.
- Door constraint: the front low-profile tie remains inside the X2D top footprint,
  behind the closed front-door plane and above the complete upper-door/hinge
  sweep. The door-open envelope is a mandatory assembly keep-out volume.
- Initial working load: 10 kg per shelf with a 2.5× geometry-sizing load case.
  This is a prototype target, not a certification.
- Manufacturing assumptions: every structural member is printed in ASA; no
  aluminum or other metal structural member is permitted. M4 screws and nuts
  remain assembly hardware. Small interface and hardware coupons precede
  full-size prints.
- Positioning/mating: AMS foot pads define the payload datum; shelf upper face
  defines support Z; bracket upper chord mates to shelf underside; each planar
  tie overlaps its shelf top by 50 mm; inner AMS feet and tie spans use the
  physically verified X2D top datum.
- Source/artifact paths: `x2d_dual_ams_mount_geometry.py`,
  `x2d_dual_ams_mount_assembly.py`, `validate_mount.py`, and
  `x2d_dual_ams_mount_assembly.step`.
- Individual print exports: 14 part STEP files under `printable_parts/`, one
  for each shelf, bracket, low-tie half, and side pad occurrence. Exported
  parts retain the assembly geometry but use manufacturing coordinates:
  centered on XY, lowest face at Z=0, brackets laid on their broad truss face,
  and side pads laid on their largest face.
- Validation targets: valid labeled solids; every print part within the chosen
  bed allowance; correct 25.4 mm outer chords; M4 hole/nut alignment; AMS feet
  fully supported at the same Z with or without the bridge; no obstruction of
  AMS vents/lids; glass removal clearance; positive clearance through the full
  printer-door swing; screen/rear-module/purge access; broad PTFE bends;
  symmetric installed load path; and no collision between left/right modules.
- Individual export validation: every `printable_parts/*.step` file must contain
  exactly one valid solid, preserve source volume, and remain within the
  252 mm single-part envelope in its saved print orientation.
- Required physical inputs: top-edge profile and bearing zones, glass geometry,
  side-panel setbacks/features, closed/open front-door envelope, front/rear
  bracket locations, AMS foot pattern, AMS underside vents, and desired service
  access.
- Production blocker: published envelope dimensions do not define either mating
  interface. The current STEP is intentionally provisional and must not be
  treated as installation-ready until the physical X2D and AMS measurements
  are substituted and the assembly is proof-tested away from the printer.
