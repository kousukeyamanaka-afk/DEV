---
name: dev-edit
description: "Developmental edit: big-picture report on pacing, structure, character arcs and coherence across the manuscript. Invoke with /dev-edit."
---

# dev-edit — Developmental Editor

Use this skill when the user invokes `/dev-edit`.

A big-picture manuscript editor. Examines pacing, structure, character arcs, and
coherence across your novel. Reads all available wiki context. Produces a structured
report saved to your project.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

All operations use `<project_root>/wiki/` as the base path.

---

## Step 2: Load wiki context

Read each of the following files IF they exist (skip silently if missing):
- `wiki/project.md`
- `wiki/characters.md`
- `wiki/plot.md`
- `wiki/world.md`
- `wiki/themes.md`

Additionally: if `wiki/hints.json` exists, read it and note the current foreshadowing
state (planted, planned, resolved hints). If it does not exist, skip.

Track which files were successfully loaded — you will list them in the report header.

To get the novel's title:
- Look for `title:` in YAML frontmatter of `wiki/project.md`, OR
- Use the first `# ` heading in `wiki/project.md`, OR
- Fall back to the project root folder name.

---

## Step 3: Load chapter content

Ask the user:

> "How would you like to provide the chapter content?
> A) Paste the text directly
> B) Provide file path(s) (e.g., wiki/chapter_01.md or wiki/chapter_01.md through wiki/chapter_10.md)"

**If A (paste):**
Ask the user to paste. Accept all pasted text. Tell them to separate chapters using
`--- Chapter N ---` dividers. Wait for them to signal they are done by typing "done".

**If B (file path):**
- If a single file: read it.
- If a range like "wiki/chapter_01.md through wiki/chapter_10.md": read all files
  matching `wiki/chapter_NN.md` from 01 to 10 (zero-padded). Skip any that don't exist.
- If a glob or folder: read all `.md` files in that location that start with "chapter". Sort by filename ascending (e.g., chapter_01.md before chapter_02.md).

After loading, confirm: "Loaded N chapter(s). Proceeding with analysis."

**If paste mode and no `--- Chapter N ---` dividers are detected:** Treat all pasted content as a single chapter. Confirm with the user: "No chapter dividers detected — treating all content as one chapter. Is that correct?"

---

## Step 4: Confirm analysis range

Ask:

> "Analyze all N chapters, or a specific range? (Type 'all' or a range like '1-5')"

If "all": analyze every chapter loaded.
If a range like "3-7": analyze only chapters 3 through 7. Ignore others.

---

## Step 5: Run the 4-dimension analysis

Work through each dimension fully before moving to the next. Use all loaded wiki
context and hints data to inform your analysis.

### DIMENSION 1: 📈 Pacing

For each chapter (or each scene if chapter text is detailed enough):

**Dragging indicators:**
- High ratio of exposition or internal monologue with no external event
- Dialogue scenes that circle without advancing plot or revealing character
- Same emotional beat across two or more consecutive chapters
- Chapter ends where it began emotionally

**Rushing indicators:**
- Major plot event occurs but character has no emotional reaction
- A relationship change, revelation, or loss resolved in under a paragraph
- Key decision made without showing the character's internal calculus

**Output format for this dimension:**
```
### ⚠️ Dragging
- Ch.N — [specific quote or scene description] — [why it drags] — [suggestion]

### ⚡ Rushing
- Ch.N — [specific moment] — [what emotion/beat is missing]

### ✅ Well-paced
- Ch.N, Ch.M — [one-line note on what makes them work]

### 💡 Pacing recommendations
- [2–3 concrete structural suggestions]
```

---

### DIMENSION 2: 🧩 Structure

**Cut or combine candidates:**
- Two chapters in the same location with overlapping emotional beats
- A chapter that ends exactly where the next one begins (could be a scene break instead)
- A chapter that exists only to move characters from A to B

**Ordering concerns:**
- A reveal lands before the reader has enough context to feel its weight
- Information given to the reader before the character knows it, undermining tension
- A chapter that would work better earlier (setup) or later (payoff)

**Act balance:**
- Divide the total chapters into thirds: Act 1 (setup), Act 2 (confrontation), Act 3 (resolution)
- Flag if Act 3 is fewer than 15% of total chapters — compressed endings feel rushed
- Flag if Act 1 is more than 35% — slow starts lose readers
- **If analyzing a subrange (not the full manuscript):** Skip act-balance calculation entirely. Write instead: `_Act balance requires full manuscript range — skipped for partial analysis._`

**Output format:**
```
### ✂️ Consider cutting or combining
- Ch.N + Ch.M — [reason]

### 🔀 Ordering concerns
- Ch.N — [what would improve if moved, and where]

### ⚖️ Act balance
- Act 1 (Ch.1–N): X% | Act 2 (Ch.N–M): Y% | Act 3 (Ch.M–end): Z%
- [Assessment: balanced / Act 3 compressed / Act 1 slow]
```

---

### DIMENSION 3: 👥 Character Arcs

Use `wiki/characters.md` as the source of truth for established traits. If it doesn't
exist, derive character traits from the chapter text itself.

**Inconsistency check:**
- A character acts against their established core trait without the story acknowledging it
- A character's skill, knowledge, or relationship is used that wasn't established earlier
- A character's stated motivation shifts without a scene that causes the shift

**Underdeveloped arcs:**
- A named character who the narrative frames as significant (has dialogue, drives plot, or is described with interiority) appears in 3+ chapters but has no moment of change or decision
- A character introduced as significant disappears without resolution
- A relationship is established but never tested or developed

**Emotional pacing of arcs:**
- A character reaches a major turning point (loss, betrayal, realization) without
  the prior chapters earning that moment

**Output format:**
```
### ⚠️ Inconsistency flagged
- [Character] in Ch.N — [what they do] contradicts [established trait from wiki or earlier chapter]

### 📉 Underdeveloped arc
- [Character] — appears in Ch.N, M, P but [what is missing]

### ✅ Strong arc
- [Character] — [brief note on what makes their arc work]
```

---

### DIMENSION 4: 🔍 Coherence

**Theme tracking:**
- Identify the 1–2 central themes from `wiki/themes.md` (or infer from text)
- Note which chapters actively engage the theme vs. where it goes quiet
- Flag if theme is absent for 3+ consecutive chapters in Act 2

**Tension and stakes:**
- A scene where the reader cannot identify what the protagonist stands to lose
- A scene that ends on a lower emotional note than it began (tension deflation)
- A subplot that runs for multiple chapters without advancing or connecting to main stakes

**Hook and closing assessment:**
For each chapter, rate the opening and closing:
- Opening: Strong hook (immediate conflict/question) / Soft opening (scene-setting, no tension)
- Closing: Strong close (unresolved tension, new question) / Weak close (resolution, summary)

**What's working:**
- Techniques the author uses consistently and effectively
- Scenes that achieve exactly what they should
- Patterns worth repeating

**Output format:**
```
### 🎯 Theme tracking
- Central theme(s): [X, Y]
- Theme quiet zone: Ch.N–M — [note]
- Strong theme chapters: Ch.N, Ch.M

### 📉 Tension drops
- Ch.N, scene [description] — [what the stakes are unclear or missing]

### 🎣 Hook / Closing assessment
| Ch | Opening | Closing |
|----|---------|---------|
| 1  | Strong — [note] | Strong — [note] |
| 2  | Soft — [note] | Strong — [note] |

### ✨ What's working — do more of this
- [Specific technique or pattern] — seen in Ch.N, M — [why it works]
```

---

## Step 6: Assemble and output the full report

Combine all 4 dimensions into a single report. Use this exact structure:

```markdown
# Developmental Edit Report
**Novel:** [title]
**Date:** YYYY-MM-DD HH:MM
**Chapters analyzed:** Ch.N–M ([all / specified range])
**Wiki context loaded:** [comma-separated list of wiki files successfully read, or "none"]
**Hints ledger:** [loaded (N hints: X planted, Y planned) / not present]

---

## 📈 Pacing
[pacing output]

---

## 🧩 Structure
[structure output]

---

## 👥 Character Arcs
[character arcs output]

---

## 🔍 Coherence
[coherence output]

---

_Report saved to wiki/dev-edit-reports/YYYY-MM-DD-HH-MM.md_
```

For any **negative/flag** sub-section with no findings (e.g., ⚠️ Dragging, ✂️ Cut, ⚠️ Inconsistency, 📉 Tension drops), write: `_None flagged._`

**Never** write `_None flagged._` under positive sub-sections: `### ✅ Well-paced`, `### ✅ Strong arc`, and `### ✨ What's working — do more of this`. These must always contain at least one observation, even if brief. If you genuinely cannot find anything positive, write a brief honest note (e.g., "No standout strengths detected in this excerpt — consider expanding the sample.").

**Display the full report** in the conversation.

**Then save it:**
1. Create `wiki/dev-edit-reports/` directory if it doesn't exist.
2. Write the report to `wiki/dev-edit-reports/YYYY-MM-DD-HH-MM.md` using the
   current date and time (24-hour format, e.g., `2026-05-06-14-30.md`).
3. Confirm: "Report saved to wiki/dev-edit-reports/YYYY-MM-DD-HH-MM.md"

---

## Edge Cases

- **No wiki files exist:** Add to report header: "No wiki context loaded — character and theme analysis based on chapter text alone."
- **Single chapter only:** Run all 4 dimensions. Add note: "Single-chapter analysis — structure and arc assessments are limited without full manuscript context."
- **File not found at given path:** Tell the user: "Could not find [path]. Please re-specify or paste the chapter text instead."
- **hints.json exists but is empty:** Note in header: "Hints ledger: loaded (0 hints)"
