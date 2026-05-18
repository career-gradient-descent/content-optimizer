# Resume Strategy

## Default-as-baseline, tactical modification

When a default resume exists, treat it as the calibrated baseline and modify it tactically for each opportunity. Reorder bullets, swap 1-2 for stronger alternatives from career.md, tweak summary phrasing, adjust skills emphasis, toggle optional sections. Preserve voice, length, and structure. Do not regenerate from scratch — that produces hyper-optimized over-fits that read as obviously tailored. The default's calibration is doing real work; respect it.

The resume operates on three layers, each with different rules for how aggressively it can be optimized.

## The trojan horse (invisible layer)

`basics.ats_optimization`: invisible text rendered via `\atsKeywords{}` in the PDF. ATS parses it, humans never see it. This is where keywords from the JD that would look unnatural in visible text can be packed aggressively. No subtlety needed here; this text exists purely to get past the gates.

`meta.subject` and `meta.keywords`: PDF metadata fields in `\hypersetup{}`. Also invisible, also machine-readable. Use for role title, key skills, and industry terms.

## Summary

First thing a recruiter reads after the name. Sets the narrative for the entire resume. Should align with the role while reading naturally. Not a keyword dump.

## Visible content (Experience, Projects, Education, Skills)

Writing style rules apply here. Each bullet should serve the 6-second recruiter scan and the deep technical read simultaneously. The Skills section is a direct keyword matching opportunity: mirror the JD's terminology where genuine.

**Evidence over listing.** Bullets must demonstrate skills through specific achievements rather than asserting them. An LLM-based grader should be able to cite a concrete evidence span for any skill claimed. "Strong communication skills" is un-citeable; "Negotiated $2M renewal across 6 stakeholders" demonstrates the same skill with provable content. Matters most for LLM-native ATSs (Ashby, Lever Talent Fit) and future-proofs against industry drift toward LLM-based scoring.

**Canonical skill names.** Use industry-standard forms: "JavaScript" (not "JS"), "Python" (not "python3"), "Amazon Web Services (AWS)" (full + acronym on first mention). Creative rephrasing confuses taxonomy-aligned ATSs (SmartRecruiters, SAP SuccessFactors) that normalize to standard forms.

## Competency frameworks

When a JD references a formal competency framework (Australian Public Service Integrated Leadership System, UK Civil Service Behaviours, large-consultancy frameworks, etc.), mirror the exact capability titles as phrases in bullets. For APS specifically: "Achieves Results", "Communicates with Influence", "Supports Productive Working Relationships", "Shapes Strategic Thinking", "Exemplifies Personal Drive and Integrity". Literal-match ATSs (PageUp, Taleo) weight these directly.
