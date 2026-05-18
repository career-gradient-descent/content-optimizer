---
name: research-opportunity
description: Research an opportunity for context that informs downstream artifact creation
argument-hint: <opportunity-path> <context>
disable-model-invocation: true
context: fork
agent: general-purpose
model: opus
effort: xhigh
allowed-tools: WebSearch WebFetch Read Write Glob Grep Bash(curl *)
---

$ARGUMENTS

---

## Intent

Research the opportunity beyond the JD: the company's situation, the team's technical reality, the hiring process and ATS in use, the people involved, recent developments. This research drives downstream artifact creation; evaluate each finding by whether it can shape an artifact decision.

## Scope

Starting dimensions. Once these are covered, diverge into threads unique to the opportunity.

- Company: profile, business model, funding stage, financial health, revenue model
- Culture: real working norms and values
- Technical: stack, engineering practices, development culture
- Hiring: ATS system and its parsing behaviors, interview format and stages, compensation benchmarks
- People: hiring manager, team lead, potential interviewers
- Context: recent news, strategic direction, team specifics, competitive landscape for the role
- For people focused research: background, current role, interests, recent public activity, company context, approach angle

## Approach

Research in rounds.

First round: cast a wide net of searches across all relevant dimensions to map the landscape. Second round: for threads that yielded signal, go deeper. Fetch full pages, find primary sources, cross-reference claims. Third round and beyond: follow new threads that earlier rounds uncovered.

Each round should surface questions that the next round answers. A productive round opens new lines of inquiry. A spent round yields nothing actionable. Stop only when rounds stop being productive.

## Output

Write findings to `research.md` in the opportunity folder, structured for downstream consumption by another agent creating tailored career artifacts. Do not modify existing files.
