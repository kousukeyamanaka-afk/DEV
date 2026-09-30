---
name: story-analysis
description: "Story structure and arc analysis report across all chapters. Invoke with /story-analysis."
---

# story-analysis — Story Structure & Arc Analysis

Use this skill when the user invokes `/story-analysis`.

Reads all chapter files and generates a three-part analysis report:
Part A — Character Arc Tracker, Part B — Plot Thread Map, Part C — Story Structure.
Saves to `[resolved_project_root]/wiki/reports/story-analysis-YYYY-MM-DD-HH-MM.md`.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm. If `hint-core.md` cannot be read, use the algorithm below directly:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

Get the novel title from `wiki/project.md` if it exists (first `# ` heading or `title:` frontmatter; fall back to folder name).

Store the resolved project root as an absolute path. Use this absolute path for ALL file reads and writes — never use a relative path.

---

## Step 2: Load wiki context

Read the following IF they exist (skip silently if missing):
- `wiki/project.md` — novel title
- `wiki/characters.md` — known characters
- `wiki/plot.md` — established plot threads
- `wiki/world.md` — world rules

---

## Step 3: Load chapter content

Ask:
> "Analyze all chapters or a range? (all / ch1-ch3)"

- **all:** Read all `.md` files whose filename starts with "chapter" or "ch" under the project root, sorted by filename ascending.
- **range (e.g., ch1-ch3):** Parse the start and end chapter numbers. Read files matching `chapter-01.md`, `ch01.md`, `chapter_01.md` or similar patterns for each chapter in the range. Sort by numeric portion of filename ascending. If a file is missing, skip and note: "[filename] not found — skipped."
  When matching chapter numbers, zero-pad to 2 digits for file matching (e.g., ch1 → ch01, chapter3 → chapter03). If no file is found for a chapter number in the range, skip it and note: "[ch N] not found — skipped."

After loading: "Loaded N chapter(s)."

If N = 0: stop and report "No chapter files found. Please verify the project root and chapter file naming."

---

## Step 4: Run three analyses

Work through all three parts sequentially. Use the wiki context to supplement what is found in the chapters.

### Part A — Character Arc Tracker

1. Identify all named characters across all loaded chapters.
2. For each character, build a table tracking their state per chapter:

```
### Character Arc Tracker
| Character | Ch.1 | Ch.2 | Ch.3 | ... |
|-----------|------|------|------|-----|
| [Name]    | [emotional state / goal / status] | ... |
```

Each cell should briefly capture: emotional state, current goal, power/social status. Use "—" if the character does not appear in that chapter.

3. Flag any character absent from 3+ consecutive chapters with: "⚠️ [Name] absent for Ch.N–Ch.M — verify intentional."

### Part B — Plot Thread Map

1. Identify every subplot/thread by name (look for recurring goals, conflicts, mysteries, relationships).
2. For each thread, build a table:

```
### Plot Thread Map
| Thread | Chapters Active | Status | Notes |
|--------|----------------|--------|-------|
| [Name] | 1, 2, 4 | active / resolved / dropped | [optional note] |
```

Status definitions:
- **active** — introduced and still unresolved at the end of the last chapter
- **resolved** — explicitly concluded
- **dropped** — appeared in at least one chapter but not seen again without resolution. Do not flag as dropped if the thread was introduced in the final chapter of the analyzed range — it has had no opportunity to recur.

3. Flag all dropped threads: "⚠️ [Thread] — appeared in Ch.N, never resolved."

### Part C — Story Structure

1. For each chapter, assess tension/stakes level: `low` / `medium` / `high` / `peak`.
2. Identify act breaks across the full manuscript:
   - **Setup** — chapters establishing world, character, and problem
   - **Confrontation** — escalation and complication
   - **Resolution** — climax and falling action
3. Build a table:

```
### Story Structure
| Chapter | Tension | Act | Notes |
|---------|---------|-----|-------|
| Ch.1    | medium  | Setup | Inciting incident: [brief description] |
```

4. Flag pacing gaps: 3+ consecutive chapters all rated `low` tension: "⚠️ Pacing gap: Ch.N–Ch.M are all low tension."

---

## Step 5: Assemble and save report

Build the full report:

```markdown
# Story Analysis Report
**Novel:** [title]
**Date:** YYYY-MM-DD HH:MM
**Chapters analyzed:** N
**Chapters skipped:** [list or "none"]
**Wiki context loaded:** [list of wiki files successfully read, or "none"]

---

[Part A — Character Arc Tracker table]

---

[Part B — Plot Thread Map table]

---

[Part C — Story Structure table]

---

## Summary
[2–3 sentences summarizing the key findings: main character arc shape, unresolved threads count, overall pacing assessment.]
```

Replace YYYY-MM-DD HH:MM with today's actual date and current time.

Note: the filename uses dashes for the time component (`HH-MM`) because colons are not valid in Windows filenames. The report header uses `HH:MM` format.

Confirm the resolved project root with the user before writing: "I'll save the report to [resolved_project_root]/wiki/reports/. Is that correct? (yes / no)"
If the user says no, ask them to provide the correct project path and re-run detection.

1. Create `[resolved_project_root]/wiki/reports/` if it doesn't exist.
2. Save to `[resolved_project_root]/wiki/reports/story-analysis-YYYY-MM-DD-HH-MM.md`.
3. Print the Summary section to the terminal plus counts: "X characters tracked, Y threads found (Z dropped), [pacing assessment]. Report saved to [resolved_project_root]/wiki/reports/story-analysis-YYYY-MM-DD-HH-MM.md"

Do not display the full report tables in the conversation unless the user asks. Show only the Summary section and the counts line.

---

## Edge Cases

- **No chapter files found:** Stop with "No chapter files found. Please verify the project root and chapter file naming."
- **Range with missing files:** Skip missing files silently, list skipped files in report header.
- **No named characters found:** Output in Part A: "_No named characters detected. Check chapter content or try loading more chapters._"
- **No plot threads identified:** Output in Part B: "_No distinct plot threads identified. Check chapter content or try loading more chapters._"
- **Single chapter:** Add note: "Single-chapter analysis — arc progression and dropped threads cannot be assessed. Load more chapters for full analysis."
