"""Reproducible Study Agent v0.3 landscape concept wireframe.
Run: uv run python posters/study-agent-ohdsi/make_wireframe.py
Canvas: 48 x 36 inches. Concept design, not scientific final artwork.
"""
from pathlib import Path
import math
import subprocess
import argparse
import svgwrite

ROOT = Path(__file__).resolve().parent
NAVY = "#17374A"
TEAL = "#16796F"
MINT = "#5ABE9A"
CREAM = "#F4F1E9"
INK = "#243846"
MUTED = "#55727B"
LINE = "#C8D7D5"
WHITE = "#FFFFFF"


def build(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    d = svgwrite.Drawing(str(path), size=("48in", "36in"),
                         viewBox="0 0 1440 1080")
    d.add(d.rect(insert=(0, 0), size=(1440, 1080), fill=WHITE))

    def rect(x, y, w, h, fill, stroke="none", radius=0):
        d.add(d.rect(insert=(x, y), size=(w, h), rx=radius,
                     fill=fill, stroke=stroke, stroke_width=1.4))

    def text(x, y, value, size=18, color=INK, bold=False, anchor="start"):
        d.add(d.text(value, insert=(x, y), font_family="DejaVu Sans",
                     font_size=size, fill=color,
                     font_weight="bold" if bold else "normal",
                     text_anchor=anchor))

    def lines(x, y, content, size=17, step=26, color=INK):
        for i, value in enumerate(content):
            text(x, y + i*step, value, size, color)

    def panel(x, y, w, h, heading):
        rect(x, y, w, h, "#FBFCFB", LINE, 9)
        text(x+17, y+34, heading, 21, NAVY, True)
        rect(x+17, y+45, w-34, 2, MINT)

    def arrow(x1, y1, x2, y2, *, length=12, width=10, clearance=5):
        """Explicit direction-normalized arrowhead; avoids SVG marker glitches."""
        dx, dy = x2-x1, y2-y1
        distance = math.hypot(dx, dy)
        if distance <= length+clearance+2:
            raise ValueError("Arrow connector too short")
        ux, uy = dx/distance, dy/distance
        tip = (x2-clearance*ux, y2-clearance*uy)
        base = (tip[0]-length*ux, tip[1]-length*uy)
        normal = (-uy, ux)
        g = d.g(**{"class": "arrow-connector"})
        g.add(d.line(start=(x1,y1), end=base, stroke=TEAL,
                     stroke_width=3.7, stroke_linecap="round"))
        g.add(d.polygon([tip,
            (base[0]+normal[0]*width/2,base[1]+normal[1]*width/2),
            (base[0]-normal[0]*width/2,base[1]-normal[1]*width/2)],
            fill=TEAL))
        d.add(g)

    rect(0, 0, 1440, 145, NAVY)
    text(720, 50, "OHDSI Study Agent for Human–AI Team-Based",
         32, WHITE, True, "middle")
    text(720, 94, "Real-World Evidence Generation in the VHA",
         32, WHITE, True, "middle")
    text(720, 125, "Richard D. Boyce, PhD   |   University of Pittsburgh   •   VA VINCI",
         17, "#DCE9ED", anchor="middle")
    rect(17, 164, 1406, 118, "#E4F3EF", LINE, 8)
    text(45, 203, "Study Agent offers reusable, governed AI support for OHDSI research workflows",
         27, NAVY, True)
    lines(46, 239, ["Service-based ACP/MCP coordination + deterministic validation; researcher confirmation remains central."], 17, 24, MUTED)

    panel(17, 304, 322, 636, "WHY / GOVERNANCE")
    lines(36, 384, ["RWE study design involves linked", "judgments about phenotypes,",
                    "causal assumptions, cohorts,", "and interpretation."], 18, 28)
    rect(35, 505, 285, 3, MINT)
    text(36, 547, "RESEARCHER CONTROL", 17, TEAL, True)
    lines(36, 584, ["Confirmations and stage gates", "constrain consequential steps.",
                    "Model inputs use sanitized", "summaries and metadata,",
                    "not row-level clinical data."], 17, 28)
    text(36, 770, "PROTOTYPE MATURITY", 17, TEAL, True)
    lines(36, 805, ["~TRL 4–5 (report estimate)", "Scripted demonstration workflows",
                    "No comparative effectiveness", "or decision-accuracy results"], 16, 26)

    panel(357, 304, 714, 445, "1  SERVICE-BASED ARCHITECTURE")
    text(375, 369, "Multiple clients access shared services", 17, MUTED)
    clients = [(377,206,"R / Strategus","Client shells"),
               (601,207,"Atlas3 / WebAPI","Early-stage integration"),
               (827,222,"Coding agents","Skills.md interface*")]
    for x,w,label,sub in clients:
        rect(x,390,w,74,CREAM,LINE,7)
        text(x+10,421,label,17,NAVY,True)
        text(x+10,447,sub,14,MUTED)
    rect(485,511,440,84,"#D9F0E8",TEAL,8)
    text(503,543,"ACP server: orchestration + governance",19,NAVY,True)
    text(503,567,"Named flows • state • routing • confirmations",15,INK)
    for x in (475,706,930):
        arrow(x,468,706,509)
    rect(388,641,311,79,"#EEF2FA",LINE,7)
    text(407,672,"MCP servers",19,NAVY,True)
    text(407,697,"Tool contracts • prompt bundles",15,INK)
    rect(714,641,337,79,"#EEF2FA",LINE,7)
    text(732,672,"Deterministic core",19,NAVY,True)
    text(732,697,"Validation • constrained transforms",15,INK)
    arrow(659,598,544,637)
    arrow(785,598,874,637)
    text(380,741,"* Coding-agent integration: additional design context; verify before publication.",12,MUTED)

    panel(1089,304,334,445,"2  SUPPORTED FLOWS")
    lines(1107,381,["phenotype_recommendation",
                     "phenotype_make_computable",
                     "concept_sets_review",
                     "cohort_critique_general_design",
                     "workflow_context_dialogue"],15,43)
    rect(1106,611,299,108,"#E4F3EF",LINE,7)
    lines(1122,646,["OHDSI deterministic code can be",
                     "reused through bounded flows;",
                     "specific integrations to verify."],16,27)
    panel(357,769,514,171,"3  WORKFLOW CONTEXT + EXAMPLE")
    lines(377,834,["“How should I think about time at risk?”",
                    "/ohdsi uses incidence-study stage, role, and",
                    "selected artifacts to return contextual guidance."],15.5,26)
    panel(890,769,533,171,"4  DEMONSTRATIONS + EVALUATION")
    lines(908,834,["R Strategus prototype; early Atlas3/WebAPI support.",
                    "Screenshot slot: authentic demo asset required.",
                    "Needs larger validation of accuracy, utility and reliance."],15.5,26)
    rect(0,958,1440,122,CREAM)
    text(27,994,"EXHIBITS / HANDOFF",16,TEAL,True)
    lines(27,1024,["Next: verified architecture diagram; compact named-flow table; authentic application screenshot.",
                    "Unverified: coding-agent support and precise OHDSI code reuse. No outcome claims."],15,23)
    text(1406,1058,"DESIGN WIREFRAME v0.3 • NOT FINAL POSTER",14,MUTED,anchor="end")
    d.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path,
                        default=ROOT/"study-agent-wireframe.svg")
    parser.add_argument("--export", action="store_true",
                        help="Also export PDF and PNG with Inkscape")
    args = parser.parse_args()
    build(args.out)
    if args.export:
        for ext, extra in (("pdf", []), ("png", ["--export-width=1800"])):
            subprocess.run(["inkscape",str(args.out),*extra,
                "--export-filename="+str(args.out.with_suffix("."+ext))],
                check=True)
    print(args.out)


if __name__ == "__main__":
    main()
