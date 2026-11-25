# Powered Prisma drawer central — draft qualification guide

Issue #6, on top of the common tray, retainer and passive-lid changes.
The drawer is a wireless **central**, not a third pointing peripheral.
Only the genuine Seeed XIAO nRF52840 is supported by this packing and firmware
proposal; the longer nice!nano intersects the long-cell reservation.

## Mechanical design

Reuse the exact common tray, four M3 × 8 flat-head lid screws, six side
magnets, one floor magnet and three 8 × 2 mm feet. Both lids retain the
standard Choc height (1.2 mm above the halves' inner edges), rear hooks,
switch cutout and USB/reset access. No changes to the printed tray or any PCB.
The OLED variant has a top aperture and two internal locating rails; the
headless version has a closed roof. Export top-down with `python dongle.py`
to `case/dongle_lid.stl` and `case/dongle_oled_lid.stl`, copied to `stls/`.
These are source designs until verified and exported.

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

Vendor: https://www.waveshare.com/product/displays/0.91inch-oled-module.htm
The vendor specifies the PCB outline, active area 22.38 × 5.58 mm and 3.3/5 V
operation. The 3 mm body-depth and 5.5 mm local connector-depth envelopes
in CAD are **not manufacturer-confirmed thicknesses**. Measure actual
glass offset, PCB, connector and cable bend before printing; the provisional
27 × 8.5 mm aperture must expose the entire active area without bearing
on the glass. If the plug fails the envelope, try a compatible lower-profile
wire exit or a smaller/thinner unmodified 3.3 V SSD1306 module first.
Do not raise the lid or reduce battery capacity without reviewing clearance.

Follow the XIAO option in BUILD.md: populate the MSK switch, XIAO header,
eight links, correct XIAO 3.3 V selection and VBAT/R2 connections;
populate only TS-1187A on the reset board. Leave key sockets, switches,
sensor, optical parts, regulator and unused passive footprints empty.
Connect reset board G/RST only, as for the trackpad. Keep the original
switch/power circuit and verify polarity and continuity before connecting
a battery. The existing board exposes solder pads, not a battery socket.
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
   45 × 20.4 × 8 mm envelope, tabs included; lead exit separately).
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
   Route rear leads toward VBAT/G, insulated and strain-relieved away from
   screw tips, magnets, solder joints and antenna. The modeled local lead
   exit is not a complete harness. Dry-fit the actual routing and any inline
   connector before soldering. Follow the existing controller insertion
   and stacking order. No board cutting, drilling or rerouting.
4. OLED: place the board from below with screen toward aperture, orient the
   connector toward the right end. Seat the non-active PCB edges against the
   lid, not the glass; use removable insulating tape to retain the PCB to the
   rails. Ensure the tape, plug and solder joints clear the pouch and screws.
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
out the companion branch, run `b prisma -c -p` (all five targets).
Flash `prisma_peripheral_left-zmk.uf2` and `prisma_peripheral_right-zmk.uf2`
to the halves; flash `prisma_central_dongle-zmk.uf2` for headless or
`prisma_central_dongle_oled-zmk.uf2` for OLED, never the standalone left central.
Both central targets use the XIAO board and shared transform/keymap, two
BLE split peers, USB and BLE host support. OLED uses the ZMK built-in status
screen rather than the previous external 128×64 display module. Validate
layer, battery and connection widgets on the actual 128×32 panel.
No UF2 is published or claimed to build here.

## Validation and regeneration (blocking)

- Run inherited PR #7–#9 checks, then `python dongle.py`,
  `mkdir -p /tmp/opencode && python -m unittest test_dongle test_stl_export test_half_battery test_drawer test_module_assembly test_xiao_option test_switch_mount trackball.test_layout`,
  `python check_fit.py`, `python stand_mount.py`, `python verify_artifacts.py`.
  Inspect the exact CAD solids, all component/fastener collisions, tolerances,
  lid closure sweep, cable fit, both-half attachment, dock removal, standing
  plane and USB/control access. Inspect binary STL topology and public copies.
- Run `python vrml.py`, `python scene.py`, `./kicad.sh python3 render_boards.py`,
  `./render.sh`, `python render_manifest.py`, `python page.py`. Inspect
  headless/OLED and exploded scenes; regenerate/commit actual affected assets
  and manifests, reconcile page links. No STL, render or manifest regenerated here.
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

Until all applicable gates pass, this is a draft/source implementation,
not print-ready, firmware-ready or safe to assemble unattended.
