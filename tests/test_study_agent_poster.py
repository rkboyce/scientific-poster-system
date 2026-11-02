"""Poster-specific regression checks for geometry and reproducible rendering."""
from __future__ import annotations

import importlib.util
import json
from math import hypot
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
POSTER = ROOT / "posters" / "study-agent-ohdsi"
sys.path.insert(0, str(POSTER))
from figures import explicit_arrow


def test_explicit_arrow_stops_at_base_and_leaves_target_clearance():
    arrow = explicit_arrow((0, 0), (100, 100), head_length=20, head_width=16, clearance=10)
    assert arrow.shaft_end != arrow.tip
    assert round(hypot(arrow.tip[0] - 100, arrow.tip[1] - 100), 6) == 10
    assert round(hypot(arrow.tip[0] - arrow.shaft_end[0], arrow.tip[1] - arrow.shaft_end[1]), 6) == 20


def test_explicit_arrow_handles_orthogonal_direction():
    arrow = explicit_arrow((10, 50), (210, 50), head_length=18, head_width=14, clearance=12)
    assert arrow.tip == (198.0, 50.0)
    assert arrow.shaft_end == (180.0, 50.0)
    assert arrow.triangle[1][0] == arrow.triangle[2][0] == 180.0


def test_poster_build_has_print_dimensions_and_clean_preflight(tmp_path):
    subprocess.run([sys.executable, str(POSTER / "build.py"), "--out", str(tmp_path), "--no-render"], check=True, cwd=ROOT)
    report = json.loads((tmp_path / "preflight-report.json").read_text())
    assert report["ok"]
    assert report["canvas"] == {"width_pt": 3456, "height_pt": 2592, "width_in": 48.0, "height_in": 36.0}
    assert report["font_minimum_violations"] == []
    root = ET.parse(tmp_path / "study-agent-ohdsi-poster.svg").getroot()
    assert root.attrib["width"] == "48in"
    assert root.attrib["height"] == "36in"
