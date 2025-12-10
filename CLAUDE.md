# Content Optimizer

This is a toolkit for producing marketing and sales content for personal branding. This involves resumes (marketing), cover letters (sales), outreach messages (sales), and more.

## The career profile

The file `./career.md` (or alternatively at, `./canon.md` or `./identity.md`) contains the comprehensive career profile. This is the "universe of facts" or "a single source of truth" from which all content is derived. In addition to the typical resume content like bio, education, experiences, projects, and skills, it ALSO indludes other details such as interests, passion, philosophy and writing style.

The career profile file is meant to be a lot more detailed than a resume. With at least a page full of in-depth information about every job experience and project. By design, any material you produce must be a curated selection from the career profile - depending on the opportunity.

## Resume Optimization Philosophy

Generate resumes that appear naturally written while being strategically optimized for both ATS systems and human recruiters. The recruiter should see a strong, well-rounded candidate whose background aligns with the role - not a document obviously tailored to match a job description.

Draw from the career profile intelligently. You have creative freedom to emphasize, reframe, and reasonably extrapolate from the source material. The goal is producing what the candidate would write themselves if they had perfect knowledge of what works, not rigid transcription of facts.

## Repository Structure

```
./
├── career.md                      # Career profile - source of truth
├── opportunities/                 # Job-specific YAML files
│
├── cli/                           # Python CLI package
│   ├── schemas/
│   │   ├── resume.py              # ResumeSchema (Pydantic)
│   │   └── cover_letter.py        # CoverLetterSchema (Pydantic)
│   ├── app.py                     # CLI commands
│   └── core.py                    # Rendering & compilation logic
│
├── templates/
│   ├── resume/
│   │   ├── primary.tex.j2         # Default Jinja template
│   │   └── original/              # Reference LaTeX files
│   └── cover-letter/
│       ├── primary.tex.j2
│       └── original/
│
└── output/                        # Generated PDFs and TEX files
```

## Content Types

The kinds of content you will be asked to generate falls into two buckets

### Structured (PDF Pipeline)

**Resume, Cover Letter** — requires precise formatting, strict schema.

The user will specify:
- Which opportunity file
- Which entity (resume, cover-letter)
- Which template (defaults to primary)

Your job:
1. Read: `career.md` + opportunity + `./cli/schemas/<entity>.py` + `./templates/<entity>/<template>.tex.j2`
2. Produce: YAML matching the schema → save to `./opportunities/<name>.yaml`
3. Render: Run CLI command
4. Validate: Check generated PDF in `./output/`, iterate on `.tex` if needed

```zsh
# Render YAML → PDF
uv run python -m cli render resume <yaml> [-t template] [-o output.pdf]
uv run python -m cli render cover-letter <yaml> [-t template] [-o output.pdf]

# Re-compile after manual .tex edits
uv run python -m cli re-render <tex> [-o output.pdf]
```

Defaults:
- `-t` defaults to `primary`
- `-o` defaults to `./output/<input_name>.pdf`

### Freeform (Text/Markdown)

**Outreach emails, LinkedIn messages, application Q&A, anything else** — strategic content, simple output.

No schema, no CLI. Just produce well-crafted text derived from career.md.
