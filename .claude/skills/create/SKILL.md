---
name: create
description: "Produce the tailored artifacts for an opportunity: resume and cover letter by default, plus application answers and outreach actions when research provides their inputs. Use once an opportunity is researched."
argument-hint: <opportunity-folder>
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(co *)
model: opus
effort: high
---

$ARGUMENTS

---

## What this does

Produce every artifact an opportunity needs, each one tailored to it: resume and cover letter by default, application answers when the opportunity has application questions to answer, and outreach actions when research has identified outreach targets. Each artifact surfaces the candidate's real material from `career.md`, shaped for this specific opportunity. Everything is written inside the opportunity's `artifacts/`.

## Inputs

For the given opportunity, read in full:

- `career.md`, the only source of the candidate's facts.
- the entire opportunity folder and the organisation-level files above it: the JD, all research, and anything else present (manual notes, extra material). Let the research signals drive what to tailor.
- `${CLAUDE_SKILL_DIR}/voice.local.md` for voice and `${CLAUDE_SKILL_DIR}/strategy.local.md` for the candidate's cross-artifact calibration, then each artifact's own discipline at `${CLAUDE_SKILL_DIR}/<artifact>-strategy.md`.

## The discipline

Tailoring is the whole job, and it has a precise shape:

- **Tailor by selection and arrangement, never by imitation.** Choose which true material to surface, and how to order and weight it, for this opportunity's audience. Hold the candidate's own calibrated voice.
- **Map signals to decisions, not to claims.** Research yields signals: who reads this, what they value, the ATS, the culture. Signals drive selection, ordering, and emphasis. Claims come only from `career.md`.
- **Fixed and flexible.** Each artifact holds some dimensions fixed across every opportunity and lets others flex per opportunity. Its strategy file draws that line; honor it exactly. The resume in particular allows only specific, bounded variation.
- **Fit reads as discovered, not engineered.** The result should look like a strong candidate who naturally suits the role, never a document reverse-engineered from the posting.

## Producing each artifact

Read the matching strategy file before producing. Each artifact has a fixed output, all inside the opportunity's `artifacts/`:

- **resume** → `resume.yaml`, rendered with `co render` to `resume.tex` and `resume.pdf`.
- **cover letter** → `cover-letter.yaml`, rendered with `co render` to `cover-letter.tex` and `cover-letter.pdf`.
- **application answers** → `answers.md`.
- **outreach actions** → `outreach.md`.

For the rendered artifacts, after rendering read the resulting PDF and check it renders cleanly and fills its target length before finishing.
