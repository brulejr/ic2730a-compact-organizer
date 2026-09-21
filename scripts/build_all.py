#!/usr/bin/env python3
"""
Runs the full build: main plan -> appendix templates -> merge -> docs/.
Also regenerates the floor-plan PNG used in the README.

Usage:
    cd scripts
    python3 build_all.py
"""
import os
import subprocess
import sys
from pypdf import PdfReader, PdfWriter

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(HERE, "_build")
DOCS_DIR = os.path.join(HERE, "..", "docs")
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

FINAL_PDF = os.path.join(DOCS_DIR, "IC-2730A_Compact_Organizer_Build_Plan.pdf")


def run(script):
    print(f"--- running {script} ---")
    subprocess.run([sys.executable, os.path.join(HERE, script)], check=True)


def main():
    run("build_plan.py")
    run("appendix_templates.py")
    run("export_floorplan_png.py")

    writer = PdfWriter()
    for fn in ["main.pdf", "appendix.pdf"]:
        r = PdfReader(os.path.join(BUILD_DIR, fn))
        for pg in r.pages:
            writer.add_page(pg)
    with open(FINAL_PDF, "wb") as f:
        writer.write(f)
    print(f"--- wrote {FINAL_PDF} ({len(writer.pages)} pages) ---")


if __name__ == "__main__":
    main()
