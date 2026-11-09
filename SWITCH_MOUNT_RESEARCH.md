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
- Preserve 1.2 mm Choc / 1.5 mm MX local retaining thickness; nearby bosses or overhangs
  must not block clips. Check the complete PCB/plate stack, not plate thickness alone.
- Qualify the selected filament/profile on a representative mount before accepting a
  one-shot print. No material-specific hole or snap-retention qualification exists here yet.
