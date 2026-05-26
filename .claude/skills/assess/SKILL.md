---
name: assess
description: Score one or more job opportunities (URL, pasted JD, or opportunity folder path) against career.md and preferences.md. Outputs verdict (Apply / Maybe / Skip) with V/P/EV scores and evidence in chat. For triage before deciding whether to pursue.
argument-hint: <url-or-path-or-paste> [more...]
disable-model-invocation: true
allowed-tools: Read WebSearch WebFetch Glob Grep Bash(python3 *)
model: opus
effort: high
---

$ARGUMENTS

---

## Intent

Quick-fidelity triage. Produce a verdict (Apply / Maybe / Skip) per opportunity, backed by 7 dimension scores and evidence quotes, so the user can decide whether to pursue without reading every JD end-to-end.

Outcome-agnostic scoring: the LLM judges each dimension independently with a cited evidence span; arithmetic (V, P, EV, verdict) is done in deterministic inline python via Bash. The model never computes the final number in its head — that prevents subconscious bias from a desired verdict shaping the dimension scores.

## Inputs

Per opportunity, any of:
- A URL → fetch via WebFetch.
- A file path or opportunity folder path → Read. For an opportunity folder, the JD is `job-description.md`.
- Pasted JD text inside `$ARGUMENTS`.

`$ARGUMENTS` may contain multiple opportunities, mixed types, and conversational filler around them. Parse intent, isolate the JDs.

For every run, also read:
- `career.md` at repo root (candidate background, source of truth).
- `preferences.md` at repo root (floors, walk-aways, situational overrides).

If `preferences.md` doesn't exist, fall back to defaults below and flag in the output that preferences-grounding is missing — V2 and V4 scores will be guesswork without it.

## Rubric

Seven dimensions. Score each 0–4 with one evidence quote (from the JD, career.md, or preferences.md) that anchors the score. Score dimensions **independently** — do not let a prior dimension's score bias the next one. If two dimensions feel coupled, score them in separate passes mentally.

Anchors:
- **0**: missing evidence or disqualifying signal.
- **1**: present but weak.
- **2**: meets the bar.
- **3**: above the bar.
- **4**: standout / well above.

Reserve 0 for genuine absence or disqualification — not "low." A 0 in any P-dimension typically means the opportunity is unwinnable on that axis.

### Value side (V1–V4)

- **V1 Role substance** — skill variety, autonomy, ownership, feedback loops in the actual work. [Job Characteristics Model; Humphrey, Nahrgang & Morgeson 2007]
- **V2 Needs-supplies fit** — does this job match what *this* candidate explicitly wants (per preferences.md "What you want from a role" + career.md About)? [Kristof-Brown, Zimmerman & Johnson 2005]
- **V3 Demands-resources balance** — workload realism, on-call shape, sustainability. Red-flag phrases ("wear many hats", "fast-paced startup", vague unlimited scope) lower this; explicit supportive language raises it. [Job Demands-Resources; Bakker & Demerouti 2017]
- **V4 Total rewards** — comp + location/remote + benefits vs the candidate's floor in preferences.md. Pay correlates weakly with satisfaction (Judge et al. 2010, r≈0.15), so score this as a near-binary band: 0 below floor, 2 meets floor, 3 above floor, 4 well above.

### Probability side (P1–P3)

- **P1 Demands-abilities fit** — hard requirements (skills, years, level, domain) the candidate actually meets. [Kristof-Brown D-A; Sackett, Zhang, Berry & Lievens 2022]
- **P2 Surface match** — keyword overlap, role-title alignment, recency. Proxy for ATS parsing and the 7-second recruiter scan. [Bertrand & Mullainathan 2004; audit-study literature]
- **P3 Differentiation** — quantified achievements, named systems, evidence of above-bar performance versus typical applicants. [Selection-validity proxy; Sackett 2022]

## Defaults

```
V weights:  V1=0.25  V2=0.40  V3=0.20  V4=0.15
P weights:  P1=0.50  P2=0.30  P3=0.20
Verdict:    Apply if V >= 2.0 AND P >= 2.0
            Maybe if V >= 2.0 OR  P >= 2.0
            Skip  otherwise
```

If `preferences.md` has a "Situational scoring overrides" section, use those values instead. Be explicit in the output about which weights/thresholds were used.

## Aggregation

After scoring all 7 dimensions for one opportunity, compute V, P, EV, and verdict via inline python — do not eyeball the math. Substitute the actual scores; keep weights/thresholds as the defaults above unless preferences.md overrides them.

```bash
python3 -c "
v1, v2, v3, v4 = ?, ?, ?, ?
p1, p2, p3 = ?, ?, ?
vw = (0.25, 0.40, 0.20, 0.15)
pw = (0.50, 0.30, 0.20)
av, ap, mm = 2.0, 2.0, 2.0   # apply_v, apply_p, maybe_min

V  = vw[0]*v1 + vw[1]*v2 + vw[2]*v3 + vw[3]*v4
P  = pw[0]*p1 + pw[1]*p2 + pw[2]*p3
EV = V * P
verdict = ('Apply' if V >= av and P >= ap else
           'Maybe' if max(V, P) >= mm else
           'Skip')
print(f'V={V:.2f}  P={P:.2f}  EV={EV:.2f}  verdict={verdict}')
"
```

For multiple opportunities, run this once per opportunity (or fold into a single python block printing one line per opportunity if there are many — your call).

## Output format

### Single opportunity

```
# Assess: <opportunity name or URL>

**Verdict: <Apply / Maybe / Skip>**
V = <X.XX>   P = <X.XX>   EV = <X.XX>

| Dim | Score | Evidence |
|---|---|---|
| V1 Role substance      | <0-4> | "..." (source) |
| V2 Needs-supplies fit  | <0-4> | "..." (source) |
| V3 Demands-resources   | <0-4> | "..." (source) |
| V4 Total rewards       | <0-4> | "..." (source) |
| P1 Demands-abilities   | <0-4> | "..." (source) |
| P2 Surface match       | <0-4> | "..." (source) |
| P3 Differentiation     | <0-4> | "..." (source) |

## Reasoning
<3-5 sentences synthesising the verdict, surfacing the load-bearing signals.>

## Notes
<Red flags, missing data, any deviation from default weights/thresholds and why.>
```

### Multiple opportunities

Prepend a ranking, then the per-opportunity blocks:

```
# Assess: <N> opportunities

## Ranking (by EV, then by P)

1. <name>: EV=X.XX  (V=Y.YY / P=Z.ZZ) — <verdict>
2. ...

## Detail

<single-opportunity block per opportunity, in ranked order>
```

## Anti-patterns

- **Scoring without evidence.** Every dimension needs a citation. No exceptions.
- **Verdict-first reasoning.** Score the dimensions before running the math. If you have a gut verdict before scoring, score harder against it as a check.
- **Inferring P from JD vibes.** P1 is concrete D-A matching against career.md, not "feels like a good fit."
- **Over-scoring V4 (comp).** Pay weakly predicts satisfaction. Use it as a floor check, not a leading signal.
- **Hallucinating fit when preferences.md is missing data.** If a section is empty or stubbed, say "no preferences-grounding for this dimension" in the Notes rather than inventing fit.
- **Em-dashes in prose output.** Use periods, commas, colons, semicolons. (Per `.claude/rules/anti-patterns.local.md`.)
