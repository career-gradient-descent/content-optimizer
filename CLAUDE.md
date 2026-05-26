# Content Optimizer

Toolkit for producing career marketing artifacts (resumes, cover letters, outreach) tailored per opportunity.

## The opportunity is the unit

Each pursuit lives at `opportunities/<slug>/`. Contents are flexible per pursuit type — job opportunities typically include job-description.md (with YAML frontmatter), optional research.md, and supporting material. Generated content goes in an artifacts/ subfolder. Slugs can nest (e.g., opportunities/google/sre-g1/).

## Source of truth

`career.md` is the full candidate profile. Every generated artifact draws selectively from it.

## CLI

- `co new-opportunity <slug>` — scaffold an opportunity folder with an empty `job-description.md`. Optional flags pre-populate frontmatter: `--role`, `--organisation`, `--location`, `--url`, `--ats`, `--comp`.
- `co fetch-jd <url>` — extract a job description to markdown deterministically (no LLM), printed to stdout. Gives up with a non-zero exit when the page is JS-rendered or yields too little to trust.
- `co render <file>` — render a YAML artifact to PDF (writing the PDF next to the input), or recompile from a `.tex`. Entity inferred from filename stem (`resume`, `cover-letter`). Optional flag: `-t <template>` (default `primary`).

## Operating mode

Most chats are 'use chats': research, artifact generation, vetting, application support. Writes go inside `opportunities/<slug>/`; reads elsewhere are fine.

The workbench itself (CLI, skills, agents, rules, this file) is shaped in dedicated 'sharpening chats'. If a 'use chat' strays into modifying it, surface what you're about to touch first.
