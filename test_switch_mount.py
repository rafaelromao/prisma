"""The Choc switch mount: the drawing's numbers, and the pull grooves in the halves' plate.

The modules' grooves are checked in test_module_assembly.py. Run from the repository root.
"""
import unittest

from shapely import affinity
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

import case as C
import design as DZ
import switch_mount as SM


def square(centre, angle, size):
    return affinity.translate(affinity.rotate(box(-size / 2, -size / 2, size / 2, size / 2), angle, origin=(0, 0)), *centre)


def groove_plans(centre, angle, half):
    """The two grooves of a switch in plan, as switch_mount.pull_grooves cuts them."""
    out = []
    for s in (-1, 1):
        a, b = sorted((s * (half - SM.GROOVE_LAP), s * (half + SM.GROOVE_REACH)))
        out.append(affinity.translate(affinity.rotate(box(a, -SM.GROOVE_W / 2, b, SM.GROOVE_W / 2), angle, origin=(0, 0)),
                                      *centre))
    return out


class DrawingNumbersTest(unittest.TestCase):
    def test_the_plate_stack_is_the_drawings(self):
        plate = C.PLATE
        self.assertAlmostEqual(plate["gap"] + plate["thick"], SM.STACK)
        # 1.30 +-0.10 from the flange to the latches' catch faces: 1.2 mm is the thickest lip that clears them
        self.assertLessEqual(plate["thick"], SM.LATCH_DROP - .10 + 1e-9)
        self.assertAlmostEqual(plate["cut"], SM.BODY)

    def test_a_groove_takes_the_pullers_blade_and_reaches_past_the_flange(self):
        half = (C.PLATE["cut"] + 2 * C.PLATE["cut_tol"]) / 2
        self.assertGreaterEqual(SM.GROOVE_W, SM.PULL_BLADE + .4)
        self.assertGreaterEqual(half + SM.GROOVE_REACH, SM.FLANGE / 2 + .5)
        # The two latches on an edge are about 3.5 mm wide and 3.5 mm apart (scaled off the drawing), so each
        # starts about 1.75 mm from the centreline. A groove wider than the gap eats into them: allow 0.4 mm.
        self.assertLessEqual(SM.GROOVE_W / 2 - 1.75, .4)


class HalvesPlateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plate, cls.pillars = C.plate()
        cls.keys = DZ.layout_left()
        cls.half = (C.PLATE["cut"] + 2 * C.PLATE["cut_tol"]) / 2
        cls.openings = {n: square(*cls.keys[n], 2 * cls.half) for n in cls.keys}
        cls.grooves = {n: groove_plans(*cls.keys[n], cls.half) for n in cls.keys}

    def test_every_groove_is_cut_clear_through_the_lip(self):
        cs = self.plate.slice(C.PLATE["thick"] / 2)
        rings = [Polygon(p) for p in cs.to_polygons()]
        for n, (centre, angle) in self.keys.items():
            for s in (-1, 1):
                mid = affinity.translate(affinity.rotate(Point(s * (self.half + SM.GROOVE_REACH / 2), 0), angle,
                                                         origin=(0, 0)), *centre)
                with self.subTest(key=n, side=s):
                    self.assertEqual(sum(r.contains(mid) for r in rings) % 2, 0, "groove not cut")

    def test_grooves_leave_the_plate_its_webs(self):
        outline = Polygon(C.D["plate_outline"])
        bosses = unary_union([Point(h).buffer(C.SCREW["boss_d"] / 2) for h in C.D["mount_holes"]])
        reset = C.reset_pocket_plan()
        pillars = unary_union([Point(p).buffer(1.4) for p in self.pillars])
        for n in self.keys:
            others_open = unary_union([o for m, o in self.openings.items() if m != n])
            others_groove = unary_union([g for m, gs in self.grooves.items() if m != n for g in gs])
            for i, g in enumerate(self.grooves[n]):
                with self.subTest(key=n, side=i):
                    self.assertGreaterEqual(g.distance(others_open), 2.5)
                    self.assertGreaterEqual(g.distance(others_groove), 1.5)
                    self.assertGreaterEqual(g.distance(outline.exterior), 1.5)
                    self.assertGreaterEqual(g.distance(bosses), 1.0)
                    self.assertGreaterEqual(g.distance(pillars), 1.0)
                    self.assertGreaterEqual(g.distance(reset), 3.0)

    def test_the_lip_around_a_switch_is_still_closed(self):
        # The grooves are on the latch edges only: the other two edges of every opening are untouched.
        cs = self.plate.slice(C.PLATE["thick"] / 2)
        rings = [Polygon(p) for p in cs.to_polygons()]
        for n, (centre, angle) in self.keys.items():
            for s in (-1, 1):
                edge = affinity.translate(affinity.rotate(Point(0, s * (self.half + .3)), angle, origin=(0, 0)), *centre)
                with self.subTest(key=n, side=s):
                    self.assertEqual(sum(r.contains(edge) for r in rings) % 2, 1, "plate missing beside a pin edge")


if __name__ == "__main__":
    unittest.main()
