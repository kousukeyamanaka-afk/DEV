---
name: manuscript-organize
description: "Classify files in the novel project folder and propose a tidy structure. Invoke with /manuscript-organize."
---

# manuscript-organize — Organize Your Manuscript Folder

Use this skill when the user invokes `/manuscript-organize`.

Reads all files in the project folder, classifies each by content type, proposes a
clean reorganization, and executes only after user confirmation. Never deletes files.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm (or use directly if `hint-core.md` cannot be read):
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

---

## Step 2: List files

List all files directly in the project root (non-recursive). Do NOT descend into subfolders yet.

Ask the user: "Should I also scan subfolders? (yes / no — default: no)"

If yes: also list files one level deep inside any existing subfolders (excluding `.git/`, `wiki/`, `node_modules/`).

---

## Step 3: Classify each file

For each file found, classify it into one of these categories based on filename AND content (read the file if the filename is ambiguous):

| Category | What goes here | Examples |
|----------|---------------|---------|
| `chapters` | Chapter drafts, scene drafts | ch01.md, Chapter-03.docx, scene-market.txt |
| `notes` | Character notes, worldbuilding, brainstorms, ideas | mira-notes.md, magic-system.txt, ideas.md |
| `outlines` | Story outlines, beat sheets, structure docs, synopses | outline-v2.md, three-act-structure.docx, synopsis.txt |
| `research` | Reference material, articles, images, links | historical-reference.pdf, map.png, article.md |
| `output` | AI-generated files, exports, previous reports | book-bible.md (if in root), continuity-report.md |
| `keep-in-root` | CLAUDE.md, README.md, .gitignore, wiki/ folder, .git/ |

**Classification rules:**
- If a file starts with "ch", "chapter", or contains a chapter number pattern → `chapters`
- If a file contains character names + descriptions → `notes`
- If a file contains "outline", "beat", "structure", "synopsis", "arc" → `outlines`
- If a filename matches a known AI-generated report name (e.g., `book-bible.md`, `continuity-report.md`, `hints.md`, `hints.json`, `voice-profile.md`) or contains "report", "export", or "generated" → `output`
- If uncertain: classify as `notes` and flag it
- NEVER classify these for moving: `CLAUDE.md`, `README.md`, `.git/`, `wiki/`, any folder
- If subfolder scanning is active and a file is already inside a folder that matches its classification (e.g., `chapters/ch01.md` is already in `chapters/`): mark it as `(already organized)` and exclude it from the move list.

---

## Step 4: Present preview plan

Show a table of every file and its proposed destination. Flag uncertain classifications with ⚠️:

```
Reorganization Preview:

File                      → Destination
─────────────────────────────────────────────────
ch01-draft.md             → chapters/ch01-draft.md
ch02-draft.md             → chapters/ch02-draft.md
mira-character.txt        → notes/mira-character.txt
world-rules.md            → notes/world-rules.md
outline-v2.docx           → outlines/outline-v2.docx
historical-ref.pdf        → research/historical-ref.pdf
old-export.md             → output/old-export.md
CLAUDE.md                 → (keep in root)
README.md                 → (keep in root)
⚠️ random-notes.txt      → notes/random-notes.txt (uncertain — flagged)

Folders to create: chapters/, notes/, outlines/, research/, output/
Files to move: 8
Files to keep in root: 2
```

Ask: "Shall I proceed with this reorganization? (yes / edit / cancel)"

- If **yes**: proceed to Step 5.
- If **edit**: ask which file should go where, update the plan, show revised preview, ask again. Repeat this loop as many times as needed until the user confirms yes or cancel.
- If **cancel**: stop. Confirm "No changes made."

---

## Step 5: Execute reorganization

For each file in the move list:
1. Create the destination folder if it doesn't exist.
2. Move the file to its destination.
3. Do NOT overwrite any existing file — if a conflict exists, skip and report it.

**Safety invariants (enforce absolutely):**
- NEVER delete any file.
- NEVER move `CLAUDE.md`, `README.md`, `.git/`, `wiki/`, or any directory.
- NEVER move files into or out of `wiki/` — it is a protected system folder in all directions.
- If a destination file already exists with the same name: skip the move and list it as a conflict.

---

## Step 6: Generate README.md

Before writing: check if `README.md` already exists in the project root.
- If it does NOT exist: write the template below.
- If it DOES exist: ask "README.md already exists. Overwrite it, skip, or append the folder structure section? (overwrite / skip / append)"
  - overwrite: replace the file with the template below.
  - skip: do not write README.md; note "README.md kept as-is" in the final confirmation.
  - append: add the "## Project Structure" section to the end of the existing README.md.

Replace [today's date] with the actual current date in YYYY-MM-DD format.

Write `README.md` in the project root with this structure:

```
# [Novel Title or Folder Name]

## Project Structure

- **chapters/** — Chapter drafts. Each file is one chapter or scene.
- **notes/** — Character notes, worldbuilding details, brainstorms.
- **outlines/** — Story outlines, beat sheets, structure documents.
- **research/** — Reference material, articles, images.
- **output/** — AI-generated files, reports, exports.
- **wiki/** — Project knowledge base (characters, plot, world, hints).

## Files in Root
- `CLAUDE.md` — Instructions for Claude Code in this project.
- `README.md` — This file.

_Organized by /manuscript-organize on [today's date]_
```

---

## Step 7: Confirm

Report:
```
Reorganization complete.
  Moved: N files
  Skipped (conflicts): [list if any]
  Folders created: [list]
  README.md created.
```

---

## Duplicate Scan (optional follow-up)

If the user asks "find duplicates" or "scan for duplicates" after organizing:

Read all files across all organized folders (`chapters/`, `notes/`, `outlines/`, `research/`, `output/`). Compare each pair for substantial content similarity (same paragraphs, same sentences, even with different filenames).

Report as a table:
```
| File A              | File B              | Similarity | Recommendation      |
|---------------------|---------------------|------------|---------------------|
| chapters/ch01-v1.md | chapters/ch01-v2.md | ~85%       | Keep ch01-v2, archive v1 |
```

NEVER delete files. Only recommend. The user decides.

---

## Edge Cases

- **No files found in root:** Report "No files to organize in [path]. The folder may already be organized."
- **File move conflict:** Skip the conflicting file, report it as a conflict at the end.
- **Unreadable file (binary, locked):** Classify by filename only, flag with ⚠️ in preview.
