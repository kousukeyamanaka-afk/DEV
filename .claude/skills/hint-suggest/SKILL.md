---
name: hint-suggest
description: "Reverse-plan hints: given a future reveal, suggest which setups to plant in earlier chapters. Invoke with /hint-suggest."
---

# hint-suggest — Reverse-Plan Hints from a Future Reveal

Use this skill when the user invokes `/hint-suggest`.

## Steps

1. **Read** `../hint-core/hint-core.md` for shared rules.

2. **Detect project root** using the project detection algorithm in hint-core.md.

3. **Read** `wiki/hints.json` and any wiki files present (`wiki/project.md`, `wiki/characters.md`, `wiki/world.md`, `wiki/themes.md`, `wiki/plot.md`). Use these to understand the story's world, characters, and rules.

4. **Ask the user:**
   - "What truth or reveal do you want to land? Describe it fully."
   - "In which chapter will this be revealed?"
   - "How many foreshadowing hints do you want to plant? (recommended: 3–5)"

5. **Generate a foreshadowing plan** — for each suggested hint, provide:
   - **Surface text idea**: a specific sentence or detail the reader would see
   - **Disguise strategy**: one of — misdirection (reader assumes it means something else), background detail (easy to skim past), throwaway dialogue (character says it casually), rule-establishment (presents it as world-building, not a clue)
   - **Recommended chapter** to plant it (spread them out; earliest hint should be as early as possible)
   - **Why it works in retrospect**: what the reader will think back on after the reveal

   Example output:
   ```
   SUGGESTED HINT 1
   Surface: "The god-king paused at the door to the memory vault for exactly three heartbeats before entering."
   Disguise: character-behavior (reads as ritual or habit)
   Plant in: Chapter 3
   Retrospect payoff: In ch.30 we learn he pauses to listen for stolen memories — they whisper at doorways.

   SUGGESTED HINT 2
   ...
   ```

6. **Ask the user** for each suggestion: "Add to ledger as planned? (yes / skip / rewrite)"
   - If rewrite: ask what to change and revise.

7. For each accepted suggestion:
   - Create a new hint object with `status: "planned"` and `planted.chapter` set to the recommended chapter
   - Append to `hints.json`

8. **Regenerate** `wiki/hints.md`.

9. **Confirm:**
   > "Added X planned hints targeting the ch.N reveal. Use `/hint-plant` when writing those chapters."
