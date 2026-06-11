---
name: create-artifact
description: Generate a tailored career artifact (resume, cover letter, outreach, etc.) from career.md for a specific opportunity
argument-hint: <opportunity-path> <context>
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash(co *), Glob, Grep
---

$ARGUMENTS

---

## Intent

Build the artifact from the candidate's calibrated baseline at `defaults/<entity>.yaml`, projected onto the opportunity. The default is the prose anchor: its voice, phrasing, and length are deliberate. The opportunity is the arrangement driver: section order, entry order, emphasis, and content selection follow the JD and research. `career.md` is the source of truth for everything the default doesn't surface; every number and claim traces to it exactly — never round, estimate, or infer.

The result reads as a strong candidate whose background naturally aligns with the role, not a document reverse-engineered from the JD.

## Pipeline (Resume, Cover Letter)

For artifacts that go through the PDF pipeline:

1. Read `defaults/<entity>.yaml`, `career.md`, the opportunity folder (JD, `research.md` and its `## Artifact directives` if present, other notes; shared files one level up in the organisation folder count), the schema at `cli/schemas/<entity>.py`, and the template at `templates/<entity>/primary.tex.j2`. If no default exists for this entity, generate greenfield from career.md.
2. Walk the decision sheet in `${CLAUDE_SKILL_DIR}/resume-strategy.md` against the directives: arrangement freely, selection from career.md, prose anchored, invisible layer per ATS.
3. Preserve: the default's voice, two-page length, and grounding. No content-free filler bullets.
4. Save to `opportunities/<slug>/artifacts/<entity>.yaml`. Render: `co render opportunities/<slug>/artifacts/<entity>.yaml`
5. Read the generated PDF. Check the page-1 top half carries the strongest opportunity-relevant signal; rearrange and re-render until it does. For formatting-only fixes, edit the `.tex` and re-render it directly: `co render opportunities/<slug>/artifacts/<entity>.tex`

Entity is `resume` or `cover-letter`.
