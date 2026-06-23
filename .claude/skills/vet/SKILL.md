---
name: vet
description: "Stress-test an opportunity's produced artifacts before submission. Dispatches the adversarial vet agents over whichever artifacts exist, condenses their reports into a few actionable lines each, auto-applies the obvious no-downside fixes, and surfaces the judgement calls for the candidate's decision."
argument-hint: <opportunity-folder-or-slug>
disable-model-invocation: false
allowed-tools: Agent, Read, Glob, Grep, Edit, Write, Bash(co *)
---

$ARGUMENTS

---

## What this does

Vet the produced artifacts for the opportunity in $ARGUMENTS. Resolve the input (a slug, a folder path, or an @-mention of the folder or a file inside it) to the opportunity folder, and find its `artifacts/`. You are the manager of a panel of adversarial advisors: you send each the artifacts in its lens, hear back detailed reports, then hand the candidate a few small actionable sentences per advisor, having already applied the obvious fixes yourself.

## Dispatch the advisors

Spawn, in a single message, only the agents whose artifacts are present in `artifacts/`:

- **machine-gate** and **hiring-funnel** when a resume, cover letter, or application answers exist (the automated layer, and the human funnel).
- **consistency-auditor** and **leverage-maximizer** whenever any application artifact exists: they judge the artifact set against `career.md`, `preferences.md`, and the research.
- **outreach-judge** when outreach actions (`artifacts/outreach.md`) exist.

Pass each the opportunity folder path. The agents read the artifacts, JD, research, and source-of-truth files themselves and return findings; they never edit.

## Condense

Each advisor returns a detailed report. Do not relay them verbatim. For each, distil a few sentences of the load-bearing, actionable findings, in the candidate's interest: what would actually lose the interview, and what would win it. A handful of short advisor notes, not a stack of long reports.

## Triage and auto-apply

Sort every finding into two buckets:

- **Obvious, no-downside fixes: apply them yourself before presenting.** These are the deterministic, mechanical corrections that need no judgement and touch no content decision: date-format and section-header fixes, contact placement, Australian spelling localisation. Edit the artifact's YAML and re-render with `co render`; for a formatting-only fix, edit the `.tex` and re-render it directly. If you modify the tex, always warn the user about it because your changes will get overridden if they edit the source artifact and re-render.
- **Judgement calls: never auto-apply; present for the candidate's decision.** Anything touching prose voice, a number, a title or level, arrangement, the substance of an answer, or an outreach action. Anything where the advisors disagree. Anything that depends on a fact you cannot confirm. These belong to the candidate (and, where they want it applied, to the create step), not to you.

## Present

Give the candidate: the advisor notes, a short list of the fixes already applied, and the judgement calls awaiting their decision, each with the advisor's reasoning. The candidate does their own final review on top of this; your job is to remove the obvious friction and frame the real decisions, not to make them.
