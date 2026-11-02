# Evidence section integration proof

The new `src/posterkit/evidence_section.py` creates an editable SVG panel combining a measured heading, a native-SVG horizontal bar chart, a caption and interpretation text. It uses `composition.py` for preferred heights, nested component registration and bounding-box preflight.

On Ubuntu 22.04+:

```bash
sudo apt update
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 fonts-open-sans fontconfig inkscape
uv sync
uv run python -m posterkit.evidence_section --out output/evidence-section.svg
uv run --with pytest pytest -q tests/test_layout.py tests/test_composition.py tests/test_evidence_section.py
inkscape output/evidence-section.svg --export-filename=output/evidence-section.pdf
```

**All numbers and labels in the example are synthetic.** This is not a scientific result. The proof sheet is 20 x 12 inches, not a final poster. The generated component maintains a parent panel, four allocated child bounds and nested SVG group IDs. It fails rather than shrinking text for an undersized region. Individual chart marks and actual rendered glyph bounds are not independently checked. The fixed 300 pt chart height can produce unused vertical space; row-aware sizing and more robust line wrapping remain subsequent improvements.
