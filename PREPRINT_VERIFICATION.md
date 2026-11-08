# Linked pre-print review: verification and disposition

Source: https://chatgpt.com/s/t_6af0e3a4460c8191bbbedb8f92f7bcad
Baseline: Prisma `040bb00f22f1aaf9aeabb58ca209f218df590747`.
Verification date: 2026-11-08. See PRINT_READINESS.md for the remaining physical gates.

| Concern | Verification | Disposition |
|---|---|---|
| Independent stands described inconsistently | Website assumed steel; README/BUILD/BOM and scene still added six discs | Corrected to owner's tested steel platforms, direct case-magnet contact, no six additional discs; total 77 |
| Feet create a steel-platform air gap | All ten possible foot positions measured in the desk plane; minimum foot-edge to centred Ø54 circle clearance 11.5454 mm (about 11.55 mm) | Incorrect for that centred patch; documentation and stand checker corrected. Actual noncircular/larger surfaces still need checking |
| Only 1 mm radial stand edge margin | 22 mm magnet-centre radius + 4 mm disc radius in a 27 mm platform radius | Confirmed; recommend about Ø60 where it still clears feet/obstructions, retain Ø54 as the minimum |
| Trackpad front screw web 0.871 mm | Original centre distance minus 20.3 mm seat radius and 3.2 mm head radius = 0.870878 mm | Moved front screw centres outwards by 1.5 mm to x = ±21; new web 2.087 mm. No PCB/key/pad movement. Regenerated shared tray and all lids; use matched revisions |
| Trackpad gap 0.335 mm to 18 mm cap envelope | Independently reproduced 0.335471 mm from nominal source coordinates | Confirmed conservative-envelope margin; compact Choc caps required, actual travel/wobble remains a physical gate |
| Dock support dependency | Binary STL downward-facing horizontal area at Z = 4.3 mm: 5,900.424 mm² | Confirmed; explicit support/interface/removal and cleaned-pocket dimensional gates added |
| Dock and drawer tolerance | Existing rigid translation tests do not model scale/warp | Retained nominal clearances; removed the source comment promising no sanding. Added combined-edge-error budgets and material-specific long-span/warping qualification; no unsupported one-shot promise |
| Main/module USB bridges | Nominal 14.6/12.8 mm spans remain | Explicit intended-profile bridge/sag/real-plug checks, not a claim of validated Nylon bridging |
| Thin magnetic skins | Nominal 0.6–0.9 mm retaining/backing sections remain | Actual per-layer extrusion continuity and cleanup are mandatory slicer gates |
| Battery-hole annular ring | Ø0.6 drill / Ø0.96 pad gives 0.18 mm radial copper | Confirmed absolute-minimum design; retained due underside-pad/routing constraints. Fabricator acceptance required; no false claim of recommended margin |
| Controller stacking alignment | KiCad checker measured all eight corresponding pairs; worst offset 0.0000 mm | Passed nominal alignment and every controller/header/stacking/jumper net check |
| Main PCB connectivity | KiCad 9.0.9 DRC: zero violations and zero unconnected; net audit including both actual firmware pin lists: ALL CLEAR | Passed software checks, not assembly/charging qualification |
| Module panel connectivity | KiCad 9.0.9 DRC: zero errors, zero unconnected, 23 silkscreen warnings (13 text height, 5 silk/copper, 5 silk overlap) | Electrical checks pass; warnings remain disclosed. Identify wiring by pads/nets rather than silkscreen alone |
| Fabrication exports may be stale | Fresh Gerber/Excellon/job exports compared to both orderable ZIPs, 10 files each | All data match after excluding generation timestamp headers; existing archives retained |
| Half firmware rename | `keyboards` remote `prisma` at `dfbfbd146dcb1ffae9a558a212821df584fa6a10` used old includes, Kconfig symbols and selector strings | Fixed in isolated `/tmp/opencode/keyboards-prisma-review`, branch `fix/prisma-shield-references`, with regression tests. Original dirty keyboards working tree left untouched; changes are not published |
| Half/dongle firmware compilation | Pristine builds of `prisma_central_left`, `prisma_peripheral_left`, `prisma_peripheral_right` on XIAO and `prisma_central_dongle` with `dongle_display` on nice!nano, using the actual shared keymap and default modules | All four PASS after the rename fix. Pinned ZMK `9ebbeff0a8b69a42f14aec022cdf16c7a107b9e0`, Zephyr SDK 0.17.0; logs/UF2s and resolved additional-module revisions in `/tmp/opencode/prisma-firmware-review` |
| Pointing firmware compilation | Pristine builds of `prisma_trackball`, `prisma_trackball_xiao`, `prisma_trackpad`, `prisma_trackpad_xiao`, using pinned ZMK `9ebbeff0a8b69a42f14aec022cdf16c7a107b9e0` and Zephyr SDK 0.17.0 | All four PASS, with the appropriate shield and sensor/bus enabled in merged Kconfig. Build logs and UF2s in `/tmp/opencode/prisma-pointing-firmware-review`; physical sensor/charging tests remain open |
| Missing continuous mechanical/electrical checks | No verification workflow at baseline | Added `.github/workflows/verify.yml` for mechanical/export regressions, fit and stand checks, routed-board DRC and net intent. Firmware builds and slicing are not covered by that workflow |

## Scope limits

The supplied supports' magnetic attraction is user-tested evidence, not a load/tilt qualification.
Slicer toolpaths, actual shrinkage/warping, supported-surface finish, magnet retention, cap wobble,
electronics assembly, charging, RF and sensor behavior still need the checks in PRINT_READINESS.md.
No guaranteed one-shot-print or fully release-qualified claim is made.

## Independent blind review follow-up

A fresh reviewer inspected the hardware without the linked review, intended fixes or prior
findings, then reported three additional P2 issues:

1. **Half pilot axes:** the original desk-vertical pilots deviated from the tilted screw
   axis by about 0.480 mm at the tip. Pilots now follow the PCB normal, with their lower
   ends clipped at the existing 0.6 mm floor skin. A regression probes each tilted pilot core.
2. **Sensor head seating:** the original depth check omitted 0.220 mm of cone entry into
   a straight Ø3.4 mm PCB hole. At 8 mm screw length, no shim bottoms 0.22 mm past the
   pilot end; the nominal 0.4 mm shim leaves only 0.18 mm clearance. The stack helper,
   regression and renders now include seating. Assembly specifies finishing just those
   two screws to ≤7.6 mm, deburring outside the assembly, and measuring ≥0.3 mm clearance
   at the actual optical shim. Nominal clearance is 0.58 mm, or 0.38 mm with another
   0.2 mm of axial uncertainty. The four lid screws stay unmodified.
3. **Header interference:** standard 0.64 mm square pins have a 0.905 mm diagonal against
   Ø0.75 mm holes in the Seeed reference. Removed the firm-press instruction; require
   measured compatible pins (round Ø0.6 mm as a candidate), correct plastic height and
   actual revision qualification. Reference provenance from Sense resources is explicit.

The reviewer also retained the physical gates for supports/warping, stand retention,
real USB/wiring/FFC envelopes, charging/RF/sensor behavior and optical height.

Follow-up verification confirmed those three corrections, including 1.798 mm minimum
clearance to a neighbouring pocket beside the corrected half pilots. It also caught an
incorrect cap-orientation assumption introduced during the first correction pass: conventional
Choc caps follow the quarter-turned switch, so the compact cap's centred gap is **0.585 mm**,
not 1.085 mm. Tests now rotate the cap envelope from the footprint orientation; docs disclose
the further 0.3 mm seat-play budget and require actual placement/travel/wobble qualification.
The legacy pad-slot fit audit now reuses the same tilted pilot helper as the case generator.

Post-review verification: **67 mechanical/export/controller-layout tests passed**, including
the corrected cap orientation and current published STL vertices; `check_fit.py` ended
**ALL CLEAR** using the shared tilted-pilot geometry. The external half-shield rename
regressions also passed (2 tests). All eight firmware builds described above passed.
Final regenerated artifacts passed the independent binary audit: **20 production/public
STLs valid, all 10 public pairs byte-identical**. **78 PNGs** were refreshed and inventoried
with source hashes in `renders/manifest.json`; STL hashes are in `STL_EXPORT_MANIFEST.json`.
