# `co`: the deterministic CLI

The auditable half of [Content Optimizer](../README.md). Every `co` command is a pure, deterministic step: same input, same output, no model in the loop. Claude invokes them as it runs the pipeline; you can run them by hand too.

```bash
uv run co <command> [args]
uv run co <command> --help     # authoritative usage for any command
```

`--help` is generated from the code and never drifts. Treat it as the source of truth for exact flags. This document adds the *why*, the behavior, and the gotchas it can't.

| Command | Does | Writes |
|---|---|---|
| [`new-opportunity`](#new-opportunity) | Scaffold an opportunity folder + JD frontmatter | `opportunities/<slug>/` |
| [`fetch-jd`](#fetch-jd) | Extract a JD from a URL to clean markdown | stdout |
| [`render`](#render) | Compile an artifact YAML to PDF (or recompile a `.tex`) | PDF beside the input |
| [`tracker`](#tracker) | Dump the application tracker to markdown for reading | stdout |
| [`archive`](#archive) | Move a finished opportunity out of the active set | `opportunities/.archive/` |

Anticipated failures (a JS-rendered page, a missing file, a broken `.tex`) exit non-zero with a one-line message, never a traceback. Genuine bugs still surface in full.

---

## `new-opportunity`

```bash
uv run co new-opportunity <slug> [--role ...] [--organisation ...] [--location ...] [--url ...] [--ats ...] [--comp ...]
```

Creates `opportunities/<slug>/` with an `artifacts/` subfolder and a `job-description.md` containing only YAML frontmatter (empty body). Flags pre-populate the frontmatter; omitted ones render as empty keys. Slugs may nest: `google/sre-g1`.

- `--ats` is auto-detected from `--url` when recognizable (Greenhouse, Ashby, Lever, Workday, iCIMS, SmartRecruiters, Taleo, PageUp).
- Refuses to clobber: if the folder already exists, it exits non-zero and changes nothing.

It scaffolds the *container*. It does not fetch the JD body; that's `fetch-jd`. See [Setting up an opportunity](#setting-up-an-opportunity).

## `fetch-jd`

```bash
uv run co fetch-jd <url>
```

Fetches the page and extracts the main content to markdown, deterministically and with no LLM, so the JD lands word-for-word instead of paraphrased. Prints to stdout.

- **Gives up loudly** rather than guessing. JS-rendered pages (much of Workday, Ashby) and pages that yield too little to trust exit non-zero with a "paste manually" message. The clean give-up is the feature: it never writes a half-extracted JD.
- Static ATS pages (Greenhouse, Lever, Seek, most company boards) extract cleanly.

## `render`

```bash
uv run co render <file> [-t <template>]
```

YAML in → PDF out, beside the input. The entity is inferred from the filename stem: `resume.yaml` validates against the resume schema, `cover-letter.yaml` against the cover-letter schema. Passing a `.tex` recompiles it directly, for hand-tuning the LaTeX after generation.

- `-t` selects the template (default `primary`).
- Validation is strict (Pydantic): malformed YAML fails before LaTeX runs.
- Compilation runs in Docker (`texlive/texlive`); a failed build reports the LaTeX error.

## `tracker`

```bash
uv run co tracker [file]
```

Dumps every sheet of the tracker workbook (default `tracker.xlsx` at repo root) to markdown, so Claude (or you) can read the pipeline at a glance. **Read-only and structure-agnostic:** it assumes nothing about your columns, header rows, or sheet count, so you can restructure the spreadsheet freely and this keeps working.

- The tracker is yours to maintain by hand (Excel/Numbers, with your colors and validation rules). The CLI only reads it.
- No file yet? `cp tracker.xlsx.example tracker.xlsx`. A missing or non-xlsx file gives a clean message.

## `archive`

```bash
uv run co archive <slug>
```

Moves `opportunities/<slug>/` into `opportunities/.archive/<slug>/`: out of the active list and out of Claude's globs, still on disk, fully reversible. Nothing is deleted.

---

## Setting up an opportunity

Scaffolding a folder and populating its JD are deliberately **two commands**, because the right combination depends on what you have:

| You have | Flow |
|---|---|
| URL, static page | `fetch-jd <url>` → read it for role/org/comp → `new-opportunity <slug> --flags` → drop the fetched body into `job-description.md` |
| URL, JS-rendered page | `fetch-jd` gives up → `new-opportunity <slug> --flags` → paste the JD body by hand |
| Pasted JD text, no URL | `new-opportunity <slug> --flags` → paste the body |
| Nothing yet (placeholder) | `new-opportunity <slug>` → fill the JD later |

In a chat you don't run these yourself. You say *"set up an opportunity for `<url>`"* and Claude sequences them: derives the slug, fills the frontmatter from the JD, places the body, and falls back to asking you to paste when extraction gives up. The split keeps each command single-purpose; the sequencing lives here so it's never guessed.
