# Content Optimizer

A per-opportunity pipeline for career-marketing artifacts. It is reductive: it selects, arranges, and polishes the candidate's real material for a specific opportunity, rather than generating new claims. Deterministic mechanics live in the `co` CLI; judgment lives in the skills and agents.

## Vocabulary

- **Organisation**: a company or recruiting agency. The parent; holds context shared across its opportunities.
- **Opportunity**: a specific demand being pursued, usually a job opening. The unit of work.
- **Job description (JD)**: the verbatim, ground-truth text of an opportunity's posting.
- **Recon**: decision-relevant intel gathered about an opportunity and its organisation to inform its artifacts.
- **Signal**: a recon finding that informs an artifact decision, expressed as a fact, never as an instruction on how to write.
- **Target**: an outreach recipient or channel identified by recon (a person, a post, an email).
- **Artifact**: anything the pipeline produces for an opportunity to submit or act on: resume, cover letter, application answers, outreach actions.
- **Outreach action**: a drafted, ready-to-send message aimed at a target. The pipeline drafts it; the user sends it.

## The opportunity folder

Every opportunity lives at `opportunities/<organisation>/<opportunity>/`, always nested. The folder is the pursuit's source of truth, held on disk rather than in conversation. A fully-populated pursuit:

```
opportunities/
  <ORGANISATION>/             # an organisation
    org-recon.md              # recon shared across the organisation's opportunities
    <ROLE>/                   # an opportunity
      job-description.md      # the JD
      recon.md                # recon for this opportunity
      questions.md            # application-page questions
      targets.md              # outreach targets
      artifacts/              # everything produced to submit or send
        resume.pdf
        cover-letter.pdf
        answers.md
        outreach.md
```

Knowledge sits inside the opportunity folder; produced deliverables go inside its `artifacts/` subfolder; anything shared across an organisation's opportunities sits in the organisation folder, next to them.

## The pipeline

Each pursuit moves through stages, each its own skill: discovery, triage, recon, artifact creation, and vetting, with the funnel composing them over a batch. Reach for the skill that matches the work.

## Source of truth

The user maintains these by hand. Read them freely; edit only the tracker, and only when the user asks.

- **`career.md`**: the candidate's full profile. Every claim in an artifact traces back to it exactly.
- **`preferences.md`**: floors, walk-aways, and situational scoring that ground triage.
- **`tracker.xlsx`**: application state, read via `co tracker read`.

## Tools

`co` is the project's CLI: deterministic, auditable primitives for the mechanical steps (scaffolding, JD fetch, rendering, the tracker). Read `cli/README.md` or run `co <command> --help` before using it, and prefer this deterministic path for anything that must be exact.
