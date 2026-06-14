# Content Optimizer

Toolkit for producing career marketing artifacts (resumes, cover letters, outreach) tailored per opportunity. User-facing overview: `README.md`.

## The opportunity is the unit

Each pursuit lives at `opportunities/<slug>/`, holding `job-description.md` (YAML frontmatter + body), an optional `research.md`, and an `artifacts/` subfolder for generated content.

When one organisation has several roles, nest them under a shared org folder: `opportunities/<org>/<role>/`. Company research and people belong at the org level — `research.md`, an `outreach/` folder, correspondence — written once and read from one level up; each role folder holds only its own `job-description.md` and `artifacts/`. A lone role can stay flat at `opportunities/<slug>/`.

## Source of truth

- `career.md`: the full candidate profile; every artifact draws selectively from it.
- `preferences.md`: floors, walk-aways, and situational scoring used in triage.
- `tracker.xlsx`: application state. Read it via `co tracker read`; discover its columns and rules via `co tracker schema`; the user maintains it by hand. Writes only on explicit user request, via `co tracker add` / `update` / `set` (the sheet's own dropdown rules are enforced).
- `.claude/rules/*.md`: voice and anti-patterns, auto-loaded.

## CLI

Deterministic `co` commands: `new-opportunity`, `fetch-jd`, `render`, `archive`, `tracker`. Setting up an opportunity composes two of them: `new-opportunity` scaffolds the folder, `fetch-jd` pulls the JD body. Usage, flags, behavior, and the setup cases live in `cli/README.md`; read it before invoking, or run `co <command> --help`.

## Pipeline

The heavy stages are skills, slash-invocable and model-invocable alike: `/assess` (triage), `/research-opportunity`, `/create-artifact`, `/vet`. `/funnel` chains them over a batch, end to end. Invoke the matching skill when a request plainly calls for a stage; suggest the slash form when the user seems unaware of it. Everything else (application Q&A, outreach, emails, pipeline queries against the tracker) is ordinary conversation grounded in the source-of-truth files above.

The tracker follows the pursuit: when an opportunity is set up, offer to log its row (`co tracker add`); when the user reports an event ("applied", "rejected", "interview booked"), update the row (`co tracker update --match`); when rows go dead (Rejected, Ghosted, Withdrawn), suggest `co archive <slug>`.

## Operating mode

Most chats are 'use chats': research, artifact generation, vetting, application support. Writes go inside `opportunities/<slug>/`; reads elsewhere are fine.

The workbench itself (CLI, skills, agents, rules, this file) is shaped in dedicated 'sharpening chats'. If a 'use chat' strays into modifying it, surface what you're about to touch first.
