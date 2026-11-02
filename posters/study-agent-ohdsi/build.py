#!/usr/bin/env python3
"""Build the editable 48 x 36 inch Study Agent poster and QA report.

Run from repository root: uv run python posters/study-agent-ohdsi/build.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET

import svgwrite

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))
from posterkit.composition import Component, ComponentRegistry
from posterkit.layout import Box, PangoMeasurer, Overflow
from figures import draw_arrow


class Poster:
    def __init__(self, config: dict, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.w = config["poster"]["width_in"] * 72
        self.h = config["poster"]["height_in"] * 72
        self.colors = config["palette"]
        self.fonts = config["fonts"]
        self.d = svgwrite.Drawing(size=(f'{config["poster"]["width_in"]}in',
                                         f'{config["poster"]["height_in"]}in'),
                                 viewBox=f"0 0 {self.w} {self.h}")
        self.d.add(self.d.rect(insert=(0, 0), size=(self.w, self.h), fill=self.colors["surface"]))
        self.m = PangoMeasurer()
        self.registry = ComponentRegistry(Box(0, 0, self.w, self.h))
        self.text_entries: list[dict] = []
        self.connector_entries: list[dict] = []

    def panel(self, key: str, box: Box, *, fill: str, stroke: str | None = None,
              parent: str | None = None, radius: float = 16) -> None:
        self.registry.add(Component(key, box, kind="panel", parent=parent))
        self.d.add(self.d.rect(insert=(box.x, box.y), size=(box.w, box.h), rx=radius,
                               fill=fill, stroke=stroke or "none", stroke_width=2 if stroke else 0))

    def text(self, key: str, value: str, box: Box, *, pt: float, min_pt: float,
             color: str | None = None, bold: bool = False, align: str = "start",
             parent: str | None = None, line_factor: float = 1.24) -> None:
        if pt < min_pt:
            raise Overflow(f"{key}: {pt} pt below declared minimum {min_pt} pt")
        lines = value.split("\n")
        widths = [self.m.measure(line, self.fonts["family"], pt, None, bold)["width"] for line in lines]
        if max(widths, default=0) > box.w:
            raise Overflow(f"{key}: explicit line wider than its {box.w:.1f} pt box")
        measured = self.m.measure(value, self.fonts["family"], pt, box.w, bold)
        if measured["lines"] != len(lines):
            raise Overflow(f"{key}: unexpected Pango wrap; edit copy or geometry")
        need = max(measured["height"], len(lines) * pt * line_factor)
        if need > box.h:
            raise Overflow(f"{key}: needs {need:.1f} pt height; box is {box.h:.1f} pt")
        self.registry.add(Component(key, box, kind="text", parent=parent))
        if align == "middle":
            x, anchor = box.x + box.w / 2, "middle"
        elif align == "end":
            x, anchor = box.x + box.w, "end"
        else:
            x, anchor = box.x, "start"
        top = box.y + (box.h - len(lines) * pt * line_factor) / 2
        group = self.d.g(id=key, **{"class": "poster-text"})
        for index, line in enumerate(lines):
            group.add(self.d.text(line, insert=(x, top + (index + .84) * pt * line_factor),
                                  text_anchor=anchor, font_family=self.fonts["family"],
                                  font_size=pt, font_weight="bold" if bold else "normal",
                                  fill=color or self.colors["text"]))
        self.d.add(group)
        self.text_entries.append({"key": key, "pt": pt, "minimum_pt": min_pt,
                                  "bounds": box.__dict__, "lines": len(lines),
                                  "measured": measured})

    def rule(self, x1, y1, x2, y2, *, color: str | None = None, width: float = 3) -> None:
        self.d.add(self.d.line(start=(x1, y1), end=(x2, y2), stroke=color or self.colors["accent"],
                               stroke_width=width))

    def arrow(self, key: str, start, target, *, parent: str | None = None) -> None:
        group = self.d.g(id=key, **{"class": "arrow-connector"})
        g = draw_arrow(self.d, group, start, target, color=self.colors["accent"], clearance=12)
        self.d.add(group)
        points = [g.start, g.shaft_end, *g.triangle]
        box = Box(min(p[0] for p in points), min(p[1] for p in points),
                  max(p[0] for p in points) - min(p[0] for p in points),
                  max(p[1] for p in points) - min(p[1] for p in points))
        self.registry.add(Component(key, box, kind="connector", parent=parent, allow_overlap=True))
        self.connector_entries.append({"key": key, "start": g.start, "shaft_end": g.shaft_end,
                                       "tip": g.tip, "target": target, "clearance_pt": 12})


def build_svg(config: dict, output_dir: Path) -> tuple[Path, Poster]:
    p = Poster(config, output_dir)
    c, f = p.colors, p.fonts
    # Header and high-contrast main message.
    p.panel("header", Box(0, 0, p.w, 385), fill=c["primary"], radius=0)
    p.text("title", "OHDSI Study Agent for Human–AI Team-Based", Box(120, 45, 3216, 105), pt=72, min_pt=68,
           color="#FFFFFF", bold=True, align="middle", parent="header")
    p.text("subtitle", "Real-World Evidence Generation in the Veterans Health Administration", Box(120, 158, 3216, 76), pt=50, min_pt=46,
           color="#FFFFFF", bold=True, align="middle", parent="header")
    p.text("authors", "Richard D. Boyce, PhD  |  University of Pittsburgh  |  VA Informatics and Computing Infrastructure (VINCI)",
           Box(120, 267, 3216, 43), pt=24, min_pt=22, color="#DCE9ED", align="middle", parent="header")
    p.text("status", "HYPOTHETICAL SYMPOSIUM POSTER • ARCHITECTURE / FUNCTIONAL-PROTOTYPE REPORT • SCIENTIFIC REVIEW REQUIRED",
           Box(120, 322, 3216, 30), pt=18, min_pt=18, color="#A9DCD2", bold=True, align="middle", parent="header")
    p.panel("takeaway", Box(72, 424, 3312, 245), fill=c["accent_light"], stroke=c["rule"])
    p.text("takeaway-heading", "CENTRAL TAKEAWAY", Box(120, 456, 800, 35), pt=22, min_pt=20, color=c["accent"], bold=True, parent="takeaway")
    p.text("takeaway-copy", "Reusable, governed AI support for OHDSI workflows combines ACP/MCP coordination\nwith deterministic validation — while researchers remain accountable for consequential decisions.",
           Box(120, 505, 3180, 130), pt=43, min_pt=40, color=c["primary"], bold=True, parent="takeaway", line_factor=1.12)
    # Three column content field.
    left, center, right = Box(72, 718, 810, 1500), Box(918, 718, 1590, 1500), Box(2544, 718, 840, 1500)
    p.panel("governance", left, fill="#FBFCFB", stroke=c["rule"])
    p.text("gov-heading", "WHY GOVERNED TEAMING?", Box(112, 752, 730, 48), pt=30, min_pt=28, color=c["primary"], bold=True, parent="governance")
    p.rule(112, 818, 842, 818)
    p.text("gov-context", "RWE study design links judgments about\nphenotypes, causal assumptions, cohorts,\nand interpretation. AI assistance is bounded\nwhere researchers need structured support.",
           Box(112, 848, 730, 176), pt=25, min_pt=23, parent="governance")
    p.text("gov-control-heading", "RESEARCHER OVERSIGHT", Box(112, 1072, 730, 34), pt=22, min_pt=20, color=c["accent"], bold=True, parent="governance")
    p.text("gov-control", "• Explicit confirmations and stage gates\n• Validated outputs and auditable routing\n• Sanitized summaries / metadata to models\n• Fail-closed PHI/PII sanitation where applicable\n• Row-level clinical data are not sent to the model",
           Box(112, 1122, 730, 225), pt=22, min_pt=20, parent="governance")
    p.text("gov-maturity-heading", "PROTOTYPE MATURITY", Box(112, 1425, 730, 34), pt=22, min_pt=20, color=c["accent"], bold=True, parent="governance")
    p.text("gov-maturity", "Early functional prototype: approx. TRL 4–5\n(scripted laboratory demonstration).\n\nNot established: efficiency, decision accuracy,\ncalibrated reliance, or better study outcomes.",
           Box(112, 1477, 730, 195), pt=22, min_pt=20, parent="governance")
    p.text("gov-scope-heading", "SCOPE OF CLAIM", Box(112, 1775, 730, 34), pt=22, min_pt=20, color=c["accent"], bold=True, parent="governance")
    p.text("gov-scope", "The generative model is coordinated by an\nagent harness; Study Agent does not bundle\na model and does not replace researcher judgment.",
           Box(112, 1825, 730, 120), pt=22, min_pt=20, parent="governance")
    # Central architecture.
    p.panel("architecture", Box(center.x, center.y, center.w, 1012), fill="#FBFCFB", stroke=c["rule"])
    p.text("architecture-heading", "1  SERVICE-BASED, GOVERNED ARCHITECTURE", Box(958, 752, 1510, 48), pt=30, min_pt=28, color=c["primary"], bold=True, parent="architecture")
    p.text("architecture-kicker", "Distinct roles: clients access shared services; ACP, MCP and deterministic code are not interchangeable.",
           Box(958, 815, 1510, 35), pt=20, min_pt=18, color=c["muted"], parent="architecture")
    clients = [(958, "R / Strategus shells", "reported prototype integration", "client-r"),
               (1474, "Atlas3 / WebAPI", "early-stage integration", "client-atlas"),
               (1990, "Coding agents + Skills.md", "researcher context; unverified", "client-coding")]
    for x, label, detail, key in clients:
        p.panel(key, Box(x, 890, 466, 143), fill=c["surface_muted"], stroke=c["rule"], parent="architecture", radius=12)
        p.text(f"{key}-label", label, Box(x+20, 912, 426, 37), pt=22, min_pt=20, color=c["primary"], bold=True, parent=key)
        p.text(f"{key}-detail", detail, Box(x+20, 964, 426, 27), pt=18, min_pt=18, color=c["muted"], parent=key)
    p.panel("acp", Box(1165, 1144, 1096, 181), fill="#D6EEE7", stroke=c["accent"], parent="architecture", radius=14)
    p.text("acp-label", "ACP SERVER", Box(1195, 1170, 1036, 44), pt=30, min_pt=28, color=c["primary"], bold=True, align="middle", parent="acp")
    p.text("acp-detail", "Workflow orchestration • state • confirmations • routing • policy / safety checks", Box(1195, 1221, 1036, 35), pt=22, min_pt=20, align="middle", parent="acp")
    for x, key in [(1191, "arrow-r-acp"), (1707, "arrow-atlas-acp"), (2223, "arrow-coding-acp")]:
        p.arrow(key, (x, 1045), (1713, 1132), parent="architecture")
    p.panel("mcp", Box(1000, 1455, 656, 160), fill=c["surface_blue"], stroke=c["rule"], parent="architecture", radius=14)
    p.text("mcp-label", "MCP SERVERS", Box(1025, 1480, 606, 40), pt=27, min_pt=25, color=c["primary"], bold=True, align="middle", parent="mcp")
    p.text("mcp-detail", "Bounded tools • prompt bundles\nStructured schemas", Box(1025, 1528, 606, 58), pt=20, min_pt=18, align="middle", parent="mcp")
    p.panel("deterministic", Box(1770, 1455, 656, 160), fill=c["surface_blue"], stroke=c["rule"], parent="architecture", radius=14)
    p.text("det-label", "DETERMINISTIC CORE", Box(1795, 1480, 606, 40), pt=27, min_pt=25, color=c["primary"], bold=True, align="middle", parent="deterministic")
    p.text("det-detail", "Validation • constrained transformations\nStructured outputs", Box(1795, 1528, 606, 58), pt=20, min_pt=18, align="middle", parent="deterministic")
    p.arrow("arrow-acp-mcp", (1375, 1338), (1330, 1443), parent="architecture")
    p.arrow("arrow-acp-det", (2050, 1338), (2100, 1443), parent="architecture")
    p.text("architecture-note", "Source status: R/Strategus demonstrated; Atlas3/WebAPI early-stage. Coding-agent support and exact\nOHDSI deterministic package bindings are intentionally not represented as verified implementation.",
           Box(958, 1640, 1510, 55), pt=18, min_pt=18, color=c["muted"], parent="architecture")
    # Right-side flows and screenshot placeholder.
    p.panel("flows", Box(right.x, right.y, right.w, 760), fill="#FBFCFB", stroke=c["rule"])
    p.text("flows-heading", "2  NAMED GOVERNED FLOWS", Box(2584, 752, 760, 44), pt=29, min_pt=27, color=c["primary"], bold=True, parent="flows")
    p.text("flows-intro", "Excerpt of Table 1 — stable endpoints\nwith defined inputs, outputs and validation.", Box(2584, 817, 760, 62), pt=20, min_pt=18, color=c["muted"], parent="flows")
    p.text("flow-list", "phenotype_recommendation\nphenotype_make_computable\nconcept_sets_review\ncohort_critique_general_design\nworkflow_context_dialogue", Box(2584, 915, 760, 265), pt=23, min_pt=21, color=c["primary"], bold=True, parent="flows", line_factor=1.36)
    p.text("flows-foot", "Flows apply deterministic checks at each stage;\nrestricted outputs identify user-confirmable steps\nbefore consequential writes.", Box(2584, 1245, 760, 100), pt=21, min_pt=19, parent="flows")
    p.panel("screenshot-placeholder", Box(right.x, 1513, right.w, 705), fill=c["surface_muted"], stroke=c["rule"])
    p.text("placeholder-heading", "APPLICATION EVIDENCE", Box(2584, 1547, 760, 40), pt=28, min_pt=26, color=c["primary"], bold=True, parent="screenshot-placeholder")
    p.text("placeholder-icon", "□", Box(2584, 1618, 760, 140), pt=108, min_pt=90, color=c["accent"], align="middle", parent="screenshot-placeholder")
    p.text("placeholder-copy", "NO APPROVED AUTHENTIC SCREENSHOT\nAVAILABLE FOR THIS PUBLIC POSTER BUILD", Box(2584, 1788, 760, 69), pt=22, min_pt=20, color=c["warning"], bold=True, align="middle", parent="screenshot-placeholder")
    p.text("placeholder-detail", "Placeholder only — not a system interface or\nscientific evidence. Replace only with an approved\ndemo/repository artifact after source review.", Box(2584, 1892, 760, 95), pt=20, min_pt=18, color=c["muted"], align="middle", parent="screenshot-placeholder")
    # Bottom center, preserving a clear reading sequence.
    p.panel("workflow-example", Box(918, 1763, 1590, 455), fill="#FBFCFB", stroke=c["rule"])
    p.text("workflow-heading", "3  WORKFLOW-CONTEXTUAL GUIDANCE VIA /ohdsi", Box(958, 1796, 1510, 44), pt=29, min_pt=27, color=c["primary"], bold=True, parent="workflow-example")
    p.text("workflow-question-label", "EXAMPLE QUESTION", Box(958, 1865, 440, 28), pt=20, min_pt=18, color=c["accent"], bold=True, parent="workflow-example")
    p.text("workflow-question", "“How should I think about time at risk\nin this incidence design?”", Box(958, 1905, 670, 75), pt=25, min_pt=23, color=c["primary"], bold=True, parent="workflow-example")
    p.text("workflow-answer-label", "WHAT /ohdsi ADDS", Box(1710, 1865, 700, 28), pt=20, min_pt=18, color=c["accent"], bold=True, parent="workflow-example")
    p.text("workflow-answer", "The shell supplies workflow type, current step, active role,\nselected cohorts/artifacts and constraints. ACP returns a normalized\nresponse with step-specific guidance, cautions and next actions.", Box(1710, 1905, 720, 112), pt=21, min_pt=19, parent="workflow-example")
    p.text("workflow-caution", "The poster shows the contextual mechanism, not a fabricated literal LLM reply.", Box(958, 2070, 1470, 30), pt=19, min_pt=18, color=c["muted"], parent="workflow-example")
    # Footer provenance / constraints.
    p.panel("footer", Box(0, 2262, p.w, 330), fill=c["primary"], radius=0)
    p.text("footer-head", "INTERPRETATION, LIMITS & PROVENANCE", Box(72, 2295, 3312, 35), pt=23, min_pt=20, color="#A9DCD2", bold=True, parent="footer")
    p.text("footer-copy", "Architecture and functional-prototype report; not evidence of improved efficiency, decision accuracy, clinical safety or study outcomes.\nScientific source: supplied private manuscript. Design decisions: DESIGN_BRIEF.md. No patient-level data, credentials or authentic screenshot assets are included.",
           Box(72, 2342, 2525, 77), pt=20, min_pt=18, color="#FFFFFF", parent="footer")
    p.text("footer-refs", "Selected sources in supplied manuscript: Study Agent repository; SlashOhdsiStrategusAssistant; SlashOhdsiAcpClient;\nStudy Agent / Atlas3-WebAPI demonstrations. Verify URLs, branding and submission metadata before any public release.",
           Box(72, 2440, 2525, 63), pt=18, min_pt=18, color="#DCE9ED", parent="footer")
    p.text("footer-build", "EDITABLE SVG • 48 × 36 in • build.py + poster.toml\nNo QR destination supplied; none generated.", Box(2670, 2345, 642, 100), pt=19, min_pt=18, color="#FFFFFF", bold=True, align="end", parent="footer")
    svg_path = output_dir / config["outputs"]["svg"]
    p.d.saveas(str(svg_path))
    return svg_path, p


def render(svg: Path, config: dict, out: Path) -> None:
    subprocess.run(["inkscape", str(svg), "--export-filename", str(out / config["outputs"]["pdf"])], check=True)
    subprocess.run(["inkscape", str(svg), "--export-filename", str(out / config["outputs"]["png"]), "--export-dpi", "150"], check=True)
    proofs = out / "proofs"; proofs.mkdir(exist_ok=True)
    # SVG viewBox coordinates are points; Inkscape export areas are CSS pixels
    # (96 px/in, hence 4/3 px per SVG point). The crops name the actual panels.
    subprocess.run(["inkscape", str(svg), "--export-filename", str(proofs / "architecture-detail.png"), "--export-area", "1200:933:3375:2313", "--export-dpi", "220"], check=True)
    subprocess.run(["inkscape", str(svg), "--export-filename", str(proofs / "workflow-detail.png"), "--export-area", "1200:2350:3375:2957", "--export-dpi", "220"], check=True)


def validate_pdf_box(pdf: Path, width_pt: int, height_pt: int) -> dict:
    """Validate dimensions through Inkscape, avoiding PDF object-stream assumptions."""
    query = subprocess.run(["inkscape", str(pdf), "--query-width", "--query-height"],
                           check=True, text=True, capture_output=True)
    values = [float(value) for value in query.stdout.split()]
    # Inkscape reports SVG/CSS pixels: 96 pixels/inch, while SVG coordinates are points.
    expected_px = [width_pt * 96 / 72, height_pt * 96 / 72]
    return {"path": pdf.name, "media_box_expected_pt": [width_pt, height_pt],
            "renderer_size_px": values, "expected_size_px": expected_px,
            "media_box_found": len(values) == 2 and all(abs(a - b) < .01 for a, b in zip(values, expected_px))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=HERE / "build")
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    config = tomllib.loads((HERE / "poster.toml").read_text(encoding="utf-8"))
    content = json.loads((HERE / "content.json").read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)
    svg, poster = build_svg(config, args.out)
    report = poster.registry.preflight()
    report["canvas"] = {"width_pt": poster.w, "height_pt": poster.h, "width_in": poster.w / 72, "height_in": poster.h / 72}
    report["text"] = poster.text_entries
    report["font_minimum_violations"] = [x["key"] for x in poster.text_entries if x["pt"] < x["minimum_pt"]]
    report["connectors"] = poster.connector_entries
    report["unverified_scientific_statements"] = content["unverified_statements"]
    report["intended_overlaps"] = ["connector geometry may cross its parent architecture panel and participates in no sibling-collision finding"]
    report["renderer"] = {"svg": svg.name, "inkscape_command": "inkscape SVG --export-filename OUTPUT"}
    if not report["ok"] or report["font_minimum_violations"]:
        raise RuntimeError(json.dumps(report, indent=2))
    if not args.no_render:
        render(svg, config, args.out)
        report["pdf"] = validate_pdf_box(args.out / config["outputs"]["pdf"], int(poster.w), int(poster.h))
        if not report["pdf"]["media_box_found"]:
            raise RuntimeError("PDF MediaBox does not match 48 × 36 in page")
    (args.out / config["outputs"]["qa_report"]).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"svg": str(svg), "preflight": report["ok"], "components": report["component_count"]}, indent=2))


if __name__ == "__main__":
    main()
