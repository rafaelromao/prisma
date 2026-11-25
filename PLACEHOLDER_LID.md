# Passive drawer lid (#5)

**Draft: source only, not qualified or print-ready.** The old solid insert
has been retired (its two STL copies are removed; the existing
`renders/dock_insert.png` is a legacy view until regenerated).

The passive module is the canonical `case/module_tray.stl` plus a
plain, removable top-down `case/placeholder_lid.stl` (public copy
`stls/placeholder_lid.stl`), four M3 × 8 countersunk screws, seven
8 × 1.5 mm magnets and three 8 × 2 mm bump-ons. No boards, battery,
sensor screws, keys or decorations. The existing control passages remain
empty and unsealed for tray reuse; it is not dust- or water-tight.
The lid has no control openings. Do not print or modify the tray per variant.

The nominal lid top is FLUSH + 1.2 mm. At FLUSH the standard screws
would bottom out (13.477 mm tip vs 13.9 mm pilot bottom); the standard low
lid gives 0.777 mm nominal tip clearance (0.577 mm with 0.2 mm extra screw
length), and 5.8 mm nominal engagement. The broad roof is 2.0 mm nominal
(1.2 mm upper roof plus 0.8 mm inset thickening); the thinner rear hook
and perimeter region follows the shared interface. These are CAD
dimensions, not validated measurements. The plain top avoids relief
weakening the roof. No claim of solid-block strength or dock reinforcement.

## Regeneration and acceptance gates

Run from the repository root with the pinned requirements and KiCad/render
toolchain. The source and tests are intentionally not a substitute for
the generated binaries; do not publish the new lid until these pass.

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
./render.sh
python render_manifest.py
python page.py
```

First complete PR #8's retainer export and any inherited regeneration gates.
Check actual binary STL topology, orientation, connected material, source/public
parity, vertices, and updated manifests; inspect the dock and exploded
`placeholder_structure` imagery, then update legacy/pending notices.
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

No CAD execution, STL generation, rendering, physical tests or electrical
regeneration were performed in the editing environment.
