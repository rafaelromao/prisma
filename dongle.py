"""Powered drawer central on the unchanged common tray and PCB panel.

XIAO only; the long-cell reservation is inherited from issue #3. The OLED
model is a packing envelope, not a measured supplier STEP. Never force
a battery or display into an enclosure that fails these checks.
"""
from pathlib import Path
import shutil

import numpy as np
from shapely.geometry import box

import case as C
import module_shell as M
import module_battery as MB
from trackball import trackball as B
from trackball.controllers import xiao, xiao_usb_z

H = M.CHOC_TOP
OLED_Y = -80.0
# Waveshare SKU 14657, SSD1306 128x32, 36 x 12.5 mm PCB.
OLED_W, OLED_L = 36.0, 12.5
# Maximum proposed packing envelopes; only the PCB outline is vendor-dimensioned.
# Measure front glass, PCB/parts depth and the mated cable before assembly.
OLED_PCB_Z = M.FLUSH - .45  # face of the PCB, seated against dedicated land pads
OLED_DEPTH = 2.3           # PCB and underside parts (except the end connector)
GLASS_W, GLASS_L, GLASS_T = 31.0, 10.5, 1.35
GLASS_X = -.3
OLED_CLR = .3
WINDOW_W, WINDOW_L = 32.0, 11.5
OLED_Z = OLED_PCB_Z - OLED_DEPTH
BAT_ADHESIVE = .15
NAMES = {False: "dongle_lid", True: "dongle_oled_lid"}
KEEP = ("main board", "power switch", "controller board", "controller header",
        "stacking pins' plastic", "sensor board", "reset")


def rect(w, length, x=0, y=OLED_Y):
    return box(x - w / 2, y - length / 2, x + w / 2, y + length / 2)


def display():
    """PCB/parts and recessed front glass, on separate datums; connector separate."""
    return (M.extrude(rect(OLED_W, OLED_L), OLED_Z, OLED_PCB_Z)
            + M.extrude(rect(GLASS_W, GLASS_L, x=GLASS_X), OLED_PCB_Z - .01,
                        OLED_PCB_Z + GLASS_T))


def connector():
    """Right-end socket, mated plug and local bend; deliberately extend beyond the PCB."""
    return B.box3(12.5, OLED_Y - 5.5, M.FLUSH - 5.5, 21.0, OLED_Y + 5.5, OLED_Z)


def lid(oled=False):
    L = B.place()
    sh = M.lid_blank(H, 1.2)
    back = L["back"]
    main = B.main_board_plan(L)
    # Same power lever opening and body pocket as the powered Choc lids.
    sh -= B.box3(-2.5, back - M.WALL - 1.5, B.PCB_TOP,
                 2.5, back + 1.5, B.PCB_TOP + 2.6)
    sh -= B.box3(-3.55, main.bounds[3] - 3.35, B.PCB_TOP - .01,
                 3.55, main.bounds[3] - .25, B.PCB_TOP + 1.55)
    if oled:
        # Locate the non-active edges with rails and end lands. The window
        # surrounds the whole recessed glass: its edges never bear lid load.
        outer = rect(OLED_W + 2 * (OLED_CLR + 1.0), OLED_L + 2 * (OLED_CLR + 1.0))
        pocket = rect(OLED_W + 2 * OLED_CLR, OLED_L + 2 * OLED_CLR)
        rails = outer.difference(pocket).intersection(
            rect(OLED_W - 4.0, OLED_L + 2 * (OLED_CLR + 1.0)))
        sh += M.extrude(rails, M.FLUSH - 1.4, M.FLUSH + .02)
        for x in (-17.25, 17.25):
            sh += M.extrude(rect(1.3, 9.0, x=x), OLED_PCB_Z, M.FLUSH + .02)
        sh -= M.extrude(rect(WINDOW_W, WINDOW_L, x=GLASS_X), M.FLUSH - .02, H + .1)
    return M.lid_holes(M.bevel(sh, H), H)


def tray():
    return B.tray(B.place())


def cell(length=MB.MAX_LENGTH):
    return MB.long_cell(length).translate((0, 0, BAT_ADHESIVE))


def adhesive(length=MB.MAX_LENGTH):
    return B.box3(-8, MB.REAR - length + 2, MB.CELL_Z,
                  8, MB.REAR - 2, MB.CELL_Z + BAT_ADHESIVE)


def parts(oled=False, length=MB.MAX_LENGTH):
    L = B.place()
    all_parts = dict(B.parts(L, B.main_board_plan(L), B.sensor_board_plan(L), "choc"))
    out = [(name, all_parts[name]) for name in KEEP]
    floor = B.SOCKET_BOT - B.NANO_GAP - B.NANO[2]
    out += [("XIAO", xiao(B.xiao_back(L), floor)),
            ("insulated carrier", MB.carrier()), ("cell adhesive", adhesive(length)),
            ("500 mAh cell envelope", cell(length)),
            ("battery lead exit", MB.lead_exit().translate((0, 0, BAT_ADHESIVE)))]
    if oled:
        out += [("OLED", display()), ("OLED connector envelope", connector())]
    return out


def build(oled=False):
    return lid(oled), tray(), parts(oled)


def lid_print(oled=False):
    return lid(oled).mirror((0, 0, 1)).translate((0, 0, H))


def paths(oled=False):
    name = NAMES[oled] + ".stl"
    return Path("case") / name, Path("stls") / name


def check(oled=False, length=MB.MAX_LENGTH):
    L = B.place()
    cover, bottom = lid(oled), tray()
    components = parts(oled, length)
    # Existing carrier/header envelope overlaps may represent intentional
    # electrical contacts. Test new packing against all original hardware
    # separately, not board-to-pin joints.
    new = dict(components[len(KEEP) + 1:])
    fixed = components[:len(KEEP) + 1] + [
        ("stacking pins", B.stacking_pins(L)),
        ("lid screws", M.lid_fasteners(H)),
        ("floor magnet", M.floor_magnet()), ("feet", M.bumpons())]
    for x, y in B.sensor_holes(L):
        fixed.append(("reset board screw", M.flat_screw(
            x, y, B.sensor_screw_stack()["head_top"], B.SENSOR_SCREW_LENGTH)))
    def clear(a, b, label):
        assert abs((a ^ b).volume()) < 1e-3, label
    clear(cover, bottom, "lid/tray")
    for name, solid in components:
        clear(solid, bottom, name + "/tray")
        clear(solid, cover, name + "/lid")
    for name, solid in new.items():
        for label, obstacle in fixed:
            clear(solid, obstacle, name + "/" + label)
    for i, (name, solid) in enumerate(new.items()):
        for label, obstacle in list(new.items())[i + 1:]:
            clear(solid, obstacle, name + "/" + label)
    packing = (new["500 mAh cell envelope"] + new["battery lead exit"])
    obstacles = cover + bottom
    for _, solid in fixed:
        obstacles += solid
    if oled:
        obstacles += display() + connector()
    for dx in (-MB.LATERAL_ALLOWANCE, MB.LATERAL_ALLOWANCE):
        clear(packing.translate((dx, 0, 0)), obstacles, f"pack lateral clearance ({dx:+.2f} mm)")
    dock = M.K.make()
    M.check_dock_and_desk(bottom, cover, H, components, k=dock)
    assert sum(p.volume() > 1e-6 for p in cover.decompose()) == 1


def usb_insertion_clearance(oled=False):
    """Sweep a complete illustrative straight USB-C plug from outside the dock."""
    L = B.place()
    metal, plug, cable = M.usb_connection(B.xiao_back(L), xiao_usb_z(
        B.SOCKET_BOT - B.NANO_GAP - B.NANO[2]))
    dock = M.K.make()
    half = dock.p(M.K.HALF)
    docked = (dock.solid + half + half.mirror((1, 0, 0))).translate((0, 0, -M.FLOOR_Z))
    obstacles = docked + tray() + lid(oled)
    # The metal tip intentionally enters the MCU receptacle, not the enclosure.
    for offset in np.arange(0, 25, .5):
        swept = (metal + plug + cable).translate((0, offset, 0))
        assert abs((swept ^ obstacles).volume()) < 1e-3, ("USB insertion", offset)


def main():
    for oled in (False, True):
        for length in (MB.REFERENCE_LENGTH, MB.MAX_LENGTH):
            check(oled, length)
        usb_insertion_clearance(oled)
        source, public = paths(oled)
        source.parent.mkdir(parents=True, exist_ok=True)
        public.parent.mkdir(parents=True, exist_ok=True)
        C.stl(lid_print(oled), source)
        shutil.copyfile(source, public)


if __name__ == "__main__":
    main()
