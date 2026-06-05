# `co`: the deterministic CLI

The auditable half of [Content Optimizer](../README.md). Every `co` command is a pure, deterministic step: same input, same output, no model in the loop. Claude invokes them as it runs the pipeline; you can run them by hand too.

```bash
co <command> [args]
co <command> --help     # authoritative usage for any command
```

`--help` is generated from the code and never drifts. Treat it as the source of truth for exact flags. This document adds the *why*, the behavior, and the gotchas it can't.

`co` is the project's venv script: run it from the repo root (paths resolve relative to it), with `.venv/bin` on your PATH or `uv run co` as the fallback.

| Command | Does | Writes |
|---|---|---|
| [`new-opportunity`](#new-opportunity) | Scaffold an opportunity folder + JD frontmatter | `opportunities/<slug>/` |
| [`fetch-jd`](#fetch-jd) | Extract a JD from a URL to clean markdown | stdout |
| [`render`](#render) | Compile an artifact YAML to PDF (or recompile a `.tex`) | PDF beside the input |
| [`archive`](#archive) | Move a finished opportunity out of the active set | `opportunities/.archive/` |
| [`tracker`](#tracker) | Read the application tracker; edit cells on explicit request | stdout / the tracker |

Anticipated failures (a JS-rendered page, a missing file, a broken `.tex`) exit non-zero with a one-line message, never a traceback. Genuine bugs still surface in full.

---

## `new-opportunity`

```bash
co new-opportunity <slug> [--role ...] [--organisation ...] [--location ...] [--url ...] [--ats ...] [--comp ...]
```

Creates `opportunities/<slug>/` with an `artifacts/` subfolder and a `job-description.md` containing only YAML frontmatter (empty body). Flags pre-populate the frontmatter; omitted ones render as empty keys. Slugs may nest: `google/sre-g1`.

- `--ats` is auto-detected from `--url` when recognizable (Greenhouse, Ashby, Lever, Workday, iCIMS, SmartRecruiters, Taleo, PageUp).
- Refuses to clobber: if the folder already exists, it exits non-zero and changes nothing.

It scaffolds the *container*. It does not fetch the JD body; that's `fetch-jd`. See [Setting up an opportunity](#setting-up-an-opportunity).

## `fetch-jd`

```bash
co fetch-jd <url>
```

Fetches the page and extracts the main content to markdown, deterministically and with no LLM, so the JD lands word-for-word instead of paraphrased. Prints to stdout.

- **Gives up loudly** rather than guessing. JS-rendered pages (much of Workday, Ashby) and pages that yield too little to trust exit non-zero with a "paste manually" message. The clean give-up is the feature: it never writes a half-extracted JD.
- Static ATS pages (Greenhouse, Lever, Seek, most company boards) extract cleanly.

## `render`

```bash
co render <file> [-t <template>]
```

YAML in → PDF out, beside the input. The entity is inferred from the filename stem: `resume.yaml` validates against the resume schema, `cover-letter.yaml` against the cover-letter schema. Passing a `.tex` recompiles it directly, for hand-tuning the LaTeX after generation.

- `-t` selects the template (default `primary`).
- Validation is strict (Pydantic): malformed YAML fails before LaTeX runs.
- Compilation runs in Docker (`texlive/texlive`); a failed build reports the LaTeX error.

## `archive`

```bash
co archive <slug>
```

Moves `opportunities/<slug>/` into `opportunities/.archive/<slug>/`: out of the active list and out of Claude's globs, still on disk, fully reversible. Nothing is deleted.

The tracker names the candidates: `co tracker read | grep -iE 'rejected|ghosted|withdrawn'`.

## `tracker`

```bash
co tracker read [file] [--grid]
co tracker set CELL=VALUE [CELL=VALUE ...] [--sheet NAME] [--file PATH]
```

`read` dumps every sheet of the tracker workbook (default `tracker.xlsx` at repo root) to markdown. **Structure-agnostic:** it assumes nothing about your columns, header rows, or sheet count, so you can restructure the spreadsheet freely and this keeps working. `--grid` adds sheet row numbers and column letters; run it before `set` to resolve exactly which cell you're targeting. Filter with pipes, not flags: `co tracker read | grep -i rejected`.

`set` writes cell values in place, with the care rules in code rather than convention:

- **The sheet's own dropdown rules are enforced.** A value outside a cell's list validation is refused, with the allowed values in the error. The rules live once, in the spreadsheet, maintained through your spreadsheet app; the CLI makes them binding.
- **Typing is deterministic.** `YYYY-MM-DD` becomes a real date and inherits the column's existing date format; integers and floats become numbers; an empty value clears the cell; everything else is text. Values starting with `=` are refused (they would silently become formulas).
- **The round-trip is safe.** Loads with formulas intact (never `data_only`), saves atomically (temp file + rename), and refuses to touch a workbook containing charts or images, the one thing an openpyxl save silently drops.
- Appending a row is just `set` on the next empty row's cells; find it with `--grid`.

The tracker stays the user's file: writes happen only on their explicit request, and the spreadsheet app should be closed during a write. No file yet? `cp tracker.xlsx.example tracker.xlsx`.

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

Setup ends by logging the pursuit in the tracker: `co tracker read --grid` to find the next empty row, then one `co tracker set` filling the cells that map from frontmatter (organisation, role, location, ATS). The Listing hyperlink stays hand-entered; `set` writes values, not link objects.
