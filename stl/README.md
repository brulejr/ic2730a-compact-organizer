# STL Dependencies

This build uses one third-party printed part. Its STL isn't redistributed in
this repo — download it directly from the source so you get the designer's
latest revision and so their license terms are respected.

| Part | Source | Expected filename |
|---|---|---|
| PowerPole flush panel mount | [Thingiverse — thing:6874922](https://www.thingiverse.com/thing:6874922) | `Anderson_Powerpole_small_panel_mount_v3.stl` |

## Adding this to your own clone

1. Download the STL from the link above.
2. Drop it in this `stl/` folder using the expected filename so it lines up
   with the references in the main [README](../README.md) and the
   [build plan PDF](../docs/IC-2730A_Compact_Organizer_Build_Plan.pdf).
3. Slice at 0.2 mm layers / 0.4 mm nozzle in PLA — that's what the original
   27-minute print time in this project was based on.

Confirmed dimensions from this file (measured directly off the mesh, not
just the listing): 34.2 × 17.2 mm flange, 19.1 × 11.2 mm through-box cutout,
two ⌀3.7 mm mounting holes 26.7 mm apart. See the drilling template appendix
in the PDF for a 1:1 scale cutting guide built from these numbers.

## Other designs considered, not used

A couple of alternatives got evaluated and set aside during design — noted
here so nobody re-walks the same dead end:

- A two-piece gasket/bracket/dust-cap system (Printables, "Anderson Power
  Poles Panel Mount with Gasket+Template") — solid design, but its
  through-panel screw mounting and lack of a flush mating face made it a
  worse fit than the part above.
- A tower-standoff style mount — keyed socket on a ~20 mm raised tower.
  Functionally fine, but stands the connector proud of the wall by an
  additional 20 mm, which didn't suit this box's stacked position.
