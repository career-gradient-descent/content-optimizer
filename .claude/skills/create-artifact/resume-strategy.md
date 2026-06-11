# Resume Strategy

## The governing rule

Tailoring detectability lives in prose, not arrangement. A reviewer spots a tailored resume when its words echo the JD: mirrored phrasing, niche identifiers in the summary, keyword-shaped bullets. Nobody spots tailoring from which section leads, which role carries five bullets, or which projects appear; those read as the candidate's natural emphasis.

So allocate the tailoring budget by detectability:

- **The default is the prose anchor.** Words come from `defaults/resume.yaml` and `career.md`. Its voice and phrasing are calibrated; keep them.
- **The opportunity is the arrangement driver.** Structure (order, emphasis, selection) comes from the JD and `research.md`. Move it freely.

## The decision sheet

Walk every decision below for each opportunity. The `## Artifact directives` section of `research.md` grounds them; without research, decide from the JD alone and say so in the summary to the user.

### Arrangement — move freely

- **Section order** (`section_order` in the YAML): lead with what the first reviewer values. HR-gated or industrial: skills and experience up top, education and publications late. Research-shaped: education and publications early. Engineer-read (hiring manager direct, small startup): experience or projects first.
- **Entry order within Experience**: the top entry is the schema anchor, the role a scanning recruiter takes as "what this person is". Lead with the most relevant role, not necessarily the most recent. Dates stay prominent so reordering never reads as concealment.
- **Bullet budget per role**: allocate by relevance. Lead roles carry 4-5 bullets, distant ones 1-2. This shifts emphasis without changing a single word.
- **Page-1 top half**: after rendering, read the PDF. The strongest opportunity-relevant signal belongs above the fold; rearrange until it is.

### Selection — free, bounded by career.md

- **Bullets**: select from career.md's full pool per role, not only the default's picks.
- **Facets**: career.md holds several true framings of the same work (the Fisdom notifications service is simultaneously a greenfield microservice, a monolith decomposition, and regulated OTP traffic). Surface the facet this opportunity values. Selection of true facets, never composition of new claims.
- **Company taglines**: same facet logic; describe each employer by the dimension this opportunity cares about.
- **Roster toggles**: projects, publications (full section, single line, or off), education detail (coursework and thesis for grad-shaped roles, one line for industry), links (Scholar in for research roles), interests on or off.
- **Skills section**: the one visible keyword-matching surface. For skills genuinely held per career.md, mirror the JD's term for them in canonical form; naming a real skill by the reader's word is selection, not imported vocabulary.
- **Titles**: adjacent-synonym and market-localisation adjustments are fine (Back End Developer ↔ Backend Engineer; dropping an India-market level suffix like "SDE-1" for readers it won't parse). Level inflation never.

### Prose — anchored

- **Summary**: full rewrite is allowed, under hard constraints: every claim traceable to career.md, vocabulary limited to what the visible resume substantiates, ubiquitous tech only. Specialized identifiers belong in Experience or Projects (per the anti-patterns rule).
- **Bullets**: when rewording, re-anchor from career.md's richer descriptions; pick the chosen facet's words. Never import vocabulary that exists only in the JD.
- **Spelling**: match the market. Australian opportunities get Australian English ("organisation" scores on PageUp; "organization" does not).

### Invisible layer — aggressive

- `basics.ats_optimization`: invisible text rendered via `\atsKeywords{}` (hard-capped at 13 words). ATS parsers extract it, humans never see it. Pack JD keywords that would look unnatural in visible text. Adjust only for a known target ATS; with none identified (human-only review, direct email), the default's keywords stand. Greenhouse-class ATSs surface extracted text to recruiters, so keep it defensible: canonical forms and acronym expansions of skills the visible resume already claims.
- `meta.subject` and `meta.keywords`: PDF metadata in `\hypersetup{}`, also invisible and machine-readable. Role title, key skills, industry terms.

## ATS specifics

- **Evidence over listing.** LLM-rubric ATSs (Ashby, Lever Talent Fit) grade by citing evidence spans. "Strong communication skills" is un-citeable; "Negotiated $2M renewal across 6 stakeholders" demonstrates it with provable content.
- **Canonical skill names.** Taxonomy-aligned ATSs (SmartRecruiters, SAP SuccessFactors) normalize to standard forms: "JavaScript" not "JS", "Python" not "python3", "Amazon Web Services (AWS)" full plus acronym on first mention.
- **Competency frameworks.** When a JD references a formal framework, mirror the exact capability titles as phrases in bullets. APS Integrated Leadership System: "Achieves Results", "Communicates with Influence", "Supports Productive Working Relationships", "Shapes Strategic Thinking", "Exemplifies Personal Drive and Integrity". Literal-match ATSs (PageUp, Taleo) weight these directly.
