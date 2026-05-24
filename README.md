<div align="center">

# Content Optimizer

*Gradient descent for your career content.*

</div>

Toolkit for producing per-opportunity career-marketing content. Resumes, cover letters, outreach, application Q&A. No copy-pasting; no manual rewrites. A small Python CLI handles deterministic rendering (YAML to Jinja+LaTeX to PDF). Claude Code skills handle the stochastic work: triage, drafting, stress-testing.

## The model

Most career-content AI invents the substance. It generates a resume from a thin profile; writes a cover letter from a few bullet points. This toolkit refuses that. Your career, your voice, your floors and walk-aways are inputs you write once, by hand, with care. The workflows here are reductive: filter, polish, probe, project that pre-articulated substance onto a specific opportunity. They never manufacture voice; they shadow yours.

The investment is front-loaded. Half a workday on `career.md` and `preferences.md` is realistic; cutting that corner is the single failure mode that produces shallow artifacts no amount of downstream prompting will fix. Done well, per-opportunity friction drops to near-zero, and the benefit compounds: as you nudge your context files to better model your actual decision-making, more workflows can be delegated over time without losing authenticity.

## Requirements

First-class on macOS and Linux. Windows works via WSL2; expect rougher edges.

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** — Python package manager.
- **[Docker](https://www.docker.com/products/docker-desktop/)** — runs LaTeX compilation in a container. ~5 GB image on first render.
- **[Claude Code](https://www.anthropic.com/claude-code)** — the AI workflows.

Plan ~30 minutes if you have none of these; ~5 if you have all of them.

## Setup

```bash
git clone <repo>
cd content-optimizer
uv sync
```

Then set up your context files in two fresh Claude Code chats. The templates have embedded interview instructions; Claude walks you through them.

```
Have a look at @career.md.example and help me set up my career file. Iteratively ask me probing questions to make sure we cover all the relevant information.
```

```
Have a look at @preferences.md.example and help me set up my preferences file.
```

Be ruthless about depth, especially in `career.md`. The richer the source of truth, the less the generated content falls back on stock phrasing.

Two optional rules files refine voice when you're ready: `.claude/rules/writing-style.local.md` (your stylistic conventions) and `.claude/rules/anti-patterns.local.md` (phrases to never produce). Both gitignored.

## Workflow

Per opportunity:

1. **Triage** a URL, pasted JD, or several at once. Returns Apply / Maybe / Skip with V/P/EV scores grounded in your context files.
   ```
   /assess <url-or-jd>
   ```

2. **Scaffold** an opportunity folder.
   ```bash
   uv run co new-opportunity <slug>
   ```

3. **Paste the JD** into `opportunities/<slug>/job-description.md`.

4. **(Optional) Research** for deeper context: company, team, ATS, people. Output: `research.md`.
   ```
   /research-opportunity opportunities/<slug>/
   ```

5. **Generate** the artifact (YAML to PDF).
   ```
   /create-artifact resume opportunities/<slug>/
   ```

6. **(Optional) Stress-test** with three subagents in parallel: ATS simulator, recruiter funnel, gap analyzer.
   ```
   /vet <slug>
   ```

7. **Iterate** on formatting by editing the `.tex`; `uv run co render <file>.tex` recompiles.

Step 5 is the only essential one once the JD is pasted.

---

<div align="center">

*If you find this useful, consider starring the repo.*

</div>
