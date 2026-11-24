"""Kailh Choc v1 (PG1350) mounting numbers and the pull grooves, shared by the halves' plate and the
Choc module lids (trackball, trackpad). Sources and the reading of the drawing: SWITCH_MOUNT_RESEARCH.md.

A Choc v1 is held in its plate by four latch barbs, two on each of two opposite edges: the ends of
the peg axis, which is the footprint's local x axis. They catch under the plate's lip, so a pull on
the keycap cannot lift the switch out unless it bends the lip or the barbs. Choc has no side indents
for a puller, so, as on the ZSA Voyager, the plate carries grooves: at the middle of each latch edge
(in the 3.5 mm gap between its two latches) the opening is cut wider and out past the flange, and a
puller's hooked blades go down there, hook under the flange and lift the switch straight up.
"""
from manifold3d import Manifold

# Kailh drawing CPG135001D01, rev A0. Its title block gives +-0.20 mm to dimensions of 10 to 30 mm and
# +-0.10 mm to those of 5 mm or less.
BODY = 13.80           # lower housing, square
FLANGE = 15.00         # square
FLANGE_T = 0.80
STACK = 2.20           # flange underside to the seating face: plate top to PCB top
LATCH_DROP = 1.30      # flange underside to the barbs' catch faces: a plate lip over 1.2 mm may not latch
LATCH_SPAN = 14.50     # barb tip to barb tip, along the peg axis (so 0.35 mm proud of the body each side)

# The owner's puller: U-shaped spring tweezers whose tips are flat steel blades, 3.72 mm wide and
# 0.19 mm thick, with the end bent inward into a short hook (measured with calipers). The blade goes
# down beside the flange, so the groove reaches past the flange's edge (7.5 mm from the centre).
PULL_BLADE = 3.72
GROOVE_W = 4.2         # the blade plus 0.25 mm each side for the printed edge
GROOVE_REACH = 1.2     # past the opening's edge: 8.2 mm from the centre, 0.7 mm past the flange
GROOVE_LAP = 0.5       # starts this far inside the opening, so the cut joins it cleanly


def pull_grooves(centre, angle, half, z0, z1):
    """The two pull grooves of one switch, as a solid to subtract from the plate or lid.

    centre: the switch's centre (x, y); angle: degrees, counter-clockwise in the frame the solid is
    built in, of the footprint's x axis (the peg and latch axis); half: half the opening's width
    (the groove starts there); z0..z1: the heights to cut between."""
    out = Manifold()
    for s in (-1, 1):
        a, b = sorted((s * (half - GROOVE_LAP), s * (half + GROOVE_REACH)))
        out += Manifold.cube((b - a, GROOVE_W, z1 - z0)).translate((a, -GROOVE_W / 2, z0))
    return out.rotate((0, 0, angle)).translate((centre[0], centre[1], 0))
