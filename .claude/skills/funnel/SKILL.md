---
name: funnel
description: "Take a batch of job opportunities (URLs, screenshots, pasted JDs, or existing opportunity folders) through the whole pipeline: triage, setup, recon, second-pass triage, artifact creation, and vetting, ending in an action sheet. Use when several opportunities arrive at once, or when the user wants end-to-end processing rather than a single stage."
argument-hint: <urls, pasted JDs, folder paths, or "continue">
disable-model-invocation: false
allowed-tools: Skill(assess), Skill(recon), Skill(create), Skill(vet), Read, Glob, Grep, Bash(co *)
---

$ARGUMENTS

---

## Intent

Run the whole pursuit pipeline over a batch, so the user specifies opportunities once and receives applications ready to submit. The stage skills do the work and hold the judgement; this protocol only sequences them, carries state between stages, and pauses at the checkpoints. It has no domain logic of its own.

## The checklist

At the start of a run, emit this table and re-emit it updated as stages complete. It is the funnel's working state in the conversation.

| Opportunity | Triage | Recon | Verdict | Effort | Artifacts | Vet |
|---|---|---|---|---|---|---|

State on disk is authoritative: folder presence, the JD frontmatter, the recon files, `artifacts/`, and the tracker. When asked to continue a funnel (this session or a later one), rebuild the table from disk and proceed from where it stands.

## Stages

**1. Intake.** Accept a batch in any mix: fetchable URLs, screenshots, pasted JD text, pre-made folders. Create nothing yet. (Discovering new opportunities is a separate front door; the funnel runs from whatever it is handed.)

**2. Triage.** One `/assess` pass over everything. **Checkpoint: present the verdicts and wait for the user's nod.** On the nod, a Skip with an existing folder is archived (`co archive <slug>`), a Skip without one is dropped, and neither is logged in the tracker.

**3. Setup.** For each survivor without a folder, scaffold it (`co new-opportunity <organisation>/<opportunity>`, then place the JD, per `cli/README.md`), and offer to log each pursuit in the tracker.

**4. Recon.** `/recon` per survivor, fanned out concurrently across organisations. **Serialise within an organisation:** opportunities of the same organisation share and accrete the same `org-recon.md`, so run those one after another; opportunities of different organisations run in parallel. Recon may resolve a listing to a different first-party employer (re-parenting the folder), flag a better-fit sister role as a new opportunity, or flag a listing as a likely ghost or unresolvable.

**5. Resolve.** `/assess` each researched folder for a second-pass, recon-grounded verdict. **Any sister role recon spawned, and any newly-created opportunity, re-enters at first-pass triage** (step 2) rather than skipping it; a ghost or unresolvable listing is dropped. From the second-pass verdict and EV, set the effort tier in the `job-description.md` frontmatter (`low`, `standard`, `high`): it records the pursuit's stakes and orders the work, highest first.

**6. Produce.** Per Apply, highest effort first, `/create`. Create produces every artifact the opportunity's inputs allow: resume and cover letter by default, application answers when recon captured questions, outreach actions when recon identified targets.

**7. Vet.** `/vet` per Apply. Vet condenses its panel into a few actionable notes per advisor, applies the obvious no-downside fixes itself, and surfaces the judgement calls. **Checkpoint: the judgement calls wait for the user's nod.**

**8. Action sheet.** The terminal output:

```
# Action sheet, <date>

## Apply
| Organisation | Role | Apply at | Artifacts | Effort |
|---|---|---|---|---|

## High-leverage actions
<from each opportunity's targets.md and recon signals: who to contact and on what hook, referral paths to check in the user's own network, sister roles worth pursuing>

## Pipeline updates
<tracker rows added or pending; reminders to report outcomes>
```

As the user reports applying, update the tracker.

## Bounds

Stages run in the main conversation; only the stage skills themselves fork or spawn agents. If the user supplies a single opportunity, the protocol still applies; it just has one row.
