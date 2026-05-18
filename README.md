<div align="center">

# Content Optimizer

*Gradient descent for your career content.*

</div>

A semi-deterministic, semi-stochastic pipeline for producing career-advancement content tailored per opportunity. Resumes, cover letters, outreach, application Q&A. No copy-pasting, no manual rewrites.

The deterministic half: YAML schemas, Jinja templates, LaTeX compilation, ATS-aware rendering. The stochastic half: AI skills that research opportunities, draft artifacts from your career profile, and stress-test the results before you submit.

## The mental model

Two foundations.

`career.md` holds your full career profile. It's the source of truth. Every generated artifact draws selectively from it.

`opportunities/<slug>/` holds one folder per pursuit. A job application, a networking target, anything you're chasing. Contents are flexible: typically `job-description.md` (with YAML frontmatter), optional `research.md`, and supporting material like LinkedIn PDFs. Generated content goes in an `artifacts/` subfolder.

## Quickstart

Requirements:
- Python 3.13+
- Docker (for LaTeX compilation)
- [uv](https://docs.astral.sh/uv/) (recommended)
- [Claude Code](https://www.anthropic.com/claude-code) (for the AI workflows)

```bash
uv sync
```

## Workflow

The typical flow for an outbound job application:

1. **Scaffold the opportunity folder.**
   ```bash
   uv run co new-opportunity <slug>
   ```
   Optional flags (`--role`, `--organisation`, `--url`, etc.) pre-populate the frontmatter. See `--help`.

2. **Paste the JD** into `opportunities/<slug>/job-description.md`.

3. **Research the opportunity.** Gathers context the JD alone doesn't give you. Output: `research.md`.
   ```
   /research-opportunity opportunities/<slug>/
   ```

4. **Generate the artifact.** Writes YAML, renders to PDF.
   ```
   /create-artifact resume opportunities/<slug>/
   ```

5. **Stress-test before submission.** Three subagents in parallel: ATS-layer simulator, recruiter funnel, gap analyzer.
   ```
   /vet <slug>
   ```

6. **Iterate** on formatting if needed. Edit the `.tex` directly; `uv run co render <file>.tex` recompiles.

Steps 3 and 5 are optional refinements. Step 4 is the only essential one once you've pasted the JD.

## Setting yourself up properly

The output is bounded by the quality of `career.md`. Spend real time on it.

Write everything down. Every role, every project, every academic mark, every publication, every side endeavor. What you owned. What you wrestled with. What you'd do differently. What types of work you liked, what you didn't. Get philosophical about your trajectory. Go for both breadth (cover everything) and depth (a page or more on each substantive thing).

The richer the source of truth, the less the generated content falls back on stock phrasing, and the less likely you'll see fabricated achievements that don't trace back to anything real.

You'll also want to calibrate baselines. The `create-artifact` skill expects defaults at `defaults/resume.yaml`, `defaults/cover-letter.yaml`, etc. that represent your usual voice, structure, and content selection, rendered cleanly without any opportunity context. Per-opportunity artifacts are tactical modifications of these defaults, not rewrites from scratch. Without calibrated defaults, every resume reads as obviously reverse-engineered from the JD.

## Personalization (optional)

Three project-local files customize Claude's behavior for your specific voice and context. All gitignored, all auto-load into the session.

- `.claude/rules/writing-style.local.md` for your voice and stylistic conventions
- `.claude/rules/anti-patterns.local.md` for phrases and patterns to avoid
- `CLAUDE.local.md` at the repo root for any personal context you want loaded into every Claude session for this project

You don't need any of these to get started.

## How it works

```
career.md     ─┐
               ├──► YAML (Pydantic-validated) ──► Jinja+LaTeX template ──► .tex ──► pdflatex (Docker) ──► PDF
opportunity   ─┘
```

- **Schemas** in `cli/schemas/` define what each artifact YAML can contain.
- **Templates** in `templates/` define how YAML renders to LaTeX.
- **`co render`** chains validation → template → compile.

The Python CLI handles the deterministic rendering. The skills handle the stochastic content generation. You spend your time on `career.md` and reviewing the output.

---

<div align="center">

*If you find this useful, consider starring the repo.*

</div>
