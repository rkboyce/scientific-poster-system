# Study Agent OHDSI poster build

This directory produces a 48 × 36-inch landscape SVG poster for a hypothetical OHDSI symposium. It is an architecture/functional-prototype communication artifact, not evidence of efficiency, decision accuracy, clinical safety, or improved study outcomes.

## Reproduce

On Ubuntu 22.04 or newer, install these system packages (or their distribution equivalents): `python3`, `python3-venv`, `libpango-1.0-0`, `libpangocairo-1.0-0`, `fonts-open-sans`, and `inkscape`. `poppler-utils` is useful for independent PDF inspection but is not required by the build script.

From the repository root:

```sh
uv sync --locked
uv run python posters/study-agent-ohdsi/build.py
uv run pytest
```

The one-command poster build is:

```sh
uv run python posters/study-agent-ohdsi/build.py
```

It writes the editable SVG, print PDF, 150-DPI full-poster PNG, two 220-DPI zoomed QA proofs, and `preflight-report.json` under `posters/study-agent-ohdsi/build/`.

The PDF renderer command used by the build is `inkscape INPUT.svg --export-filename=OUTPUT.pdf`; the PNG proof uses the same renderer. The build validates the expected PDF MediaBox of 3456 × 2592 pt (48 × 36 in). Inkscape diagnostics about the accessibility bus in headless environments are non-fatal and do not affect output.

## Inputs and provenance

| Input | Role | Publication status |
| --- | --- | --- |
| `DESIGN_BRIEF.md` | Approved direction and claim boundaries | Versioned |
| `CODEX_HANDOFF.md` | Build, privacy, and acceptance instructions | Versioned |
| `content.json` | Claim/provenance and unverified-statement inventory | Versioned |
| `poster.toml` | Physical size, palette, typography, output names | Versioned |
| `figures.py` | Native SVG architecture connectors with explicit polygons | Versioned |
| `134-Boyce-…-REPORT.pdf` | Authoritative scientific source | Private/local only; ignored by Git |

The local private manuscript used for source checking had SHA-256 `914de30a03b80bdcdcdfaa3e97a11725d7c2f75f007f9641468106bd8326597b`. It is deliberately excluded by `.gitignore` and must never be added without explicit permission.

The locked Python dependency file SHA-256 is `5e65ca9bfc33db9b92929fd6e2f489296232596cb8730d00a8ea4d7709daa024`; see the checked-in `uv.lock` for exact Python package versions. The source tree’s intended font family is Open Sans (the tested local `fc-match` resolved `OpenSans-Regular.ttf`); the configured fallback is DejaVu Sans. This build was checked with Inkscape `1.2.2 (b0a8486541, 2022-12-01)`. Record the tested Git SHA and package revisions in the release review, because this branch is intentionally not release-tagged without researcher approval.

## QA scope

`preflight-report.json` records canvas/component bounds, sibling-overlap findings, declared text sizes and minima, explicit connector geometry/clearance, intended overlaps, and unverified scientific statements. `tests/test_study_agent_poster.py` checks diagonal and orthogonal polygon-arrow geometry plus a no-render SVG build. The full test suite and renderer test should be rerun before publication.

Manual review still required: inspect the full PNG plus `proofs/architecture-detail.png` and `proofs/workflow-detail.png` at print scale; confirm author/affiliation text, institutional marks, venue requirements, URLs, public-release permissions, and any replacement authentic screenshots. No QR code is generated because a verified destination was not supplied.

## Difference log from a PPTX-style workflow

This build has no prior PPTX source to compare. Relative to a manual slide workflow, the reproducible repair is structural: physical page size is defined in `poster.toml`; all architecture boxes, labels, and arrowheads are editable SVG; connector shafts end at explicit polygon-arrow bases; Pango rejects silent text shrink/wrap; and output dimensions, component bounds, collisions, font minima, and claim uncertainty are captured in machine-readable QA.
