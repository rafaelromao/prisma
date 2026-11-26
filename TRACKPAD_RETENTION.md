# Hidden trackpad retainer

The pad loads from underneath and sits 0.8 mm below the lid surface at rest.
The 0.7 mm-thick lid rim covers 0.8 mm of the pad edge nominally (0.5 mm at
maximum radial shift). The mirrored tabs support the component-free underside
and are hidden with the lid installed. They hold the pad independently of the
tray, with 0.1 mm nominal axial play rather than pressure on the sensor.
The common tray, PCBs, lid height and key positions are unchanged.

![Exploded view of the Cirque pad, the two green support tabs and their screws beneath the lid](renders/trackpad_holder.png)

The tabs use two **M3 × 4 mm pan-head screws**
(under-head length, head ≤5.5 mm diameter and ≤2.0 mm height) in Ø2.5 mm,
3.4 mm-deep blind pilots. Each tab seats against the lid boss, not against
the pad. With ±0.1 mm each for screw length and
flange thickness, modeled engagement is 2.6–3.0 mm and tip clearance is at
least 0.4 mm, before print error at the pilot bottom. Verify actual pull-out
strength and at least 0.4 mm tip clearance. Do not substitute the M3 × 8
enclosure screws.

Use the 1.8 mm breakout spacer to recover cable room under the recessed pad.
Check the actual spacer and components against the screw heads, and verify
the FFC bend and slack during closure.

## Regeneration and qualification

The revised lid and clips are exported as source/public STL pairs. To reproduce
them and the trackpad views without changing PCB fabrication files, run:

```sh
python -m pip install -r requirements.txt
mkdir -p /tmp/opencode
python trackpad/trackpad.py
python -m unittest test_module_assembly test_stl_export test_drawer
python check_fit.py
python verify_artifacts.py
python vrml.py
python scene.py
./kicad.sh python3 render_boards.py
views="$(git ls-files 'renders/trackpad*.png' | xargs -n1 basename) dock_unibody.png dock_unibody_side.png"
./render.sh $views
python render_manifest.py --update $views
python page.py
```

Physical qualification remains open. Check that the slicer produces a
continuous rim and that the actual overlay has an inactive edge wide enough
for the overlap and any shift. Verify free play without preload, screw seating
and pull-out strength, retention and service, key travel, wired closure, and
touch response near the rim with both controller options. Replace the old lid
and clips together.
