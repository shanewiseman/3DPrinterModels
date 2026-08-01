# CAD brief

- Model: WPC 25 mm open-end wrench, three labeled color bodies for multi-material printing.
- Task type: parametric CAD modification using the supplied circular Wiseman Precision logo image as visual design intent.
- Units: millimeters.
- Coordinate convention: wrench profile lies in XY; extrusion is +Z; the nominal bolt center is at XY origin; jaw opens toward +X; handle extends toward -X.
- Functional size: nominal 25 mm across-flats hex fastener; jaw opening is 25.4 mm to provide 0.2 mm clearance per flat for a first FDM print.
- Profile depth: 25.0 mm in Z.
- Handle length: 101.6 mm (4.000 in) from the rear head/neck datum at X=-27.0 mm to the physical handle end at X=-128.6 mm.
- Handle intent: smooth convex palm bulge to 36 mm overall width, rounded end, one shallow continuous R210 finger contour along the lower edge, and 3 mm comfort rounds around the palm/back perimeter on both broad faces.
- Head/neck intent: 27 mm head radius, reinforced 28 mm minimum neck width, tangent convex transitions between the head, neck, grip, and palm stations, and a semicircular jaw throat to avoid square stress risers.
- Marking: 31 mm photo-inspired circular logo on the top face, constructed as printable vector geometry with concentric rings, curved `WISEMAN PRECISION` and `CARTRIDGES` text, separator dots, stacked W/PC monogram, `ACTON, MA`, and `EST. 2026` details. The logo is a flush 0.8 mm-deep secondary-color inlay, not an open engraving.
- Color split: the complete wrench volume from Z=0 through Z=5 mm is a labeled secondary-color body; the remaining body from Z=5 through Z=25 mm is primary color except for the top logo pocket/inlay.
- Manufacturing assumption: conceptual/light-duty FDM tool; print strength depends on material, layer orientation, walls/infill, temperature, and fastener torque. No FEA, torque rating, or safety certification is claimed.
- Paths: `wpc_25mm_open_end_wrench.py`, sibling STEP, `validate_wrench.py`, and `snapshots/` review packet.
- Validation targets: valid labeled primary, 5 mm secondary layer, and logo bodies; 25.0 mm Z depth; 25.4 mm unobstructed jaw gap with material on both jaws; 101.6 mm datum-to-handle-end length; minimum neck width at least 28 mm at mid-depth; exactly one R210 finger-contour face; secondary layer exactly Z=0..5 mm; logo exactly Z=24.2..25 mm and flush; zero volumetric overlap; reconstructed volume equals the unsplit wrench; bbox, labels, planes, and color-body positioning inspected from exported STEP.
