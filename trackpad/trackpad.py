"""Prisma Trackpad: a 40 mm Cirque trackpad and two Choc hot-swap keys, in a drawer module.

It is the trackball's module with a different lid. The tray, the main board (keys, sockets, power
switch), the nice!nano, the battery and a sensor board are all the same, in the same places: the
power switch and USB-C at the back, the reset button pressed from below. Only the lid differs: it
carries the pad, on a ledge. The sensor board carries only reset. The supplied I2C breakout and
flat cable are retained; four wires go to the breakout and a separate DR wire to the pad.

Writes trackpad/design.json (placement, wiring), case/lid.stl and case/retainer.stl, and prints the fit check.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import numpy as np
from manifold3d import Manifold
from shapely.geometry import Point, box

import case as C
import module_shell as M
from trackball import trackball as B
from trackball.controller_pinout import SIGNALS, GPIO

H = M.PCB_TOP + B.CHOC["below_plate"]   # the Choc trackball's height
TOP_T = 1.2                    # the top: a Choc plate (the switches clip into 1.2 to 1.3 mm)
# TM040040 spec: 0.99 mm PCB + overlay, 5.15 +/- 0.2 mm with components, none in the outer 2 mm ring.
# Keep the original seat and pad datum; the ledge supports the free underside ring.
# Two removable hooks capture only the two side edge sectors, with no adhesive or preload.
PAD = dict(d=40.0, t=1.2, back=4.4, clr=0.3, rim=1.0, ledge=1.8, gap=12.0)
# M3 x 4 pan-head, length under head. The project uses M3 fasteners only; the
# short screw still fits the blind lid bosses without touching the PCB or tray.
# Each station is (hook/slot angle about the pad centre, local screw x, local
# screw y). The screw is offset sideways from the slot so the stem channel does
# not cut the pilot, and the hook pair is a mirror set. Printed thread pull-out
# strength, the 0.55 mm bearing land and the actual hardware remain to be
# qualified.
RETAINER = dict(diameter=3.0, length=4.0, pilot=M.SCREW["pilot"], clearance=3.4,
                 head_d=5.5, head_h=2.0, flange=1.2, boss_depth=4.0, roof=.6,
                 boss_r=2.25, slide=1.55, axial_play=.2,
                 length_tol=.1, flange_tol=.1,
                 edge_overlap=.8, lip_t=.8)
# A mirror pair on the two flanks: nearly opposite lips catch a tilt about
# either horizontal axis. The flanks keep the 5.5 mm screw head inside the
# tray's top rim through the whole lid-closing sweep, clear of the lid's front
# countersink webs. Both screws sit 4.4 mm tangentially off the stem channel,
# clear of the 2.5 mm pilot and the 3.8 mm channel, and each boss stays outside
# the 40 mm pad.
RETAINER_STATIONS = ((-10.76, 22.16, -4.4), (-169.24, 22.16, 4.4))
RETAINER_ANGLES = tuple(station[0] for station in RETAINER_STATIONS)
BREAKOUT = (24.0, 18.0, 4.5)   # reserved maximum envelope, including parts/connector, not a measured kit
BREAKOUT_LIFT = 2.5            # insulating spacer clears the sensor-board screw heads; no holder
NANO = B.NANO
box3 = B.box3
usb_z = B.usb_z
PLATE_TOP = B.PLATE_TOP


def place():
    L = dict(B.place())
    top = M.lid_top_plan(H)
    r = PAD["d"] / 2 + PAD["clr"]
    # the pad: as far forward as fits with PAD['rim'] of top round it
    L["pad"] = (0.0, next(y for y in np.arange(top.bounds[1] + r, -30, 0.1)
                          if top.buffer(-PAD["rim"]).contains(Point(0, y).buffer(r))))
    L["reset"] = B.sensor_reset(L)
    return L


def parts(L, main_plan, sensor_plan):
    """The parts as solids, for the checks and the renders."""
    out = [p for p in B.parts(L, main_plan, sensor_plan, "choc")
           if not p[0].startswith(("ball", "bearing", "lens", "sensor's parts"))]
    px, py = L["pad"]
    pz = H - PAD["t"]
    out.append(("pad", Manifold.cylinder(PAD["t"], PAD["d"] / 2, circular_segments=96).translate((px, py, pz))))
    out.append(("pad's back parts", Manifold.cylinder(PAD["back"], PAD["d"] / 2 - PAD["ledge"] - 0.3,
                                                       circular_segments=96).translate((px, py, pz - PAD["back"]))))
    out.append(("I2C breakout envelope", breakout_envelope(L)))
    out.append(("FFC bend envelope", ffc_envelope(L)))
    for i, clip in enumerate(retainers(L), 1):
        out.append(("pad retainer %d" % i, clip))
    for i, head in enumerate(retainer_screws(L, heads_only=True), 1):
        out.append(("pad retainer screw %d" % i, head))
    return out


def breakout_envelope(L):
    """Reserved insulated packing space, not a printed holder or exact supplied PCB model."""
    x, y = L['ball']
    z = B.PLATE_TOP + B.SENSOR_BELOW + B.PCB_T + BREAKOUT_LIFT
    w, length, height = BREAKOUT
    return box3(x - w / 2, y - length / 2, z, x + w / 2, y + length / 2, z + height)


def ffc_envelope(L):
    """Space for a 6 mm-wide 12-pin FFC and its bend above the breakout."""
    top = breakout_envelope(L).bounding_box()[5]
    return box3(-3.5, L['ball'][1] - 2, top + .3,
                3.5, L['pad'][1] + 18, H - PAD['t'] - PAD['back'] - .3)


def dr_lead_corridor():
    """Separate DR lead's local drop beside the FFC, excluding its solder joint."""
    return Manifold.cylinder(6.2, .45, circular_segments=32).translate((4.8, -60.2, 10.8))


def breakout_visual(L):
    """Illustrative supplied breakout within its reserved envelope, not a measured PCB."""
    x, y = L['ball']
    z = breakout_envelope(L).bounding_box()[2]
    w, length, h = BREAKOUT
    board = box3(x - w / 2, y - length / 2, z, x + w / 2, y + length / 2, z + 1.6)
    board += box3(-4.5, y + 4, z + 1.6, 4.5, y + 8, z + h)
    return board


def ffc_visual(L):
    """Illustrative 6 mm-wide flat cable, kept inside the tested bend envelope."""
    bounds = ffc_envelope(L).bounding_box()
    z0, z1 = bounds[2], bounds[5]
    py, by = L['pad'][1], L['ball'][1]
    path = [(py + 15, z1 - .15), (py + 17, (z0 + z1) / 2),
            (py + 15, z0 + .2), (by + 6, z0 + .15)]
    strips = [box3(-3, y - .1, z - .1, 3, y + .1, z + .1) for y, z in path]
    out = Manifold()
    for a, b in zip(strips, strips[1:]):
        out += (a + b).hull()
    return out


def at_pad(solid, L, angle):
    """Place a local solid in either of the two edge-retainer stations."""
    return solid.rotate((0, 0, angle)).translate((*L["pad"], 0))


def retainer_floor():
    return H - RETAINER["boss_depth"]


def _clip(sx, sy):
    """One keyed hook. Insert through the slot from below, slide in, screw to the boss.

    The hard flange seats on the boss, not on the sensor. The top hook has axial
    play above the nominal overlay; its inner edge covers only the outer 0.8 mm.
    """
    q = RETAINER
    z = retainer_floor()
    stem = box(20.8, -1.6, 21.5, 1.6)
    flange = stem.union(Point(sx, sy).buffer(q["boss_r"], quad_segs=16)).convex_hull
    clip = M.extrude(flange, z - q["flange"], z)
    clip += M.extrude(stem, z - .02, H + q["axial_play"] + q["lip_t"])
    clip += box3(PAD["d"] / 2 - q["edge_overlap"], -1.6, H + q["axial_play"],
                 21.5, 1.6, H + q["axial_play"] + q["lip_t"])
    hole = Manifold.cylinder(q["flange"] + .1, q["clearance"] / 2,
                             circular_segments=40).translate((sx, sy, z - q["flange"] - .04))
    return clip - hole


def retainers(L):
    return retainer_poses(L)


def retainer_poses(L, outward=0, down=0):
    """Clip positions along their individual straight assembly/removal paths."""
    out = []
    for angle, sx, sy in RETAINER_STATIONS:
        clip = _clip(sx, sy).translate((outward, 0, -down))
        out.append(at_pad(clip, L, angle))
    return out


def retainer_print():
    """Print the left/right pair, each lying on its side so the lip is not a cantilever."""
    pair = []
    for _, sx, sy in RETAINER_STATIONS:
        m = _clip(sx, sy).rotate((90, 0, 0))
        x, y, z = m.bounding_box()[:3]
        pair.append(m.translate((-x, -y, -z)))
    gap = 5.0
    right, left = pair
    left = left.translate((right.bounding_box()[3] + gap, 0, 0))
    return right + left


def retainer_screws(L, heads_only=False, extra=0.0, flange_error=0.0):
    q = RETAINER
    z = retainer_floor() - q["flange"] - flange_error
    head = Manifold.cylinder(q["head_h"], q["head_d"] / 2, circular_segments=48)
    out = []
    for angle, sx, sy in RETAINER_STATIONS:
        screw = head.translate((sx, sy, z - q["head_h"]))
        if not heads_only:
            screw += Manifold.cylinder(q["length"] + extra, q["diameter"] / 2,
                                       circular_segments=48).translate((sx, sy, z))
        out.append(at_pad(screw, L, angle))
    return out


def _retainer_mounts(sh, L):
    q = RETAINER
    z = retainer_floor()
    boss = Manifold.cylinder(q["boss_depth"] - TOP_T + .02, q["boss_r"],
                             circular_segments=64)
    # The blind hole opens on the underside. Leave the full 0.6 mm roof.
    pilot = Manifold.cylinder(q["boss_depth"] - q["roof"] + .02, q["pilot"] / 2,
                              circular_segments=48).translate((0, 0, -.02))
    # Insertion clearance for the lip, and a narrow keyed stem channel. The
    # channel starts 0.4 mm outside the 20.3 mm pad opening, so the lid keeps a
    # printable web instead of a sliver. Its outer edge stays within the top
    # bevel; the vertical wall below is at least 0.45 mm. The rest of the
    # original ledge remains unchanged, including the rear gap.
    slot = box3(20.70, -1.9, z - .1, 23.10, 1.9, H + 1.1)
    for angle, sx, sy in RETAINER_STATIONS:
        sh += at_pad(boss.translate((sx, sy, z)), L, angle)
        sh -= at_pad(pilot.translate((sx, sy, z)) + slot, L, angle)
    return sh


def lid(L):
    sh = B.lid(L, "choc", ball=False)
    # the pad's seat: through the top, and a ledge round it under its rim, open at the back
    px, py = L["pad"]
    r = PAD["d"] / 2 + PAD["clr"]
    sh -= Manifold.cylinder(TOP_T + 1, r, circular_segments=120).translate((px, py, H - TOP_T - 0.5))
    ledge_z = H - PAD["t"]
    ring = Point(px, py).buffer(r + 3.0).difference(Point(px, py).buffer(PAD["d"] / 2 - PAD["ledge"]))
    ring = ring.difference(box(px - PAD["gap"] / 2, py, px + PAD["gap"] / 2, py + 40))
    ring = ring.difference(B.main_board_plan(L).buffer(.3)).intersection(M.inner().buffer(-M.LID_CLR, join_style=2))
    for x, y in M.lid_screws()[:2]:
        ring = ring.difference(Point(x, y).buffer(M.SCREW["post"] / 2 + .3))
    # It grows inwards at 45 degrees as the lid prints, top down, so its seat needs no support
    seat = M.K.module_front(M.extrude(ring, ledge_z - 1.0, ledge_z + .01), M.P, M.WALL + M.LID_CLR)
    cone = Manifold.cylinder(1.0, PAD["d"] / 2 - PAD["ledge"] + 1.0, PAD["d"] / 2 - PAD["ledge"],
                             circular_segments=120).translate((px, py, ledge_z - 1.0))
    sh += seat - cone
    sh -= Manifold.cylinder(TOP_T + 1, r, circular_segments=120).translate((px, py, ledge_z))
    return M.lid_holes(M.bevel(_retainer_mounts(sh, L), H), H)


def wiring():
    """nice!nano I2C breakout wiring, plus the separate underside DR wire."""
    return {
        "breakout SDA": ("D3", "P0.20"), "breakout SCL": ("D2", "P0.17"), "pad DR": ("D4", "P0.22"),
        "breakout GND": ("GND", ""), "breakout VDD": ("VCC", "3.3 V"),
        "main board K1": ("D19", "P0.02"), "main board K2": ("D21", "P0.31"),
        "main board GND": ("GND", ""), "main board VBAT": ("B+", ""), "main board RST": ("RST", ""),
    }


def main():
    L = place()
    tray_m, main_plan, sensor_plan = B.tray(L), B.main_board_plan(L), B.sensor_board_plan(L)
    lid_m = lid(L)
    ps = parts(L, main_plan, sensor_plan)
    M.check_common("Prisma Trackpad", lid_m, tray_m, ps)
    M.check_dock_and_desk(lid_m, tray_m, H, ps)
    print("  height %.2f mm, pad centre y %.2f, keys at y %s" % (H, L["pad"][1], ["%.1f" % k[1] for k in L["keys"]]))
    print("  lid %.1f cm3, genus %d" % (lid_m.volume() / 1000, lid_m.genus()))
    os.makedirs(os.path.join(HERE, "case"), exist_ok=True)
    B.stl_lid(lid_m, H, os.path.join(HERE, "case", "lid.stl"))
    shutil.copyfile(os.path.join(HERE, "case", "lid.stl"), os.path.join(HERE, "..", C.STLS, "trackpad_lid.stl"))
    C.stl(retainer_print(), os.path.join(HERE, "case", "retainer.stl"))
    shutil.copyfile(os.path.join(HERE, "case", "retainer.stl"), os.path.join(HERE, "..", C.STLS, "trackpad_retainer.stl"))
    json.dump(dict(layout={k: v for k, v in L.items()}, height=H, screws=M.lid_screws(), feet=M.feet_spots(),
                    wiring=wiring(), controllers=SIGNALS['trackpad'], gpio=GPIO,
                     breakout_envelope=BREAKOUT, breakout_lift=BREAKOUT_LIFT,
                     retainer=dict(RETAINER, angles=RETAINER_ANGLES,
                                   stations=RETAINER_STATIONS)), open(os.path.join(HERE, "design.json"), "w"), indent=1,
              default=lambda o: [float(v) for v in o])
    return L, lid_m, tray_m, ps


if __name__ == "__main__":
    main()
