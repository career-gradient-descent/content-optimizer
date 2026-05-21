# Content Optimizer

Toolkit for producing career marketing artifacts (resumes, cover letters, outreach) tailored per opportunity.

## The opportunity is the unit

Each pursuit lives at `opportunities/<slug>/`. Contents are flexible per pursuit type — job opportunities typically include job-description.md (with YAML frontmatter), optional research.md, and supporting material. Generated content goes in an artifacts/ subfolder. Slugs can nest (e.g., opportunities/google/sre-g1/).

## Source of truth

`career.md` is the full candidate profile. Every generated artifact draws selectively from it.

## CLI

- `co new-opportunity <slug>` — scaffold an opportunity folder (creates `job-description.md`; flags pre-populate frontmatter)
- `co render <file>` — render YAML→PDF or recompile from TEX. Entity inferred from filename stem (`resume.yaml`, `cover-letter.yaml`).

## Operating mode

Most chats are 'use chats': research, artifact generation, vetting, application support. Writes go inside `opportunities/<slug>/`; reads elsewhere are fine.

The workbench itself (CLI, skills, agents, rules, this file) is shaped in dedicated 'sharpening chats'. If a 'use chat' strays into modifying it, surface what you're about to touch first.
