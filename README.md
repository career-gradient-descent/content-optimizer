<div align="center">

# Content Optimizer

*Gradient descent for your career content.*

</div>

## What This Does

Build your career profile once. Generate resumes, cover letters, and other career content tailored to specific opportunities without copy-pasting or manual rewrites.

One source of truth (`career.md`) → many outputs.

## Requirements

- Docker
- Python 3.13+

## Setup

**1. Build your career profile**

Create `career.md` with detailed descriptions of your work, projects, education, and skills. This is your source of truth.

Go deep. If your algorithms course grade was a 67, write that. The richer your profile, the better the output, and the less likely you'll see hallucinated achievements that never happened.

**2. Install**

```bash
# Recommended - https://docs.astral.sh/uv/
uv sync
```

or

```bash
pip install -e .
```

## Usage

**With Claude Code (recommended):**

1. Drop an opportunity file in `opportunities/` - job description, role details, whatever
2. Ask Claude to generate content for it
3. Review the PDF in `output/`

**Manual:**

```bash
# Generate resume
uv run python -m cli render resume opportunities/example.yaml

# Generate cover letter
uv run python -m cli render cover-letter opportunities/example.yaml

# Recompile after editing the .tex file
uv run python -m cli re-render output/example.tex
```

_(If using pip instead of uv: same commands, just drop the `uv run` prefix)_

## How It Works

You create opportunity-specific YAML files that select and frame content from your career profile. Templates render these to LaTeX, compile to PDF.

- **Content changes?** Edit the YAML, re-render.
- **Formatting tweaks?** Edit the generated `.tex` file, recompile.
- **Want to customize templates?** They're in `templates/`.

The CLI uses Pydantic schemas to validate structure. Check `cli/schemas/` if you're curious.

---

<div align="center">

*If you find this useful, consider starring the repo.*

</div>
