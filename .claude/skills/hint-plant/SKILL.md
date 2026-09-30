---
name: hint-plant
description: "Suggest where to plant registered hints in a chapter draft. Invoke with /hint-plant."
---

# hint-plant — Suggest Hint Insertions in a Chapter Draft

Use this skill when the user invokes `/hint-plant`.

## Steps

1. **Read** `../hint-core/hint-core.md` for shared rules.

2. **Detect project root** using the project detection algorithm in hint-core.md.

3. **Read** `wiki/hints.json`. Filter hints where `status == "planned"`.

4. If no `planned` hints exist, respond:
   > "No planned hints to plant. Use `/hint-add` to register a planned hint first, or `/hint-suggest` to generate some."
   Then stop.

5. **Show the user** all `planned` hints:
   ```
   hint_003 — Surface idea: "Something about the east wall warmth" | Truth: "Crystals are Ruin's sensors" [world-rule / main]
   ```

6. **Ask the user** to paste their current chapter draft, OR provide a file path to the chapter.
   - If path provided: read the file.

7. **Analyze the draft** against each `planned` hint. For each hint, identify:
   - The best scene or paragraph where the hint could be inserted naturally
   - A suggested sentence or phrase that embeds the hint subtly (no dramatic emphasis)
   - Why this location works (reader won't notice but will remember in retrospect)

8. **Present suggestions** one at a time:
   ```
   HINT hint_003 — Suggested insertion:
   Location: After "She filed it away as a quirk of the ventilation"
   Suggested text: "...though the crystals on the east wall radiated a faint, unnatural warmth she couldn't explain."
   Why: Reads as atmospheric detail; pays off in ch.22 when Ruin's network is revealed.

   Plant this hint here? (yes / skip / rewrite)
   ```

9. For each accepted hint:
   - Ask: "Which chapter number is this draft? Scene name?"
   - Update `status` to `"planted"`, fill `planted.chapter`, `planted.scene`, `planted.note` (use the "why" as the note)
   - Write `hints.json`

10. After all hints processed, **regenerate** `wiki/hints.md`.

11. **Summarize:**
    > "Planted X hints in this chapter draft. Y skipped. Ledger updated."
