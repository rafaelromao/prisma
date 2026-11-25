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
        aperture = M.extrude(D.rect(D.WINDOW_W - .2, D.WINDOW_L - .2),
                             M.FLUSH + .1, D.H - .1)
        self.assertAlmostEqual((D.lid(False) ^ aperture).volume(), aperture.volume(), delta=1e-3)
        self.assertLess(abs((D.lid(True) ^ aperture).volume()), 1e-3)

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
