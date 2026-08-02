# CAD brief: LRS-350-24 and SAB-1060 enclosures

## Objective

Create printable covers for a Mean Well LRS-350-24 power supply and a Dayton
Audio SAB-1060 amplifier board while preserving access to every connection and
maintaining airflow. Use separate enclosures to segregate mains wiring from the
low-voltage audio board and to keep each print within the target printer bed.

## Source dimensions

- LRS-350 family: 215 x 115 x 30 mm, from the Mean Well manufacturer sheet.
- SAB-1060 with fan: 152.4 x 114.3 x 28.6 mm, from Dayton Audio.
- SAB-1060 connector identities: Dayton Audio quick-start guide.
- SAB-1060 mounting pattern: 142 x 104 mm with reported 3.8 mm holes. This is
  a provisional third-party datum and must be checked on the physical board.
- SAB-1060 PCB thickness: user-specified 1.7 mm.
- SAB fan: user-measured 60.5 x 60.5 mm frame, centered on X by direction and
  biased 7 mm toward the +Y rear by user observation. Its 14 mm height remains
  provisional because Dayton does not publish a fan drawing.
- SAB USB-C: user-directed orientation on the negative-X short side, centered
  29 mm toward -Y; exact receptacle and molded-plug envelope remain
  unpublished and must be checked physically.

## Datums and coordinate convention

- Global XY is the printer bed; +Z is up.
- Each base floor starts at Z=0.
- Component length is global X, width is global Y.
- Lid source geometry is exterior-face-down at Z=0 for support-free printing.

## Functional geometry

- 3.0 mm walls, floor, and lid top.
- 0.30 mm lid locating clearance per side.
- The LRS uses four external M3 lid towers with 4.6 mm heat-set-insert pockets.
- The SAB lid replaces through-screws with four integral 4.6 mm tapered pins,
  5.5 mm long. Their 3.6 mm lead-in tips taper to a full-diameter clamping land
  in four 4.6 mm diameter x 6.0 mm deep blind base receivers. The nominal fit
  is line-to-line radially with 0.50 mm axial clearance.
- The four SAB lid/base screw locations use filled, broad-root gussets tied
  into both adjacent enclosure walls. Their wall contact is twice the original
  tangent run while the final approach to each circular boss remains 45 degrees.
- LRS internal clearance: 4.0 mm per side; full terminal-end service bay;
  slotted side, rear, and lid ventilation; four bottom mounting pads and
  4.5 mm through holes on the official 150 x 50 mm M4 pattern.
- SAB internal clearance: 3.0 mm per side; five
  22 x 12 mm cable exits on one long side with 5 mm vertical ribs, a 17 mm
  lower sill, and a 5.6 mm upper rail; one 16 x 10 mm USB-C plug window with
  1.5 mm internal corner radii on the negative-X short wall, centered 29 mm
  toward -Y, with a 7 mm sill and 17.6 mm top rail; four raised 9 mm-diameter
  mounting standoffs. Each standoff carries an integral 3.4 mm post that clears
  the reported 3.8 mm PCB hole by 0.40 mm diametrally and extends through the
  1.7 mm board for 8.0 mm of nominal cap engagement.
- Four separate 10.2 mm-diameter, 10 mm-high push-on caps retain the SAB PCB;
  each cap is exactly three times the 3.4 mm post diameter.
  Each cap's support-free tapered through-bore narrows from 3.8 mm at the board
  face to 3.3 mm at the top, reaching the 3.4 mm post diameter at 8.0 mm depth.
- SAB finished height: 37.6 mm. A 62.5 x 62.5 mm lid opening surrounds the
  user-measured 60.5 mm fan with 1 mm clearance per side, centered on X, so its
  upper frame is flush with the lid surface.
- The LRS STEP print set contains two spatially separated objects. The SAB STEP
  print set contains six: base, lid, and four separate top-face-down caps.

## Outputs

- `lrs_350_24_print_set.step`: Mean Well base and lid, laid out for printing.
- `sab_1060_print_set.step`: Dayton base, lid, and four separate retaining caps,
  laid out for printing.
- `enclosure_fit_check.step`: both installed-pose enclosures with simplified
  component reference envelopes.

## Acceptance criteria

- Four printable parts are valid, positive-volume single solids.
- Reference envelopes do not intersect printed base or installed lid geometry.
- Terminal/connector access probes remain unobstructed.
- The reported SAB hole pattern is represented exactly but documented as a
  measurement that must be verified.
- The board reference is 1.7 mm thick; all four posts clear its modeled holes,
  and all four installed caps seat on its top surface without solid overlap.
- The user-measured SAB fan square and X centering are represented exactly;
  its rearward center and provisional height must be physically verified before
  a production print.
- The user-directed USB-C wall, negative-Y center, and plug clearance must be
  physically verified before a production print.
- The LRS mounting pattern is represented at the official 150 x 50 mm spacing.
- Each layout fits within 350 x 320 mm and remains above Z=0; the SAB layout
  exports exactly six positive-volume print objects.

## Out of scope

- Electrical safety certification, flame-rating certification, and wiring.
- Tight connector-shaped SAB cutouts; the wiring exits through a reinforced
  cable bay after all board connectors are populated.
- Thread modeling; the LRS lid hardware is represented by clearance and insert
  bores, while the SAB uses printed friction-fit retainers.
