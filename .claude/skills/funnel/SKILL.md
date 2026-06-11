---
name: funnel
description: Take a batch of job opportunities (URLs, screenshots, pasted JDs, or existing opportunity folders) through the full pipeline - triage, setup, research, second-pass assessment, artifact generation, vetting - ending in an action sheet. Use when several opportunities arrive at once, or when the user wants end-to-end processing rather than a single stage.
argument-hint: <urls, pasted JDs, folder paths, or "continue">
disable-model-invocation: false
allowed-tools: Skill(assess), Skill(research-opportunity), Skill(create-artifact), Skill(vet), Read, Glob, Grep
---

$ARGUMENTS

---

## Intent

Run the whole pursuit pipeline over a batch, so the user specifies opportunities once and receives applications ready to submit. The stage skills stay pure functions; this protocol is the program that sequences them, carries the contracts between stages, and pauses at exactly two checkpoints.

## The checklist

At the start of a run, emit this table; re-emit it updated as stages complete. It is the funnel's working state in the conversation.

| Opportunity | Triage | Research | Verdict | Effort | Artifact | Vet |
|---|---|---|---|---|---|---|

State on disk is authoritative: folder presence, frontmatter, `research.md`, `artifacts/`, the tracker. When asked to continue a funnel (this session or a later one), rebuild the table from disk and proceed from where it stands.

## Stages

**1. Intake.** Accept 1-10 opportunities in any mix: fetchable URLs, screenshots, pasted JD text, pre-made folders. Create nothing yet.

**2. Triage.** One `/assess` pass over everything. Then **checkpoint: present verdicts and wait for the user's nod.** On the nod: Skips with existing folders are archived (`co archive <slug>`), Skips without folders are dropped, and neither is logged in the tracker.

**3. Setup + research.** For each survivor without a folder, set it up per the cases in `cli/README.md`, and offer to log each pursuit in the tracker. Then `/research-opportunity` per survivor.

**4. Resolve.** `/assess` each researched folder (second-pass verdict, research-grounded). From the verdict and EV, set the effort tier and record it in the folder's `job-description.md` frontmatter:

- **low**: borderline Apply, low stakes. Vet fixes auto-applied, final PDF + changelog presented.
- **standard**: solid Apply. Vet fixes auto-applied where no-downside; prose-adjacent suggestions proposed first.
- **high**: high-stakes pursuit. Full vet reports, diffs proposed before any edit, re-vet after fixes.

**5. Produce + harden.** Per Apply, in effort order (high first): `/create-artifact resume`, then `/vet`, then act on the reports as the effort tier prescribes.

Auto-applicable (no-downside) fixes: deterministic-layer findings (date formats, section headers, contact placement), arrangement and selection changes fully covered by career.md, spelling localisation, invisible-layer keywords within the cap. Always proposed, never auto-applied: prose rewording, anything touching a number, title or level presentation. **Checkpoint: proposed fixes wait for the user's nod.** Re-render after edits.

**6. Action sheet.** The terminal output:

```
# Action sheet — <date>

## Apply
| Organisation | Role | Apply at | Resume | Effort |
|---|---|---|---|---|

## High-leverage actions
<from each research.md's artifact directives: people to contact, referral paths, sister roles>

## Pipeline updates
<tracker rows added or pending; reminders to report outcomes>
```

As the user reports applying, update the tracker.

## Bounds

Stages run in the main conversation; only the stage skills themselves fork or spawn agents. Cover letters and outreach are produced on request, not by default. If the user supplies a single opportunity, the protocol still applies; it just has one row.
