# CAD brief: LRS-350-24 and SAB-1060 enclosures

## Objective

Create printable covers for a Mean Well LRS-350-24 power supply and a Dayton
Audio SAB-1060 amplifier board while preserving access to every connection and
maintaining airflow. Use separate enclosures to segregate mains wiring from the
low-voltage audio board and to keep each print within the target printer bed.

## Source dimensions

- LRS-350 family: 215 x 115 x 30 mm, from the Mean Well manufacturer sheet.
- LRS cable-service allowance: user-directed 15 mm extension of only the +X
  side; the power-supply envelope and 150 x 50 mm mount pattern remain at
  their original global coordinates.
- SAB-1060 with fan: 152.4 x 114.3 x 28.6 mm, from Dayton Audio.
- SAB-1060 connector identities: Dayton Audio quick-start guide.
- SAB-1060 mounting pattern: 142 x 104 mm with reported 3.8 mm holes. This is
  a provisional third-party datum and must be checked on the physical board.
- SAB-1060 PCB thickness: user-specified 1.7 mm.
- SAB fan: user-measured 60.1 x 60.1 mm frame. Viewed from the rear, its edge
  clearances are rear 24.5 mm, front 35.9 mm, left 47.6 mm, and right 50.7 mm.
  Rear-view left maps to +X and rear maps to +Y, giving a measurement-derived
  center of X=+1.55 mm and Y=+5.70 mm. The latest user direction shifts the
  fan opening/reference/guard 2 mm toward rear-view right (global -X), so the
  final center is X=-0.45 mm and Y=+5.70 mm. The physical Y measurements total 120.5 mm versus
  the fixed 120.3 mm CAD-base interior, so the 0.2 mm discrepancy is reconciled
  evenly. Its 14 mm height remains provisional because Dayton does not publish
  a fan drawing.
- SAB USB-C: user-directed orientation on the negative-X short side, centered
  29 mm toward -Y; exact receptacle and molded-plug envelope remain
  unpublished and must be checked physically.
- SAB lid clearance: user-reported interference with capacitors located 5 mm
  inward from the base wall; the replacement lid adds 8 mm of interior height
  while retaining the existing base mating geometry. A later USB-window move
  changes the negative-X base wall and therefore requires a reprinted base.
- SAB front plug access: one 35.2 x 16 mm roof opening above J013 at
  X=+44.0 mm and one continuous 49.7 x 16 mm opening centered at X=-36.75 mm
  for the J012 14-pin header and four-pin DC input. The joined opening removes
  the former 1.3 mm divider while preserving 35.2 and 13.2 mm access envelopes.
  These retain the user-sized 16 mm depth while adding 1.6 mm of X clearance
  on each side beyond the original 32, 32, and 10 mm widths. The user-corrected
  zone centers +44.0, -29.5, and -55.0 mm mirror the initial top-view estimate;
  all share installed Y=-50.5 mm and require physical verification.

## Datums and coordinate convention

- Global XY is the printer bed; +Z is up.
- Each base floor starts at Z=0.
- Component length is global X, width is global Y.
- Lid source geometry is exterior-face-down at Z=0 for support-free printing.

## Functional geometry

- 3.0 mm walls and floor. The SAB lid top remains 3.0 mm; the LRS lid top is
  3.30 mm so its 1.65 mm button-head recess is exactly half the lid thickness.
- 0.30 mm lid locating clearance per side.
- The LRS uses four external M3 lid towers with side-loading captive-nut traps.
  Standard 5.5 mm-across-flats x 2.4 mm-thick M3 nuts fit 5.8 mm-across-flats
  x 2.8 mm-high pockets through 5.8 x 3.0 mm outward-facing insertion slots.
  Their centers are at Z=25.25 mm in the 38 mm base. Four M3 x 16 mm
  button-head screws pass through 3.4 mm lid/base bores and seat in 6.2 mm
  diameter x 1.65 mm-deep lid recesses. The modeled 1.65 mm-high heads finish
  flush with the 3.30 mm-thick lid exterior. A separate 14 x 14 x 10 mm coupon
  reproduces the production nut fit, insertion slot, and screw bore.
- The SAB lid uses four integral 4.0 mm tapered locating pins, 5.5 mm long.
  Their 3.2 mm lead-in tips taper to a 4.0 mm straight land in four unchanged
  4.6 mm diameter x 6.0 mm deep blind base receivers. The free-sliding fit has
  0.60 mm diametral (0.30 mm radial) and 0.50 mm axial clearance; the pins
  center the lid but intentionally provide no retention.
- The SAB lid is a support-free 8 mm raised hood. Its roof underside is
  Z=42.6 mm and exterior is Z=45.6 mm, while its mating rim, plug, and pins
  retain the original Z=34.6 mm base interface. The full interior region at
  least 5 mm inward from every base wall remains free of lid geometry from the
  plug depth through the raised roof.
- All four LRS and all four SAB lid/base corner locations use filled,
  broad-root gussets tied into both adjacent enclosure walls. Their wall
  contact is twice the original tangent run while the final approach to each
  circular boss remains 45 degrees.
- LRS internal clearance: 4.0 mm per side; full terminal-end service bay;
  the +X cable side adds 15 mm, making the final clearances 4.0 mm at -X and
  19.0 mm at +X. The inner X limits are -111.5 and +126.5 mm, the outer wall
  limits are -114.5 and +129.5 mm, and the 244 mm-long enclosure body is
  centered at X=+7.5 mm while the PSU remains centered at X=0. Closed long
  walls and slotted lid ventilation; four bottom mounting pads and
  4.5 mm through holes on the official 150 x 50 mm M4 pattern. The four former
  rectangular windows on the positive-X short end are replaced by 8 mm and
  5 mm circular ports. Viewed from outside that wall, their centers are 20 mm
  and 60 mm from the right edge respectively, both at Z=20 mm. Six 3.0 mm-wide
  x 0.5 mm-high ribs form a pad-to-pad orthogonal grid while preserving 0.5 mm
  clearance below the modeled power-supply chassis. The matching lid retains
  its eight original vent columns and adds one at X=+108 mm above the new bay.
- SAB internal clearance: 3.0 mm per side; both long base walls are closed;
  both short base walls carry 5 mm circular ventilation perforations in a
  seven-column by four-row grid. The positive-X wall retains all 28 holes and
  the negative-X USB wall retains 22 after applying a 1 mm inlet keepout. Hole
  edges remain at least 1 mm above the interior floor, below the wall top, and
  away from the wall sides;
  two rectangular raised-lid roof openings provide vertical service above the
  three front plug zones—35.2 x 16 mm at X=+44.0 mm for J013 and a continuous
  49.7 x 16 mm opening centered at X=-36.75 mm for J012/DC, both centered at
  Y=-50.5 mm; one 16 x 10 mm USB-C plug window with
  1.5 mm internal corner radii on the negative-X short wall, centered 29 mm
  toward -Y, raised to a 17.6 mm lower sill and 7 mm upper sill; four raised
  9 mm-diameter
  mounting standoffs. Each standoff carries an integral 3.4 mm post that clears
  the reported 3.8 mm PCB hole by 0.40 mm diametrally and extends through the
  1.7 mm board for 8.0 mm of nominal cap engagement. The posts terminate in
  0.4 mm conical insertion chamfers.
- Six 2.0 mm-wide x 1.75 mm-high floor ribs form a low orthogonal grid between
  standoff rows and columns. Their 4.75 mm top remains 4.25 mm below the PCB.
- Four separate 10.2 mm-head, 10 mm-high push-on mushroom caps retain the SAB
  PCB. Their lower 8 mm body is 6.8 mm diameter; each cap head remains exactly
  three times the 3.4 mm post diameter. Each support-free tapered through-bore
  narrows from 3.8 mm at the board face to 3.0 mm at the top, reaching the
  3.4 mm post diameter at 5.0 mm depth. At the end of the straight post, the
  nominal bore is 3.192 mm, providing about 0.208 mm diametral interference.
  Three 0.5 mm-wide x 6 mm-deep radial slots make the upper taper compliant,
  while a 4 mm uncut board-side ring and shorter fingers increase spring force.
  The print-bed face has a 0.4 mm outer chamfer and flared bore lead-in for
  elephant-foot tolerance.
- The SAB fan top remains at Z=37.6 mm. A 62.1 x 62.1 mm raised-roof opening
  surrounds the user-measured 60.1 mm fan with 1 mm clearance per side at
  X=-0.45 mm and Y=+5.70 mm after the 2 mm rear-view-right shift. The new roof underside is 5 mm above the fan top.
- A separate 64.1 mm, six-spoke, 1.6 mm-thick fan guard locates in that opening
  with a 1.2 mm-deep skirt. An integral perimeter riser supports the spoke
  field 2 mm above the lid, placing the installed guard top 49.2 mm above the
  base.
- A separate 14 x 10 mm fit coupon reproduces the production 3.4 mm post and
  8.0 mm cap engagement so retention can be tuned before the full print.
- A second 14 x 10 mm coupon carries the exact 4.0 mm x 5.5 mm tapered lid pin
  so it can be tested directly in the already-printed base receiver.
- The LRS STEP print set contains three spatially separated objects: base,
  lid, and M3 captive-nut-trap fit coupon. The SAB STEP print set contains
  nine: base, raised lid, four top-face-down caps, fan guard, and two fit
  coupons. The SAB caps and coupons nest in the lid opening; the guard sits
  beside the enclosure, and no print solids overlap.

## Outputs

- `lrs_350_24_print_set.step`: Mean Well base, lid, and M3 captive-nut fit
  coupon, laid out for printing.
- `sab_1060_print_set.step`: Dayton base, raised lid, four separate retaining
  caps, fan guard, and two fit coupons laid out for printing.
- `enclosure_fit_check.step`: both installed-pose enclosures with simplified
  component reference envelopes.

## Acceptance criteria

- All twelve printable enclosure objects are valid, positive-volume single solids.
- Reference envelopes do not intersect printed base or installed lid geometry.
- Terminal/connector access probes remain unobstructed; the three SAB roof
  zones retain 35.2 x 16, 35.2 x 16, and 13.2 x 16 mm access envelopes. One
  continuous 49.7 x 16 mm probe proves no divider remains between J012 and DC.
- Both LRS long walls and the positive-X short end have no rectangular
  windows; the short end's unobstructed circular ports are exactly 8 mm and
  5 mm diameter, with centers 20 mm and 60 mm from the exterior-view right
  edge.
- All four LRS mount centers retain side-loading M3 nut traps at Z=25.25 mm;
  nominal 5.5 x 2.4 mm nuts and M3 x 16 button-head screw envelopes clear the
  printed base and lid. The 6.2 x 1.65 mm lid recesses fit the modeled 5.7 x
  1.65 mm button heads, occupy half the 3.30 mm lid thickness, and leave the
  heads flush with the exterior.
- The reported SAB hole pattern is represented exactly but documented as a
  measurement that must be verified.
- The board reference is 1.7 mm thick; all four posts clear its modeled holes,
  and all four installed caps seat on its top surface without solid overlap.
- The LRS floor ribs preserve 0.5 mm PSU clearance, the SAB floor ribs remain
  below the PCB, the fan guard clears both fan and lid, its spoke field is
  supported 2 mm above the lid, and all coupons duplicate their production
  interfaces.
- The SAB base exterior dimensions and 4.6 x 6.0 mm receiver interface remain
  unchanged, while the raised USB opening changes the negative-X wall. The SAB
  lid adds exactly 8 mm above the original mating plane and clears the 5 mm
  inset component zone.
- The user-measured SAB fan square and user-directed 2 mm rear-view-right
  center shift are represented exactly; its rearward center and provisional height must be physically verified before
  a production print.
- The user-directed USB-C wall, negative-Y center, and plug clearance must be
  physically verified before a production print.
- The LRS mounting pattern is represented at the official 150 x 50 mm spacing.
- The LRS -X enclosure wall, PSU envelope, and four PSU mount centers remain
  fixed while only the +X wall, two +X lid fasteners, ports, and matching lid
  extend 15 mm.
- Both enclosures retain broad-root 45-degree reinforcement at every base
  tower and lid ear.
- Each layout fits within 350 x 320 mm and remains above Z=0; the LRS layout
  exports exactly three and the SAB layout exactly nine non-overlapping,
  positive-volume print objects.

## Out of scope

- Electrical safety certification, flame-rating certification, and wiring.
- Connector-latch-specific contours; the three front accesses are rectangular
  service openings and their photo-derived centers require physical checking.
- Thread modeling; the LRS lid hardware is represented by clearance and insert
  bores, while the SAB uses printed friction-fit retainers.
