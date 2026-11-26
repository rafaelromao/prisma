# Powered Prisma drawer central — qualification guide

Issue #6, on top of the common tray, retainer and passive-lid changes.
The drawer is a wireless **central**, not a third pointing peripheral.
Only the genuine Seeed XIAO nRF52840 is supported by this packing and firmware
proposal; the longer nice!nano intersects the long-cell reservation.

## Mechanical design

Reuse the exact common tray, four M3 × 8 flat-head lid screws, six side
magnets, one floor magnet and three 8 × 2 mm feet. The headless dongle has no
lid of its own: it uses the [passive drawer lid](PLACEHOLDER_LID.md), 1.0 mm
above the halves' inner edges; the OLED lid stands 1.2 mm. Both have the rear
hooks, power switch pocket and lever slot, and USB/reset access. No changes to the printed tray or any PCB.
The OLED variant has a recessed glass aperture, two locating rails and two
lands that bear on the non-active PCB ends. The headless roof is closed.
`python insert.py` exports the headless (placeholder) lid and `python dongle.py`
the OLED lid, top-down. The
[placeholder STL](stls/placeholder_lid.stl) and [OLED STL](stls/dongle_oled_lid.stl)
are CAD-verified prototypes, not physically qualified parts.

### Required parts and wiring

| Part | Quantity / specification |
|---|---|
| Existing three-board pointing panel | 1; main, controller carrier, reset board, unmodified |
| Genuine Seeed XIAO nRF52840 | 1, existing XIAO header/mount and eight stacking links |
| MSK-12C02 / TS-1187A | 1 each; only switch on main and reset on sensor board |
| Protected 1S LiPo | 1, **500 mAh**; actual dimensions including tabs and protection must fit the reservation |
| Dielectric carrier | 0.5 mm rigid smooth insulating sheet and three insulating blocks per `module_battery.py`; thin removable adhesive included in block heights |
| Battery retention | ≤0.15 mm removable battery-compatible insulating adhesive on sheet, no pressure on pouch or tabs |
| Battery connector | Optional insulated polarized inline connector only if measured harness fits; baseline existing direct soldered battery leads |
| Sensor-board screws | 2 M3 flat head, finished ≤7.6 mm, 0.4 mm equal shims, measured ≥0.3 mm pilot-bottom clearance |
| Optional OLED | Waveshare 0.91-inch OLED Module SKU 14657, SSD1306, 128×32, I²C, PCB 36 × 12.5 mm, 3.3 V supply |
| OLED retention | Removable dielectric tape at non-active board ends, not on glass; optional thin clear insulating window after measuring height |
| OLED harness | Original PH2.0 plug or compatible low-profile insulated harness; four conductors, strain relief and service slack |

The [vendor](https://www.waveshare.com/0.91inch-oled-module.htm) specifies the
36 × 12.5 mm PCB outline, 22.38 × 5.58 mm active area and 3.3/5 V operation.
The 31 × 10.5 × 1.35 mm glass, 2.3 mm PCB/parts depth below the PCB face,
and 5.5 mm local connector depth below the lid are **unmeasured fit limits**.
The plug and bend keepout extends 3 mm beyond the PCB. Check the actual
glass offset and board-end bearing surfaces; the 32 × 11.5 mm aperture
surrounds the recessed glass, not just its active pixels. If the original
plug fails the envelope, evaluate a lower-profile harness or a smaller
unmodified 3.3 V SSD1306 module.
Do not raise the lid or reduce battery capacity without reviewing clearance.

Follow the XIAO option in BUILD.md: populate the MSK switch, XIAO header,
eight links, correct XIAO 3.3 V selection and VBAT/R2 connections;
populate only TS-1187A on the reset board. Leave key sockets, switches,
sensor, optical parts, regulator and unused passive footprints empty.
Connect reset board G/RST only, as for the trackpad. Solder the battery to
the main board's **`+` (BAT+) and `−` (GND)** pads. **Do not connect the
pack to `VBAT`**: that is the switched output to XIAO BAT+, not the battery
input. Before connecting the pack or USB, meter polarity and continuity:
main `+` to `VBAT` open with the switch off and continuous with it on;
main `−` to `G` continuous in both positions.
Switch off disconnects battery; USB can still power MCU; charge with switch on.
Disconnect USB and physically isolate the battery before wiring.

| OLED wire | Existing main pad | XIAO |
|---|---|---|
| SCL | CK | D4 / P0.04 |
| SDA | IO | D5 / P0.05 |
| VCC | 3V | 3.3 V |
| GND | G | GND |

Verify 0x3c address, SDA/SCL idle voltage and pull-ups to **3.3 V**, not
VBAT/5 V. Meter OLED current at full pixels and idle/off; do not infer
runtime from the 500 mAh rating. The headless configuration needs no
display or display wires. Keep cables and metallic material clear of the
XIAO antenna; verify RF link and battery clearance in both assemblies.

## Packing and assembly

1. Measure the protected pack's entire body (reference 41 mm long, maximum
   45 × 20.0 × 8 mm installed envelope, tabs and insulation included;
   lead exit separately).
   Reject any larger pack or one with an incompatible lead exit; the actual
   owner's 500 mAh cell has not been measured. Do not use a smaller capacity.
2. Fit reset-only board first with shims and qualified screws, meter reset.
   Install carrier sheet and blocks over the original short cradle and
   component-free reset PCB areas. Sheet underside z=9.6, top z=10.1 mm.
   Secure blocks with removable thin dielectric adhesive; insulate all
   screws and solder joints, round/deburr edges, and check the sheet cannot
   shift. Retain the pack to the sheet with the specified removable adhesive,
   never clamp or wrap it tightly. Verify retention in all orientations.
3. Place the cell rear-aligned at y=-42.5, with adhesive thickness 0.15 mm;
   maximum modeled cell top z=18.25 mm, below main PCB underside.
    Route rear leads to main-board `+`/`−`, insulated and strain-relieved away from
   screw tips, magnets, solder joints and antenna. The modeled local lead
   exit is not a complete harness. Dry-fit the actual routing and any inline
   connector before soldering. Follow the existing controller insertion
   and stacking order. No board cutting, drilling or rerouting.
4. OLED: place the board from below with screen toward aperture, orient the
   connector toward the right end. Seat the non-active PCB edges against the
    end lands, not the glass; use removable insulating tape to retain the PCB.
    Ensure tape, plug and solder joints clear the pouch and screws.
   Route harness along a free side corridor, protect it from the rim and
   allow the lid to tilt open without loading the plug. Unplug display before
   removing lid. Measure real cable routing; do not pinch the cable to close.
5. Fit rear hooks first, lower lid and verify switch travel and USB connector
   access before inserting four standard screws. Tighten to flush only.
   Reset from below after withdrawing drawer; once reboot, twice bootloader.
   Test battery isolation, charger current and termination before unattended use.

## Firmware

Companion draft [keyboards PR #41](https://github.com/rafaelromao/keyboards/pull/41)
targets branch `prisma` and corrects stale shield symbols/includes.
Use the existing project container and pinned ZMK dependencies. After checking
out the companion branch, run `b prisma -c -p`. This also builds four
additional pointing-central targets; they are not required for the powered drawer.
Flash `prisma_peripheral_left-zmk.uf2` and `prisma_peripheral_right-zmk.uf2`
to the halves; flash `prisma_central_dongle-zmk.uf2` for headless or
`prisma_central_dongle_oled-zmk.uf2` for OLED, never the standalone left central.
Both central targets use the XIAO board and shared transform/keymap, two
BLE split peers, USB and BLE host support. OLED uses the ZMK built-in status
screen rather than the previous external 128×64 display module. Validate
layer, battery and connection widgets on the actual 128×32 panel.
At companion head `1b2093e3` on ZMK `9ebbeff0`, both dongle variants, both
peripherals and the standalone left central built locally for `xiao_ble//zmk`.
The generated configs confirm USB, BLE and two split peers on each dongle;
the OLED image selects a 128 × 32 SSD1306 with P0.04 SCL and P0.05 SDA.
UF2s were generated for verification, not published or flashed.

## Validation and regeneration

- Run inherited PR #7–#9 checks, then `python dongle.py`,
  `mkdir -p /tmp/opencode && python -m unittest test_dongle test_stl_export test_half_battery test_drawer test_module_assembly test_xiao_option test_switch_mount trackball.test_layout`,
  `python check_fit.py`, `python stand_mount.py`, `python verify_artifacts.py`.
  Inspect the exact CAD solids, all component/fastener collisions, tolerances,
  lid closure sweep, cable fit, both-half attachment, dock removal, standing
  plane and USB/control access. Inspect binary STL topology and public copies.
- Run `python vrml.py`, `python scene.py` and `./kicad.sh python3 render_boards.py`.
  Refresh `dongle_headless.png`, `dongle_oled.png`, `dongle_headless_structure.png`
  and `dongle_oled_structure.png` using `./render.sh` and
  `python render_manifest.py --update` with those basenames, then `python page.py`.
- Run both electrical DRCs, `python3 check_pcb.py` and
  `python3 trackball/check_controller_pcb.py`. Compare geometry, nets and
  Gerber/drill bytes against PR #9, ignoring only proved metadata. Never
  commit changed PCB/fabrication artifacts. Git blob comparison is not DRC.
- Build all firmware targets; inspect generated devicetree/Kconfig and UF2s.
  Physically test pair/reconnect both halves, all keys, layer changes,
  USB HID and BLE host switching, headless with no panel, OLED content,
  orientation, current and timeout, charging, off, reset and bootloader.
- Print and measure both lids; test real cell protection, retention,
  screw-tip isolation, antenna clearance, display retention, wire strain
  relief, temperatures and charging; confirm safe repeatable service.
  No physical testing, battery dimension or runtime measurement performed.

Until physical qualification passes and the companion firmware lands,
do not present this as a print-ready or field-tested assembly.
