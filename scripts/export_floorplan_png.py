#!/usr/bin/env python3
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics import renderPM

NAVY = colors.HexColor("#1F3040")
SLATE = colors.HexColor("#5B6B79")
BOX_FILL = colors.HexColor("#E7E9EB")
BOX_STROKE = colors.HexColor("#4B5A66")
RADIO_FILL = colors.HexColor("#F4C7B8")
RADIO_STROKE = colors.HexColor("#B5533C")
SHELF_FILL = colors.HexColor("#D9CCEA")
SHELF_STROKE = colors.HexColor("#7B5EA7")

d = Drawing(560, 300)

# outer case
d.add(Rect(100, 20, 360, 240, rx=10, ry=10, fillColor=BOX_FILL,
            strokeColor=BOX_STROKE, strokeWidth=1))
d.add(String(112, 244, "Compact Organizer box", fontSize=10, fontName="Helvetica-Bold",
              fillColor=NAVY))
d.add(String(112, 232, "300 x 200 x 70 mm interior", fontSize=8, fillColor=SLATE))

# ESP32 / buck shelf (back wall, offset from right)
d.add(Rect(280, 220, 120, 36, rx=6, ry=6, fillColor=SHELF_FILL,
            strokeColor=SHELF_STROKE, strokeWidth=1))
d.add(String(340, 241, "ESP32", fontSize=8.5, fontName="Helvetica-Bold",
              fillColor=colors.HexColor("#3F2E63"), textAnchor="middle"))
d.add(String(340, 227, "+ buck converter", fontSize=7.5,
              fillColor=colors.HexColor("#3F2E63"), textAnchor="middle"))

# radio
d.add(Rect(189, 56, 182, 162, rx=8, ry=8, fillColor=RADIO_FILL,
            strokeColor=RADIO_STROKE, strokeWidth=1))
d.add(String(280, 145, "IC-2730A", fontSize=10.5, fontName="Helvetica-Bold",
              fillColor=colors.HexColor("#7A2E17"), textAnchor="middle"))
d.add(String(280, 131, "heatsink end faces right", fontSize=8,
              fillColor=colors.HexColor("#7A2E17"), textAnchor="middle"))
d.add(String(280, 118, "30mm front / 35mm back margin", fontSize=7.5,
              fillColor=colors.HexColor("#7A2E17"), textAnchor="middle"))

def leader_left(y, label):
    d.add(Line(100, y, 90, y, strokeColor=SLATE, strokeWidth=0.75))
    d.add(Circle(100, y, 2, fillColor=NAVY, strokeColor=None))
    d.add(String(86, y - 3, label, fontSize=9, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="end"))

def leader_right(y, label):
    d.add(Line(460, y, 470, y, strokeColor=SLATE, strokeWidth=0.75))
    d.add(Circle(460, y, 2, fillColor=NAVY, strokeColor=None))
    d.add(String(474, y - 3, label, fontSize=9, fontName="Helvetica-Bold",
                  fillColor=NAVY, textAnchor="start"))

leader_left(220, "Console (RJ11/12)")
leader_left(140, "Filtered vent")
leader_left(60, "Power (PowerPole)")
leader_right(220, "Antenna (SO-239)")
leader_right(140, "Fan (NF-A4x20)")
leader_right(60, "Speaker (TRRS)")

d.add(String(280, 6, "Back (hinge) at top of diagram  \u2022  Front (latch) at bottom",
              fontSize=7.5, fillColor=SLATE, textAnchor="middle"))

import os
from reportlab.pdfgen import canvas as pdfcanvas
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "_build")
os.makedirs(BUILD_DIR, exist_ok=True)
tmp_pdf = os.path.join(BUILD_DIR, "_floorplan_tmp.pdf")
c = pdfcanvas.Canvas(tmp_pdf, pagesize=(560, 300))
d.drawOn(c, 0, 0)
c.showPage()
c.save()

from pdf2image import convert_from_path
imgs = convert_from_path(tmp_pdf, dpi=300)
imgs[0].save(os.path.join(HERE, "..", "docs", "floor-plan.png"))
print("saved")
