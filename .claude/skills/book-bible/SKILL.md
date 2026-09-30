---
name: book-bible
description: "Generate a book bible (characters, places, timeline, recurring objects) from all chapter files. Invoke with /book-bible."
---

# book-bible — Auto-Generate a Book Bible

Use this skill when the user invokes `/book-bible`.

Reads all chapter files and generates a comprehensive book bible: character profiles,
locations, timeline, world rules, relationship map, and open threads. Saves to
`wiki/reports/book-bible.md`.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm (or use directly if `hint-core.md` cannot be read):
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

---

## Step 2: Load wiki context

Read each of the following files IF they exist (skip silently if missing):
- `wiki/project.md` — use for novel title (first `# ` heading or `title:` frontmatter; fall back to folder name)
- `wiki/characters.md`
- `wiki/world.md`
- `wiki/themes.md`
- `wiki/plot.md`

---

## Step 3: Load chapter content

Ask:
> "How would you like to provide the chapter content?
> A) Paste the text directly
> B) Provide file path(s) (e.g., chapters/ch01.md or chapters/ch01.md through chapters/ch10.md)"

**If A (paste):** Accept all pasted text. Tell them to separate chapters using `--- Chapter N ---` dividers. If no dividers detected, treat as single chapter and confirm: "No chapter dividers detected — treating all content as one chapter. Is that correct?"

**If B (file path):**
- Single file: read it.
- Range ("X through Y"): X and Y are filenames. Sort all files in the range by the numeric portion of the filename. If a file in the range does not exist, skip it and note: "[filename] not found — skipped."
- Folder: If the provided path ends with `/` or resolves as a directory, read all `.md` files in that directory starting with "chapter" or "ch", sort by filename ascending. If a path cannot be read as a file, ask: "Did you mean a folder? (yes / no)"

After loading: "Loaded N chapter(s). Proceeding."

If N = 0 (no content loaded at all): stop and report "No chapter content could be loaded. Please verify your input and try again."

---

## Step 4: Full or update mode

Ask: "Generate full bible or update existing? (full / update)"

- **full:** Generate from scratch. Before writing, check if `wiki/reports/book-bible.md` already exists. If it does, ask: "A book bible already exists. Overwrite it? (yes / no — choose 'no' to run update mode instead)". Only proceed if the user confirms yes.
- **update:** Read existing `wiki/reports/book-bible.md` first as the baseline. Re-read chapters. For each section, flag what has changed since the last bible with `[UPDATED]` or `[NEW]` markers.
- If **update** chosen but no existing bible found: fall back to full generation. Notify: "No existing bible found — generating full bible."

---

## Step 5: Generate the 6 sections

Analyze all chapter content and produce the following. Be specific — use actual names, quotes, and chapter references from the text.

### Section 1: Character Profiles
For every named character who appears in the chapters:

```
### [Character Name]
- **Physical:** [description — hair, eyes, build, distinguishing marks]
- **Personality:** [core traits — 3-5 adjectives with brief evidence]
- **Backstory:** [what is revealed about their past]
- **First appears:** Ch.N — [scene description]
- **Key relationships:** [with whom, nature of relationship]
- **Arc so far:** [how they have changed, or what drives them]
```

### Section 2: Location Guide
For every named location:

```
### [Location Name]
- **Description:** [physical details]
- **Significance:** [why it matters to the plot]
- **Characters associated:** [who frequents or is connected to this place]
- **First appears:** Ch.N
```

### Section 3: Timeline
Chronological list of major events in story-time (not chapter order):

```
| Story Period | Event | Chapter |
|-------------|-------|---------|
| Day 1 | [Event description] | Ch.N |
| Day 3 | [Event description] | Ch.M |
```

If story-time is unclear, use chapter order and note: "Story-time unclear — listed by chapter order."

### Section 4: World Rules
Established rules of the story world:

```
### Magic / Power System
- [Rule 1]
- [Rule 2]

### Social / Political Structure
- [Rule 1]

### Technology / Physical Laws
- [Rule 1]

### ⚠️ Possible Rule Violations
- Ch.N — [description of possible inconsistency]
```

If the story has no fantasy/sci-fi elements, note: "Contemporary setting — no special world rules detected."

### Section 5: Relationship Map
Key relationships between characters:

```
| Character A | ↔ | Character B | Relationship | Evolution |
|------------|---|------------|--------------|-----------|
| Mira | ↔ | The Archivist | Wary observer / possible threat | Mira grows suspicious by Ch.3 |
```

### Section 6: Open Threads
Plot threads introduced but not yet resolved:

```
| Thread | Introduced | Status |
|--------|-----------|--------|
| [Description] | Ch.N | Unresolved |
| [Description] | Ch.M | Partially addressed in Ch.P |
```

---

## Step 6: Assemble and save

Combine all 6 sections into this structure:

Replace YYYY-MM-DD in the template below with today's actual date.

```
# Book Bible
**Novel:** [title]
**Generated:** YYYY-MM-DD
**Chapters read:** N
**Mode:** [full / update]

---

## 1. Character Profiles
[section content]

---

## 2. Location Guide
[section content]

---

## 3. Timeline
[section content]

---

## 4. World Rules
[section content]

---

## 5. Relationship Map
[section content]

---

## 6. Open Threads
[section content]
```

1. Create `wiki/reports/` directory if it doesn't exist.
2. Write to `wiki/reports/book-bible.md` (overwrite if exists).
3. Summarize the bible in the conversation: show section headings, character count, location count, open thread count, and any flagged issues. Do not display the full content unless the user asks.
4. Confirm: "Book bible saved to wiki/reports/book-bible.md"

---

## Edge Cases

- **No character names found:** Flag: "No named characters detected — verify chapter content was loaded correctly."
- **Single chapter:** Generate partial bible. Add note at top: "Single-chapter bible — incomplete. Add more chapters for full coverage."
- **Update mode, no existing bible:** Fall back to full generation with notification.
