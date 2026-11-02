# posterkit reusable layout prototype

This is an **experimental partial poster** based on the AMIA qualitative poster. It intentionally leaves unused areas because the test is about trustworthy text placement, not complete composition.

## Ubuntu 22.04+ prerequisites

```bash
sudo apt update
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 fonts-open-sans fonts-lato fontconfig inkscape
```

Inside the existing scientific-poster-system repository after copying `src/posterkit/layout.py` and `src/posterkit/header_demo.py`:

```bash
uv sync
uv run python -m posterkit.header_demo --out output/header-layout.svg
inkscape output/header-layout.svg --export-filename=output/header-layout.pdf
uv run --with pytest pytest -q tests/test_layout.py
```

The code uses installed Pango via ctypes and therefore adds no Python dependency; it uses the repository's existing `svgwrite`. The output JSON includes measured text rectangles and preflight results. The sample contains no claims beyond supplied reference-poster text, but publication metadata is abbreviated for a design test.

## Current behavior

- Pango-measured dimensions and no unexpected wrapping at the configured point size.
- Explicit minimum font size; no automatic downsizing.
- Inkscape-editable SVG text groups with stable IDs.
- Checks for canvas out-of-bounds and collisions among registered text rectangles.
- 4 automated tests including intended overlap/overflow failures.

## Limitations

- SVG rendering and Pango measurement may differ on fallback fonts or more complicated scripts; requires review in Inkscape.
- This detects *registered text rectangle* overlaps, not all SVG shape/text overlaps (intentional background overlaps are excluded).
- Manual explicit line breaks remain necessary for deterministic layout; Pango-based line breaking and bidi rendering would be later improvements.
- Supports Unix/Linux system Pango library names only.


## Component-aware composition experiment

The branch also provides `src/posterkit/composition.py`, a first step toward
content-driven poster layout. It uses the existing Pango measurement layer and
adds:

- `ComponentRegistry`: registers panels, text, and figures by bounding box,
  validates parent containment, and rejects unintended sibling collisions.
- `TextSpec`: reports preferred height for a specified width, font size, and
  minimum size; it never silently reduces the requested type size.
- `FixedSpec`: supports figures/screenshots with a specified height and minimum.
- `VerticalStack`: positions components vertically using their measured
  preferred heights and rejects overflow.

Run the new and original tests:

```bash
uv run --with pytest pytest -q tests/test_layout.py tests/test_composition.py
```

A component must explicitly register its geometry for collision checking; this
is **not** arbitrary SVG path intersection testing. Decorative backgrounds
should be registered as parents of their child content. `VerticalStack`
calculates bounds but does not yet produce a completed poster by itself.
Pango measurements can differ slightly from Inkscape rendering, so PDF and SVG
visual inspection remains necessary.
