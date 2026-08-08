# Centered AMS pair and shelf connection concept

## Selected constraints

- All structural members are printed in ASA; no aluminum, tube, rod, or other
  metal structural member is used.
- M4 screws and standard hex nuts remain purchased assembly hardware.
- The two AMS 2 Pro units face the same direction as the X2D.
- The AMS pair is centered on the X2D top centerline with a 25.4 mm gap.
- The shelf connection must not raise any modeled AMS foot above Z=0 or
  obstruct the front door.

## Centered AMS placement

Each AMS is 372 mm wide. A 25.4 mm center gap gives a combined 769.4 mm
footprint and places the AMS centers at X=±198.7 mm. The outer envelope is
X=±384.7 mm, so each AMS extends 188.7 mm beyond the corresponding 196 mm X2D
side instead of being placed completely outboard. The shelf roots remain at
X=±199.0 mm and their outer edges are X=±410.1 mm, leaving an exact 25.4 mm
printed margin beyond each AMS outer face.

The assumed AMS feet are spaced 320 × 220 mm. With the centered placement:

- the left AMS outer foot row is at X=-358.7 mm and lands on the left shelf;
- the left AMS inner foot row is at X=-38.7 mm and lands on the X2D top;
- the right AMS inner foot row is at X=+38.7 mm and lands on the X2D top;
- the right AMS outer foot row is at X=+358.7 mm and lands on the right shelf.

All four foot rows retain Z=0. No foot rail or riser is needed in this revision.
The exact X2D top bearing surface and AMS foot pattern remain provisional and
must be measured before production use.

## Twin low-profile printed tie trusses

The earlier tall torsion-box beams would intersect the newly centered AMS
envelopes. They are replaced by two removable planar ASA truss ties, one at
Y=-70 mm and one at Y=+70 mm. These positions sit between the provisional AMS
foot rows at Y=±110 mm.

Each tie has:

- a 50 mm front-to-back truss envelope;
- a 3 mm planar frame and alternating 8 mm diagonal webs;
- left and right printable halves, each 249 mm long;
- a 50 mm solid overlap onto its shelf;
- three vertical M4 button-head bolts per shelf overlap;
- a 9 mm-wide center boss on each half, rising to 25.4 mm;
- three transverse M4 bolts through the paired center bosses.

The flat tie spans occupy Z=0–3 mm. The provisional AMS body begins at Z=4 mm,
leaving 1 mm modeled clearance. The center bosses occupy X=-9 to +9 mm, leaving
3.7 mm clearance to each AMS body inside the 25.4 mm center gap. Button heads
are recessed flush with the 3 mm tie lands and standard M4 nuts are captive.

The ties lie on the modeled X2D top and therefore do not create an AMS riser.
They must be removable for top-glass service. Whether direct tie/glass contact
is acceptable, or whether a measured structural rim/contact insert is needed,
is a required physical verification item.

## Shelf-end connection

Each tie half overlaps the corresponding 211.1 × 252 mm shelf by 50 mm. Three
vertical M4 bolts use a staggered pattern through the solid tie land and shelf.
The button heads are recessed into the tie; standard hex nuts load from captive
underside pockets in the 6 mm shelf skin.

This removes the previous tall vertical receiver and keeps every tie-end feature
below the provisional AMS body without placing hardware beneath an AMS foot.
The tie lands are integrated into the same load plane as the shelf top and
connect into the shelf rib grid.

## Load path

Each centered AMS divides vertical load between the X2D top at its inner foot
row and one printed shelf at its outer foot row. The shelf load flows through
its front/rear 25.4 mm-chord triangular brackets and printed side contact pads.
The two planar truss ties resist left/right shelf separation and fore/aft
racking; they are stabilizing ties rather than primary vertical shelf beams.

This is geometric design intent, not a structural certification. The physical
X2D top, glass, side frame, AMS feet, ASA creep behavior, and loaded-spool mass
must be verified and proof-tested away from the printer.

## Door and service clearance

Both low ties are at or above Z=0, while the provisional door top is Z=-25 mm.
The generated assembly validates zero intersection with both the closed door
and the modeled -105° open-door keep-out. No tie, bracket, or shelf crosses the
closed front-door plane.

Routine top-glass removal requires loosening/removing the low-profile ties. The
center bosses and M4 hardware are accessible through the 25.4 mm AMS gap after
the AMS units are removed.

## Modeled M4 hardware count

- 6 M4 screws and 6 nuts for the two three-bolt center-boss joints.
- 12 M4 screws and 12 nuts for the four three-bolt tie-to-shelf overlaps.
- 16 M4 screws and 16 nuts for the four four-bolt bracket-to-shelf joints.

Final screw lengths follow physical nut/head measurements and printed coupons.

## Printing and validation strategy

- Print one low-tie center-boss coupon with the transverse screw and captive-nut
  pockets before printing full 249 mm halves.
- Print one tie/shelf overlap coupon with the 3 mm flush head recess and 6 mm
  shelf nut pocket.
- Print one bracket/shelf nut-trap coupon.
- Print planar tie halves flat so all frame and diagonal members remain in the
  layer plane.
- Use ASA wall counts and local solid regions sufficient to make the 8 mm webs
  and fastener lands resolve primarily as walls, not sparse infill.
- Proof-test the connected assembly away from the X2D with distributed dead
  weight and a sustained warm-load period.
- Inspect the center bosses, shelf overlaps, bracket roots, and side pads for
  whitening, permanent set, loose hardware, or layer separation.

## Measurements needed before the production revision

- Exact AMS foot spacing, foot dimensions, foot height, and body-underfloor
  clearance between the two Y foot rows.
- AMS underside vents and any features crossing the proposed Y=±70 mm ties.
- X2D top/glass size, thickness, corner radii, load rating, gaps, and removal
  direction.
- Structural top-rim or insert locations if the printed ties must not bear on
  the glass.
- X2D side-frame bearing zones and all removable-panel, vent, and fastener
  locations near the four bracket pads.
- Closed door plane, door-top height, hinge geometry, and full physical opening
  sweep.
- PTFE/cable exits and full AMS lid-opening clearance with the 25.4 mm center
  gap.
