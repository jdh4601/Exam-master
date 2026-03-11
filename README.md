# claude-skills

A collection of custom skills for [Claude Code](https://claude.ai/code), installable in one line via the `skills` CLI.

→ 한국어 README는 [README.ko.md](README.ko.md)를 참고하세요.

---

## Skills

| Skill | Description |
|-------|-------------|
| [exam-master](skills/exam-master/) | Adaptive exam prep powered by reinforcement learning + cognitive science |
| [pdf-to-markdown](skills/pdf-to-markdown/) | Convert password-protected PDFs into clean, structured Markdown |
| [pptx-to-markdown](skills/pptx-to-markdown/) | Convert PowerPoint slides into structured Markdown with speaker notes |

---

## Prerequisites

Before installing any skill, make sure you have the following:

- **[Claude Code](https://claude.ai/code)** — the AI coding assistant this skill system runs on
- **Python 3.9+** — required for `pdf-to-markdown` and `pptx-to-markdown`

---

## Installation

### 1. Install the `skills` CLI (one-time setup)

```bash
npm install -g skills
```

### 2. Install the skill(s) you want

```bash
# Exam preparation skill
npx skills add jdh4601/Exam-master@exam-master

# PDF → Markdown conversion skill
npx skills add jdh4601/Exam-master@pdf-to-markdown

# PowerPoint → Markdown conversion skill
npx skills add jdh4601/Exam-master@pptx-to-markdown
```

### 3. Use them in Claude Code

```
/exam-master /path/to/lecture-notes/
/pdf-to-markdown lecture.pdf -p "PASSWORD"
/pptx-to-markdown lecture.pptx
```

That's it. Skills are ready to use immediately after installation.

---

## Skills

### exam-master

> Reinforcement learning + cognitive science based exam preparation

`exam-master` analyzes your lecture materials (Markdown files) and runs an **8-step adaptive study loop** that maximizes retention through spaced repetition, adaptive difficulty, and self-explanation grading.

#### How it works — 8-step execution flow

```
Pre-flight   Load materials + check spaced repetition schedule
    ↓
STEP 0       Prior recall — you list what you already know
    ↓
STEP 1       Extract key concepts from all lecture files
    ↓
STEP 2       Build a concept graph (with explicit relationship types)
    ↓
STEP 3       Predict likely exam question types
    ↓
STEP 4       Generate N questions at adaptive difficulty levels
    ↓
STEP 5       Self-explanation + per-question immediate grading
    ↓
STEP 6       Save error notebook (with spaced repetition schedule)
    ↓
STEP 7       5 interleaved review questions → decide whether to loop
```

#### Reinforcement learning principles

- **Reward-Based Policy Update**: Answer correctly → next question gets harder. Answer wrong → next question gets easier.
- **Error buffer**: Wrong concepts are stored in a buffer. Review intervals are dynamically adjusted (1d → 3d → 7d).
- **Penalty for repeated mistakes**: Concepts missed 3+ times in a row get a longer cooldown before re-appearing.

#### Cognitive science principles

- **Prior recall (STEP 0)**: You retrieve knowledge *before* reading materials — this "testing effect" dramatically improves retention compared to passive re-reading.
- **Reasoning evaluation**: Your thought process is graded, not just your final answer — this encourages metacognitive monitoring.
- **Concept graph (STEP 2)**: Building a visual schema of relationships trains structured thinking, not just memorization.

#### Difficulty levels

| Level | Type | Description |
|-------|------|-------------|
| L1 | Recall | Define terms, name concepts |
| L2 | Explain | Answer "why" and "how" |
| L3 | Synthesis | Connect 2+ concepts |
| L4 | Application | Apply to new scenarios |
| L5 | Trap | Identify common misconceptions |

#### Usage

```
/exam-master /path/to/lecture-notes/
```

Examples:
```
/exam-master ~/Documents/database/
/exam-master ~/Documents/algorithms/week3/
```

> Your lecture materials must be in `.md` format. If you have PDFs, convert them first with `pdf-to-markdown`.

**Tip — combine both skills:**
```
/pdf-to-markdown lecture.pdf -p "password"
/exam-master ./
```

---

### pdf-to-markdown

> Convert password-protected PDFs into clean, structured Markdown

`pdf-to-markdown` automates the full pipeline: decrypt → extract → clean → Claude refinement. The output is a well-structured `.md` file ready for use with `exam-master` or any other tool.

#### Conversion pipeline

```
PDF (encrypted) → decrypt → extract → clean → raw .md → Claude refinement → final .md
```

1. **Decrypt** — removes password protection via `pypdf`
2. **Extract** — pulls text with structure detection via `pdfplumber`:
   - Font-size based heading detection (h1/h2/h3)
   - Bullet/numbered list detection
   - Tables → Markdown pipe tables
   - Monospace font → code blocks
3. **Clean** — removes repeated headers/footers, fixes encoding artifacts, normalizes whitespace
4. **Claude refinement** — Claude reads the raw output and fixes heading hierarchy, table alignment, and list formatting

#### Usage

**Single file:**
```
/pdf-to-markdown lecture.pdf -p "PASSWORD"
```

**Or run the script directly:**
```bash
# Single file
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  -i lecture.pdf -p "PASSWORD" -o lecture.md

# Batch convert entire folder
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  --input-dir ./pdfs/ -p "PASSWORD" --output-dir ./markdown/

# Specific page range
python3 ~/.claude/skills/pdf-to-markdown/scripts/convert_pdf.py \
  -i lecture.pdf -p "PASSWORD" --pages 1-50
```

#### CLI options

| Option | Short | Description |
|--------|-------|-------------|
| `--input` | `-i` | Input PDF file path |
| `--input-dir` | | Batch mode: input directory |
| `--password` | `-p` | PDF password |
| `--output` | `-o` | Output Markdown file path |
| `--output-dir` | | Batch mode: output directory |
| `--pages` | | Page range (e.g. `1-50`) |

#### Dependencies

Python dependencies (`pdfplumber`, `pypdf`) are **auto-installed on first run** — no manual setup needed.

---

### pptx-to-markdown

> Convert PowerPoint slides into structured Markdown with speaker notes

`pptx-to-markdown` extracts the full content of a `.pptx` file — slide titles, bullet points, tables, and speaker notes — and renders it as a clean, structured `.md` file ready for `exam-master` or any other tool.

#### Conversion pipeline

```
PPTX → load → extract per slide → clean → raw .md → Claude refinement → final .md
```

1. **Load** — opens the `.pptx` file via `python-pptx`
2. **Extract** — processes each slide:
   - Title placeholder → `## Slide N: Title`
   - Body bullets → nested lists using indent level (`-`, `  -`)
   - Subtitle → italic paragraph
   - Tables → Markdown pipe tables
   - Images / Charts → `[이미지: name]` / `[차트: name]` placeholders
   - Speaker notes → `> **Notes:** ...` blockquote
3. **Clean** — removes empty slides, normalizes whitespace
4. **Claude refinement** — Claude reads the raw output and fixes heading hierarchy, list nesting, and table formatting

#### Usage

**Single file:**
```
/pptx-to-markdown lecture.pptx
```

**Or run the script directly:**
```bash
# Single file
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  -i lecture.pptx -o lecture.md

# Batch convert entire folder
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  --input-dir ./slides/ --output-dir ./markdown/

# Specific slide range
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  -i lecture.pptx --slides 1-30

# Exclude speaker notes
python3 ~/.claude/skills/pptx-to-markdown/scripts/convert_pptx.py \
  -i lecture.pptx --no-notes
```

#### CLI options

| Option | Short | Description |
|--------|-------|-------------|
| `--input` | `-i` | Input PPTX file path |
| `--input-dir` | | Batch mode: input directory |
| `--output` | `-o` | Output Markdown file path |
| `--output-dir` | | Batch mode: output directory |
| `--slides` | | Slide range (e.g. `1-30`) |
| `--no-notes` | | Exclude speaker notes |

#### Dependencies

Python dependency (`python-pptx`) is **auto-installed on first run** — no manual setup needed.

---

## Recommended workflow

If you have lecture slides (PDF or PPTX) and an upcoming exam:

```bash
# Step 1: Convert slides to Markdown
/pdf-to-markdown ./lectures/ -p "yourpassword"   # encrypted PDFs
/pptx-to-markdown ./slides/                      # PowerPoint files

# Step 2: Start adaptive exam prep
/exam-master ./lectures/
```

Claude will handle the rest — concept extraction, adaptive questions, grading, and spaced repetition scheduling.

---

## License

MIT
