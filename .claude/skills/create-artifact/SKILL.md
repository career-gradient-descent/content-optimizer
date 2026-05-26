---
name: create-artifact
description: Generate a tailored career artifact (resume, cover letter, outreach, etc.) from career.md for a specific opportunity
argument-hint: <opportunity-path> <context>
disable-model-invocation: true
allowed-tools: Read Write Edit Bash(uv *) Glob Grep
---

$ARGUMENTS

---

## Intent

Build the artifact from the candidate's calibrated baseline at `defaults/<entity>.yaml` (representing their baseline voice, structure, and content selection), tactically modified for the opportunity. `career.md` is the source of truth for everything (every experience, skill, nuance) the default doesn't surface.

Tactical modification, not greenfield reselection. Reorder, swap, tweak. Don't rewrite. The default's length, voice, and overall structure are deliberate; deviations require justification. The result should read as a strong candidate whose background naturally aligns with the role, not a document reverse-engineered from the JD.

## Pipeline (Resume, Cover Letter)

For artifacts that go through the PDF pipeline:

1. Read `defaults/<entity>.yaml` (the calibrated baseline), `career.md`, the opportunity folder (JD + `research.md` if available), the relevant schema at `cli/schemas/<entity>.py`, and the template at `templates/<entity>/primary.tex.j2`. If no default exists for this entity, generate greenfield from career.md.
2. Start from the default and apply targeted modifications based on the opportunity:
   - Reorder bullets within sections so the most opportunity-relevant lead
   - Swap 1-2 bullets for stronger alternatives drawn from career.md (only where the opportunity values different signals than the default emphasizes)
   - Adjust summary phrasing to align with opportunity emphasis (subtle rewording, not a full rewrite)
   - Update skills emphasis (reorder categories or items, swap individual items)
   - Adjust `ats_optimization` keywords for the specific ATS (only with a known target ATS; only adding keywords the visible content doesn't already cover)
   - Toggle optional sections (publications, certifications, specific projects) based on opportunity fit
3. Preserve: voice, two-page length, depth-of-detail balance per role, structural integrity. Avoid full bullet rewrites, restructuring, content-free filler bullets, large length changes.
4. Save to `opportunities/<slug>/artifacts/<entity>.yaml`. Render: `uv run co render opportunities/<slug>/artifacts/<entity>.yaml`
5. Read the generated PDF to validate. If formatting needs adjustment, edit the `.tex` and re-render: `uv run co render opportunities/<slug>/artifacts/<entity>.tex`

Entity is `resume` or `cover-letter`.

## Strategy

For resume strategy, read `${CLAUDE_SKILL_DIR}/resume-strategy.md`.
