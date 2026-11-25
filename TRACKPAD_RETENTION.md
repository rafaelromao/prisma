# Trackpad edge retainer (issue #4)

Stacked on the shared drawer interface (#7). No PCB or common tray changes. The existing ledge remains the lower support; two identical keyed hooks retain opposite side sectors from above. The hooks rise 1.0 mm above the nominal lid face (below the keycap envelope). The pad centre and Z datum remain unchanged. The 0.9 mm nominal overlap and 0.2 mm axial play are provisional; confirm the actual overlay has an inactive edge, and that the clips do not touch active area or preload the PCB. The underside boss is blind and the screws seat against the clip flanges.

## Remaining generation and qualification gates

This source change must not be treated as print-ready until the generated artifacts and nominal tests pass. On an environment with the pinned requirements and KiCad, regenerate the trackpad only and render the mechanical scenes using the repository's documented pipeline, without routing or regenerating fabrication files:

```sh
python -m pip install -r requirements.txt
mkdir -p /tmp/opencode
python trackpad/trackpad.py
python -m unittest test_module_assembly test_stl_export test_drawer
python check_fit.py
python verify_artifacts.py
python scene.py
./kicad.sh python3 render_boards.py
./render.sh
python render_manifest.py
python page.py
```

Commit the revised trackpad lid/retainer STL and their public copies, design JSON, updated mechanical renders and manifests; reject any changes to PCB fabrication files. Verify all CI jobs. Test actual 40 mm Cirque edge and thickness, print fit, screw engagement and blind depth, retention under normal use and removal, full key travel, cable routing during closure and sensor operation for both controller options. Do not print the prior published lid with the new clips.
