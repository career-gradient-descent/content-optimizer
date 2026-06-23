<div align="center">

# Content Optimizer

*Gradient descent for your career content.*

</div>

A per-opportunity career-marketing pipeline for resumes, cover letters, application answers, and outreach. Half of it is deterministic: YAML schemas, Jinja+LaTeX, ATS-aware PDF rendering, a small Python CLI you can audit line by line. Half is stochastic: Claude Code skills that triage opportunities, research them, draft from your profile, and stress-test the result before you send it.

## The model

Most career-content AI invents the substance. Hand it a thin profile and it manufactures a resume; give it three bullet points and it writes you a voice you don't have. This toolkit refuses that.

Your career, your voice, your floors and walk-aways are **inputs you write once, by hand, with care.** Everything downstream is reductive: it filters, polishes, probes, and projects that pre-articulated substance onto a specific opportunity. It never fabricates a metric, never inflates a title, never invents a story. It shadows you.

> ### It reduces your effort, not your authenticity.

That's the whole thesis. The pipeline is a state machine you can read end to end, and what it surfaces is *your* material, approximated under each opportunity.

The cost is front-loaded and real. Half a workday on `career.md` is the honest figure, and skipping it is the one failure mode that yields shallow, obviously reverse-engineered output no prompt can save. Do it properly and per-opportunity friction approaches zero, then keeps compounding as you tune your context files to model your own judgment and hand more of the loop over without losing a thing.

## The pipeline

> **`/assess` → set up → `/recon` → `/create` → `/vet` → submit**

| Stage | You say | Result |
|---|---|---|
| **Triage** | `/assess <url, text, or several>` | Apply / Maybe / Skip per JD, with V/P/EV scores against your profile |
| **Set up** | *"set up an opportunity for `<url>`"* | Folder scaffolded, JD pulled in, row logged in your tracker |
| **Recon** *(opt.)* | `/recon <folder>` | First-party source resolved; `recon.md`, `org-recon.md`, `questions.md`, `targets.md` |
| **Create** | `/create <folder>` | Tailored resume + cover letter by default, plus answers and outreach when recon supplies them |
| **Vet** *(opt.)* | `/vet <slug>` | Five-agent adversarial panel, condensed to a few actionable notes with the obvious fixes already applied |

Run a single stage at will, or hand a whole batch to **`/funnel`**, which composes the stages end to end: triage, setup, recon, a second-pass triage, creation, and vetting, finishing in an action sheet.

JD extraction is deterministic where the page allows. JS-heavy ATS pages (much of Workday, Ashby) you paste by hand.

Everything around the edges is plain conversation, grounded in the same context files: follow-up emails, *"have I applied here before?"*, *"what's stalled in my pipeline?"*. Those last two read straight from `tracker.xlsx`, the state you keep by hand; Claude reads it freely and edits a cell only at your word, with your spreadsheet's own dropdown rules enforced.

## Requirements

First-class on macOS and Linux. Windows works through WSL2; expect rougher edges.

| Tool | For |
|---|---|
| **Python 3.13+** | the CLI |
| **[uv](https://docs.astral.sh/uv/)** *(recommended)* | environment + running `co` |
| **[Docker](https://www.docker.com/products/docker-desktop/)** | LaTeX compilation, sandboxed (~5 GB image on first render) |
| **[Claude Code](https://www.anthropic.com/claude-code)** | the skills and agents |

Other coding agents can drive the CLI and read the context files, but the skills, subagents, and slash commands are built for Claude Code, so expect partial function elsewhere.

## Setup

This is not a clone-and-go repo. The setup is the filter, and most won't clear it. By design.

```bash
git clone <repo> && cd content-optimizer
uv sync
```

Then build your context files. Each ships with a `.example` template that embeds its own interview instructions. Open a fresh Claude Code chat and let it walk you through:

```
Look at @career.md.example and help me set up my career file.
Ask me probing questions until you have everything.
```
```
Look at @preferences.md.example and help me set up my preferences file.
```

| File | What it is | Effort |
|---|---|---|
| `career.md` | Your full profile, the source every artifact draws from | **High, upfront** |
| `preferences.md` | Floors, walk-aways, situational scoring for triage | Medium |
| `.claude/skills/create/voice.local.md` | Your voice, conventions, and phrasings to never produce *(optional)* | Low, ongoing |
| `tracker.xlsx` | Application state: `cp tracker.xlsx.example tracker.xlsx`, then maintain it in your spreadsheet app | Ongoing |

Be ruthless about depth in `career.md`. Every role, project, mark, publication, side quest: what you owned, what you wrestled with, what you'd do differently.

<details>
<summary><b>Calibrating baselines (recommended, once you're rolling)</b></summary>

<br>

`create` works best when `defaults/resume.yaml` holds a clean, opportunity-agnostic version of your resume in your usual voice and structure. Per-opportunity artifacts then become *tactical edits* of that baseline rather than greenfield rewrites, which is what keeps every resume from reading as machine-made. Generate one well, save it as the default, refine over time. Without it, generation still works; it just starts from scratch each time.

</details>

## The CLI

The deterministic half is a handful of `co` commands: `new-opportunity`, `fetch-jd`, `render`, `tracker`, `archive`. You rarely call them directly; Claude does, as it runs the pipeline. Full reference: **[`cli/README.md`](cli/README.md)**.

---

<div align="center">

*A meticulous job hunt, version-controlled. If it's useful to you, star it.*

</div>
