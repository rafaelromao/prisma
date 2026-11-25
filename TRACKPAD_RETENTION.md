# Trackpad edge retainer (issue #4)

The common tray and the PCBs are unchanged. The original ledge supports the pad;
a mirrored pair of keyed hooks captures its two side edge sectors. Each hook rises
1.0 mm above the lid, below the keycaps. The pad stays in its original position.
Confirm the actual overlay has an inactive edge for the nominal 0.8 mm overlap
and that the nominal 0.2 mm vertical play does not become preload.

The hooks use the project's M3 family: two **M3 × 4 mm pan-head screws**
(under-head length, head ≤5.5 mm diameter and ≤2.0 mm height) in Ø2.5 mm,
3.4 mm-deep blind pilots, with the screws 4.4 mm tangentially off the insertion channel. The
screw bears on the clip, not the pad. With ±0.1 mm each for screw length and
flange thickness, modeled engagement is 2.6–3.0 mm and tip clearance is at
least 0.4 mm, before print error at the pilot bottom. Verify actual pull-out
strength and at least 0.4 mm tip clearance. Do not substitute the M3 × 8
enclosure screws.

The stations are the two flanks, not the front corners. An M3 head is 5.5 mm
across, and at the corners it would hit the tray's front rim as the lid closes
and the lid's countersink webs; the flanks leave the boss outside the pad and
inside the rim through the whole closing sweep. The earlier smaller-screw
attempt is superseded; the current design and bill of materials use only M3
fasteners.

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
