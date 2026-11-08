# Pre-print acceptance gates

Static geometry is not a guarantee of first-print fit. Use the current tray and lids
together: the front screw pair moved from x = ±19.5 to ±21.0 mm (y = −91.5 mm),
without moving the PCB, pad or keys. Old trays and new lids do not mate.
Half-case pilots also now follow the tilted screw/PCB normal instead of desk Z.

## Verified nominal dimensions

| Interface | Result / disposition |
|---|---|
| Trackpad seat to front M3 head envelope | 2.087 mm web, previously 0.871 mm; checked in the generated lid |
| 40 mm pad to compact 17.5 × 16.5 mm cap | 0.585 mm centred gap with the footprint's 17.5 mm front-to-back orientation; 18 mm square envelope gives only 0.335 mm. Seat play can consume another 0.3 mm before wobble/print error |
| Steel stand contact | Existing magnets only; owner confirmed actual supports attract magnets |
| Feet to centred Ø54 mm platform circle | All ten possible foot edges at least 11.55 mm outside; no foot-induced air gap |
| Stand magnet edge margin | 1 mm at Ø54; about Ø60 preferred if the actual platform clears feet and obstructions |
| Main battery plated holes | Ø0.6 mm drill, Ø0.96 mm pad: 0.18 mm annular ring, absolute-minimum rule rather than recommended margin |

`stand_mount.py` assumes flush case magnets and a flat centred circular patch. Platform
shape, coatings, recessed magnets and adhesive can change the contact. Attraction does not
prove resistance to slip/peel under typing or qualify the stand's hinge/base stability.

## Dimensional process gate — before the complete print

Use the intended printer, nozzle, dry filament, orientation, cooling and support profile.
Measure XY shrinkage independently in both axes, repeatability, Z error, flatness/warping
and elephant foot after the parts have cooled/conditioned. A small coupon alone does not
establish flatness over the full dock; include a representative long-span test or prior
measurements from the same process. Record the process and measurements with the release.

The following are **local, per-side nominal gaps**, not allowable global shrink percentages:

| Mating interface | Gap | Conservative acceptance budget |
|---|---:|---|
| Dock ↔ half | 0.30 mm | Combined inward/outward edge error + lateral warp + placement error < 0.30 mm |
| Drawer ↔ module/placeholder | 0.35 mm | Same combined errors < 0.35 mm, along the entire removal path |
| Tray ↔ lid locating lip | 0.25 mm | Same combined errors < 0.25 mm |
| Ø8 magnet ↔ pocket | 0.15 mm radial | Actual magnet oversize + pocket undersize + cleanup residual < 0.15 mm |

For example, opposite 0.10 mm edge errors consume 0.20 mm before warp or positioning:
only 0.10 mm remains at the dock/half interface. A hypothetical 0.5% error across the
199 mm dock is approximately 1 mm, not covered by ±0.2 mm rigid-translation regressions.
Those tests do **not** test scale, anisotropy, bow or twist. Inspect magnet alignment and
both fits over their full lengths. Do not simply enlarge the drawer allowance or scale
one STL: that also alters wall skins, magnetic gaps, facets and alignment. If the measured
process cannot satisfy the budgets, revise the parametric model and rerun all checks.
There is currently no measured printer profile or shrinkage/warp qualification in this repo.

## Slicer and assembly gates — still physical/unverified

- **Dock pocket:** about 5,900 mm² of downward-facing roof at Z = 4.3 mm. Generate supports,
  inspect their interface and removal route, and verify the cleaned pocket fits the real base.
  Do not accept an unsupported full-width bridge or inaccessible/trapped supports.
- **USB bridges:** inspect the half's approximately 14.6 mm span, module's 12.8 mm span and
  8.6 mm pad-slot roofs. Qualify Nylon sag with the real plug and board clearances.
- **Thin skins:** inspect every layer/toolpath through 0.6–0.9 mm magnetic backings and
  retaining skins; verify continuity with the actual extrusion width. Do not force magnets.
- **Trackpad:** check actual cap dimensions, stem wobble, switch travel, pad size and adhesive;
  ensure the countersinks remain intact. Tighten only to flush, not to flatten a warped lid.
- **Stands:** test at the intended tilt with the battery/electronics fitted, then apply typing,
  lateral and peel loads while supporting the half. Confirm no slipping, rocking or stand collapse.
- **PCB order:** ask the fabricator to accept the 0.18 mm battery-hole annular rings explicitly.
  Their constrained underside-pad/routing region requires redesign and rerouting to increase
  the minimum ring; a clean DRC against 0.18 mm rules is not a yield guarantee. The module
  panel also retains silkscreen warnings: identify connections by pad/net, not text alone.
- **Electronics:** clean firmware builds are not physical RF, charging, battery-polarity,
  sensor-bus, optical-gap or sleep/wake validation. Follow the powered/unpowered tests in BUILD.md.
- **Sensor screws:** finish the two tips to ≤7.6 mm overall, outside the assembly, then deburr.
  The model includes 0.22 mm head seating into the straight PCB hole. With the nominal 0.4 mm
  shim, a finished 7.6 mm screw has 0.58 mm pilot-bottom clearance, or 0.38 mm with a further
  0.2 mm axial uncertainty. Measure actual head seating, optical shims, engagement and tip
  clearance (≥0.3 mm); do not substitute extra optical shims for correct screw length.
- **Controller header:** the reference's Ø0.75 mm holes do not clear a 0.64 mm square pin
  (0.905 mm diagonal). Measure the actual controller and candidate pins; do not force them
  or drill plated holes. Round Ø0.6 mm pins are a candidate, not confirmed for every revision.
  Confirm the Sense-sourced reference against the selected plain XIAO/clone and the full stack.

## Reproducible software checks

Install `requirements.txt`, then run:

```sh
python3 -m unittest test_stl_export test_half_battery test_drawer test_module_assembly test_xiao_option trackball.test_layout
python3 check_fit.py
python3 stand_mount.py
python3 verify_artifacts.py
./kicad.sh kicad-cli pcb drc --exit-code-violations --severity-error --format json -o .render/prisma-drc.json pcb/prisma.kicad_pcb
./kicad.sh kicad-cli pcb drc --exit-code-violations --severity-error --format json -o .render/module-drc.json trackball/pcb/trackball.kicad_pcb
./kicad.sh python3 check_pcb.py
./kicad.sh python3 trackball/check_controller_pcb.py
```

Regenerate changed CAD exports with the README commands, including their `stls/` copies.
The automated mechanical workflow checks regenerated geometry and binary export integrity;
the electrical job checks routed boards and net intent. Neither performs material-specific slicing.
Before printing, freeze sources, firmware revisions, STLs, fabrication archives and checksums
together at a single commit, with the physical gates above marked passed or explicitly deferred.
