"""Kailh Choc v1 (PG1350) mounting numbers and the pull grooves, shared by the halves' plate and the
Choc module lids (trackball, trackpad). Sources and the reading of the drawing: SWITCH_MOUNT_RESEARCH.md.

A Choc v1 is held in its plate by four latch barbs, two on each of two opposite edges: the ends of
the peg axis, which is the footprint's local x axis. They catch under the plate's lip, so a pull on
the keycap cannot lift the switch out unless it bends the lip or the barbs. Choc has no side indents
for a puller, so, as on the ZSA Voyager, the plate carries grooves: at the middle of each latch edge
(in the gap between its two latches) the opening is cut wider and out past the flange, and a
puller's hooked blades go down there, hook under the flange and lift the switch straight up.
"""
from manifold3d import CrossSection, JoinType, Manifold
from shapely import affinity
from shapely.geometry import box

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
GROOVE_W = 4.0  # 0.14 mm clearance per side of the measured blade
GROOVE_REACH = 1.2     # past the opening's edge: 8.2 mm from the centre, 0.7 mm past the flange
GROOVE_LAP = 0.5       # starts this far inside the opening, so the cut joins it cleanly


TOL_LONG, TOL_SHORT = 0.20, 0.10  # Drawing tolerances for lengths of 10–30 mm and up to 5 mm.
LATCH_Y = (1.8, 5.3)  # Latch extent along the edge, scaled from the drawing.
GROOVE_R = 0.25
PULL_BLADE_T = 0.19
HOOK_DROP = 1.9  # Estimated from a photo of the measured puller.
BLADE_OFF_WALL = 0.10
FLOOR_CLEAR = STACK - HOOK_DROP
CONTACT_X, CONTACT_Y = (-0.10, 0.60), (1.6, 5.4)
SUPPORT_X, SUPPORT_Y = (-0.10, 1.50), (1.4, 5.8)
PAD_MARGIN = 0.3


def groove_plans(centre, angle, half):
    """Return the two rounded pull grooves as polygons in the plate plane."""
    grooves = []
    for sign in (-1, 1):
        low, high = sorted((sign * (half - GROOVE_LAP), sign * (half + GROOVE_REACH)))
        groove = box(low, -GROOVE_W / 2, high, GROOVE_W / 2)
        groove = groove.buffer(-GROOVE_R).buffer(GROOVE_R, quad_segs=16)
        grooves.append(affinity.translate(affinity.rotate(groove, angle, origin=(0, 0)), *centre))
    return grooves


def pull_grooves(centre, angle, half, z0, z1):
    """The two pull grooves of one switch, as a solid to subtract from the plate or lid.

    centre: the switch's centre (x, y); angle: degrees, counter-clockwise in the frame the solid is
    built in, of the footprint's x axis (the peg and latch axis); half: half the opening's width
    (the groove starts there); z0..z1: the heights to cut between."""
    length = GROOVE_LAP + GROOVE_REACH
    section = CrossSection.square((length - 2 * GROOVE_R, GROOVE_W - 2 * GROOVE_R), center=True)
    section = section.offset(GROOVE_R, JoinType.Round, circular_segments=32)
    cell = section.extrude(z1 - z0).translate((0, 0, z0))
    out = Manifold()
    for sign in (-1, 1):
        out += cell.translate((sign * (half + (GROOVE_REACH - GROOVE_LAP) / 2), 0, 0))
    return out.rotate((0, 0, angle)).translate((centre[0], centre[1], 0))


def latch_zones(centre, angle, half, kind="contact"):
    """Return the four catch-face or supporting lip regions for one switch."""
    (x0, x1), (y0, y1) = (CONTACT_X, CONTACT_Y) if kind == "contact" else (SUPPORT_X, SUPPORT_Y)
    zones = []
    for side in (-1, 1):
        for end in (-1, 1):
            a, b = sorted((side * (half + x0), side * (half + x1)))
            c, d = sorted((end * y0, end * y1))
            zones.append(affinity.translate(affinity.rotate(box(a, c, b, d), angle, origin=(0, 0)), *centre))
    return zones


def puller_envelope(centre, angle, half, z_flange, z_high):
    """Model blade descent beside the flange and hook travel below it."""
    outer = half + GROOVE_REACH - BLADE_OFF_WALL
    out = Manifold()
    for sign in (-1, 1):
        for inner, z0, z1 in (
            (BODY / 2 + .05, z_flange - HOOK_DROP, z_flange),
            (FLANGE / 2 + .01, z_flange, z_high),
        ):
            a, b = sorted((sign * inner, sign * outer))
            out += Manifold.cube((b - a, PULL_BLADE, z1 - z0)).translate((a, -PULL_BLADE / 2, z0))
    return out.rotate((0, 0, angle)).translate((*centre, 0))


def tolerance_budget(opening=14.0, opening_err=0.10, lip=1.2, lip_err=0.10):
    """Return worst, nominal and best dimensions in mm using assumed print tolerances."""
    bearing = (LATCH_SPAN - opening) / 2
    bearing_err = (TOL_LONG + opening_err) / 2
    clearance = opening - BODY
    clearance_err = opening_err + TOL_LONG
    slack = LATCH_DROP - lip
    slack_err = TOL_SHORT + lip_err
    return {
        "bearing": (bearing - bearing_err, bearing, bearing + bearing_err),
        "clearance": (clearance - clearance_err, clearance, clearance + clearance_err),
        "slack": (slack - slack_err, slack, slack + slack_err),
        "stack": (STACK - TOL_SHORT, STACK, STACK + TOL_SHORT),
    }
