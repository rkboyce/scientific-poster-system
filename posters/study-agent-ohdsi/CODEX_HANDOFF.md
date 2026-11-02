# Codex CLI handoff — Study Agent OHDSI poster

## Goal

Build the first end-to-end scientifically faithful reproducible SVG poster for a **hypothetical** OHDSI symposium, 48 × 36 in landscape. The poster is based on the separately supplied *OHDSI Study Agent for Human-AI Team-Based Real-World Evidence Generation in the Veterans Health Administration* manuscript. This is an acceptance test of the poster system, **not** a real submitted conference poster.

## Repository / Git procedure

You are already on `poster/study-agent-ohdsi`, branched from tested `main`. **Do not create another branch or reset to `test/posterkit-next`.** Read `posters/study-agent-ohdsi/DESIGN_BRIEF.md`, `docs/design-preferences.md`, `src/posterkit/`, its tests, and the poster wireframe generator in this directory. Add implementation to `posters/study-agent-ohdsi/`. Reusable improvements to `posterkit` require tests. Leave `main` alone. Commit/push only this poster branch when work and tests are complete. Record base SHA and dependencies; use a final release tag only with researcher approval.

## Manuscript privacy

The full report may be located on the user's local machine. **Do not add it to a public Git repository without explicit permission.** If absent, work from the scientific design brief as a provisional specification and request the manuscript locally for source checking rather than inventing missing details. Do not insert private VA data, credentials, patient data or sensitive artifacts in outputs.

## Content / fidelity

- Main message: reusable service-based and governed AI support for OHDSI research workflows.
- Researcher oversight, explicit confirmations and stage-aware support are architectural contributions, not outcome measures.
- Distinguish the ACP server (orchestration and governance), MCP services (tools/prompt resources) and deterministic core (validation/transformations).
- R/Strategus functional prototype; Atlas3/WebAPI early integration. Coding agents / Skills.md and precise OHDSI deterministic code reuse are researcher-provided architectural context requiring implementation verification.
- Follow manuscript Table 1 for flow names and Table 2 for realistic workflow-contextual example. If exact original files cannot be accessed, label specifics as provisional.
- Manuscript estimates TRL 4–5 using scripted lab demonstration; it **does not** establish efficiency, decision accuracy or improved study outcomes. Never invent metrics or outcomes.
- No authentic screenshot available? Use a clearly marked placeholder; do not synthesize a fake system interface.

## Implement

1. Inventory repo/tests and verify `uv sync`.
2. Generate an editable 48 × 36 in vector poster from reusable `posterkit` components, starting from the v0.3 architecture and design priorities. Retain palette configuration; color schemes are poster-specific.
3. Implement standalone figure logic and connectors as native editable SVG elements. For explicit polygon arrows, compute unit vector and stop shaft at arrowhead base; keep tip clear of target boxes. Test diagonal and orthogonal directions.
4. Preserve Pango-measured font size thresholds; no silent font shrinking. Make figures readable at actual print scale.
5. Create `poster.toml`, content sources, vector figures, and the composition script; output SVG, PDF, PNG; validate printed page box; include zoomed QA screenshots of dense areas and connector details.
6. Produce `BUILD.md` documenting Ubuntu 22.04 apt packages, `uv sync --locked`, Inkscape command, fonts/version, `uv.lock` hash, tested SHA, asset provenance and a reproducible one-command build.
7. Create a machine-readable preflight/QA report including tested component bounds, sizes, font-minimum violations, intended/unintended overlaps, and any unverified scientific statements.
8. Include auto-tests for renderer and connector geometry, then run all existing tests. Flag visual problems honestly; iterate before delivery.

## Reproduction and review

Record all inputs and script paths. Retain outputs as review artifacts, with large binaries only where repository policy allows. A final tagged release should bind source, fonts, Python dependencies and assets. Use a short manual-difference log to quantify repairs relative to earlier PPTX workflow.

## Source attribution

- The provided manuscript is the authoritative source of scientific content.
- `DESIGN_BRIEF.md` captures user editorial decisions and flags extra manuscript-independent architecture context.
- For source-verification claims involving coding-agent interfaces or deterministic OHDSI components, inspect the appropriate actual repositories before representing them as implemented. Distinguish source verified vs interpretation.
