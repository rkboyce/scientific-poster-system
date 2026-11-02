# Scientific poster SVG starter (prototype)

This is a **proof of concept** for the vector-first workflow, not a finalized template. It is not fitted to the user's final posters yet. All example text is synthetic.

## Ubuntu 22.04+ with uv

Install [uv](https://docs.astral.sh/uv/) if necessary, then:

```sh
uv sync
uv run poster-demo --out output/poster-wireframe.svg
uv run poster-demo --palette navy-orange --out output/alternate.svg
inkscape output/poster-wireframe.svg
inkscape output/poster-wireframe.svg --export-filename=output/poster-wireframe.pdf
```

Run `uv lock` on a computer with PyPI connectivity to create a lockfile, then commit it for reproducibility. The prototype pins `svgwrite==1.4.3` and `cairosvg==2.8.2` and supports Python 3.10+. `cairosvg` is optional for the core authoring script but useful for automated previews.

## Code structure

- `src/posterkit/demo.py`: physical-size SVG canvas, palette/style objects, and reusable layout functions
- `output/poster-wireframe.svg`: generated 36 x 48 inch sample
- `output/poster-wireframe.png`: generated low-resolution preview

SVG coordinates use **points (72 per inch)**. Text sizes are therefore in conventional typographic points. Edits to `Palette` and `Style` change the theme independently of layout. SVG remains editable in Inkscape.

## Next iteration after receiving final posters

1. Extract measured fonts, positions, whitespace, and graphic proportions from approved final posters.
2. Replace this loose prototype with reusable sections driven by a YAML or TOML poster specification.
3. Add precise text measurement (Pango), automatic layout preflight, print-scale previews, and comparison against source designs.
4. Add standalone figure workflows (Graphviz, SVG, PDF).

**Important:** SVG does not guarantee perfect line wrapping or font portability. This prototype uses explicit line breaks, so labels and paragraphs must be composed for their boxes. Fonts must be installed locally and their final rendered appearance checked in Inkscape. Production export should be tested in SVG and PDF.
