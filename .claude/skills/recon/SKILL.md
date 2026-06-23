---
name: recon
description: "Resolve an opportunity to its first-party source and gather the decision-relevant intel and outreach targets that drive artifact creation. Produces org-recon.md, recon.md, questions.md, and targets.md, and writes the resolved listing link and ATS into the JD frontmatter. Use after triage, before creating artifacts."
argument-hint: <opportunity-path>
disable-model-invocation: false
context: fork
agent: general-purpose
model: opus
effort: xhigh
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep, Bash(curl *), Bash(co tracker read *)
---

$ARGUMENTS

---

## Intent

Resolve the opportunity to its first-party source, then gather the intel and outreach targets that drive create and outreach. Every finding must map to a named downstream decision: a cover-letter line, a resume bullet or facet to surface, an application answer, a target to contact, or a parser constraint. If a fact maps to none of these, do not gather it. Recon produces signals, facts that inform an artifact decision, never instructions on how to arrange or write the artifact.

## Operating architecture: prefer login-free, escalate to the burner when it pays off

Treat the listing link as a pointer and resolve to the first-party source, reaching for, in order:

- **ATS public JSON APIs** (keyless, un-throttled): the most robust tier.
- **Logged-out search-engine X-ray** (Google, Bing), which needs no account and sidesteps platform throttles.
- **First-party careers pages**, read logged out.

When the login-free tiers come up short, step up the browser: first use a search engine's own advanced search logged out, then log in with a burner account for a platform's native advanced search (LinkedIn, Seek). Burner accounts are cheap and disposable, so use them freely once the cheaper tiers are exhausted; browse private and anonymous to keep the account clean. The earlier tiers are preferred for reliability and simplicity, not because the burner is off-limits: reach for it whenever it is the only thing that gets the result.

## Order of operations (order is leverage here)

First, check the tracker for prior applications to this organisation (`co tracker read | grep -i <organisation>`) and any existing `org-recon.md`, and skip ground already covered. Then:

1. **Resolve and identify the ATS in one move.** The board host is the ATS, so resolving the first-party listing and identifying the ATS are the same lookup, and that same ATS token also enumerates the company's other open roles (step 6). Do it first. Write the resolved first-party link and the identified ATS into the JD frontmatter (`url`, `ats`). If the listing is unresolvable or a likely ghost, record that and flag it for triage rather than spending effort downstream.
2. **Read the JD's working-rights language** as a signal (see Sponsorship).
3. **Hunt outreach targets** into `targets.md`.
4. **Gather the actionable company signals** into `recon.md` and `org-recon.md`.
5. **Pull the real application questions** from the first-party form into `questions.md`.
6. **Scan for a better-fit sister role** at the same organisation (same ATS token); on a find, flag it as a new opportunity for triage, never fan one resume across many roles.

## Resolving to first-party

The agency or aggregator link is rarely the real source. Resolve it:

- **Follow the external-apply redirect.** An aggregator "apply on company site" destination is the canonical ATS page. (Fails on in-platform apply such as LinkedIn Easy Apply.)
- **Distinctive-phrase reverse search is the single highest-yield move,** for both finding the first-party listing and un-blinding an agency ad: quote one unusual, verbatim 8-to-15-word line from the JD body into a search engine, since agencies paste the client's real JD and a distinctive line surfaces it. Use role-specific lines (named products, teams, quirky responsibilities), never EEO or boilerplate.
- **Confirm the ATS via its public API.** ATS URLs are predictable (`boards.greenhouse.io/<slug>`, `jobs.lever.co/<slug>`, `jobs.ashbyhq.com/<slug>`, `<tenant>.myworkdayjobs.com`, `apply.workable.com/<slug>`), and a keyless API confirms a guessed slug and returns the full JD plus the form questions:
  - Greenhouse: `boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true` (and `?questions=true` for the questions)
  - Lever: `api.lever.co/v0/postings/<slug>?mode=json`
  - Ashby: `api.ashbyhq.com/posting-api/job-board/<slug>`
  - Workable: `apply.workable.com/api/v1/widget/accounts/<slug>`

  Do not assume the token equals the company name; confirm with a live hit. Workday, iCIMS, and Taleo are JS-rendered and poorly indexed, so expect to fall back to the careers page for those.
- **Deduce a concealed employer** from a distinctive phrase, a named product or team or reporting line (both near-decisive when present), or a niche tech-stack-plus-city or funding-stage-plus-location shortlist (narrowing only, then confirm). Benefits language and generic jargon do not identify anyone.
- **Know when to stop.** Spend resolution effort only while the ad offers a distinctive, externally-checkable handle (a phrase, product, person, reporting line, or matching careers page). When three or more dead-end signals cluster (a fully boilerplate JD, a generic location only, "talent pool / EOI / register your interest" framing, several agencies running near-identical ads, board-only existence with no careers-page match), record "unresolvable" and move on; further automated resolution has negative value. A listing on aggregators but absent from the employer's own careers page is a likely ghost (about 1 in 9 in Australia): flag it for triage rather than tailoring against it.

Australian notes: on Seek, the "more jobs by this advertiser" pivot is the best local un-blinding move, since several ads from one anonymous poster can leak a shared detail; a registered entity or ABN essentially never leaks from a blind ad. When you deduce a concealed employer, the recruiter stays the outreach target: cold-contacting the deduced employer around the agency can backfire.

## Why first-party matters

The first-party source carries the fuller, cleaner JD (better keyword tailoring), the real application questions (so knockouts can be cleared before tailoring effort is spent), a smaller and more qualified applicant field, and an accurate open or closed state. Resolve before investing in artifacts.

## Outreach targets

Identify, do not contact: recon surfaces targets with evidence, and the candidate acts later from their own real, well-connected account. Per target, capture name, role, organisation, **agency or internal**, evidence (a post URL and date, a Meet-the-Hiring-Team listing, or a People-tab find), recency, a specific true **personalization hook**, and a **warm-path flag** ("check own network for a connection to this person"), since the burner cannot see the candidate's real network.

- **The highest-value find is anyone who publicly posted about this opening,** preferably recent: a fresh "we're hiring" post identifies a receptive, reachable human, often before the listing floods. Recency is load-bearing; a months-old post is near-worthless. Prefer logged-out X-ray (`site:linkedin.com/posts "we're hiring" "<role>" "<company>"`, with a recent-date filter), and fall back to the burner's in-app Posts search when X-ray comes up short. This LinkedIn hunt is browser work: if the browser tier is genuinely unavailable, record that gap in `targets.md` rather than reporting that no targets exist from a search you could not actually run.
- **Classify each opening agency or internal,** because Australian tech is heavily agency-run and it flips the target. Agency (anonymized employer, a recruiter named in the post, Seek agency branding) means the posting recruiter is the right target, since placing the candidate is their payday. Internal (named company, careers-page ATS link, an engineering-manager or talent poster) means the hiring manager and team, with internal talent as secondary.
- **Use the LinkedIn Meet-the-Hiring-Team block and the company People tab** (filter by title) to find the hiring manager, team, and recruiter when no post exists.
- **Never surface a target without a hook.** A target the candidate could only approach generically is a reputational liability on a real account.

## Intel: gather only the actionable forms

Apply the gate to every category. Company signals mostly move the cover letter and a few resume emphasis decisions; the resume core is governed by the JD.

- **Product launches and new lines (highest value):** a launch names skills they are now staffing, so it drives a matching bullet and one cover-letter line.
- **Funding with stated use-of-funds:** gather the round and its purpose; a bare "raised $X" alone is borderline.
- **Concrete strategic direction** (a named region, segment, or platform shift): gather; abstract "AI-first" filler is noise, and job-posting clusters are the best proxy for what they are actually building.
- **A forming team in the candidate's domain, or a named leader priority:** gather selectively; generic reorg churn is noise.
- **Stated values:** gather lightly; sets the cover-letter register and may cue one true story. It never touches the resume.
- **Comp:** triangulate lightly, enough to answer the salary field defensibly: a recruiter guide (Hays or Robert Half AU) for the base-salary spine, levels.fyi for the total-comp upper reach (it skews big-tech, so treat it as a ceiling), and the ABS or Jobs and Skills Atlas as an unbiased floor. Avoid Blind, Payscale, and advertised-ad aggregators for AU comp.
- **Interview shape:** at most one optional, non-blocking line from the company's own "how we hire" page (roughly how many rounds, whether there is a heavy take-home), since that touches the apply-or-skip and effort decision. Do not collect specific questions or round-by-round detail; that is cramming, not recon.

Do not gather (no artifact decision attached): founding year, static headcount, office locations as anything but a triage filter, mission and values boilerplate, a high-level description of what the product does (the JD already conveys it), generic perks and awards, and any abstract strategy statement.

## Sponsorship stance (a signal, not an answer)

Surface the company's sponsorship stance and the JD's own working-rights language as a signal for create to answer against; do not script the answer here. The load-bearing distinction in JD language: "**full** or **valid** working rights" can include a temporary visa with full work permission, while "**unlimited** or no-end-date rights, PR, or citizenship required" excludes a temporary-visa holder. Note which the JD uses. For the company's ability to sponsor, there is no live public Australian sponsor register; the only source is a stale Home Affairs FOI snapshot PDF (months out of date, and it errors on fetchers, so hand the user its URL rather than fetching it), and absence from it proves nothing. Prior sponsored ads (Seek visa-sponsorship listings) and explicit JD language are the usable signals. A security-clearance or "Australian citizenship required" role is a hard filter, not something to finesse.

## Outputs

- **`org-recon.md`** (organisation level, above the opportunities): the company dossier shared across the organisation's roles, accreted across runs. Datestamp each addition, dedupe against what is there, and never clobber or silently contradict a prior finding; surface a contradiction for the user instead. If a fresh org dossier already exists, augment it rather than re-researching the company.
- **`recon.md`** (role level): this role's intel, closing with a **Signals** section that states decision-relevant facts for create: who reads the artifact first and what they weight, the identified ATS, which true facets of the candidate's work this opportunity values, the language legitimately mirrorable (artifacts default to Australian spelling), and the resolution result. State signals as facts; do not prescribe section order or arrangement, which are create's to decide.
- **`questions.md`**: the real application-page questions, pulled from the first-party form.
- **`targets.md`**: the outreach targets, in the schema above.
- **JD frontmatter**: write the resolved first-party `url` and the identified `ats`.
- **Sister role or ghost**: flag a better-fit sister role as a new opportunity for triage, and flag a likely-ghost or unresolvable listing so triage can drop it.

## Posture

Research in rounds: cast a wide net, go deep on threads that yield signal, follow what each round uncovers, and stop when rounds stop being productive. Resolve first, because it unlocks the ATS, the real questions, and the sister-role scan in one move. Hold every finding to the gate: if it does not name a downstream decision, it does not belong in the files.
