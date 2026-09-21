# ICOM IC-2730A Compact Organizer

RIDGID Pro Gear 2.0 build plan &middot; mobile install, GMC Sierra 1500

📄 **[Download the printable build plan (PDF)](docs/IC-2730A_Compact_Organizer_Build_Plan.pdf)** — includes this
same content plus six 1:1 scale drilling templates in a duplex-safe appendix.

---

## 1. Design Overview

This box houses the ICOM IC-2730A main RF unit (control head mounted separately in the cab) inside a
RIDGID Pro Gear 2.0 "Half Organizer" (254071), interior approximately 300 × 200 × 70 mm. The box sits
stacked directly on top of the battery box, so only the left and right walls are usable for connector
cutouts — the top is the lid and the back wall is against the stack.

Cooling is vented forced air: a filtered intake on the left wall and a Noctua fan exhausting on the
right, pulling air directly across the radio. The IC-2730A has its own fan at the heatsink end, and the
case fan sits directly behind both it and the adjacent heatsink — so the case fan's job is to carry that
discharge out of the box, not to drive air through the fin channels itself. That is why the case fan's
height is not tied to the heatsink's fin-channel direction. A sealed conduction-plate approach was ruled
out because the box's floor sits flush on the battery box below it — there is no ambient air on the far
side of the floor for heat to go.

Power and control cabling (DC power, console/control-head cable) route out the left wall; antenna and
speaker audio route out the right wall. This keeps DC and switching noise away from the RF and audio
paths, consistent with the noise-isolation practice used elsewhere in the build (ferrite choke at the DC
entry, twisted/separated runs). There is no master power switch — the PowerPole disconnect already
serves that role, and a switch on this box would sit out of reach of the operating position.

### Floor Plan

![Floor plan — back (hinge) at top, front (latch) at bottom. Left wall carries console, vent, and power; right wall carries antenna, fan, and speaker; radio sits with its heatsink end toward the right wall; ESP32 and buck converter sit on a shelf against the back wall.](docs/floor-plan.png)

---

## 2. Parts & Hole Schedule

| Component | Wall / Position | Key Dimensions | Notes |
|---|---|---|---|
| SO-239 bulkhead | Right wall, back row | 16 mm hole, 25×25 mm flange, 22 mm depth | Chassis-mount UHF female, solder-cup |
| TRRS bulkhead | Right wall, front row | 22 mm dia., 30 mm depth | Speaker output |
| Fan — Noctua NF-A4x20 5V PWM | Right wall, center | 40×40×20 mm, 32×32 mm hole spacing | 4-pin true PWM, powered from 5V buck rail, not raw 12V |
| Filtered vent | Left wall, center | 40×40mm frame · 32×32mm hole spacing (provisional — matches the fan footprint) | Media: 120 µm polyester monofilament mesh, washable, clamped between shroud and the **outside** face of the wall so it cleans without opening the box. TPU-printed shroud, ~95A shore hardness; one shroud design can serve both fan and vent; actual open-air area still depends on shroud design |
| PowerPole bulkhead | Left wall, front row | 34.2×17.2mm flange · 19.1×11.2mm through-box cutout · 2× ⌀3.7mm holes, 26.7mm apart | Printed tower mount, flange-flush — connector body hides inside the box, not proud of the wall. Doubles as the box's power disconnect |
| Console bulkhead (RJ11/12) | Left wall, back row | 21 mm round · flat side to 19 mm — drill round, file the flat | Weatherproof, tethered threaded cap, pigtail lead (not a straight pass-through) |
| ESP32 dev board | Floor, back wall, ~50 mm in from right, 100 mm wide | — | Fan PWM control, tach (with divider), DS18B20 read, temp logging |
| Buck converter (12V→5V) | Same shelf as ESP32 | Automotive-transient rated | Feeds ESP32 and fan; not the radio |
| DS18B20 temp probe | Mounted against heatsink | Waterproof probe form | 1-Wire, 4.7kΩ pull-up to 3.3V |

### Wiring reference

| Run | Gauge | Notes |
|---|---|---|
| 12V main (radio) | 12 AWG | Anderson PowerPole; ferrite choke at DC entry; ~13A TX draw |
| 5V rail (ESP32 + fan) | 22 AWG | Off buck converter output, not raw 12V |
| Fan PWM control | — | ESP32 GPIO direct, 3.3V logic, no MOSFET needed |
| Fan tach (optional) | — | 10k/20k divider before ESP32 GPIO — fan's internal pull-up is 5V |
| DS18B20 data | — | 4.7kΩ pull-up to 3.3V |

---

## 3. Box Preparation

- Dry-fit the ICOM main unit and existing L-brackets in the empty case to confirm the 30 mm front /
  35 mm back margin and left/right wall clearances before cutting anything.
- Remove the left and right internal parts-cup ribs with an oscillating multi-tool (flush-cut blade).
  Leave the front and back ribs in place — nothing mounts to those walls. Cut slightly proud of flush
  and finish by hand with a file or sanding block rather than trying to hit flush in one pass.
- Dry-fit the SO-239 flange, TRRS body, PowerPole print, and fan against the cut walls before final
  mounting. Check for leftover rib stubs under any flange or gasket surface — even 1 mm of proud
  material will tilt a connector or keep a gasket from compressing evenly.
- Where a rib is being removed right where a connector will be torqued down (PowerPole print, SO-239),
  plan a stainless backing washer behind the nut rather than relying on the bare wall for stiffness.
- Cut the HDPE sub-plate to fit the case floor. Confirm final floor flatness once the bin-tray ribs (if
  any remain molded into the floor) are accounted for.

---

## 4. Step-by-Step Build

1. **Sub-plate hardware** — Drill and countersink four holes in the HDPE plate matching the radio
   L-bracket footprint. Mount the brackets to the plate from the top with flat-head M4 bolts (existing
   hardware from the prior go-box project). This keeps the radio-to-plate connection independent of
   however the plate attaches to the case, so no underside access is ever needed.
2. **Plate-to-case attachment** — Apply 3M Dual Lock strips to the case floor and the matching strips to
   the underside of the HDPE plate, positioned under the radio's footprint for the load-bearing contact
   area. No standoffs, no heat-set inserts into the case itself — the plate sits flush and lifts off as
   a unit for service.
3. **Cable-tie anchors** — At each planned cable run, drill two small holes close together through the
   plate. Cables route atop the plate; the zip tie passes down through one hole and back up through the
   other to cinch over the cable on top. Anchor each run close to its connector and again partway to the
   radio, keeping the left-side (DC/console) and right-side (antenna/speaker) runs from crossing paths.
4. **Wall cutouts** — With the ribs removed (Section 3), mark and cut the six wall openings per the hole
   schedule: SO-239 and TRRS on the right (back and front rows), PowerPole and console RJ11/12 on the
   left (front and back rows), vent and fan centered on their respective walls.
5. **Install bulkheads** — Mount each bulkhead per its dry-fit position. Install the PowerPole print and
   SO-239 with backing washers where a rib was removed underneath. Fit the TPU vent and fan shrouds.
6. **Wire the radio side** — Run 12 AWG DC power and the antenna coax to the radio's rear panel; dress
   the DC leads across to the left-wall PowerPole per the original photo reference, keeping the run away
   from the antenna feed. Fit the ferrite choke at the DC entry point.
7. **Wire the control/monitoring side** — Wire the ESP32 and buck converter on their back-wall shelf: 5V
   rail to ESP32 and fan, PWM line from ESP32 GPIO to the fan's control pin, tach line through the
   divider if RPM feedback is wanted, DS18B20 data line with its pull-up, probe bonded to the heatsink.
8. **Seat the sub-assembly** — Press the finished radio-and-plate assembly onto the Dual Lock in the
   case. Connect the console, antenna, speaker, and power runs to their bulkheads. Confirm the fan and
   vent sit in the radio's own airflow path before closing the lid — the case fan should be pulling in
   the same direction the radio's fan discharges, not opposing it, with clearance between the two.
9. **Final check** — Power up, confirm ESP32 reads a sane temperature, fan responds to PWM commands, and
   TX current draw and cable dressing look correct before the box goes into the truck.

---

## 5. Still Open

- [ ] Standoff height (reused hardware) — sets the clearance for airflow under the radio and confirms
      the stack still fits under the lid.
- [ ] Filtered vent open area — media is settled (120 µm polyester monofilament mesh), but the 40×40mm
      frame is still provisional, matched to the fan's footprint (see the appendix template in the PDF);
      confirm once the shroud design fixes the actual open-air passage.
- [ ] TPU shroud dimensions for the vent and fan — not yet drawn.

---

## 6. Resources

Reference links for printed parts and other reusable designs, collected as the build progresses.

- Anderson Powerpole small panel mount — <https://www.thingiverse.com/thing:6874922>

See [`stl/README.md`](stl/README.md) for exact filenames, confirmed dimensions, and the alternate
designs that were considered and set aside.

---

## Drilling Templates

The PDF's appendix has six 1:1 scale, duplex-safe cut-out templates (SO-239, TRRS, fan, vent, RJ11/12,
PowerPole) with paper-cutter alignment guides — print it at Actual Size, not "Fit to page." See
[`docs/IC-2730A_Compact_Organizer_Build_Plan.pdf`](docs/IC-2730A_Compact_Organizer_Build_Plan.pdf).

## Repo Contents

```
.
├── README.md                 — this file
├── LICENSE                   — CC BY 4.0
├── docs/
│   ├── IC-2730A_Compact_Organizer_Build_Plan.pdf   — full build plan + drilling templates
│   └── floor-plan.png                              — floor plan diagram used above
├── stl/
│   └── README.md              — third-party STL sourcing (not redistributed here)
├── photos/
│   └── README.md              — expected build-photo filenames
└── scripts/                   — Python source that generates the PDF + diagram
    ├── build_plan.py
    ├── appendix_templates.py
    ├── export_floorplan_png.py
    ├── build_all.py            — run this to regenerate everything
    └── requirements.txt
```

## License

This build plan, its diagrams, and any photos in this repo are licensed under
[CC BY 4.0](LICENSE) — share and adapt freely, with attribution. Third-party
files referenced but not redistributed here (see [`stl/README.md`](stl/README.md))
remain under their original licenses.

---

KC1ZDJ &middot; White Mountains, NH &middot; Ham Radio Mobile Base Station project
