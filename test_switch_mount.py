"""Volumetric checks for Choc pull grooves, latch support and puller clearance."""

from pathlib import Path
import unittest

import numpy as np
from manifold3d import CrossSection, FillRule, Manifold, Mesh
from shapely import affinity
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

import case as C
import design as DZ
import switch_mount as SM


def square(centre, angle, size):
    return affinity.translate(affinity.rotate(box(-size / 2, -size / 2, size / 2, size / 2), angle, origin=(0, 0)), *centre)


def prism(poly, z0, z1):
    """Extrude the polygon and preserve any holes."""
    rings = []
    for part in getattr(poly, "geoms", [poly]):
        if not part.is_empty:
            rings.append(list(part.exterior.coords)[:-1])
            rings.extend(list(ring.coords)[:-1] for ring in part.interiors)
    if not rings:
        return Manifold()
    return CrossSection(rings, FillRule.EvenOdd).extrude(z1 - z0).translate((0, 0, z0))


def stl_solid(path):
    data = Path(path).read_bytes()
    record = np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")])
    triangles = np.frombuffer(data, dtype=record, offset=84)["vertices"].astype(float).reshape(-1, 3)
    vertices, inverse = np.unique(np.round(triangles, 5), axis=0, return_inverse=True)
    solid = Manifold(Mesh(vertices.astype(np.float32), inverse.reshape(-1, 3).astype(np.uint32)))
    if solid.is_empty():
        raise ValueError(f"Unusable STL mesh: {path}")
    return solid


def hit(a, b):
    return abs((a ^ b).volume())


class DrawingNumbersTest(unittest.TestCase):
    def test_the_plate_stack_is_the_drawings(self):
        plate = C.PLATE
        self.assertAlmostEqual(plate["gap"] + plate["thick"], SM.STACK)
        # 1.30 +-0.10 from the flange to the latches' catch faces: 1.2 mm is the thickest lip that clears them
        self.assertLessEqual(plate["thick"], SM.LATCH_DROP - SM.TOL_SHORT + 1e-9)
        self.assertAlmostEqual(plate["cut"], SM.BODY)

    def test_a_groove_takes_the_pullers_blade_and_reaches_past_the_flange(self):
        half = (C.PLATE["cut"] + 2 * C.PLATE["cut_tol"]) / 2
        self.assertGreaterEqual(SM.GROOVE_W, SM.PULL_BLADE + .2)
        self.assertGreaterEqual(half + SM.GROOVE_REACH, SM.FLANGE / 2 + .5)
        self.assertGreater(SM.GROOVE_R, 0)
        self.assertLessEqual(SM.GROOVE_R, SM.GROOVE_LAP)
        self.assertGreaterEqual(SM.FLOOR_CLEAR, .25)
        bite = SM.GROOVE_W / 2 - SM.LATCH_Y[0]
        self.assertLessEqual(bite, .3)
        self.assertLessEqual(bite / (SM.LATCH_Y[1] - SM.LATCH_Y[0]), .09)

    def test_tolerance_budget(self):
        expected = {"bearing": (.10, .25, .40), "clearance": (-.10, .20, .50),
                    "slack": (-.10, .10, .30), "stack": (2.10, 2.20, 2.30)}
        for quantity, values in SM.tolerance_budget().items():
            for actual, target in zip(values, expected[quantity], strict=True):
                self.assertAlmostEqual(actual, target, msg=quantity)
        self.assertAlmostEqual(SM.tolerance_budget(opening=13.8)["clearance"][1], 0)


class HalvesPlateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plate, cls.pillars = C.plate()
        cls.keys = DZ.layout_left()
        cls.half = (C.PLATE["cut"] + 2 * C.PLATE["cut_tol"]) / 2
        cls.openings = {n: square(*cls.keys[n], 2 * cls.half) for n in cls.keys}
        cls.t, cls.gap = C.PLATE["thick"], C.PLATE["gap"]
        cls.pads = C.module_pads()
        cls.grooves = {n: SM.groove_plans(*cls.keys[n], cls.half) for n in cls.keys}

    def test_every_groove_is_clear_through_the_whole_plate(self):
        for key, grooves in self.grooves.items():
            for index, groove in enumerate(grooves):
                probe = prism(groove.buffer(-.02), -self.gap + .01, self.t + 1)
                with self.subTest(key=key, groove=index):
                    self.assertLess(hit(probe, self.plate), 1e-3)

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

    def test_the_other_two_edges_are_solid(self):
        for key, (centre, angle) in self.keys.items():
            for sign in (-1, 1):
                strip = box(-2, sign * (self.half + .05), 2, sign * (self.half + .5))
                strip = affinity.translate(affinity.rotate(strip, angle, origin=(0, 0)), *centre)
                probe = prism(strip, .6, self.t - .05)
                with self.subTest(key=key, side=sign):
                    self.assertAlmostEqual(hit(probe, self.plate), probe.volume(), delta=1e-3)

    def lip_regions(self, kind):
        outline = Polygon(C.D["plate_outline"]).buffer(-C.PLATE["chamfer"] - .1)
        heads = [Point(h).buffer(C.SCREW["head_d"] / 2 + .1) for h in C.D["mount_holes"]]
        away = unary_union(list(self.openings.values()) + [g for gs in self.grooves.values() for g in gs]
                           + heads + [p.buffer(SM.PAD_MARGIN) for p in self.pads])
        for key, (centre, angle) in self.keys.items():
            for index, zone in enumerate(SM.latch_zones(centre, angle, self.half, kind)):
                region = zone.intersection(outline).difference(away)
                if region.area > 1e-6:
                    yield key, index, region

    def test_every_latch_keeps_the_full_lip_under_it(self):
        for kind in ("contact", "support"):
            regions = list(self.lip_regions(kind))
            self.assertGreaterEqual(len(regions), 45)
            for key, index, region in regions:
                probe = prism(region.buffer(-.01), .02, self.t - .02)
                with self.subTest(kind=kind, key=key, latch=index):
                    self.assertAlmostEqual(hit(probe, self.plate), probe.volume(), delta=1e-3)

    def test_the_pocket_covers_the_pads_and_margin(self):
        pocket = C.blob_pocket_plan()
        zone = Polygon(C.D["blob_zone"])
        for pad in self.pads:
            with self.subTest(pad=pad.centroid.wkt):
                self.assertAlmostEqual(pad.intersection(zone).difference(pocket).area, 0, delta=1e-6)
                self.assertAlmostEqual(C.carved_lip().intersection(pad.buffer(SM.PAD_MARGIN)).area, 0, delta=1e-6)

    def test_only_two_latches_reach_the_solder_pocket(self):
        zone = Polygon(C.D["blob_zone"])
        reaching = [(key, index) for key, (centre, angle) in self.keys.items()
                    for index, contact in enumerate(SM.latch_zones(centre, angle, self.half))
                    if contact.intersects(zone)]
        self.assertEqual({key for key, _ in reaching}, {"middle_bottom", "ring_bottom"})
        self.assertEqual(len(reaching), 2)

    def test_the_puller_envelope_clears_the_plate_and_solder(self):
        blob = prism(C.solder_blob_plan(), -self.gap, -self.gap + 1.4)
        reset = prism(C.reset_pocket_plan().buffer(2.0), -self.gap, self.t)
        for key, (centre, angle) in self.keys.items():
            envelope = SM.puller_envelope(centre, angle, self.half, self.t, self.t + 8)
            with self.subTest(key=key):
                for obstacle in (self.plate, blob, reset):
                    self.assertLess(hit(envelope, obstacle), 1e-3)

    def test_exported_plates_have_the_grooves_and_lip(self):
        def print_orientation(probe, side):
            probe = C.real(probe).mirror((0, 0, 1)).translate((0, 0, self.t))
            return probe.mirror((1, 0, 0)) if side == "right" else probe

        for side in ("left", "right"):
            solid = stl_solid(f"case/plate_{side}.stl")
            for key, grooves in self.grooves.items():
                for index, groove in enumerate(grooves):
                    probe = prism(groove.buffer(-.02), -self.gap + .01, self.t + 1)
                    with self.subTest(plate=side, key=key, groove=index):
                        self.assertLess(hit(print_orientation(probe, side), solid), 1e-2)
            for key, index, region in self.lip_regions("support"):
                probe = prism(region.buffer(-.01), .02, self.t - .02)
                with self.subTest(plate=side, key=key, latch=index):
                    self.assertAlmostEqual(hit(print_orientation(probe, side), solid), probe.volume(), delta=1e-2)


if __name__ == "__main__":
    unittest.main()
