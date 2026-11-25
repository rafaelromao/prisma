"""Regression gates for the complete powered common-tray variants."""
import unittest

import dongle as D
import module_battery as MB
import module_shell as M
from trackball import trackball as B


class DongleTest(unittest.TestCase):
    def test_both_variants_and_battery_lengths(self):
        for oled in (False, True):
            for length in (MB.REFERENCE_LENGTH, MB.MAX_LENGTH):
                with self.subTest(oled=oled, length=length):
                    D.check(oled, length)
                    self.assertAlmostEqual(D.lid_print(oled).bounding_box()[2], 0)

    def test_tray_is_canonical_and_headless_has_no_display(self):
        a = D.tray()
        b = B.tray(B.place())
        self.assertLess(abs((a - b).volume()) + abs((b - a).volume()), 1e-3)
        self.assertNotIn("OLED", dict(D.parts(False)))
        self.assertIn("OLED", dict(D.parts(True)))
        aperture = M.extrude(D.rect(D.WINDOW_W - .2, D.WINDOW_L - .2, x=D.GLASS_X),
                             M.FLUSH + .1, D.H - .1)
        self.assertAlmostEqual((D.lid(False) ^ aperture).volume(), aperture.volume(), delta=1e-3)
        self.assertLess(abs((D.lid(True) ^ aperture).volume()), 1e-3)

    def test_oled_bears_on_pcb_ends_not_glass_and_has_a_cell_gap(self):
        lid = D.lid(True)
        display = D.display()
        glass_top = D.OLED_PCB_Z + D.GLASS_T
        self.assertGreaterEqual(D.H - glass_top, .25)
        glass_play = D.rect(D.GLASS_W + .3, D.GLASS_L + .3, x=D.GLASS_X)
        self.assertLess(abs((M.extrude(glass_play, D.OLED_PCB_Z, glass_top) ^ lid).volume()), 1e-3)
        for x in (-17.25, 17.25):
            land = M.extrude(D.rect(1.0, 8.0, x=x), D.OLED_PCB_Z + .02, M.FLUSH)
            self.assertLess(abs((land - lid).volume()), 1e-3)
        self.assertGreaterEqual(D.OLED_Z - D.cell().bounding_box()[5], .4)
        self.assertGreater(D.connector().bounding_box()[3], display.bounding_box()[3] + 2)

    def test_docked_usb_insert_and_remove(self):
        for oled in (False, True):
            with self.subTest(oled=oled):
                D.usb_insertion_clearance(oled)

    def test_lid_closure_and_reset_access(self):
        L = B.place()
        tray = D.tray()
        x, y = B.sensor_reset(L)
        reset = dict(D.parts(False))["reset"]
        pin = B.box3(x - .5, y - .5, -10, x + .5, y + .5, reset.bounding_box()[2] - .01)
        pivot = M.OUTLINE.bounds[3]
        for oled in (False, True):
            lid = D.lid(oled)
            self.assertLess(abs((pin ^ (tray + lid)).volume()), 1e-3)
            # The display moves with the lid; fixed electronics remain in the tray.
            moving = lid + (D.display() + D.connector() if oled else lid)
            fixed = tray
            for name, solid in D.parts(False):
                fixed += solid
            for tenth in range(0, 121, 5):
                tilted = moving.translate((0, -pivot, -M.FLUSH)).rotate(
                    (-tenth / 10, 0, 0)).translate((0, pivot, M.FLUSH))
                self.assertLess(abs((tilted ^ fixed).volume()), .05)

    def test_export_copies(self):
        for oled in (False, True):
            source, public = D.paths(oled)
            self.assertEqual(source.read_bytes(), public.read_bytes())


if __name__ == "__main__":
    unittest.main()
