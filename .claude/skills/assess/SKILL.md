---
name: assess
description: "Score one or more job opportunities (URL, pasted JD, or opportunity folder) for whether to apply. Produces a V (value to the candidate) and P (probability of getting it) score, an EV ranking, and an Apply/Maybe/Skip verdict backed by cited evidence. Use to triage before pursuing."
argument-hint: <url-or-path-or-paste> [more...]
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash(python3 *), Bash(co fetch-jd *), Bash(co tracker read *)
model: opus
effort: high
---

$ARGUMENTS

---

## Intent

Quick triage. Per opportunity, produce a verdict (Apply / Maybe / Skip) backed by two scores: **V**, how good the role is for the candidate, and **P**, how likely the candidate is to get it. The scores let a batch be sorted by EV so the worthwhile ones surface without reading every JD end to end.

Score each dimension on its own evidence, then compute the verdict with deterministic python, never in your head. The arithmetic is what stops a wanted verdict from bending the dimension scores.

## Inputs

Per opportunity, any of:

- A URL → fetch the JD verbatim with `co fetch-jd <url>`; if it gives up, ask for a paste.
- A pasted JD, or a screenshot/image of one → read it directly.
- An opportunity folder → read everything in it (JD, recon, notes), plus shared organisation-level files one level up. A recon'd folder is a second-pass verdict: recon grounds the dimensions a JD alone cannot.

For every run also read `career.md` (the candidate, source of truth) and `preferences.md` (floors, walk-aways, situational scoring). Search the tracker per organisation (`co tracker read | grep -i <organisation>`); on a hit, surface the prior application in the notes. If `preferences.md` is missing or thin on a dimension, say so and do not invent fit.

## Rubric

Seven dimensions, each scored 0–4 with one evidence quote (from the JD, `career.md`, `preferences.md`, or recon). Score them **independently**, not letting one dimension's score pull the next. Reserve **0 for a genuine absence or disqualifier, never for "the JD didn't say"**: missing evidence is *unknown*, flagged for recon, never a silent zero.

Anchors: 0 absent or disqualifying · 1 weak · 2 meets the bar · 3 above · 4 standout.

**Value: how good the role is for the candidate**

- **V1 Role substance**: skill variety, autonomy, ownership, and real feedback loops in the work. Autonomy and feedback are the strongest drivers.
- **V2 Needs-supplies fit**: does the work match what *this* candidate wants (`preferences.md` "what you want" plus `career.md` About)? The strongest predictor of satisfaction, and the easiest to over-read from a JD: score it conservatively and never inflate it when `preferences.md` is thin.
- **V3 Sustainability**: demands versus resources: workload realism, on-call shape, team support. A low score is a burnout risk, and is **surfaced prominently in the notes**. A great-fit role with no resourcing is a trap, not a win, and a strong V1 or V2 never buys that back.
- **V4 Total rewards**: comp, location, and remote against the candidate's floor. Near-binary (below floor / meets / above); never let comp lead the verdict.

**Probability: how likely the candidate is to get it**

- **P1 Demands-abilities fit**: does the candidate plausibly clear the bar? Listed requirements are wish-lists, not gates: score **2 at roughly half of them met**, and reserve 0–1 only for a genuine disqualifier (no work rights, a categorical level mismatch), flagged in the notes rather than left to quietly sink the role.
- **P2 Surface match**: keyword, title, and recency overlap: the ATS-parse and seven-second-scan proxy.
- **P3 Differentiation**: quantified achievements, named systems, evidence of above-typical performance. The strongest real signal in the candidate's favour.

A known **referral or warm intro** is the single biggest real lever on P; when the user supplies one, raise P toward Apply and note it. The single biggest lever on **V**, who the candidate would report to and the team, is usually invisible at triage: name it as the top thing recon should surface, and weigh it at the second pass.

## Defaults

```
V weights:  V1=0.30  V2=0.30  V3=0.25  V4=0.15
P weights:  P1=0.35  P2=0.30  P3=0.35
Verdict:    Apply if V >= 2.0 AND P >= 2.0
            Maybe if V >= 2.0 OR  P >= 2.0
            Skip  otherwise
EV = V * P, a coarse ranking key for ordering a batch, never the verdict itself.
```

If `preferences.md` has a "Situational scoring overrides" section, use those weights and thresholds instead, and say which you used.

## Aggregation

After scoring all seven dimensions, compute V, P, EV, and the verdict in one python block. Do not eyeball it.

```bash
python3 -c "
v1, v2, v3, v4 = ?, ?, ?, ?
p1, p2, p3     = ?, ?, ?
vw = (0.30, 0.30, 0.25, 0.15)
pw = (0.35, 0.30, 0.35)
av, ap, mm = 2.0, 2.0, 2.0   # apply_v, apply_p, maybe_min
V  = sum(w*s for w, s in zip(vw, (v1, v2, v3, v4)))
P  = sum(w*s for w, s in zip(pw, (p1, p2, p3)))
EV = V * P
verdict = ('Apply' if V >= av and P >= ap else
           'Maybe' if max(V, P) >= mm else
           'Skip')
print(f'V={V:.2f}  P={P:.2f}  EV={EV:.2f}  verdict={verdict}')
"
```

For several opportunities, run it once each, or fold them into one block printing a line apiece.

## The verdict is the caller's signal

The verdict is what the caller acts on, and the caller may be the user or the funnel (which drops Skips early), so it must be decisive where the evidence is decisive and cautious only where the call is genuinely close.

- A clear non-match, low value and low odds on solid evidence, is a confident **Skip**. Most blindly-submitted URLs are these; do not soften an obvious no into Maybe.
- Reserve the caution for the genuinely close call: when a score sits near a threshold, or the JD is too thin to score with confidence, lean **Maybe** rather than a silent Skip, because a wrongly-dropped good role is never seen again.
- A single weak dimension does not sink a role the rest of the evidence supports; surface it as a flagged concern in the notes and let the weighted verdict stand. The skill flags; the caller decides.
- EV orders a batch coarsely; small EV gaps are noise, not a precise ranking.

## Output format

### Single opportunity

```
# Assess: <name or URL>

**Verdict: <Apply / Maybe / Skip>**
V = <X.XX>   P = <X.XX>   EV = <X.XX>

| Dim | Score | Evidence |
|---|---|---|
| V1 Role substance     | <0-4> | "..." (source) |
| V2 Needs-supplies fit | <0-4> | "..." (source) |
| V3 Sustainability     | <0-4> | "..." (source) |
| V4 Total rewards      | <0-4> | "..." (source) |
| P1 Demands-abilities  | <0-4> | "..." (source) |
| P2 Surface match      | <0-4> | "..." (source) |
| P3 Differentiation    | <0-4> | "..." (source) |

## Reasoning
<3-5 sentences on the load-bearing signals behind the verdict.>

## Notes
<Flagged concerns (low sustainability, a disqualifier, a thin JD), missing data routed to recon, tracker history, and which weights/thresholds were used.>
```

### Multiple opportunities

Prepend a ranking by EV, then the per-opportunity blocks in ranked order.

```
# Assess: <N> opportunities

## Ranking (by EV)
1. <name>: EV=X.XX  (V=Y.YY / P=Z.ZZ), <verdict>
2. ...

## Detail
<one single-opportunity block each, in ranked order>
```

## Anti-patterns

- **Scoring without evidence.** Every dimension needs a cited quote.
- **Verdict-first reasoning.** Score before the math; if you feel a verdict coming, score harder against it.
- **Treating a JD's requirement list as hard gates.** They are wish-lists; roughly half met clears the bar.
- **Silent Skips on uncertainty.** A clear non-match is a confident Skip, but never let a thin JD or one weak dimension quietly drop a role the evidence does not clearly rule out; lean Maybe and surface the reason.
- **Comp or halo inflation.** Pay barely predicts satisfaction, and needs-supplies fit is the easiest score to over-read; never let either carry a verdict.
