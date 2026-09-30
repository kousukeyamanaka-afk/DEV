---
name: continuity-check
description: "Scan all chapters for continuity errors (names, timeline, places, objects, facts) and cross-check against the book bible. Invoke with /continuity-check."
---

# continuity-check — Continuity Error Scanner

Use this skill when the user invokes `/continuity-check`.

Scans all chapters for continuity errors across 7 categories. Cross-references against
the book bible if available. Saves a dated report to `wiki/reports/`.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm. If `hint-core.md` cannot be read, use the algorithm below directly:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

---

## Step 2: Load context

Read the following IF they exist (skip silently if missing):
- `wiki/reports/book-bible.md` — established canon baseline (most important)
- `wiki/project.md` — for novel title
- `wiki/characters.md`
- `wiki/world.md`

Note which context was loaded — include in report header.

---

## Step 3: Load chapter content

Ask:
> "How would you like to provide the chapter content?
> A) Paste the text directly
> B) Provide file path(s) (e.g., chapters/ch01.md through chapters/ch10.md)"

**If A:** Accept pasted text with `--- Chapter N ---` dividers. If no dividers detected, treat as single chapter and notify the user: "No chapter dividers detected — treating all input as a single chapter. Is that correct?"

**If B:** Read files, sort by filename ascending. X and Y in a range are filenames; sort by numeric portion of filename; if a file in the range does not exist, skip it and note: "[filename] not found — skipped."

After loading: "Loaded N chapter(s)."

If N = 0: stop and report "No chapter content could be loaded. Please verify your input and try again."

---

## Step 4: Scan mode

Ask:
> "Scan mode?
> A) Bible check — compare chapters against book bible canon only
> B) Full scan — cross-reference chapters against each other + bible (if available)"

- **Bible check:** Use `wiki/reports/book-bible.md` as the source of truth. Flag anywhere chapters contradict it.
- **Full scan:** Also cross-reference all chapters against each other to find internal contradictions.

If no book bible exists and user chose bible check: switch to full scan. Notify: "No book bible found — running full cross-chapter scan."

---

## Step 5: Scan for errors

Check all 7 categories:

### Category 1: Physical Description Changes
Look for: eye color, hair color/length, height, build, scars, tattoos, clothing described as permanent features — that change between chapters without explanation.
Flag: "[Character] described as [X] in Ch.N but [Y] in Ch.M."

### Category 2: Timeline Contradictions
Look for: events that happen "yesterday" or "last week" that don't match the established timeline. Characters referencing past events in the wrong order.
Flag: "Ch.N implies Event A happened before Event B, but Ch.M establishes the opposite."

### Category 3: Information Access Violations
Look for: a character knowing something they have no way of knowing at that point in the story (no one told them, they weren't there, the information hasn't been revealed yet).
Flag: "[Character] knows [X] in Ch.N, but this is only revealed to them in Ch.M."

### Category 4: World Rule Violations
Look for: magic, technology, or social rules that were established as absolute but are broken without acknowledgment.
Flag: "Ch.N establishes [rule]. Ch.M violates it when [description]."

### Category 5: Location Impossibilities
Look for: a character appearing in Location A at the end of Ch.N and Location B (impossibly far) at the start of Ch.N+1 with no time passage indicated.
Flag: "[Character] ends Ch.N in [Location A] but begins Ch.M in [Location B] with no travel shown."

### Category 6: Factual Contradictions
Look for: a statement in Ch.N that directly contradicts a statement in Ch.M on a concrete, verifiable fact (a date, a number, a name, a stated fact).
Flag: "Ch.N states [X]. Ch.M states the opposite: [Y]."

### Category 7: Tone/Voice Inconsistencies
Look for: sections where the narrative voice shifts significantly — a first-person narrator suddenly becomes omniscient, or the prose style changes dramatically in a way that seems unintentional.
Flag: "Ch.N paragraph [quote] — tone shifts significantly from established voice. Possible unintentional drift."
Note: Only flag if clearly unintentional. POV shifts between chapters are normal.

---

## Step 6: Assign severity

For each error found:
- **critical** — breaks story logic; a reader would notice and it cannot be explained away
- **minor** — small inconsistency; most readers won't notice but should be fixed
- **stylistic** — possible intentional; flag for author review but don't assume it's wrong

---

## Step 7: Output report

```
# Continuity Report
**Novel:** [title]
**Date:** YYYY-MM-DD
**Chapters scanned:** N
**Scan mode:** [bible check / full scan]
**Book bible:** [used / not present]
**Context loaded:** [list of wiki files successfully read, or "none"]

---

## 🚨 Critical Errors
- **[Category]** Ch.N vs Ch.M — [specific description with quote] — **Fix:** [suggested fix]

_If none: No critical errors found._

---

## ⚠️ Minor Errors
- **[Category]** Ch.N — [description] — **Fix:** [suggested fix]

_If none: No minor errors found._

---

## 🔍 Stylistic Flags (review manually)
- Ch.N — [description]

_If none: No stylistic flags._

---

## ✅ Clean Categories
- [List of the 7 categories where no issues were found]
```

Replace YYYY-MM-DD with today's actual date.

After generating the report, summarize it in the conversation: show error counts by severity and any clean categories. Do not display the full report text unless the user asks.

---

## Step 8: Save and confirm

Confirm the resolved project root with the user before writing: "I'll save the report to [resolved_project_root]/wiki/reports/. Is that correct? (yes / no)"

1. Create `wiki/reports/` if it doesn't exist.
2. Save to `wiki/reports/continuity-YYYY-MM-DD-HH-MM.md` (use today's date and current 24-hour hour and minute).
3. Confirm: "Found X critical, Y minor, Z stylistic issues. Report saved to wiki/reports/continuity-YYYY-MM-DD-HH-MM.md"

---

## Edge Cases

- **No errors found:** Save report with "No errors found" in all sections. Confirm: "Clean manuscript — no continuity errors detected."
- **Single chapter:** Note at top: "Single-chapter scan — cross-chapter contradictions not detectable. Only internal consistency checked."
- **No book bible:** Note: "Running without book bible — cross-chapter scan only. Run /book-bible first for more accurate canon checking."
