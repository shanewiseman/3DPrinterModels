# CAD brief: FIDE-guideline modular chessboard for Bambu Lab X2D

- Model: full-size modular chessboard assembly, printable as four playing
  quarters plus removable perimeter, seam bridges, and color inlays.
- Task type: new parametric assembly with STEP-first geometry and STL
  sidecars.
- Units: millimeters.
- Coordinate convention: assembled board centered at the origin; XY is the
  playing plane; White sits at negative Y; +Z is upward. File `a` is at
  negative X and rank `1` is at negative Y.
- Square size: 60.0 mm, the largest square allowed by the current FIDE
  equipment guideline. The user's 33 mm pawn bases cannot satisfy the
  separate four-pawns-on-one-square suitability test within the permitted
  50-60 mm square range; the design prioritizes the permitted square size.
- Playing area: 480 x 480 mm (8 x 8 squares).
- Perimeter: 20 mm wide outside the playing area, giving a 520 x 520 mm
  overall footprint. Its top is 10 mm above the playing surface.
- Playing quarters: four 240 x 240 mm nominal panels. Male alignment tongues
  add at most 4 mm to selected inner edges, keeping every printable quarter
  within a 244 x 244 mm XY envelope for the X2D's 256 x 256 mm main-nozzle
  area.
- Playing panel construction: 8.0 mm structural body plus a 1.6 mm color face.
  Light squares are integral with the body. Exact 60 mm dark-square bodies are
  supplied in the multi-body STEP files; a 59.6 mm loose inlay STL is also
  supplied for separately printed/glued assembly.
- Quarter joinery: horizontal assembly sequence with 4.0 mm tongues and
  0.25 mm nominal groove clearance, then eight underside bridge plates. Each
  bridge uses two M3 x 12 screws and two captured standard M3 hex nuts.
- Seam registration: each internal 240 mm interface also has two concealed
  20 mm upper keys at +/-90 mm. The 3.0 mm keys sit at Z = 5-7 mm and use
  0.25 mm depth, 0.20 mm per-end, and 0.20 mm per-side vertical clearances.
- Print-fit treatment: 0.5 mm lead-in chamfers on projecting tongues, upper
  keys, rail tongues, fit openings, and corner ribs; 0.4 mm build-plane relief
  on quarter, rail, and corner-cap footprints; enlarged 0.8 mm-deep cap-slot
  entrances.
- Nut retention: side-loaded, blind hexagonal nut traps; no heat-set inserts.
  Nominal M3 nut envelope is 5.5 mm across flats x 2.4 mm thick. Pockets allow
  approximately 0.2-0.4 mm FDM clearance.
- Perimeter construction: eight straight 240 mm rail sections, one per
  quarter outer edge, plus four vertically keyed corner caps. Each rail has an
  under-panel flange and is fixed by two M3 x 12 screws into captured nuts in
  the quarter. The two 15 mm under-panel flanges at each corner terminate on
  complementary 45-degree faces with 0.30 mm normal clearance, eliminating
  the former coplanar 15 x 15 x 8 mm overlap.
- Corner joinery: hidden 7.0 x 14.0 mm rail cores extend into each cap and
  terminate on complementary 45-degree faces. The selected locking core has
  an integral, build-plane-supported 2.5 mm mortise-and-tenon projection that
  enters the neighbor's open mortise during the same inward motion that seats
  the rail tongue in the playing-panel groove, using 0.25 mm nominal
  clearance. This repeats the lower tongue/groove design language used by the
  playing panels without adding another printed part or a cyclic assembly
  constraint.
- Corner retention: each hollowed cap captures both mitered rail cores and is
  positively retained by one hidden M2 x 12 cross-screw and a top-loaded
  standard M2 nut in the selected locking core. The nut pockets retain 0.25 mm
  across-flats and 0.30 mm thickness clearance.
- Cosmetic edge treatment: 2 mm fillets on every exposed perimeter top edge.
  Rail-to-rail and rail-to-corner mating seams remain square so the assembled
  border does not develop rounded valleys at its joints.
- Notation: lowercase `a-h` on both horizontal sides and `1-8` on both
  vertical sides. Glyphs are flush 1.2 mm inlays with enlarged pockets for
  separately printed PLA Matte inserts. Pocket clearance is formed from four
  diagonally shifted glyph cutters so exported rail bodies round-trip as
  closed STEP solids. File letters face their adjacent player. Rank numerals
  are rotated across the rail rather than along it: the east/right-side set is
  upright from White at negative Y, the west/left-side set is upright from
  Black at positive Y, and the two rank sets differ by 180 degrees.
- Underside stability: recessed locations for adhesive felt or rubber pads in
  the perimeter rails and corner caps.
- Material: PLA Matte. Color intent is ivory/light squares, dark brown dark
  squares, black perimeter, and ivory notation.
- Printing assumptions: 0.4 mm nozzle, 0.20 mm layers, 4-5 walls, 15-20%
  cubic/gyroid infill, and dimensional compensation calibrated for the user's
  printer. Exact slicer settings remain user-controlled.
- Source paths: `chessboard_geometry.py`, `chessboard_assembly.py`, printable
  wrapper generators, and `validate_chessboard.py` in this project directory.
- Primary output: `chessboard_assembly.step`.
- Secondary outputs: per-quarter STEP files; per-rail STEP files; printable
  STL files for structural/color bodies, one repeated bridge, one repeated
  corner cap, a repeated dark-square inlay, and the notation inlay set.
- Separated print kit: `separated_print_kit.step` contains 56 printable
  objects and 88 colored leaf solids, bedded at Z = 0 and grouped into nine
  non-overlapping 256 x 256 mm virtual-plate modules. Each playing quarter is
  one single-color structural body with integral light squares. The 32 dark
  squares are separate 59.6 x 59.6 x 1.6 mm glue-in bodies arranged sixteen
  per plate on two plates. Each perimeter rail contains its black rail body
  and four ivory notation bodies. The virtual plates are positioning datums
  only and are not exported as geometry.
- Validation targets: 60 mm square pitch; 480 mm playing area; 520 mm outer
  footprint; 240/244 mm quarter and 247.1 mm rail print envelopes; 20 mm border
  width; 10 mm raised perimeter; 9.6 mm playing height; captured-nut and M3 x
  12 stack; zero positive-volume intersection between every adjacent corner
  rail pair; 45-degree flange/core faces with the specified clearance; seated
  mortise-and-tenon joints without interference; clear M2 cross-screw path;
  labeled STEP children; mandatory assembly snapshot packet.

## Eight-panel X2D variant

- Task type: source-level assembly modification that preserves the original
  four-quarter files as a legacy option.
- Playing panels: eight named 120 x 240 mm panels arranged as four file pairs
  (`ab`, `cd`, `ef`, `gh`) by two rank halves (`south`, `north`). Every new
  seam follows a 60 mm square boundary.
- Printable envelope: at most 124 x 244 mm including male keys. Each panel is
  offset toward the left side of its own 256 x 256 mm virtual plate, leaving
  at least 120 mm of clear width on the right for slicer-generated supports
  and a prime tower.
- Joinery: the established 4 mm tongue/groove and concealed anti-lip key
  system is repeated on the new seams. Two M3 nut locations are retained on
  240 mm edges; 120 mm edges use one centered M3 location.
- Eight-panel M3 fit adjustment after a PLA Matte print test: retain the
  0.5 mm opening lead-in and 2.8 mm pocket/channel height, increase the nut
  entry channel from 5.9 to 6.1 mm, increase the panel-only vertical screw
  passage from 3.4 to 3.6 mm, and increase the captured hex pocket from 5.72
  to 5.8 mm across flats. Seam bridges, rails, corner caps, and the legacy
  four-quarter model retain their existing geometry.
- Mesh topology: each 2 x 4 playing body has a 0.2 x 0.2 mm relief at its
  three internal checker vertices. This prevents diagonally opposite raised
  light regions from meeting along a zero-width vertical edge that slicers can
  triangulate as non-manifold. The relief is below nozzle width and does not
  change the 60 mm grid pitch, dark-square seat, joinery, or hardware.
- Reinforcement: twelve underside bridges cross the three vertical board
  seams and four cross the horizontal center seam, for sixteen bridges total.
  Each bridge uses two M3 x 12 screws and two standard captured M3 nuts.
- Perimeter compatibility: the same eight named rail locations and four cap
  locations are retained, but future-print rail/cap files use the corrected
  45-degree keyed corner revision. Horizontal rails span two 120 mm panels and
  add stiffness across the added vertical seams; their screw positions remain
  aligned with the centered panel nut traps.
- Color workflow: each panel remains one light structural body with integral
  light squares. The existing 32 loose 59.6 x 59.6 x 1.6 mm dark inlays are
  printed separately and glued into the face recesses.
- Coordinate convention: assembled board remains centered at the origin with
  file `a` at negative X, rank `1` at negative Y, and +Z upward. Printable
  panel bodies are centered locally and bedded at Z = 0. Their centering
  transforms are baked into the standalone geometry so each STEP has one
  top-level product label matching its filename stem; this prevents Bambu
  Studio from displaying an OpenCascade occurrence ID as the object name.
- Source paths: `eight_panel_geometry.py`,
  `eight_panel_chessboard_assembly.py`, `eight_panel_print_kit.py`, and eight
  `panel_*_light_body.py` wrappers.
- Primary review output: `eight_panel_chessboard_assembly.step`.
- Primary slicer output: `eight_panel_print_kit.step`, with thirteen labeled
  256 x 256 mm virtual-plate modules and no physical plate solids.
- Validation targets: eight closed monolithic playing bodies; four exact dark
  squares per panel in the review assembly; 120 x 240 mm nominal panel size;
  no panel exceeding 124 x 244 mm; 480 x 480 mm playing area; unchanged
  520 x 520 mm outer footprint; sixteen correctly located seam bridges;
  unchanged rail/corner interfaces; filename-matched standalone STEP product
  labels; and closed-shell STEP round-trip.
