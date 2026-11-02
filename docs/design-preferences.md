# Scientific Poster Design Preferences

**Version:** 0.3 (draft)  
**Date:** 2026-11-02  
**Reference designs:** The two final AMIA 2026 posters supplied in the Scientific Poster Sandbox project.

## 1. Design principles

- **Lead with the science.** State one defensible, memorable takeaway; make primary evidence prominent and methods concise but sufficient.
- **Poster 2.0 is a guide, not a rigid template.** Support large takeaways, clear reading paths and evidence-first composition while adapting to qualitative, quantitative, system-design and usability studies.
- **Maintain scientific fidelity.** Distinguish exploratory findings from confirmatory evidence, show denominators and uncertainty, preserve quotations, and make key limitations visible. The following are **study-specific defaults to consider, not universal requirements**:
  - **Qualitative studies:** Present primary themes, representative quotations, and an overview of subthemes by interview, observation, or other data source, when informative. Distinguish the number of files containing a code from the number of coded references.
  - **Quantitative epidemiology:** Prioritize population/cohort characteristics, primary estimates with uncertainty, and appropriate comparisons. Show an inclusion/exclusion cohort flow when relevant; a PRISMA flowchart specifically serves evidence reviews and should not be assumed for every observational study.
  - **System design/usability:** Prioritize authentic screenshots and suitable architecture, knowledge artifacts, and decision algorithms, alongside evaluation results. Distinguish feasibility, usability/satisfaction, efficiency, decision accuracy, and clinical effectiveness.
  - Each poster requires focused planning based on the scientific contribution and the venue.

- **Readability is a constraint.** Do not automatically reduce font size to force content into fixed boxes; edit text or change geometry instead.
- **Use space deliberately.** Keep related content together, avoid collisions and accidental whitespace, and preserve clean alignment.
- **Prefer reproducible vector assets.** Use SVG as the primary source, PDF as the print deliverable, and editable scripts for charts and diagrams.
- **Inspect the output.** Check both whole-poster composition and close-range text/figure legibility after final rendering.

## 2. Reference conventions

The two completed AMIA posters share a 36 × 48-inch portrait canvas, centered title/author/affiliation area in a dark full-width banner, a large left-hand takeaway panel, thin accent rules, restrained warm-neutral surfaces, central emphasis on scientific evidence, a bottom interpretation/limitations band, and compact branding/funding/reference/QR information.

Their content differs by study:
- The qualitative interview poster emphasizes three theme cards, verbatim quotations, and coded-subcategory counts.
- The CBD-CDS system poster emphasizes authentic SMART-on-FHIR screenshots, clinical decision algorithms, and cautious presentation of formative usability measures.

Poster formatting requirements imposed by the venue override this document's defaults. 

**Do not copy visible flaws in the reference PDFs** (crowded author text, awkward wrapping or clipped quotations). They provide design direction, not pixel-perfect specifications.

## 3. Layout system

- Configure physical canvas dimensions and orientation per venue; 36 × 48-inch portrait is an AMIA reference, not a global default.
- Center title text visually; reserve adequate height for title, authors, affiliations and logos.
- Use a prominent high-contrast takeaway, generally left of evidence, with subordinate background, objective and study-at-a-glance information when appropriate.
- Establish grid, margins, gutters and proportional column widths before filling components.
- Allocate space according to figure complexity and readable type sizes; do not mandate equally sized decision trees or screenshots.
- Place figure captions close to figures and avoid duplicating captions as body prose.
- Leave secondary references and branding in the footer without making them illegible.
- Maintain a versioned, **selectable** library of institutional and organizational logos, potentially including University of Pittsburgh, UT Southwestern, the U.S. Department of Veterans Affairs (VA), and the VA Informatics and Computing Infrastructure (VINCI). Record approved source, reuse permissions, current branding guidelines, and light/dark variants; inclusion in the library does not imply authorization for a particular poster.
- During project intake, ask about applicable funding/grant acknowledgments, institutional branding, IRB approval, exemption, or other determination (if applicable), and contact/QR destination. Do not assume every study has an IRB determination or grant.

## 4. Typography

Preferred families: **Open Sans** or **Fjalla One** for large headings; **Karla**, **Franklin Gothic FS**, or **Lato** for body copy; **Futura** as an optional alternative. Use installed fonts and record fallbacks. Never distribute proprietary font files. Use LaTeX-derived vector output for mathematical expressions when useful. Code listings should use a monospaced font and language-appropriate syntax highlighting; see Section 8. 

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

Institutional palette presets, including a potential UT Southwestern theme, should be based on current authoritative brand guidance and applied only when appropriate to the poster's purpose. 

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

## 8. Code listings and technical text

Use code when it contributes to the scientific argument: a computational method, analysis decision, API interaction, implementation pattern, or algorithm. Avoid decorative listings or oversized excerpts.

**Authoring and generation**
- Treat a UTF-8 source file or fenced Markdown block with an explicit language identifier (Python, R, SQL, shell, etc.) as the source of truth.
- Start with **Pygments** syntax highlighting and its SVG formatter to produce selectable vector text; verify its sizing and rendering in Inkscape and exported PDF before adopting it for production.
- Use installed monospaced fonts such as DejaVu Sans Mono or Liberation Mono, with per-poster minimum font sizes. Do not distribute restricted fonts.
- Optionally use **markdown-it-py** when broader Markdown parsing is actually needed. Render parsed content into native SVG components; avoid HTML `foreignObject` or browser rendering as a required production dependency.
- Retain **LaTeX** for equations, mathematical notation, and pseudocode where it communicates more clearly than source code.

**Visual and content constraints**
- Prefer short, meaningful excerpts (typically 5–15 lines) with an optional language/file label; point to complete, versioned code by a link or QR when useful.
- Coordinate syntax token colors with the poster palette, maintain contrast, and do not rely on syntax color alone.
- Preserve exact indentation, operators, punctuation, line breaks, and Unicode. Never auto-wrap code; shorten the excerpt or mark any omitted lines explicitly.
- Show line numbers only when useful. Highlight a few crucial lines rather than including decorative IDE chrome.
- Do not silently shrink or rasterize code to fit. Keep code selectable in SVG where practicable.
- Check public excerpts for secrets, tokens, PHI, sensitive endpoints, and intellectual-property or licensing restrictions.

**Planned reusable component:** `CodeListing(source, language, font_family, font_size, palette, line_numbers, highlight_lines, title, caption, width, height)` should return a standalone SVG and measured bounds/overflow diagnostics. If the Pygments SVG formatter is insufficient for precise dimensions, build a token-to-SVG renderer using Pango font measurement.

**Preflight:** Validate declared language, syntax coloring, indentation and line integrity, minimum type size, no wrapping/clipping, print-scale readability, and publication safety.

## 9. Production workflow

1. Review manuscripts, abstracts, scientific figures, conference instructions and institutional requirements.
2. Identify scientific takeaway, evidence priorities, claims/limitations; ask a few consequential questions.
3. Produce a low-fidelity SVG wireframe and agree on overall area allocation.
4. Independently generate and review scientific figures as editable SVG.
5. Compose a full-size SVG using a project-specific palette, font choices and layout.
6. Render SVG to PDF and PNG, and inspect overview and high-resolution detail crops.
7. Run preflight checks; correct clipping, collisions, subminimum text, low-resolution assets and mismatched physical dimensions.
8. Deliver SVG, PDF, preview PNG, scripts, configuration, uv dependency lock and a short QA report.
9. Compare the user-edited final poster with the draft and incorporate validated improvements.

## 10. Technical environment

- **OS:** Ubuntu 22.04 or newer
- **Python:** managed using **uv**; commit `pyproject.toml` and generated `uv.lock`
- **Primary authoring:** Python + `svgwrite`, revisiting alternatives if layout complexity requires it
- **Typography:** evaluate Pango for accurate font measurements
- **Other tools:** Graphviz for decision logic, Matplotlib for plotted graphics, LaTeX for equations, Inkscape for editing/export
- **Code-listing tools:** Start with `uv add pygments` after the SVG rendering experiment; add `markdown-it-py` only when broader Markdown parsing is needed. Commit tested `pyproject.toml` and `uv.lock` changes; avoid making a browser-based Markdown-to-image pipeline mandatory.
- **Outputs:** SVG source and print PDF; ODG/PPTX only when needed
- Keep paths portable, source assets versioned and content metadata separate from drawing code.

## 11. Preflight / acceptance criteria

Automated where feasible: correct physical dimensions, text and asset bounds inside canvas, no unintended overlap, min font compliance, resolved assets, raster effective PPI, valid QR target, correct PDF page box, and code-listing integrity (indentation, source fidelity, syntax/language choice, and clipping).

Human-reviewed: title/affiliations centered and readable, main takeaway visible at distance, evidence hierarchy unmistakable, diagrams/quotes/code legible at print size, no awkward wrapping or large accidental voids, factual claims faithful to manuscript, SVG/PDF visual equivalence, and absence of secrets/PHI or unlicensed code excerpts.

## 12. Open questions

- Measure recurring geometry and typography more precisely from the final posters without reproducing their defects.
- Agree on font availability/fallbacks for the user's Ubuntu installation.
- Decide initial support for landscape and unusual conference dimensions.
- Define hard font minima and a consistent print-proof method.
- Add a reusable preflight CLI plus SVG/PDF comparison tests.
- Prototype a `CodeListing` with Python, R and SQL examples; compare its Inkscape SVG and exported PDF at realistic poster sizes before promoting it to production.

*This is a living design preference specification, not an inflexible branding standard.*
