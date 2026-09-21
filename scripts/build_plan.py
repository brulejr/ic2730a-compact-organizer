#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, ListFlowable, ListItem
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle

import os
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "_build")
os.makedirs(BUILD_DIR, exist_ok=True)
OUT = os.path.join(BUILD_DIR, "main.pdf")

# ---------- palette ----------
NAVY = colors.HexColor("#1F3040")
SLATE = colors.HexColor("#5B6B79")
LIGHT = colors.HexColor("#F4F5F6")
RULE = colors.HexColor("#C7CDD2")
BOX_FILL = colors.HexColor("#E7E9EB")
BOX_STROKE = colors.HexColor("#4B5A66")
RADIO_FILL = colors.HexColor("#F4C7B8")
RADIO_STROKE = colors.HexColor("#B5533C")
SHELF_FILL = colors.HexColor("#D9CCEA")
SHELF_STROKE = colors.HexColor("#7B5EA7")
HEADBG = colors.HexColor("#1F3040")

styles = getSampleStyleSheet()

title_style = ParagraphStyle("TitleX", parent=styles["Title"], textColor=NAVY,
                              fontSize=22, leading=26, spaceAfter=2)
subtitle_style = ParagraphStyle("SubtitleX", parent=styles["Normal"], textColor=SLATE,
                                 fontSize=11, leading=14, spaceAfter=14)
h1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=NAVY, fontSize=15,
                     spaceBefore=18, spaceAfter=8, leading=18)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=NAVY, fontSize=12.5,
                     spaceBefore=12, spaceAfter=6, leading=15)
body = ParagraphStyle("BodyX", parent=styles["Normal"], fontSize=9.7, leading=14,
                       textColor=colors.HexColor("#232323"))
small = ParagraphStyle("SmallX", parent=styles["Normal"], fontSize=8.7, leading=12,
                        textColor=SLATE)
stepnum = ParagraphStyle("StepNum", parent=body, fontSize=9.7, leading=14, spaceAfter=4)
tablehead = ParagraphStyle("TH", parent=body, fontSize=9, textColor=colors.white,
                            fontName="Helvetica-Bold")
tablecell = ParagraphStyle("TC", parent=body, fontSize=9, leading=12)

def rule():
    return HRFlowable(width="100%", thickness=0.75, color=RULE, spaceBefore=4, spaceAfter=10)

def section(title):
    return [Paragraph(title, h1), rule()]

# ---------- floor plan drawing ----------
def floor_plan_drawing():
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
    return d

# ---------- tables ----------
def styled_table(data, col_widths, header_rows=1, small_font=False):
    t = Table(data, colWidths=col_widths, repeatRows=header_rows)
    fs = 8.3 if small_font else 9
    style = [
        ("BACKGROUND", (0, 0), (-1, header_rows - 1), HEADBG),
        ("TEXTCOLOR", (0, 0), (-1, header_rows - 1), colors.white),
        ("FONTNAME", (0, 0), (-1, header_rows - 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), fs),
        ("FONTNAME", (0, header_rows), (-1, -1), "Helvetica"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [colors.white, LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style))
    return t

def p(text, style=tablecell):
    return Paragraph(text, style)

# ================= BUILD DOCUMENT =================
doc = SimpleDocTemplate(OUT, pagesize=letter,
                         topMargin=0.6 * inch, bottomMargin=0.6 * inch,
                         leftMargin=0.65 * inch, rightMargin=0.65 * inch,
                         title="IC-2730A Compact Organizer Build Plan")

E = []

# --- Title block ---
E.append(Paragraph("ICOM IC-2730A Compact Organizer", title_style))
E.append(Paragraph("RIDGID Pro Gear 2.0 build plan &nbsp;\u2022&nbsp; mobile install, GMC Sierra 1500", subtitle_style))
E.append(rule())

# --- Design overview ---
E += section("1. Design Overview")
E.append(Paragraph(
    "This box houses the ICOM IC-2730A main RF unit (control head mounted separately in the cab) "
    "inside a RIDGID Pro Gear 2.0 &ldquo;Half Organizer&rdquo; (254071), interior approximately "
    "300 &times; 200 &times; 70 mm. The box sits stacked directly on top of the battery box, so only "
    "the left and right walls are usable for connector cutouts &mdash; the top is the lid and the back "
    "wall is against the stack.", body))
E.append(Spacer(1, 6))
E.append(Paragraph(
    "Cooling is vented forced air: a filtered intake on the left wall and a Noctua fan exhausting on "
    "the right, pulling air directly across the radio. The IC-2730A has its own fan at the heatsink "
    "end, and the case fan sits directly behind both it and the adjacent heatsink &mdash; so the case "
    "fan's job is to carry that discharge out of the box, not to drive air through the fin channels "
    "itself. That is why the case fan's height is not tied to the heatsink's fin-channel direction. "
    "A sealed conduction-plate approach was ruled out "
    "because the box's floor sits flush on the battery box below it &mdash; there is no ambient air on "
    "the far side of the floor for heat to go.", body))
E.append(Spacer(1, 6))
E.append(Paragraph(
    "Power and control cabling (DC power, console/control-head cable) route out the left wall; "
    "antenna and speaker audio route out the right wall. This keeps DC and switching noise away from "
    "the RF and audio paths, consistent with the noise-isolation practice used elsewhere in the build "
    "(ferrite choke at the DC entry, twisted/separated runs). There is no master power switch &mdash; "
    "the PowerPole disconnect already serves that role, and a switch on this box would sit out of "
    "reach of the operating position.", body))
E.append(Spacer(1, 10))
E.append(KeepTogether([Paragraph("Floor Plan", h2), floor_plan_drawing()]))

E.append(PageBreak())

# --- Parts & connector schedule ---
E += section("2. Parts &amp; Hole Schedule")

parts_data = [
    [p("Component", tablehead), p("Wall / Position", tablehead), p("Key Dimensions", tablehead), p("Notes", tablehead)],
    [p("SO-239 bulkhead"), p("Right wall, back row"), p("16 mm hole, 25\u00d725 mm flange, 22 mm depth"),
     p("Chassis-mount UHF female, solder-cup")],
    [p("TRRS bulkhead"), p("Right wall, front row"), p("22 mm dia., 30 mm depth"), p("Speaker output")],
    [p("Fan &mdash; Noctua NF-A4x20 5V PWM"), p("Right wall, center"), p("40\u00d740\u00d720 mm, 32\u00d732 mm hole spacing"),
     p("4-pin true PWM, powered from 5V buck rail, not raw 12V")],
    [p("Filtered vent"), p("Left wall, center"), p("40\u00d740mm frame \u00b7 32\u00d732mm hole spacing (provisional \u2014 matches the fan footprint)"),
     p("Media: 120 µm polyester monofilament mesh, washable, clamped between shroud and the <b>outside</b> face of the wall so it cleans without opening the box. TPU-printed shroud, ~95A shore hardness; one shroud design can serve both fan and vent; actual open-air area still depends on shroud design")],
    [p("PowerPole bulkhead"), p("Left wall, front row"), p("34.2\u00d717.2mm flange \u00b7 19.1\u00d711.2mm through-box cutout \u00b7 2\u00d7 \u2205 3.7mm holes, 26.7mm apart"),
     p("Printed tower mount, flange-flush \u2014 connector body hides inside the box, not proud of the wall. Doubles as the box's power disconnect")],
    [p("Console bulkhead (RJ11/12)"), p("Left wall, back row"), p("21 mm round \u00b7 flat side to 19 mm \u2014 drill round, file the flat"),
     p("Weatherproof, tethered threaded cap, pigtail lead (not a straight pass-through)")],
    [p("ESP32 dev board"), p("Floor, back wall, ~50 mm in from right, 100 mm wide"), p("&mdash;"),
     p("Fan PWM control, tach (with divider), DS18B20 read, temp logging")],
    [p("Buck converter (12V\u21925V)"), p("Same shelf as ESP32"), p("Automotive-transient rated"),
     p("Feeds ESP32 and fan; not the radio")],
    [p("DS18B20 temp probe"), p("Mounted against heatsink"), p("Waterproof probe form"),
     p("1-Wire, 4.7k\u03a9 pull-up to 3.3V")],
]
E.append(styled_table(parts_data, [1.55 * inch, 1.35 * inch, 2.15 * inch, 1.65 * inch], small_font=True))

E.append(Spacer(1, 12))
E.append(Paragraph("Wiring reference", h2))
wire_data = [
    [p("Run", tablehead), p("Gauge", tablehead), p("Notes", tablehead)],
    [p("12V main (radio)"), p("12 AWG"), p("Anderson PowerPole; ferrite choke at DC entry; ~13A TX draw")],
    [p("5V rail (ESP32 + fan)"), p("22 AWG"), p("Off buck converter output, not raw 12V")],
    [p("Fan PWM control"), p("&mdash;"), p("ESP32 GPIO direct, 3.3V logic, no MOSFET needed")],
    [p("Fan tach (optional)"), p("&mdash;"), p("10k/20k divider before ESP32 GPIO \u2014 fan's internal pull-up is 5V")],
    [p("DS18B20 data"), p("&mdash;"), p("4.7k\u03a9 pull-up to 3.3V")],
]
E.append(styled_table(wire_data, [1.7 * inch, 0.9 * inch, 4.1 * inch], small_font=True))

E.append(PageBreak())

# --- Box prep ---
E += section("3. Box Preparation")
prep_items = [
    "Dry-fit the ICOM main unit and existing L-brackets in the empty case to confirm the 30 mm front "
    "/ 35 mm back margin and left/right wall clearances before cutting anything.",
    "Remove the left and right internal parts-cup ribs with an oscillating multi-tool (flush-cut blade). "
    "Leave the front and back ribs in place \u2014 nothing mounts to those walls. Cut slightly proud of "
    "flush and finish by hand with a file or sanding block rather than trying to hit flush in one pass.",
    "Dry-fit the SO-239 flange, TRRS body, PowerPole print, and fan against the cut walls before final "
    "mounting. Check for leftover rib stubs under any flange or gasket surface \u2014 even 1 mm of proud "
    "material will tilt a connector or keep a gasket from compressing evenly.",
    "Where a rib is being removed right where a connector will be torqued down (PowerPole print, SO-239), "
    "plan a stainless backing washer behind the nut rather than relying on the bare wall for stiffness.",
    "Cut the HDPE sub-plate to fit the case floor. Confirm final floor flatness once the bin-tray ribs "
    "(if any remain molded into the floor) are accounted for.",
]
E.append(ListFlowable([ListItem(Paragraph(t, body), spaceAfter=6) for t in prep_items],
                       bulletType="bullet", start="circle", leftIndent=14))

E.append(PageBreak())

# --- Step by step build ---
E += section("4. Step-by-Step Build")

steps = [
    ("Sub-plate hardware",
     "Drill and countersink four holes in the HDPE plate matching the radio L-bracket footprint. "
     "Mount the brackets to the plate from the top with flat-head M4 bolts (existing hardware from the "
     "prior go-box project). This keeps the radio-to-plate connection independent of however the plate "
     "attaches to the case, so no underside access is ever needed."),
    ("Plate-to-case attachment",
     "Apply 3M Dual Lock strips to the case floor and the matching strips to the underside of the HDPE "
     "plate, positioned under the radio's footprint for the load-bearing contact area. No standoffs, no "
     "heat-set inserts into the case itself \u2014 the plate sits flush and lifts off as a unit for service."),
    ("Cable-tie anchors",
     "At each planned cable run, drill two small holes close together through the plate. Cables route "
     "atop the plate; the zip tie passes down through one hole and back up through the other to cinch "
     "over the cable on top. Anchor each run close to its connector and again partway to the radio, "
     "keeping the left-side (DC/console) and right-side (antenna/speaker) runs from crossing paths."),
    ("Wall cutouts",
     "With the ribs removed (Section 3), mark and cut the six wall openings per the hole schedule: "
     "SO-239 and TRRS on the right (back and front rows), PowerPole and console RJ11/12 on the left "
     "(front and back rows), vent and fan centered on their respective walls."),
    ("Install bulkheads",
     "Mount each bulkhead per its dry-fit position. Install the PowerPole print and SO-239 with backing "
     "washers where a rib was removed underneath. Fit the TPU vent and fan shrouds."),
    ("Wire the radio side",
     "Run 12 AWG DC power and the antenna coax to the radio's rear panel; dress the DC leads across "
     "to the left-wall PowerPole per the original photo reference, keeping the run away from the "
     "antenna feed. Fit the ferrite choke at the DC entry point."),
    ("Wire the control/monitoring side",
     "Wire the ESP32 and buck converter on their back-wall shelf: 5V rail to ESP32 and fan, PWM line "
     "from ESP32 GPIO to the fan's control pin, tach line through the divider if RPM feedback is wanted, "
     "DS18B20 data line with its pull-up, probe bonded to the heatsink."),
    ("Seat the sub-assembly",
     "Press the finished radio-and-plate assembly onto the Dual Lock in the case. Connect the console, "
     "antenna, speaker, and power runs to their bulkheads. Confirm the fan and vent sit in the radio's "
     "own airflow path before closing the lid — the case fan should be pulling in the same "
     "direction the radio's fan discharges, not opposing it, with clearance between the two."),
    ("Final check",
     "Power up, confirm ESP32 reads a sane temperature, fan responds to PWM commands, and TX current "
     "draw and cable dressing look correct before the box goes into the truck."),
]

flow = []
for i, (title, text) in enumerate(steps, 1):
    flow.append(KeepTogether([
        Paragraph(f"<b>Step {i} &mdash; {title}</b>", stepnum),
        Paragraph(text, body),
        Spacer(1, 8),
    ]))
E += flow

E.append(PageBreak())

# --- Open items ---
E += section("5. Still Open")
open_items = [
    "Standoff height (reused hardware) \u2014 sets the clearance for airflow under the radio and "
    "confirms the stack still fits under the lid.",
    "Filtered vent open area \u2014 media is settled (120 \u00b5m polyester monofilament mesh), but the "
    "40\u00d740mm frame is still provisional, matched to the fan's footprint (see the appendix "
    "template); confirm once the shroud design fixes the actual open-air passage.",
    "TPU shroud dimensions for the vent and fan \u2014 not yet drawn.",
]
for t in open_items:
    E.append(Paragraph("[ ]&nbsp;&nbsp;" + t, body))
    E.append(Spacer(1, 6))

E.append(PageBreak())

# --- Resources ---
E += section("6. Resources")
E.append(Paragraph(
    "Reference links for printed parts and other reusable designs, collected as the build progresses.",
    body))
E.append(Spacer(1, 8))

resource_links = [
    ("Anderson Powerpole small panel mount",
     "https://www.thingiverse.com/thing:6874922"),
]
res_items = []
for label, url in resource_links:
    txt = f'{label} &mdash; <link href="{url}"><font color="#1a5fb4"><u>{url}</u></font></link>'
    res_items.append(ListItem(Paragraph(txt, body), spaceAfter=8))
E.append(ListFlowable(res_items, bulletType="bullet", leftIndent=14))

E.append(Spacer(1, 16))
E.append(rule())
E.append(Paragraph("KC1ZDJ &nbsp;\u2022&nbsp; White Mountains, NH &nbsp;\u2022&nbsp; Ham Radio Mobile Base Station project",
                    small))

doc.build(E)
print("done")
