---
name: voice-extract
description: "Analyze the author's prose style across 7 dimensions and produce a voice profile. Invoke with /voice-extract."
---

# voice-extract — Author Voice Profile

Use this skill when the user invokes `/voice-extract`.

Analyzes the author's writing style across 7 dimensions and generates a voice profile
for maintaining consistency or guiding AI-assisted writing. Saves to
`wiki/reports/voice-profile.md`.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm. If `hint-core.md` cannot be read, use the algorithm below directly:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

Get the novel title from `wiki/project.md` if it exists (first `# ` heading or `title:` frontmatter; fall back to folder name).

Store the resolved project root as an absolute path (e.g., `F:/my-novel/`). Use this absolute path for ALL file reads and writes in subsequent steps — never use a relative path.

Confirm the resolved project root with the user before proceeding: "I'll save the voice profile to [absolute_project_root]/wiki/reports/voice-profile.md. Is that correct? (yes / no)"
If the user says no, ask them to provide the correct project path and re-run detection.

---

## Step 2: Load chapter content

Ask:
> "How would you like to provide the chapter content?
> A) Paste the text directly (more chapters = more accurate profile)
> B) Provide file path(s) (e.g., chapters/ch01.md through chapters/ch10.md)"

**If A:** Accept pasted text with `--- Chapter N ---` dividers. If no dividers detected, treat as single chapter and notify the user: "No chapter dividers detected — treating all input as a single chapter. Is that correct?"

**If B:** Read files, sort by filename ascending. If a file range is provided (e.g., ch01.md through ch10.md), sort by the numeric portion of the filename. If a file in the range does not exist, skip it and note: "[filename] not found — skipped." If the path ends with `/` or resolves as a directory, read all `.md` files starting with "chapter" or "ch", sorted by filename ascending.

After loading:
- If N = 0: stop and report "No chapter content could be loaded. Please verify your input and try again."
- If under 2000 words total: warn "Sample is short (under 2000 words) — profile may not be reliable. Consider adding more chapters."
- Otherwise: "Loaded N chapter(s) — [word count] words. Analyzing..."

---

## Step 3: Analyze across 7 dimensions

Read the full text carefully and analyze each dimension:

### Dimension 1: Sentence Structure
- Characterize the average sentence length (short = under 10 words, medium = 10-20, long = 20+)
- Identify preferred sentence type (simple / compound / complex / mixed)
- Note use of sentence fragments (for effect / rarely / never)
- Find a representative example sentence

### Dimension 2: Vocabulary
- Assess formality level (literary / conversational / mixed)
- Identify distinctive word choices — words or phrases this author uses repeatedly
- Note what this author avoids (purple prose? passive voice? adverbs? clichés?)

### Dimension 3: POV and Narrative Distance
- Identify POV (first person / third limited / third omniscient / other)
- Assess narrative distance (close interiority / moderate / cinematic/external)
- Identify how interiority is shown: direct thought ("She thought...") / free indirect ("Why would he do that?") / action-only

### Dimension 4: Dialogue Patterns
- Identify tag style (plain "said" / action beats / mixed / minimal tags)
- Assess how characters are differentiated (strongly / moderately / weakly)
- Note any dialect, register differences, or speech patterns

### Dimension 5: Paragraph Length
- Characterize the typical paragraph length (short/punchy = 1-3 sentences / medium = 4-6 / long/flowing = 7+)
- Note variation patterns (does length vary with mood/pacing?)

### Dimension 6: Pacing Rhythm
- Compare action scene prose vs quiet scene prose
- Note chapter length consistency (consistent / variable)
- Identify what creates momentum in this author's style

### Dimension 7: Emotional Tone
- Identify the register (restrained / expressive / oscillating between)
- Identify how emotion is conveyed: direct statement / physical sensation / action / implication
- Find an example of emotional expression from the text

---

## Step 4: Generate voice profile

Produce this document using actual examples from the text:

```
# Author Voice Profile
**Novel:** [title]
**Generated:** [today's date in YYYY-MM-DD format]
**Chapters analyzed:** N ([word count] words)

## Writing Style Summary
[2-3 sentences capturing the essence of this author's voice — what makes it distinctive]

---

## Sentence Structure
- **Average length:** [short / medium / long]
- **Preference:** [simple / compound / complex / mixed]
- **Fragments:** [used for effect / rarely / not used]
- **Example:** "[actual sentence from the text]"

---

## Vocabulary
- **Formality:** [literary / conversational / mixed]
- **Distinctive choices:** [list 5-8 characteristic words/phrases with brief note on why they're distinctive]
- **Avoids:** [what this author consistently avoids]

---

## POV & Narrative Distance
- **POV:** [first person / third limited / third omniscient]
- **Distance:** [close interiority / moderate / cinematic]
- **Interiority method:** [direct thought / free indirect / action-based]
- **Example:** "[actual passage showing interiority]"

---

## Dialogue
- **Tag style:** [plain "said" / action beats / mixed / minimal]
- **Character differentiation:** [strong / moderate / weak]
- **Notable patterns:** [any distinctive dialogue habits]
- **Example:** "[actual dialogue exchange from the text]"

---

## Paragraph Length & Rhythm
- **Typical length:** [short / medium / long]
- **Variation:** [how and when length shifts]
- **What creates momentum:** [specific technique this author uses]

---

## Emotional Tone
- **Register:** [restrained / expressive / oscillating]
- **Conveyance method:** [direct / physical sensation / action / implication]
- **Example:** "[actual passage showing emotional expression]"

---

## Rules for Matching This Voice

**DO:**
(List 4–8 specific rules. More is better, but every rule must be concrete and derived from the actual text — no generic advice.)
1. [Specific, concrete instruction derived from the analysis]
2. [Specific, concrete instruction]
3. [Specific, concrete instruction]
4. [Specific, concrete instruction]
5. [Specific, concrete instruction]

**DON'T:**
(List 4–8 specific rules. Focus on patterns this author genuinely avoids, not generic writing tips.)
1. [Specific, concrete instruction — what to avoid]
2. [Specific, concrete instruction]
3. [Specific, concrete instruction]
4. [Specific, concrete instruction]
5. [Specific, concrete instruction]

**When in doubt:** [One guiding principle that captures the author's essence]
```

All examples must be actual quotes or paraphrases from the loaded text — never invent examples.

---

## Step 5: Save and confirm

1. Create `[absolute_project_root]/wiki/reports/` if it doesn't exist.
2. Check if `[absolute_project_root]/wiki/reports/voice-profile.md` already exists.
   - If it does NOT exist: write the profile.
   - If it DOES exist: ask "A voice profile already exists. Overwrite it? (yes / no)"
     - If no: stop. Report "Voice profile not saved. Existing profile kept."
3. Write to `[absolute_project_root]/wiki/reports/voice-profile.md`.
4. Summarize the profile in the conversation: show the Writing Style Summary, the DO/DON'T rules, and any notable flags. Do not display the full profile unless the user asks.
5. Confirm: "Voice profile saved to [absolute_project_root]/wiki/reports/voice-profile.md"

---

## Edge Cases

- **Under 2000 words:** Proceed but add note at top of profile: "⚠️ Short sample — profile may not capture full range. Add more chapters for accuracy."
- **Single chapter only:** Add note: "Single-chapter profile — voice analysis is most reliable with 3+ chapters."
- **No dialogue found:** Note in the Dialogue section: "No dialogue found in the provided chapters — dialogue analysis skipped."
- **Poetry or non-prose detected:** Note: "Content appears to be poetry or non-standard prose — sentence analysis dimensions may not apply accurately."
