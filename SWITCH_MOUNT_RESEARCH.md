# Switch mounting dimensions

Checked online against manufacturer-authored drawings, 2026-11-09. Distributor-hosted
copies below are the original manufacturer's documents, not distributor dimension summaries.

## Kailh Choc v1 / PG1350

Source: Kaihua **CPG135001D01** mechanical drawing, sheet 1, revision A0 (2017-03-31),
in the [manufacturer datasheet hosted by Adafruit](https://cdn-shop.adafruit.com/product-files/5113/CHOC+keyswitch_Kailh-CPG135001D01_C400229.pdf).
The drawing specifies a **13.80 mm lower housing**, **15.00 mm flange**, **2.20 mm
PCB-to-flange stack**, and a **1.30 mm clip-related axial dimension** in the side view.
The latter must not be mistaken for the PCB thickness or total below-flange height.
This sheet does not provide a separately toleranced plate-cutout manufacturing drawing;
13.8 mm is a housing dimension, not evidence of a guaranteed snap fit in any 14 mm opening.

Prisma uses a 1.2 mm retaining plate with its underside 1.0 mm above the PCB: total
2.2 mm, matching the drawing's stack. The 14.0 mm CAD aperture is 13.8 mm plus
0.1 mm per side of **provisional printed-hole allowance**. Actual printed holes, switch
variation, corner buildup and latch engagement must be checked with real switches.

Confirmed defect: Choc trackball/trackpad lids reused the MX 14.2 mm opening, whereas
the half plates used 14.0 mm. They now use the half plate's shared Choc allowance.
Do not extend these results to Choc v2, mini Choc or other low-profile families.

## Choc v1 latches and the pull grooves

Added 2026-11-24, from the same Kaihua CPG135001D01 drawing, read at 400 dpi (side, top and bottom
views). The drawing gives its dimensions no tolerance of their own; its title block applies
**±0.20 mm** from 10 to 30 mm and **±0.10 mm** up to 5 mm.

| What | Drawing | General tolerance |
|---|---|---|
| Lower housing | 13.80 square | ±0.20 |
| Flange | 15.00 square, 0.80 thick | ±0.20 / ±0.10 |
| Flange underside to the housing's seating face (the PCB's top) | 2.20 | ±0.10 |
| Flange underside to the latches' catch faces | 1.30 | ±0.10 |
| Latch tip to latch tip | 14.50 | ±0.20 |

The four latch barbs sit two to an edge, on the two edges at the ends of the peg axis (the
footprint's local x axis, in both the halves' footprint and the modules' merged MX/Choc one). Each
is about 3.5 mm wide, centred about 3.55 mm either side of the centreline, with about 3.5 mm
between the pair: scaled off the drawing, not dimensioned. Their catch faces are flat on the flange
side, so a pull on the keycap does not release them; the plate's lip would have to bend.

What follows for the printed plates and lids:

- **Stack:** plate top to PCB top is 2.20 ±0.10 mm. Prisma's 1.2 mm lip over a 1.0 mm gap is exactly
  that, in the halves, the Choc trackball lid and the trackpad lid (checked on the exported STLs).
- **Lip thickness:** the latch slot is 1.30 ±0.10 mm, so 1.2 mm is the thickest lip guaranteed to
  clear the latches. Measure the printed lip; do not go thicker.
- **Latch bearing:** (14.50 − opening) / 2 per side: 0.25 mm at the 14.0 mm opening, 0.35 mm at
  13.8 mm. Over the drawing's tolerance and an assumed ±0.1 mm printed opening, about 0.10 to
  0.40 mm. Whether that holds a switch against a keycap pull depends on the lip's stiffness in the
  chosen material and on the socket's grip; nothing here tests it.

### Pull grooves

Choc has no side indents for a puller to grip. The ZSA Voyager's top plate has small grooves at the
edges of its switch openings for the tweezers of its key puller
([change it yourself](https://www.zsa.io/voyager/change-it-yourself), [teardown](https://www.zsa.io/voyager/teardown):
"insert the tweezers under the switch, aligning with the grooves"). ZSA publishes no plate CAD or groove
dimensions; only its text and one render were used, and its page notes that a whole switch can still
come out with the keycap.

Prisma's Choc plates and lids (the halves' plates, the Choc trackball lid, the trackpad lid; not the MX
lid) carry two grooves per switch, built by `switch_mount.py`:

- **Where:** the latch edges, centred in the 3.5 mm gap between the two latches. The edges between
  them are not used: the halves have only 3.0 mm of plate between rows (17 mm pitch), and two grooves
  there would leave 0.6 mm.
- **Size:** 4.2 mm wide, cut 1.2 mm past the opening (8.2 mm from the centre, against the flange's
  edge at 7.5 mm), through the lip. The plate's underside is open there: nothing sits under a groove.
- **Why:** sized for the owner's puller, measured with calipers: U-shaped spring tweezers whose tips
  are flat steel blades 3.72 mm wide and 0.19 mm thick, hooked inward, about 28 mm apart at rest.
  The width is the blade plus 0.25 mm each side for the printed edge.
- **Cost:** a 4.2 mm groove takes about 0.3 mm (9%) off the inner end of each latch's 3.5 mm bearing.
- **Plate left (CAD):** in the halves at least 2.8 mm to the next opening, 1.6 mm to the next groove and
  1.5 mm to the plate's edge; in the modules 2.65 mm between the two keys' facing grooves.

### Reference designs read (nothing copied)

- A community printed Choc plate with hot-swap sockets, supplied by the owner (source not recorded):
  1.2 mm lip, 13.8 mm square opening, and under the lip a pocket 14.50 mm wide along the latch axis
  and about 1.0 mm tall; seat to top 2.20 mm. It agrees with the drawing above.
- Corne Mini Choc Case by Nate Cox (CC BY 4.0): 14.000 mm openings through a 1.0 mm layer over a
  15.80 mm pocket 1.2 mm deep, 2.2 mm in all. No grooves.
- Open Choc plates read on GitHub (LambBT, temper) use plain 13.8 mm openings.

## Standard MX, not MX Low Profile

Source: Cherry **MX Series** manufacturer catalogue, printed pages 10-2/10-3,
[copy hosted by SparkFun](https://cdn.sparkfun.com/datasheets/Components/Switches/MX%20Series.pdf).
The standard desktop switch drawing gives a **5.0 mm PCB-to-flange stack** and
15.6 mm outer flange envelope. Its frame-mount diagram specifies 0.197 +0.012 inch
PCB-to-frame top spacing (approximately 5.004 +0.305 mm). Prisma's 5.0 mm nominal
stack agrees with the rounded metric switch dimension.

Prisma retains a 1.5 mm MX plate and 14.2 mm CAD opening (14.0 nominal plus 0.2 mm
total provisional FDM compensation). The retrieved catalogue does **not** establish
an independently toleranced 14.2 mm cutout or certify clip retention in that opening.
Neither CAD compensation nor this research should be presented as a manufacturer
tolerance. Confirm the exact purchased MX-compatible switch's mounting drawing and
measure printed latch engagement before production; clones can differ.

Current first-party product/download entry:
[Cherry MX2A Black downloads](https://www.cherry.de/en-us/product/mx2a-black/downloads).
This is a separate product revision; do not silently substitute its dimensions for all MX clones.

## Acceptance before printing the complete set

- Measure the **finished** hole at the switch-body and latch planes, not only its STL bounds.
- Verify both clips engage under the retaining land and the flange sits flat, without force.
- Check removal with a switch puller: the switch must not lift the plate or hot-swap socket.
  With your own puller, both blades must drop into a groove, hook under the flange and lift the
  switch straight up; a pull on the keycap alone should leave a seated switch in place. Both are
  physical checks no CAD test covers; the groove width and reach are `GROOVE_W` and `GROOVE_REACH`
  in `switch_mount.py`.
- Preserve 1.2 mm Choc / 1.5 mm MX local retaining thickness; nearby bosses or overhangs
  must not block clips. Check the complete PCB/plate stack, not plate thickness alone.
- Qualify the selected filament/profile on a representative mount before accepting a
  one-shot print. No material-specific hole or snap-retention qualification exists here yet.
