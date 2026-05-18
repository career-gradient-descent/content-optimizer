---
name: vet
description: Run ats-insights, recruiter-scan, and gap-analyzer in parallel on an opportunity's resume. Use for a complete pre-submission stress test.
argument-hint: <opportunity-folder-or-slug>
---

Spawn three subagents in parallel via the Agent tool to evaluate the resume for the opportunity referenced by $ARGUMENTS. The input may be a slug (`sonder-fullstack-ai-agentic-systems`), a folder path (`opportunities/sonder-fullstack-ai-agentic-systems/`), an @-mention of the folder, or even an @-mention of a file inside the folder (`job-description.md`, etc.). Resolve all of these to the opportunity folder, then locate the resume PDF at `<opportunity-folder>/artifacts/resume.pdf`.

Agents to spawn (all three in a single message, in parallel):
- `ats-insights` — machine-layer ATS evaluation
- `recruiter-scan` — human reviewer funnel (4 personas, visual scan)
- `gap-analyzer` — things the JD wants that career.md has but the resume doesn't surface

All three are JD-specific; this skill assumes a job-shaped opportunity. Pass each agent the opportunity folder path as its input. Present each agent's full report verbatim, in the order listed above.