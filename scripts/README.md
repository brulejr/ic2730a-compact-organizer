# Build Scripts

Regenerates `docs/IC-2730A_Compact_Organizer_Build_Plan.pdf` and
`docs/floor-plan.png` from source.

| Script | What it does |
|---|---|
| `build_plan.py` | Main plan: overview, floor plan diagram, parts/wiring tables, box prep, build steps, still-open list, resources |
| `appendix_templates.py` | The six 1:1 scale drilling templates, duplex-padded |
| `export_floorplan_png.py` | Standalone PNG of the floor plan diagram, for the README |
| `build_all.py` | Runs all three and merges the final PDF into `docs/` |

## Setup

```bash
pip install -r requirements.txt
```

`pdf2image` also needs [Poppler](https://poppler.freedesktop.org/) installed
and on your PATH (it shells out to `pdftoppm`) — used to convert the
appendix drawing to a PNG:

- macOS: `brew install poppler`
- Debian/Ubuntu: `apt install poppler-utils`
- Windows: see the [pdf2image docs](https://github.com/Belval/pdf2image#windows)

## Build

```bash
cd scripts
python3 build_all.py
```

Writes intermediate files to `scripts/_build/` (gitignored) and the final
PDF + PNG to `docs/`.

## Where things live

- Page/hole dimensions in `build_plan.py`'s `parts_data` table and
  `appendix_templates.py`'s per-template blocks are the source of truth —
  edit there, not in the PDF.
- The appendix pads with blank pages so every template has a blank reverse
  when duplex-printed. If you add or remove a template, re-check the
  page-parity comment at the top of `appendix_templates.py` — it explains
  the logic.
