"""500 mAh bay and the independent-stand contact. Run: python3 -m unittest test_half_battery."""
import unittest
import math

from shapely.geometry import Polygon
from manifold3d import Manifold

import case as C
import stand_mount


class HalfBatteryTest(unittest.TestCase):
    def test_half_pilots_follow_the_tilted_screws_and_keep_the_floor(self):
        body = C.build()
        top = C.PCB_T + C.PLATE["gap"] + C.PLATE["thick"]
        tip = top - C.SCREW["length"]
        for x, y in C.D["mount_holes"]:
            # A core down the screw axis must be empty; thread interference is
            # deliberately excluded by using a radius slightly below the pilot.
            core = C.to_desk_solid(Manifold.cylinder(-tip + .1, C.PILOT_R - .03,
                                                     circular_segments=20).translate((x, y, tip)))
            self.assertLess(abs((core ^ body).volume()), 1e-3)
            X, Y, _ = C.to_desk(x, y, tip)
            skin = Manifold.cylinder(.2, .5, circular_segments=20).translate((X, Y, .2))
            self.assertLess(abs((skin - body).volume()), 1e-3)

    def test_larger_envelope_clears_case_and_all_board_parts(self):
        self.assertEqual(C.D["battery_capacity_mah"], 500)
        self.assertEqual(C.D["battery_nominal_size"], [20, 40, 7])
        self.assertEqual(C.D["battery_size"], [20.5, 41, 7.5])
        battery = C.battery()
        self.assertLess(abs((battery ^ C.build()).volume()), 1e-3)
        for name, polygon, height in C.part_footprints():
            part = C.to_desk_solid(C.slab(polygon, -height, 0))
            self.assertLess(abs((battery ^ part).volume()), 1e-3, name)
        pcb = C.to_desk_solid(C.slab(Polygon(C.D["pcb_outline"]), 0, C.PCB_T))
        self.assertLess(abs((battery ^ pcb).volume()), 1e-3)

    def test_platform_mount_clears_feet_on_both_halves(self):
        self.assertEqual(len(C.D["magnets_floor"]), 7)
        self.assertEqual(len(C.D["magnets_side_y"]), 6)
        self.assertEqual(C.D["magnet_nominal_size"], [8, 1.5])
        stand_mount.check()

    def test_steel_platform_does_not_rest_on_any_foot(self):
        mount = C.D["stand_mount"]
        centre = C.plan([mount["centre"]])[0]
        for slot in C.D["pads"]["slots"]:
            for foot in C.plan(slot):
                clearance = math.dist(foot, centre) - C.D["pads"]["size"][0] / 2 - mount["contact_diameter"] / 2
                self.assertGreaterEqual(clearance, 11.5)

    def test_side_magnets_span_wall_at_equal_pitch(self):
        ys = C.D["magnets_side_y"]
        self.assertEqual(len(ys), 6)
        for a, b in zip(ys, ys[1:]):
            self.assertAlmostEqual(b - a, 17.8)
        self.assertAlmostEqual(ys[0], -24.8)
        self.assertAlmostEqual(ys[-1], 64.2)


if __name__ == "__main__":
    unittest.main()
