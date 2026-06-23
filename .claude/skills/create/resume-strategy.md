# Resume Strategy

A per-opportunity resume is a *bounded deviation* from a calibrated default: never a from-scratch rewrite, never a verbatim copy. Stay between two failure poles. A resume rebuilt for the role reads as bespoke and too-eager, painting the candidate as suspiciously perfect for it. A resume that merely re-emits the default is not tailored at all. The work is meaningful tailoring inside tight bounds.

## Anchor on the default

Tailor the calibrated default at `defaults/resume.yaml`: make selection and arrangement edits over known-good material rather than generating greenfield. The default supplies the voice, the structural home, and the candidate's full set of entries; per-opportunity work moves within it. Candidate-specific bounds live in the Resume section of `strategy.local.md`.

## Fixed across every opportunity

- **Fill the page; never leave it short.** When there is enough real material for the target length, use it; an underfull resume is a defect, not restraint. Trim to fit only when there is too much, and never pad with filler.
- **Substantial roles are not dropped or buried.** Real experience stays present and in rough chronology; tailoring reorders within bounds, it does not erase history.
- **Voice and prose** come from the default and `voice.local.md`.

## Flexible per opportunity, within bounds

- **Section order leans to the audience; it does not reshuffle.** Industry-facing roles lead with experience and projects and push education and publications later; research- or academia-leaning roles bring education and publications forward. Skills may rise to just under the summary when the first reviewer is non-technical HR or a keyword gate. Interests stay last.
- **Lead with the stronger asset.** Order experience and projects by which is the candidate's stronger signal; the weaker one supports it, never displaces it.
- **Select within a pool.** Where the candidate has more material than fits (extra projects, optional entries), choose the most relevant; the rest sit out.
- **Place each entry by relevance.** A recent but less-relevant role may move down while the core holds rough chronology. Within an entry, pick the bullets and framing the opportunity values, from `career.md`'s fuller pool.

## Act on the ATS signal

Recon identifies the ATS. Let it shape word choice, never honesty:

- **Canonical skill names.** Taxonomy-aligned platforms normalise to standard forms: prefer "JavaScript" to "JS", "Amazon Web Services (AWS)" full plus acronym on first use. Name a real skill by the reader's canonical word; that is selection, not imported vocabulary.
- **Literal matchers** (Taleo, PageUp, legacy Workday) reward verbatim JD terminology over synonyms. For an APS role, reproduce the work-level or ILS capability titles exactly as written ("Achieves Results", "Communicates with Influence"); paraphrase loses the match.

## The invisible layer

- **`meta.subject` and `meta.keywords`** are PDF metadata: machine-readable, never rendered, always defensible. Set them on every resume to the role title, key skills, and industry terms. Always safe, always on.
- **`basics.ats_optimization`** renders an invisible-but-extractable keyword line (hard-capped at 13 words). **Off by default.** It is a deliberate, rare choice, never a routine one: deploy it only when recon confirms a literal-keyword-gate ATS (Taleo, PageUp, legacy Workday) where dictionary matching rewards it and no content-integrity scan runs. Leave it off for Greenhouse, modern Workday, iCIMS, SmartRecruiters, Ashby, and Lever, which strip, flag, or surface the extracted text to a human, so the line runs from wasted to damaging. When deployed at all, keep it defensible regardless: only canonical forms and acronym expansions of skills the visible resume already substantiates, never a claim the resume does not back.

## Hard-to-fake credentials stay, and move

Publications, patents, and similar rare, verifiable credentials are signal reviewers weight precisely because they cannot be faked. Reposition them by audience (early and detailed for research-leaning roles, a single late line for purely industry ones) rather than dropping them.