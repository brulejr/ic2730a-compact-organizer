#!/usr/bin/env python3
"""
Appendix: 1:1 scale cut-out drilling templates.

Page order is padded so that every template page has a guaranteed BLANK
reverse when the combined document is duplex-printed. The main build plan
is 6 pages (even), so page 6 is already a back page (paired with page 5 as
its front) -- the appendix starts immediately on page 7, a fresh sheet
front, with no leading blank needed. From there it alternates content/blank:

  7  instructions + calibration ruler
  8  blank   (back of 7)
  9  SO-239 template
  10 blank   (back of 9)
  11 TRRS template
  12 blank   (back of 11)
  13 Fan (NF-A4x20) template
  14 blank   (back of 13)
  15 Vent template
  16 blank   (back of 15)
  17 RJ11/12 console bulkhead template
  18 blank   (back of 17)
  19 PowerPole flush panel mount template
  20 blank   (back of 19)
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

import os
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "_build")
os.makedirs(BUILD_DIR, exist_ok=True)
OUT = os.path.join(BUILD_DIR, "appendix.pdf")
MM = 72.0 / 25.4  # points per millimeter

PW, PH = letter
CX, CY = PW / 2.0, PH / 2.0 + 30  # shape center, nudged up to leave room for label

NAVY = colors.HexColor("#1F3040")
SLATE = colors.HexColor("#5B6B79")
INK = colors.HexColor("#232323")
RULE = colors.HexColor("#C7CDD2")

c = canvas.Canvas(OUT, pagesize=letter)


def header(title):
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.65 * 72, PH - 0.55 * 72, "IC-2730A Compact Organizer \u2014 Drilling Template")
    c.setFillColor(SLATE)
    c.setFont("Helvetica", 8.5)
    c.drawRightString(PW - 0.65 * 72, PH - 0.55 * 72, title)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.75)
    c.line(0.65 * 72, PH - 0.62 * 72, PW - 0.65 * 72, PH - 0.62 * 72)


def blank_page(note="This page is intentionally blank \u2014 keeps the template on the reverse side intact if you print duplex."):
    c.setFillColor(colors.HexColor("#AEB6BC"))
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(CX, 0.6 * 72, note)
    c.showPage()


def scale_note():
    c.setFillColor(colors.HexColor("#B33A3A"))
    c.setFont("Helvetica-BoldOblique", 8.5)
    c.drawCentredString(CX, PH - 0.85 * 72,
                         "Print at 100% / Actual Size \u2014 disable \u201cFit to page\u201d or \u201cScale to fit\u201d")


def crosshair(x, y, half_len_mm, width=0.6):
    L = half_len_mm * MM
    c.setStrokeColor(INK)
    c.setLineWidth(width)
    c.setDash([])
    c.line(x - L, y, x + L, y)
    c.line(x, y - L, x, y + L)


def dashed_rect_centered(x, y, w_mm, h_mm):
    w, h = w_mm * MM, h_mm * MM
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.75)
    c.setDash([4, 3])
    c.rect(x - w / 2, y - h / 2, w, h, stroke=1, fill=0)
    c.setDash([])


def solid_rect_centered(x, y, w_mm, h_mm, color=INK, width=1.1):
    w, h = w_mm * MM, h_mm * MM
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.rect(x - w / 2, y - h / 2, w, h, stroke=1, fill=0)


def solid_roundrect_centered(x, y, w_mm, h_mm, r_mm, color=INK, width=1.1, dashed=False):
    w, h = w_mm * MM, h_mm * MM
    c.setStrokeColor(color)
    c.setLineWidth(width)
    if dashed:
        c.setDash([1, 2])
    c.roundRect(x - w / 2, y - h / 2, w, h, r_mm * MM, stroke=1, fill=0)
    c.setDash([])


def dim_line(x1, x2, y, label):
    c.setStrokeColor(INK)
    c.setLineWidth(0.6)
    c.setDash([])
    c.line(x1, y, x2, y)
    tick = 3
    c.line(x1, y - tick, x1, y + tick)
    c.line(x2, y - tick, x2, y + tick)
    c.setFillColor(INK)
    c.setFont("Helvetica", 8)
    c.drawCentredString((x1 + x2) / 2, y - 11, label)


def dashed_circle_centered(x, y, dia_mm):
    r = (dia_mm * MM) / 2
    c.setStrokeColor(SLATE)
    c.setLineWidth(0.75)
    c.setDash([4, 3])
    c.circle(x, y, r, stroke=1, fill=0)
    c.setDash([])


def solid_circle_centered(x, y, dia_mm, color=INK, width=1.1):
    r = (dia_mm * MM) / 2
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.circle(x, y, r, stroke=1, fill=0)


def diam_label(x, y, dia_mm, dy=-6):
    c.setFillColor(INK)
    c.setFont("Helvetica", 8)
    c.drawCentredString(x, y + dy * MM, f"\u00d8 {dia_mm} mm")


def flat_sided_circle(x, y, dia_mm, flat_width_mm, dashed=False, color=INK, width=1.1):
    """Draw a circle of dia_mm with one side flattened so the full width
    across that axis is flat_width_mm (a 'D' shape). Flat sits at the
    bottom of the shape."""
    import math
    r = dia_mm / 2.0
    flat_y = r - flat_width_mm  # distance below center to the flat line (negative = below)
    # half-chord at the flat line
    half_chord = math.sqrt(max(r * r - flat_y * flat_y, 0))
    ang1 = math.degrees(math.atan2(flat_y, half_chord))       # right-hand intersection
    ang2 = math.degrees(math.atan2(flat_y, -half_chord))      # left-hand intersection
    # sweep the MAJOR arc counterclockwise from ang1, the long way around, back to ang2
    start = ang1
    end = ang2 if ang2 > ang1 else ang2 + 360
    steps = 72
    pts = []
    for i in range(steps + 1):
        a = math.radians(start + (end - start) * i / steps)
        pts.append((x + r * MM * math.cos(a), y + r * MM * math.sin(a)))
    c.setStrokeColor(SLATE if dashed else color)
    c.setLineWidth(0.75 if dashed else width)
    c.setDash([4, 3] if dashed else [])
    path = c.beginPath()
    path.moveTo(pts[0][0], pts[0][1])
    for px, py in pts[1:]:
        path.lineTo(px, py)
    path.close()  # closes back to start via the flat chord
    c.drawPath(path, stroke=1, fill=0)
    c.setDash([])
    return flat_y  # mm offset (signed) of the flat line from center, for labeling


def cutline_note(y_bottom):
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawCentredString(CX, y_bottom, "cut along dashed line")


def caption(lines, y_top):
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawCentredString(CX, y_top, lines[0])
    c.setFillColor(INK)
    c.setFont("Helvetica", 8.5)
    y = y_top - 14
    last_y = y_top
    for ln in lines[1:]:
        c.drawCentredString(CX, y, ln)
        last_y = y
        y -= 11
    return last_y


def trim_rect(shape_half_w_mm, shape_half_h_mm, caption_lines, caption_top_y, caption_last_y):
    """Draw a rectangular trim card around the shape + caption, plus thin
    dotted guide lines extending to the page edges so a straight-blade
    paper cutter can be aligned to each edge in one pass."""
    cap_w = max(
        stringWidth(caption_lines[0], "Helvetica-Bold", 10.5),
        max((stringWidth(ln, "Helvetica", 8.5) for ln in caption_lines[1:]), default=0),
    )
    half_w = max(shape_half_w_mm * MM, cap_w / 2.0) + 10 * MM
    top = CY + shape_half_h_mm * MM + 12 * MM
    bottom = caption_last_y - 10
    left, right = CX - half_w, CX + half_w

    # card border -- solid, this is the actual trim line
    c.setStrokeColor(NAVY)
    c.setLineWidth(1)
    c.setDash([])
    c.rect(left, bottom, right - left, top - bottom, stroke=1, fill=0)

    # full-page alignment guides, thin dotted, for lining up a paper cutter
    c.setStrokeColor(colors.HexColor("#B7BEC4"))
    c.setLineWidth(0.5)
    c.setDash([1, 2])
    margin = 4
    c.line(margin, top, PW - margin, top)
    c.line(margin, bottom, PW - margin, bottom)
    c.line(left, margin, left, PH - margin)
    c.line(right, margin, right, PH - margin)
    c.setDash([])



# Main doc is now 6 pages (even), so page 6 is already a back page (paired with
# page 5 as its front) -- the appendix can start immediately on page 7, a fresh
# sheet front, with no protective blank needed first.

# ---------- page 7: instructions + calibration ruler ----------
header("Instructions")
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 15)
c.drawString(0.65 * 72, PH - 1.0 * 72, "Appendix \u2014 Drilling Templates")

c.setFillColor(INK)
c.setFont("Helvetica", 9.3)
body_lines = [
    "The six templates that follow (SO-239, TRRS, the fan mounting pattern, the intake vent, the",
    "RJ11/12 console bulkhead, and the PowerPole flush panel mount) are drawn at true 1:1 scale. Print",
    "this document at 100% / Actual Size \u2014 most print dialogs default to \u201cFit to page,\u201d which will",
    "rescale everything and make the holes the wrong size. Before cutting anything, measure the ruler",
    "below with a tape measure or ruler \u2014 it should read exactly 100 mm end to end. If it doesn\u2019t, your",
    "printer rescaled the page; reprint with scaling disabled.",
    "",
    "Cut each template out along its dashed line, position it on the case wall per the wall/row assignment",
    "in Section 2 (Parts & Hole Schedule), and hold it with a small piece of double-sided tape. Use the",
    "crosshair marks to center-punch before drilling \u2014 the crosshairs mark true center, not the tape.",
    "",
    "Each template also has a solid rectangular border (the trim card) with thin dotted lines extending to",
    "the page edges. Those dotted lines are alignment guides for a paper cutter \u2014 line the blade up with",
    "where a dotted line meets the edge of the sheet, cut, rotate the sheet, and repeat for all four sides",
    "to trim the rectangle out squarely. Then cut the finer dashed/round shape inside it by hand.",
    "",
    "Not templated yet: the master power switch (not chosen, and would need its own cutout).",
    "",
    "This appendix is padded with blank pages so every template's reverse side is blank \u2014 safe to print",
    "single-sided or duplex.",
]
y = PH - 1.25 * 72
for ln in body_lines:
    c.drawString(0.65 * 72, y, ln)
    y -= 13.2

# calibration ruler: 100mm, ticks every 10mm
ruler_y = PH - 6.6 * 72
ruler_x0 = CX - 50 * MM
ruler_x1 = CX + 50 * MM
c.setStrokeColor(INK)
c.setLineWidth(1.2)
c.line(ruler_x0, ruler_y, ruler_x1, ruler_y)
c.setFont("Helvetica", 7)
for i in range(0, 101, 10):
    xt = ruler_x0 + i * MM
    tick_h = 10 if i % 50 == 0 else 6
    c.setLineWidth(1.0 if i % 50 == 0 else 0.6)
    c.line(xt, ruler_y, xt, ruler_y + tick_h)
    c.drawCentredString(xt, ruler_y - 10, str(i))
c.setFillColor(SLATE)
c.setFont("Helvetica-Oblique", 8)
c.drawCentredString(CX, ruler_y - 26, "Calibration ruler \u2014 should measure exactly 100 mm")

c.showPage()

# ---------- page 8: blank ----------
blank_page()

# ---------- page 9: SO-239 template ----------
header("SO-239 \u2014 Antenna Bulkhead")
scale_note()
dashed_rect_centered(CX, CY, 35, 35)
solid_rect_centered(CX, CY, 25, 25)
solid_circle_centered(CX, CY, 16)
crosshair(CX, CY, 12)
diam_label(CX, CY, 16, dy=-11)
cutline_note(CY - 35 * MM / 2 - 16)
cap_top = CY - 35 * MM / 2 - 34
cap_lines = [
    "SO-239 Antenna Bulkhead",
    "16 mm center hole \u00b7 25 \u00d7 25 mm flange",
    "Right wall, back row",
]
last_y = caption(cap_lines, cap_top)
trim_rect(35 / 2, 35 / 2, cap_lines, cap_top, last_y)
c.showPage()

# ---------- page 10: blank ----------
blank_page()

# ---------- page 11: TRRS template ----------
header("TRRS \u2014 Speaker Bulkhead")
scale_note()
dashed_rect_centered(CX, CY, 32, 32)
solid_circle_centered(CX, CY, 22)
crosshair(CX, CY, 14)
diam_label(CX, CY, 22, dy=-14)
cutline_note(CY - 32 * MM / 2 - 16)
cap_top = CY - 32 * MM / 2 - 34
cap_lines = [
    "TRRS Speaker Bulkhead",
    "22 mm diameter hole",
    "Right wall, front row",
]
last_y = caption(cap_lines, cap_top)
trim_rect(32 / 2, 32 / 2, cap_lines, cap_top, last_y)
c.showPage()

# ---------- page 12: blank ----------
blank_page()

# ---------- page 13: Fan template ----------
header("Fan \u2014 Noctua NF-A4x20")
scale_note()
dashed_rect_centered(CX, CY, 50, 50)
solid_rect_centered(CX, CY, 40, 40, color=SLATE, width=0.9)
# 32x32mm hole spacing -> +/-16mm from center
offs = 16
pilot_dia = 3.2  # typical M3 fan screw clearance -- verify against actual hardware
for dx in (-offs, offs):
    for dy in (-offs, offs):
        x = CX + dx * MM
        y = CY + dy * MM
        solid_circle_centered(x, y, pilot_dia)
        crosshair(x, y, 4, width=0.5)
crosshair(CX, CY, 6, width=0.5)
c.setFillColor(INK)
c.setFont("Helvetica", 7.5)
c.drawCentredString(CX, CY + 21 * MM, "32 \u00d7 32 mm hole spacing")
caption_lines_fan = [
    "Fan Mounting \u2014 Noctua NF-A4x20 5V PWM",
    "40 \u00d7 40 mm frame \u00b7 32 \u00d7 32 mm hole spacing \u00b7 pilots shown at ~3.2 mm (typical M3 \u2014 verify)",
    "Right wall, center. Airflow opening not shown \u2014 pending vent/shroud sizing (Section 5).",
]
cap_top = CY - 50 * MM / 2 - 26
last_y = caption(caption_lines_fan, cap_top)
cutline_note(CY - 50 * MM / 2 - 12)
trim_rect(50 / 2, 50 / 2, caption_lines_fan, cap_top, last_y)
c.showPage()

# ---------- page 14: blank ----------
blank_page()

# ---------- page 15: Vent template (opposite wall from the fan) ----------
header("Vent \u2014 Left Wall Intake")
scale_note()
dashed_rect_centered(CX, CY, 50, 50)
solid_rect_centered(CX, CY, 40, 40, color=SLATE, width=0.9)
offs = 16
for dx in (-offs, offs):
    for dy in (-offs, offs):
        x = CX + dx * MM
        y = CY + dy * MM
        solid_circle_centered(x, y, 3.2)
        crosshair(x, y, 4, width=0.5)
crosshair(CX, CY, 6, width=0.5)
c.setFillColor(INK)
c.setFont("Helvetica", 7.5)
c.drawCentredString(CX, CY + 21 * MM, "32 \u00d7 32 mm hole spacing (matches fan)")
caption_lines_vent = [
    "Filtered Vent \u2014 Intake",
    "40 \u00d7 40 mm frame \u00b7 32 \u00d7 32 mm hole spacing \u2014 provisionally matched to the fan's own",
    "mounting footprint so one TPU shroud design can serve both. Confirm before finalizing \u2014 the",
    "actual open-air passage size still depends on your filter media and shroud design (Section 5).",
    "Left wall, center \u2014 directly opposite the fan.",
]
cap_top = CY - 50 * MM / 2 - 26
last_y = caption(caption_lines_vent, cap_top)
cutline_note(CY - 50 * MM / 2 - 12)
trim_rect(50 / 2, 50 / 2, caption_lines_vent, cap_top, last_y)
c.showPage()

# ---------- page 16: blank ----------
blank_page()

# ---------- page 17: RJ11/12 console bulkhead template ----------
header("Console \u2014 RJ11/12 Bulkhead")
scale_note()
dashed_rect_centered(CX, CY, 29, 29)  # cut-line margin
flat_y = flat_sided_circle(CX, CY, 21, 19)
crosshair(CX, CY, 13)
c.setFillColor(INK)
c.setFont("Helvetica", 8)
c.drawCentredString(CX, CY + 17 * MM, "\u00d8 21 mm round side")
c.drawCentredString(CX, CY + flat_y * MM - 17, "19 mm across the flat")
# small arrow pointing at the flat edge
c.setStrokeColor(INK)
c.setLineWidth(0.6)
c.line(CX, CY + (flat_y + 2) * MM, CX, CY + (flat_y + 5) * MM)
cutline_note(CY - (21 / 2 + 8) * MM - 16)
cap_top = CY - (21 / 2 + 8) * MM - 34
cap_lines_rj = [
    "Console Bulkhead \u2014 RJ11/12",
    "21 mm round \u00b7 flat side brings it to 19 mm \u2014 drill round, then file the flat",
    "Left wall, back row",
]
last_y = caption(cap_lines_rj, cap_top)
trim_rect(21 / 2 + 8, 21 / 2 + 8, cap_lines_rj, cap_top, last_y)
c.showPage()

# ---------- page 18: blank ----------
blank_page()

# ---------- page 19: PowerPole flush panel mount template ----------
header("Power \u2014 PowerPole Bulkhead")
scale_note()

# flange reference (gray, not a cut line) -- 34.2 x 17.2mm, ~4mm corner radius
solid_roundrect_centered(CX, CY, 34.2, 17.2, 4.0, color=SLATE, width=0.9)

# through-box cutout -- the actual thing to cut, 19.1 x 11.2mm
solid_rect_centered(CX, CY, 19.1, 11.2)
crosshair(CX, CY, 8)

# two screw holes, 3.7mm dia, 26.7mm apart center-to-center
hx = 13.35 * MM
solid_circle_centered(CX - hx, CY, 3.7)
crosshair(CX - hx, CY, 4, width=0.5)
solid_circle_centered(CX + hx, CY, 3.7)
crosshair(CX + hx, CY, 4, width=0.5)

# hole-spacing dimension line, below the flange
dim_line(CX - hx, CX + hx, CY - 8.6 * MM - 10, "26.7 mm")

dashed_rect_centered(CX, CY, 44.2, 27.2)
cutline_note(CY - 27.2 * MM / 2 - 26)
cap_top = CY - 27.2 * MM / 2 - 44
cap_lines_pp = [
    "PowerPole Bulkhead \u2014 Flush Panel Mount",
    "19.1 \u00d7 11.2 mm through-box cutout \u00b7 2\u00d7 \u2205 3.7 mm holes, 26.7 mm apart",
    "34.2 \u00d7 17.2 mm flange shown gray \u2014 reference only, not a cut line",
    "Left wall, front row",
]
last_y = caption(cap_lines_pp, cap_top)
trim_rect(44.2 / 2, 27.2 / 2, cap_lines_pp, cap_top, last_y)
c.showPage()

# ---------- page 20: blank ----------
blank_page()

c.save()
print("appendix done")
