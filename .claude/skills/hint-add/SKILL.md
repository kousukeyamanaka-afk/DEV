---
name: hint-add
description: "Register a new foreshadowing hint (setup -> payoff) in the hint ledger. Invoke with /hint-add."
---

# hint-add — Register a New Hint

Use this skill when the user invokes `/hint-add`.

## Steps

1. **Read** `../hint-core/hint-core.md` for shared rules.

2. **Detect project root** using the project detection algorithm in hint-core.md.

3. **Read** `wiki/hints.json`. If the file doesn't exist, create it:
   ```json
   { "hints": [] }
   ```

4. **Gather hint details** by asking the user these questions one at a time:

   - "What is the **surface text** — the exact sentence or phrase the reader will see? (Keep it subtle, no dramatic emphasis)"
   - "What is the **truth** — what does this actually mean or foreshadow? (Author-only knowledge)"
   - "What **type** is this hint? Choose: object / prophecy / character-behavior / world-rule / dialogue / symbol"
   - "What is the **importance**? Choose: main / subplot / easter-egg"
   - "What is the **status**? Choose: planned (not yet in a chapter) / planted (already written in)"
   - If status is `planted`: "Which chapter? Which scene? Any note about how it's disguised?"

5. **Assign the next ID** per hint-core.md ID generation rules.

6. **Build the hint object:**
   ```json
   {
     "id": "<next_id>",
     "surface": "<user answer>",
     "truth": "<user answer>",
     "type": "<user answer>",
     "importance": "<user answer>",
     "status": "<user answer>",
     "planted": {
       "chapter": <number or null>,
       "scene": "<string or null>",
       "note": "<string or null>"
     },
     "resolved": {
       "chapter": null,
       "scene": null,
       "note": null
     },
     "abandoned_reason": null,
     "created_at": "<ISO timestamp>"
   }
   ```

7. **Append** the hint object to the `hints` array in `hints.json` and write the file.

8. **Regenerate** `wiki/hints.md` per the format in hint-core.md.

9. **Confirm** to the user:
   > "Hint `<id>` registered. Ledger updated."
