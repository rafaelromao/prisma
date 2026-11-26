"""Passive drawer lid: one print on the canonical pointing-module tray.

The assembled module uses the existing feet, magnets, rear hooks and four
M3 x 8 flat-head screws. No electronics, no dedicated bottom. The roof is
1.0 mm above the halves' top-edge datum: a flush roof would bottom the
unchanged screws in the tray's pilots.
"""
from pathlib import Path
import shutil

from shapely.geometry import Point, box

import case as C
import module_shell as M
from trackball import trackball as B

TOP_T = 1.0
H = M.FLUSH + TOP_T
# Thicken the broad forward roof down into the empty enclosure, without
# crossing the post tops or extending into the rear hook/service region.
ROOF_EXTRA = 1.0
SOURCE = Path("case/placeholder_lid.stl")
PUBLIC = Path("stls/placeholder_lid.stl")


def diamond():
    """Original joined-board emblem, kept over the thick roof and off the screws."""
    room = M.lid_top_plan(H).intersection(box(-99, -200, 99, -22))
    for x, y in M.lid_screws():
        room = room.difference(Point(x, y).buffer(M.SCREW["head"] / 2))
    outline, seam, _ = M.K.diamond_fit(room)
    return M.K.relief_solid(outline, seam, H)


def lid():
    body = M.lid_blank(H, TOP_T)
    roof = M.inner().buffer(-M.LID_CLR, join_style=2).intersection(
        box(-99, -200, 99, -22))
    body += M.K.module_front(M.extrude(roof, M.FLUSH - ROOF_EXTRA, M.FLUSH + .01),
                             M.P, M.WALL + M.LID_CLR)
    return M.lid_holes(M.bevel(body, H), H) - diamond()


def tray():
    """Exactly the canonical complete tray, including its unused PCB seats."""
    return B.tray(B.place())


def build():
    """Assembly-frame lid and tray, separately (never export their union)."""
    return lid(), tray()


def lid_print():
    """Top down, like the other module lids."""
    return lid().mirror((0, 0, 1)).translate((0, 0, H))


def main():
    cover, bottom = build()
    M.check_common("Passive drawer lid", cover, bottom, [])
    M.check_dock_and_desk(bottom, cover, H, feet=M.bumpons())
    assert sum(p.volume() > 1e-6 for p in cover.decompose()) == 1
    assert H - M.SCREW["length"] - .2 - 13.9 >= .3
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC.parent.mkdir(parents=True, exist_ok=True)
    C.stl(lid_print(), SOURCE)
    shutil.copyfile(SOURCE, PUBLIC)
    print("Passive lid: %.1f cm3; top %.1f mm above the halves' edge" %
          (cover.volume() / 1000, H - M.FLUSH))


if __name__ == "__main__":
    main()
