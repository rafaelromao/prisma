"""Reload the actual binary STL format: no importer repair or topology assumptions."""
from pathlib import Path
import tempfile
import unittest

import numpy as np

import case as C
import dock
import insert
import dongle as D
from trackball import trackball as B
from trackpad import trackpad as T


class StlExportTest(unittest.TestCase):
    def test_canonical_tray_has_only_one_public_copy(self):
        source = Path("case/module_tray.stl")
        public = Path("stls/module_tray.stl")
        self.assertEqual(source.read_bytes(), public.read_bytes())
        self.assertEqual(sorted(Path("stls").glob("*tray*.stl")), [public])
        for folder in (Path("trackball/case"), Path("trackpad/case")):
            self.assertEqual(list(folder.glob("*tray*.stl")), [])

    def test_placeholder_lid_public_copy(self):
        self.assertEqual(insert.SOURCE.read_bytes(), insert.PUBLIC.read_bytes())
        self.assertFalse(Path("case/insert.stl").exists())
        self.assertFalse(Path("stls/insert.stl").exists())

    def test_all_printable_variants_survive_binary_stl_quantization(self):
        half = C.real(C.build())
        plate = C.real(C.plate()[0]).mirror((0, 0, 1)).translate((0, 0, C.PLATE["thick"]))
        solids = {"left": half, "right": C.mirrored(half), "plate_left": plate,
                  "plate_right": plate.mirror((1, 0, 0)), "dock": dock.make().solid,
                  "cover": insert.lid_print()}
        layout = B.place()
        solids["tray"] = B.tray(layout).translate((0, 0, -B.M.FEET))
        solids["trackball_cover"] = B.cover(layout).translate((0, 0, -B.M.CHOC_TOP))
        for name, lid, height in (("choc", B.lid(layout), B.M.CHOC_TOP), ("trackpad", T.lid(T.place()), T.H)):
            solids[name] = lid.mirror((0, 0, 1)).translate((0, 0, height))
        solids["trackpad_retainer"] = T.retainer_print()
        for oled in (False, True):
            solids[D.NAMES[oled]] = D.lid_print(oled)
        record = np.dtype([("normal", "<f4", 3), ("vertices", "<f4", (3, 3)), ("attribute", "<u2")])
        published = {"left": "case/case_left.stl", "right": "case/case_right.stl",
                     "plate_left": "case/plate_left.stl", "plate_right": "case/plate_right.stl",
                     "dock": "case/dock.stl", "cover": "case/placeholder_lid.stl",
                     "tray": "case/module_tray.stl", "trackball_cover": "trackball/case/cover.stl",
                     "choc": "trackball/case/lid_choc.stl", "trackpad": "trackpad/case/lid.stl",
                     "trackpad_retainer": "trackpad/case/retainer.stl"}
        for oled in (False, True):
            published[D.NAMES[oled]] = str(D.paths(oled)[0])
        with tempfile.TemporaryDirectory(dir="/tmp/opencode", prefix="prisma-stl-test-") as folder:
            for name, solid in solids.items():
                with self.subTest(variant=name):
                    path = Path(folder) / (name + ".stl")
                    C.stl(solid, path)
                    data = path.read_bytes()
                    count = int.from_bytes(data[80:84], "little")
                    self.assertEqual(len(data), 84 + 50 * count)
                    triangles = np.frombuffer(data, dtype=record, offset=84)["vertices"].astype(float)
                    vertices, inverse = np.unique(triangles.reshape(-1, 3), axis=0, return_inverse=True)
                    faces = inverse.reshape(-1, 3)
                    area = np.linalg.norm(np.cross(triangles[:, 1] - triangles[:, 0],
                                                   triangles[:, 2] - triangles[:, 0]), axis=1) / 2
                    self.assertTrue(np.all(area >= 1e-10), "degenerate STL faces")
                    directed = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
                    _, edge_ids, incidence = np.unique(np.sort(directed, axis=1), axis=0,
                                                       return_inverse=True, return_counts=True)
                    self.assertTrue(np.all(incidence == 2), "non-manifold welded STL edges")
                    directions = np.where(directed[:, 0] < directed[:, 1], 1, -1)
                    self.assertTrue(np.all(np.bincount(edge_ids, weights=directions) == 0), "inconsistent winding")
                    signed_volume = np.einsum("ij,ij->i", triangles[:, 0],
                                               np.cross(triangles[:, 1], triangles[:, 2])).sum() / 6
                    self.assertAlmostEqual(signed_volume, solid.volume(), delta=0.05)
                    # Compare the regenerated quantized vertices, not just volume:
                    # relocated holes can preserve volume. Avoid near-coincident 3D
                    # booleans, which are unnecessarily expensive on a full dock.
                    generated_vertices = vertices
                    data = Path(published[name]).read_bytes()
                    triangles = np.frombuffer(data, dtype=record, offset=84)["vertices"]
                    vertices = np.unique(triangles.reshape(-1, 3), axis=0)
                    np.testing.assert_allclose(vertices, generated_vertices, rtol=0, atol=1e-4,
                                               err_msg="published STL differs from current CAD")


if __name__ == "__main__":
    unittest.main()
