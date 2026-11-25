# Trackpad edge retainer (issue #4)

The common tray and the PCBs are unchanged. The original ledge supports the pad;
two identical keyed hooks capture its front-side edge sectors. Each hook rises
1.0 mm above the lid, below the keycaps. The pad stays in its original position.
Confirm the actual overlay has an inactive edge for the nominal 0.9 mm overlap
and that the nominal 0.2 mm vertical play does not become preload.

The M3 retainer design interfered with the tray and main PCB. Use two **M2 × 3 mm
pan-head screws** (under-head length, head ≤3.8 mm diameter and ≤1.6 mm height)
in the new 1.65 mm blind pilots. The screw bears on the clip, not the pad.
With ±0.1 mm each for screw length and flange thickness, modeled engagement is
1.6–2.0 mm and tip clearance is at least 0.4 mm, before print error at the
pilot bottom. Verify actual pull-out strength and at least 0.3 mm tip clearance.
Do not substitute the M3 × 8 enclosure screws.

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
views=$(git ls-files 'renders/trackpad*.png' | xargs -n1 basename)
./render.sh $views
python render_manifest.py --update $views
python page.py
```

Physical qualification remains open. Test the actual 40 mm Cirque edge and
thickness, print fit, screw engagement and blind depth, retention in normal
use and removal, key travel, wired closure and sensor operation for both
controller options. Do not pair a prior lid with these clips.
