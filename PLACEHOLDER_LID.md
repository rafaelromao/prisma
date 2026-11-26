# Passive drawer lid (#5)

The old solid insert has been retired. The shared-tray lid's STL and dock
views are CAD-verified; the physical assembly is not yet qualified.

The passive module is the canonical `case/module_tray.stl` plus a
removable, diamond-marked top-down `case/placeholder_lid.stl` (public copy
`stls/placeholder_lid.stl`), four M3 × 8 countersunk screws, seven
8 × 1.5 mm magnets and three 8 × 2 mm bump-ons. No boards, battery,
sensor screws or keys. The existing control passages remain
empty and unsealed for tray reuse; it is not dust- or water-tight.
The lid has no control openings. Do not print or modify the tray per variant.
The restored diamond is cut 0.6 mm deep into the lid's top; the shared tray
carries the recessed PRISMA wordmark on its front facet, so every module
variant shows it.

The nominal lid top is FLUSH + 1.0 mm. At FLUSH the standard screws
would bottom out (13.477 mm tip vs 13.9 mm pilot bottom). A 0.923 mm rise is
the theoretical minimum for 0.3 mm tip clearance plus 0.2 mm screw allowance.
The 1.0 mm upper roof gives 0.577 mm nominal tip clearance (0.377 mm with
the allowance), and 6.0 mm nominal engagement. The broad roof is 2.0 mm nominal
(1.0 mm upper roof plus 1.0 mm inset thickening); the thinner rear hook
and perimeter region follows the shared interface. These are CAD
dimensions, not validated measurements. The diamond stays over the 2.0 mm
forward roof, 2.5 mm inside the top rim and clear of the screw heads; its
0.6 mm relief leaves 1.4 mm of backing there, so it does not weaken the
screw-bearing roof. No claim of solid-block strength or dock reinforcement.

## Regeneration and acceptance gates

Run from the repository root with the pinned requirements and KiCad/render
toolchain. These checks are not a substitute for physical tests.

```sh
python insert.py
mkdir -p /tmp/opencode
python -m unittest test_stl_export test_half_battery test_drawer test_module_assembly test_xiao_option test_switch_mount trackball.test_layout
python check_fit.py
python stand_mount.py
python verify_artifacts.py
python vrml.py
python scene.py
./kicad.sh python3 render_boards.py
./render.sh dock_insert.png placeholder_structure.png
python render_manifest.py --update dock_insert.png placeholder_structure.png
python page.py
```

Check actual binary STL topology, orientation, connected material, source/public
parity, vertices, and updated manifests; inspect the dock and exploded
`placeholder_structure` imagery.
Run the electrical CI checks and compare regenerated PCB geometry, netlists,
Gerber and drill data to the pinned baseline; never commit changed fabrication
outputs. Stored PCB blob equality is distinct from regenerated equivalence.

## Physical qualification (not yet performed)

- Print and dry-fit the common tray and lid; inspect roof and hook continuity,
  bevel, seam, screw bearing land, actual pilot engagement and tip clearance.
  Verify screws seat flush without bottoming, splitting posts or pulling through.
- Fit magnets and feet; confirm correct polarity, even standing plane,
  full dock seating, horizontal removal and standalone attachment to either
  half. Check retention in normal use and at the intended angles, including
  repeated assembly and removal, without lifting the unsupported keyboard.
- On a supported bench, apply gradually increasing representative handling
  and typing loads to the roof centre, front edge and dock assembly. Observe
  deflection, permanent set, cracks, screw pull-out, hook damage or unexpected
  release. Record material, print settings, force, measured deflection and
  acceptance criteria before testing. Do not use as a load-bearing lap support
  until validated; revise the removable lid if insufficient, not the tray/PCBs.
- Check the unused openings remain harmless and nothing loose can enter the
  assembly during intended handling. No electronics are installed.

Physical tests and electrical regeneration were not performed.
