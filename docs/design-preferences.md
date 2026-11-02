# Scientific Poster Design Preferences

**Version:** 0.1 (draft)  
**Date:** 2026-11-02  
**Reference designs:** The two final AMIA 2026 posters supplied in the Scientific Poster Sandbox project.

## 1. Design principles

- **Lead with the science.** State one defensible, memorable takeaway; make primary evidence prominent and methods concise but sufficient.
- **Poster 2.0 is a guide, not a rigid template.** Support large takeaways, clear reading paths and evidence-first composition while adapting to qualitative, quantitative, system-design and usability studies.
- **Maintain scientific fidelity.** Distinguish exploratory findings from confirmatory evidence, show denominators and uncertainty, preserve quotations, and make key limitations visible.
- **Readability is a constraint.** Do not automatically reduce font size to force content into fixed boxes; edit text or change geometry instead.
- **Use space deliberately.** Keep related content together, avoid collisions and accidental whitespace, and preserve clean alignment.
- **Prefer reproducible vector assets.** Use SVG as the primary source, PDF as the print deliverable, and editable scripts for charts and diagrams.
- **Inspect the output.** Check both whole-poster composition and close-range text/figure legibility after final rendering.

## 2. Reference conventions

The two completed AMIA posters share a 36 × 48-inch portrait canvas, centered title/author/affiliation area in a dark full-width banner, a large left-hand takeaway panel, thin accent rules, restrained warm-neutral surfaces, central emphasis on scientific evidence, a bottom interpretation/limitations band, and compact branding/funding/reference/QR information.

Their content differs by study:
- The qualitative interview poster emphasizes three theme cards, verbatim quotations, and coded-subcategory counts.
- The CBD-CDS system poster emphasizes authentic SMART-on-FHIR screenshots, clinical decision algorithms, and cautious presentation of formative usability measures.

**Do not copy visible flaws in the reference PDFs** (crowded author text, awkward wrapping or clipped quotations). They provide design direction, not pixel-perfect specifications.

## 3. Layout system

- Configure physical canvas dimensions and orientation per venue; 36 × 48-inch portrait is an AMIA reference, not a global default.
- Center title text visually; reserve adequate height for title, authors, affiliations and logos.
- Use a prominent high-contrast takeaway, generally left of evidence, with subordinate background, objective and study-at-a-glance information when appropriate.
- Establish grid, margins, gutters and proportional column widths before filling components.
- Allocate space according to figure complexity and readable type sizes; do not mandate equally sized decision trees or screenshots.
- Place figure captions close to figures and avoid duplicating captions as body prose.
- Leave secondary references and branding in the footer without making them illegible.

## 4. Typography

Preferred families: **Open Sans** or **Fjalla One** for large headings; **Karla**, **Franklin Gothic FS**, or **Lato** for body copy; **Futura** as an optional alternative. Use installed fonts and record fallbacks. Never distribute proprietary font files. Use LaTeX-derived vector output for mathematical expressions when useful.

Initial 36 × 48-inch targets (subject to design approval, not measurements taken from the final posters):

| Role | Proposed size |
| --- | --- |
| Poster title | 68–80 pt |
| Main takeaway | 55–72 pt |
| Section headings | 38–48 pt |
| Main body | 28–36 pt |
| Figure labels | 22–30 pt |
| References | 18–24 pt |

Set per-poster minimum text sizes. Measure text with the actual font and renderer, support deliberate line breaks, and issue warnings for overflow or text below minima.

## 5. Colors and themes

**Palettes vary with the scientific topic.** The AMIA poster palette is a reusable *preset*, not a required default:

- Dark navy: `#16384C` / `#183849`
- Dark green: `#1D732B`
- Light green: `#6AC181`
- Dark khaki: `#686758`
- Oatmeal: `#ABA588`
- Sand: `#EADDC5`
- White or warm off-white paper

Expose semantic tokens such as `primary`, `accent`, `surface`, `surface_muted`, `text`, `text_inverse` and `rule` in TOML/YAML configuration. Maintain sufficient contrast and avoid encoding categorical differences in color alone.

## 6. Reusable components

- Centered full-width title/author/affiliation header
- Main takeaway/sidebar, background and objective
- Section header and accent rule
- Qualitative findings card and quotation inset
- Quantitative/statistical summary and comparative chart
- Screenshot with enlargements/callouts
- Decision tree or system architecture diagram
- Methods and limitations blocks
- Interpretation/implications strip
- Funding, references, institution logo and manuscript QR footer

Components should expose position, content and dimensions while reporting measured bounds and overflow. Resizing must not silently shrink type.

## 7. Scientific-figure conventions

- Keep original diagrams and screenshots available for comparison.
- Prefer scripted Graphviz SVG for directed decision trees; verify every decision node, edge and Yes/No outcome against source.
- Prefer SVG chart export with data/units/denominators/uncertainty clearly labeled.
- Present authentic application screenshots; use readable crops or callouts rather than inventing interface content.
- When coding qualitative data, distinguish **number of interview files** from **number of coded references**.
- Deliver reproducible source files alongside SVG figure assets.

## 8. Production workflow

1. Review manuscripts, abstracts, scientific figures, conference instructions and institutional requirements.
2. Identify scientific takeaway, evidence priorities, claims/limitations; ask a few consequential questions.
3. Produce a low-fidelity SVG wireframe and agree on overall area allocation.
4. Independently generate and review scientific figures as editable SVG.
5. Compose a full-size SVG using a project-specific palette, font choices and layout.
6. Render SVG to PDF and PNG, and inspect overview and high-resolution detail crops.
7. Run preflight checks; correct clipping, collisions, subminimum text, low-resolution assets and mismatched physical dimensions.
8. Deliver SVG, PDF, preview PNG, scripts, configuration, uv dependency lock and a short QA report.
9. Compare the user-edited final poster with the draft and incorporate validated improvements.

## 9. Technical environment

- **OS:** Ubuntu 22.04 or newer
- **Python:** managed using **uv**; commit `pyproject.toml` and generated `uv.lock`
- **Primary authoring:** Python + `svgwrite`, revisiting alternatives if layout complexity requires it
- **Typography:** evaluate Pango for accurate font measurements
- **Other tools:** Graphviz for decision logic, Matplotlib for plotted graphics, LaTeX for equations, Inkscape for editing/export
- **Outputs:** SVG source and print PDF; ODG/PPTX only when needed
- Keep paths portable, source assets versioned and content metadata separate from drawing code.

## 10. Preflight / acceptance criteria

Automated where feasible: correct physical dimensions, text and asset bounds inside canvas, no unintended overlap, min font compliance, resolved assets, raster effective PPI, valid QR target, and correct PDF page box.

Human-reviewed: title/affiliations centered and readable, main takeaway visible at distance, evidence hierarchy unmistakable, diagrams/quotes legible, no awkward wrapping or large accidental voids, factual claims faithful to manuscript, and SVG/PDF visual equivalence.

## 11. Open questions

- Measure recurring geometry and typography more precisely from the final posters without reproducing their defects.
- Agree on font availability/fallbacks for the user's Ubuntu installation.
- Decide initial support for landscape and unusual conference dimensions.
- Define hard font minima and a consistent print-proof method.
- Add a reusable preflight CLI plus SVG/PDF comparison tests.

*This is a living design preference specification, not an inflexible branding standard.*
