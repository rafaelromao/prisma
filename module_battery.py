"""Removable long-cell reservation for the existing drawer tray (issue #3).

The pointing modules retain their original low 250 mAh cradle. A future
dongle can use a dielectric sheet and removable spacers above the cradle
and reset-only sensor PCB, with the shorter XIAO on its existing mount.
No board-defining coordinates or printed tray geometry are changed.

All dimensions are CAD envelopes, not a qualification of a particular pack.
"""
from trackball import trackball as B
import module_shell as M

# Reference 40 mm pack plus 1 mm; 45 mm is the reserved overall longitudinal
# envelope, including protection/tabs. The actual selected pack must be measured.
REFERENCE_LENGTH = 41.0
MAX_LENGTH = 45.0
MAX_WIDTH = 20.4
MAX_THICKNESS = 8.0
REAR = -42.5
SHEET_WIDTH = 20.0
SHEET_T = .5
SHEET_Z = 9.6
CELL_Z = SHEET_Z + SHEET_T
LEAD_REAR = -39.8


def long_cell(length=REFERENCE_LENGTH, width=MAX_WIDTH, thickness=MAX_THICKNESS):
    """Rear-aligned protected-pack envelope (tabs included, leads exit rear)."""
    if not (B.BAT[1] < length <= MAX_LENGTH and
            0 < width <= MAX_WIDTH and 0 < thickness <= MAX_THICKNESS):
        raise ValueError("pack exceeds reserved drawer envelope")
    return B.box3(-width / 2, REAR - length, CELL_Z,
                  width / 2, REAR, CELL_Z + thickness)


def carrier():
    """Dielectric sheet and three removable dielectric support blocks.

    The rear block sits on the original battery seat. The two forward
    blocks rest on component-free areas of the reset-only sensor PCB.
    Dimensions include adhesive; use rigid insulation, not a compression
    fit against the pouch. Round/deburr all edges.
    """
    sheet = B.box3(-SHEET_WIDTH / 2, REAR - MAX_LENGTH, SHEET_Z,
                   SHEET_WIDTH / 2, REAR, CELL_Z)
    board_top = B.PLATE_TOP + B.SENSOR_BELOW + B.PCB_T
    rear = B.box3(-4, -52, B.BAT_Z, 4, -46, SHEET_Z)
    middle = B.box3(-3, -74, board_top, 3, -71, SHEET_Z)
    front = B.box3(-3, -85, board_top, 3, -83, SHEET_Z)
    return sheet + rear + middle + front


def lead_exit():
    """Local protected lead-exit reservation; final routing belongs to #6."""
    return B.box3(-3, REAR, CELL_Z, 3, LEAD_REAR, CELL_Z + 3)


def interface_lid():
    """Closed, standard-height lid fixture, not a deliverable variant.

    Exercises the existing rim, four screws and rear hooks without keys,
    optics or electronics. The final passive/powered lids belong to #5/#6.
    """
    return M.lid_holes(M.bevel(M.lid_blank(M.CHOC_TOP, 1.2), M.CHOC_TOP), M.CHOC_TOP)
