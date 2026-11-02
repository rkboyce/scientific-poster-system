# Scientific poster SVG starter (prototype)

This is a **proof of concept** for the vector-first workflow, not a finalized template. It is not fitted to the user's final posters yet. All example text is synthetic.

## Ubuntu 22.04+ with uv

Install the Ubuntu system dependencies first (tested package names for Ubuntu 22.04):

```bash
sudo apt update
sudo apt install -y \\
  inkscape graphviz poppler-utils \\
  texlive-latex-base texlive-latex-extra texlive-fonts-recommended \\
  fonts-dejavu-core fontconfig
```

Install [uv](https://docs.astral.sh/uv/) separately if needed; it is not assumed to be available from the Ubuntu 22.04 apt repositories. Then:

```sh
uv sync
uv run poster-demo --out output/poster-wireframe.svg
uv run poster-demo --palette navy-orange --out output/alternate.svg
inkscape output/poster-wireframe.svg
inkscape output/poster-wireframe.svg --export-filename=output/poster-wireframe.pdf
```

Run `uv lock` on a computer with PyPI connectivity to create a lockfile, then commit it for reproducibility. The prototype pins `svgwrite==1.4.3` and `cairosvg==2.8.2` and supports Python 3.10+. `cairosvg` is optional for the core authoring script but useful for automated previews.

## Code listings, LaTeX, and font-aware layout experiment

The layout experiment is in `experiments/layout_components.py` and uses Python dependencies managed by `uv`; system dependencies are installed with the `apt` command above.

```bash
uv sync
uv run python experiments/layout_components.py
inkscape output/layout-components.svg
```

The components demonstrate non-shrinking text measurement, syntax-colored native SVG tokens for Python and R, LaTeX-to-PDF-to-SVG conversion, and an intentionally failing overflow test. The sample export is an **18 × 12-inch proof sheet**, not a final poster. Font measurement uses Pillow/FreeType as an initial step, **not yet Pango**; exact shaping and sophisticated multilingual layout still require a Pango-based implementation. LaTeX text becomes vector glyph artwork; edit equations in their `.tex` source.

## Code structure

- `src/posterkit/demo.py`: physical-size SVG canvas, palette/style objects, and reusable layout functions
- `output/poster-wireframe.svg`: generated 36 x 48 inch sample
- `output/poster-wireframe.png`: generated low-resolution preview
- `experiments/layout_components.py`: exploratory text, code, and equation components with preflight checks

SVG coordinates use **points (72 per inch)**. Text sizes are therefore in conventional typographic points. Edits to `Palette` and `Style` change the theme independently of layout. SVG remains editable in Inkscape.

## Next iteration after receiving final posters

1. Extract measured fonts, positions, whitespace, and graphic proportions from approved final posters.
2. Replace this loose prototype with reusable sections driven by a YAML or TOML poster specification.
3. Add precise text measurement (Pango), automatic layout preflight, print-scale previews, and comparison against source designs.
4. Add standalone figure workflows (Graphviz, SVG, PDF).

**Important:** SVG does not guarantee perfect line wrapping or font portability. This prototype uses explicit line breaks, so labels and paragraphs must be composed for their boxes. Fonts must be installed locally and their final rendered appearance checked in Inkscape. Production export should be tested in SVG and PDF.
