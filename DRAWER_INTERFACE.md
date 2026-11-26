# Common drawer interface (issue #3)

There is one canonical printed bottom: `case/module_tray.stl`, byte-identically
published as `stls/module_tray.stl`. Use `trackball.trackball.tray(B.place())`
as the existing complete tray generator; `module_shell.tray()` is its lower
level shell, not a second printable option. The trackpad passes the same
board/battery placement into the complete generator. Do not fork the tray.

## Mechanical contract

All coordinates are in the existing case frame, millimetres, with Z measured
from the standing plane. No changes to the footprint, front facets, dock,
magnet seats, foot roofs, rear hood, service openings, PCB seats or screw
pilots are required for this approach.

| Interface | Existing datum / requirement |
|---|---|
| Bottom / seam | Feet stand at Z=0; printed bottom starts at Z=0.5; seam at `M.FLUSH` |
| Locating lip | `M.lid_blank()`, nominal 0.25 mm side clearance; rear hooks at X=±5 |
| Lid screws | Four M3 × 8 flat-head, 90° countersunk, 2.5 mm pilots; front X=±21, Y=-91.5; board pair X=±12.3, Y=-54 |
| Standard low lid | `M.CHOC_TOP = M.FLUSH + 1.2`; MX remains at `M.FLUSH + 4` |
| Magnet / feet | Six 8 × 1.5 mm side magnets, one floor magnet, three 8 × 2 mm bump-ons |
| Service | Rear USB-C and power slot, existing downward reset hole; no additional holes |
| Insertion | Rear hooks first for lid; horizontal front removal for the complete module |
| Front marking | 35 × 8 mm PRISMA wordmark in front projection, recessed 0.4 mm across the three front facets; no footprint or insertion change |

A non-pointing standard-height blank fixture in `module_battery.interface_lid()`
exercises the existing interface. The passive lid in `insert.py` (#5)
uses the standard low-lid height, with a locally thickened broad roof.
At `M.FLUSH`, an 8 mm screw tip would be at Z=13.477, below the existing
Z=13.9 pilot bottom; the 1.2 mm rise avoids this without changing the tray
or screw standard. See [passive lid verification](PLACEHOLDER_LID.md).
The installed passive lid is only 1.0 mm above FLUSH, using the standard
M3 × 8 screws. The solid insert is retired; the dongle (#6) is separate.

## Battery reservation

The pointing variants keep the 752025 (20 × 25 × 7.5 nominal) cell, its
integral cradle, the sensor screw posts and every existing board placement.
A longer cell cannot simply extend forward on the same low seat: the front
cradle wall and the centre sensor post interrupt the channel. Cutting them
would change the existing optical/reset assembly and invalidate the tray STL.

Use the permitted removable insulated carrier alternative instead: keep the
same nominal 20 mm cell width and 7.5 mm thickness, but raise the long cell
into the freed pointing-device space. Use the **plain XIAO** on the existing
controller board, the main board with power switch but no keys/sockets, and
the existing sensor PCB populated only for reset. No lens, optical sensor,
Cirque, or breakout. The longer nice!nano overlaps this raised reservation
and is not supported by this layout.

The carrier is a cut-to-size **20 × 45 × 0.5 mm dielectric sheet** (not another
tray or PCB), with rounded/deburred edges and three removable rigid insulating
spacers. Use electronics-grade removable tape; support the sheet without
loading solder joints, and secure the pouch without pinching or compressing
it. Spacer heights include adhesive. Use the actual unpopulated board to
confirm safe bearing surfaces before assembly.

| Reserved item | Case-frame dimensions (mm) |
|---|---|
| Sheet | X=-10..10, Y=-87.5..-42.5, Z=9.6..10.1 |
| Rear support | X=-4..4, Y=-52..-46, Z=3.1..9.6 (original battery seat) |
| Middle support | X=-3..3, Y=-74..-71, Z=7.7..9.6 (reset board) |
| Front support | X=-3..3, Y=-85..-83, Z=7.7..9.6 (reset board) |
| Long-cell maximum installed envelope | X=-10..10, rear Y=-42.5, length up to 45, Z=10.1..18.1 |
| Reference protected length | 41 mm (40 mm nominal plus allowance, not a pack measurement) |
| Local lead exit | X=-3..3, Y=-42.5..-39.8, Z=10.1..13.1 |

The width/thickness limits include cell manufacturing variation and
insulation. The 20.4 mm nominal tray throat is not a usable pack width:
the 20.0 mm installed limit leaves 0.2 mm per side. CAD tests allow a
0.15 mm lateral offset during insertion; measure the printed tray and verify
positive residual clearance after print error, insulation and swelling. The main PCB underside
is at Z=18.877, leaving only 0.777 mm nominal above the maximum cell
envelope. Keep solder joints and wires out of that gap unless measured
clearance permits them. Do not assume the lead-exit box verifies the entire
wired path. #6 must route and verify the leads, charging, reset wiring,
actual lid and optional OLED against the measured cell and completed assembly.

Assembly order for the future dongle: fit magnets and feet; check sensor
screw tips and fit the reset-only board; fit the insulated carrier and
cell (before the main board); install the XIAO/controller stack and main
board; route and insulate wires; verify clearance and close the lid.
Remove in reverse order with USB disconnected and the cell electrically
isolated. Existing soldered stacking pins may require desoldering for service.

## Verification and release gates

`test_module_assembly.py` covers the 250 mAh placement, shared tray,
reference/maximum long-cell envelope, carrier, selected electronics and
insertion path. `test_drawer.py` covers the blank interface and dock/desk
fit. `test_stl_export.py` checks the canonical binary and public copy;
the shared tray geometry and published STL bytes remain unchanged. The carrier
is cut sheet and spacers, not a new STL. The passive lid has its own export
and updated dock/assembly views; the dongle will need its own assets.

PCB freeze: do not change `B.place()`, board plans, PCB footprints, holes,
netlists, pin assignments or fabrication artifacts. The existing mechanical
and electrical CI checks remain mandatory. Verify the PR diff excludes
all PCB/fabrication paths and board-generating parameters.

The selected 500 mAh pack's actual protected dimensions (including tabs,
lead exit, insulation, tolerance and swelling allowance) are not supplied.
This reservation is not proof that a particular cell fits, nor is it a
print/assembly qualification. If measured dimensions or safe routing exceed
the reservation, stop and revise the removable carrier or controller
arrangement within the same enclosure; do not compress the cell or alter
any PCB. Follow [PRINT_READINESS.md](PRINT_READINESS.md) and
[REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md).

## Powered central variant (draft)

The standard tray is unchanged. See [DONGLE.md](DONGLE.md) for the 500 mAh XIAO central, headless and OLED lids, shared electrical board stack and outstanding qualification. Both lids preserve the common screw/foot/magnet/hood interface; no new PCB or tray export.
