"""The drawer's placeholder: a solid insert, for when neither the trackball nor the trackpad is in.

It has the modules' outline and magnets (module_shell.py), flush with the halves' top edges, solid
down to the drawer's floor (no feet: it stands on the floor directly, so its magnets sit where a
module's do), the joined board's diamond cut into its top, and PRISMA raised 0.5 mm behind it.
Printed solid (any infill), it carries the dock's middle as the old spine did.

Writes case/insert.stl (and the repo's STL folder), and checks it against the dock and the halves.
"""
import os
import shutil

import matplotlib
matplotlib.use("Agg")
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from shapely import affinity
from shapely.geometry import Polygon

import case as C
import dock as K
import module_shell as M

H = M.FLUSH
WORD = "PRISMA"
WORD_FONT = FontProperties(family="DejaVu Sans", weight="bold")
WORD_CAP = 7.2                # cap height (mm)
WORD_W = 34.0                 # width (mm): condensed to stay inside the insert's taper
WORD_Y = -58.0                # behind the diamond, on the clear part of the top
WORD_H = 0.5                  # low relief: proud of the top


def word_outline(text=WORD, cap=WORD_CAP, width=WORD_W):
    """The word's filled outline, cap high and width wide, centred on the origin."""
    path = TextPath((0, 0), text, size=100, prop=WORD_FONT)
    shape = Polygon()
    for ring in path.to_polygons():                 # even-odd: a letter's counters are holes
        shape = shape.symmetric_difference(Polygon(ring).buffer(0))
    x0, y0, x1, y1 = shape.bounds
    shape = affinity.scale(shape, width / (x1 - x0), cap / (y1 - y0), origin=(0, 0))
    x0, y0, x1, y1 = shape.bounds
    return affinity.translate(shape, -(x0 + x1) / 2, -(y0 + y1) / 2)


def build():
    body = M.bevel(M.extrude(M.OUTLINE, 0.0, H) + M.rear_hood(), H)
    body -= M.magnet_pockets()
    diamond, seam, scale = K.diamond_fit(M.OUTLINE)
    art = K.relief_solid(diamond, seam, H)
    word = affinity.translate(word_outline(), 0.0, WORD_Y)
    assert M.OUTLINE.buffer(-1.0).contains(word), "the word hangs over the top's edge"
    assert diamond.buffer(K.RELIEF[1] / 2 + 1.0).disjoint(word), "the word fouls the diamond"
    return body - art + K.extrude(word, H - 0.01, H + WORD_H), scale


def main():
    ins, scale = build()
    word = word_outline()
    k = K.make()
    half = k.p(K.HALF)
    docked = ins.translate((0, 0, M.FLOOR_Z))
    print("Placeholder insert: x dock %.3f mm3, x left half %.3f, x right half %.3f; top %.2f mm over the"
          " halves' top edges; diamond at %.0f %% scale; word %.0f x %.1f mm, %.1f mm proud" %
          ((docked ^ k.solid).volume(), (docked ^ half).volume(), (docked ^ half.mirror((1, 0, 0))).volume(),
           H + M.FLOOR_Z - M.SPINE_TOP, 100 * scale, word.bounds[2] - word.bounds[0], WORD_CAP, WORD_H))
    b = ins.bounding_box()
    print("  %.1f x %.1f x %.1f mm, %.1f cm3, genus %d" % (b[3] - b[0], b[4] - b[1], b[5] - b[2],
                                                           ins.volume() / 1000, ins.genus()))
    C.stl(ins, "case/insert.stl")
    shutil.copyfile("case/insert.stl", os.path.join(C.STLS, "insert.stl"))


if __name__ == "__main__":
    main()
