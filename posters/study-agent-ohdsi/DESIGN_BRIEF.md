# Study Agent poster — scientific design brief v0.3

**Status:** Approved direction for first Codex build, still subject to scientific review.  
**Format:** Hypothetical OHDSI symposium, 48 × 36 inches (landscape).  
**Source manuscript:** *OHDSI Study Agent for Human-AI Team-Based Real-World Evidence Generation in the Veterans Health Administration*, Richard D. Boyce. The source PDF is private/local and must **not** be committed to this public repository.

## Central takeaway

**Study Agent offers reusable, governed AI support for OHDSI research workflows, combining service-based ACP/MCP coordination with deterministic validation while researchers remain accountable for decisions.**

This is a prototype/architecture claim, **not** an established efficacy, clinical safety, or efficiency outcome.

## Scientific emphases and relative allocation

- **Researcher oversight:** Explicit confirmations, routing, stage gates, auditable validated outputs; PII/PHI sanitation is fail-closed where applicable. Manuscript says row-level clinical data are **not sent to the generative model**, not that the wider system never accesses such data.
- **Service-based architecture (4/5):** Show multiple clients leveraging shared services. Manuscript: R/Strategus and early Atlas3/WebAPI integration. User-provided additional context: coding agents with Skills.md; verify exact present implementation before claiming as demonstrated.
- **Named governed flows (4/5):** Prioritize a selected set from manuscript Table 1: `phenotype_recommendation`, `phenotype_make_computable`, `concept_sets_review`, `cohort_critique_general_design`, `workflow_context_dialogue`. Indicate that table is excerpted, not exhaustive.
- **Prototype maturity/limitations (4/5):** Early functional prototype, manuscript estimates TRL ~4–5; scripted lab demos; user value, decision accuracy, calibrated reliance, and comparative outcomes remain to be evaluated.
- **Application screenshots (3/5):** Use only authentic screenshots from approved demo/repository artifacts; otherwise retain a labeled placeholder (never fabricate screens).
- **Detailed workflow example (3/5):** Use the manuscript's time-at-risk question to illustrate stage-aware `/ohdsi` guidance; do not invent a literal LLM reply.

## Architecture diagram semantics

Three client categories above a shared governed service layer:

1. **R/Strategus shells** — reported prototype integration.
2. **Atlas3/WebAPI** — explicitly **early-stage** integration.
3. **Coding agents using Skills.md** — additional researcher-provided context; require repo verification.

All clients connect to **ACP server** (workflow orchestration, confirmations, state and routing). ACP uses **MCP servers** (bounded tools and prompt bundles) and a **deterministic core** (validation/transformation rules). Labels must not imply that ACP, MCP and deterministic code are interchangeable. Reuse of existing OHDSI community-developed deterministic algorithms is an architectural opportunity specifically highlighted by the researcher; verify exact package-to-flow/tool bindings before asserting implemented support.

**Connectors:** Do not use SVG `marker-end` for this prototype. Compute a normalized directional vector for each connector; draw its shaft up to the arrowhead base, draw explicit triangular polygon, and leave a measured gap before the target boundary. Inspect angled arrows in both SVG and PDF.

## Proposed composition

- Navy title/author/affiliation header.
- Broad high-contrast central takeaway directly beneath.
- Left context/governance and prototype maturity column.
- Largest center pane: ACP/MCP/deterministic architecture and three clients.
- Right pane: supported named flows and note on deterministic reuse.
- Lower center/right: workflow-contextual example and demonstration/evaluation panel.
- Footer: references/branding/acknowledgments when verified, QR link only when confirmed.

Use the screenshot placeholder in the wireframe as **intent**, not fake scientific evidence. Keep mandatory title and research details above the fold; make scientific content readable at real poster print size (do not treat wireframe font sizes as final).

## Acceptance

- Trace all substantive claims to manuscript, verified public source, or explicitly labeled researcher-supplied context.
- Preserve correct maturity/limitations and distinctions between demonstrated, early-stage, and planned interfaces.
- Confirm intended venue size; export editable SVG, print PDF, and raster preview.
- Run `posterkit` tests, bounds/overlap checks, text font minima, PDF-size validation, and visual inspection including connector close-ups.
- Record build command, exact commit, uv.lock, OS apt dependencies, font package/version, asset licenses/checksums, and any omissions.
- Never commit draft manuscript or sensitive VA/VINCI data to public GitHub.

## Workflow decision

Develop on `poster/study-agent-ohdsi` independently of `main`. Codex CLI should create a reproducible project under `posters/study-agent-ohdsi/`; reuse tested `posterkit` components, add general-purpose fixes with regression tests, and avoid merging to `main` without researcher review.
