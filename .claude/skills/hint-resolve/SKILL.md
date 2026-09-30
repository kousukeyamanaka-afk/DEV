---
name: hint-resolve
description: "Mark a foreshadowing hint as paid off/resolved. Invoke with /hint-resolve."
---

# hint-resolve — Mark a Hint as Resolved

Use this skill when the user invokes `/hint-resolve`.

## Steps

1. **Read** `../hint-core/hint-core.md` for shared rules.

2. **Detect project root** using the project detection algorithm in hint-core.md.

3. **Read** `wiki/hints.json`.

4. **Show the user** all hints with status `planted`, formatted as:
   ```
   hint_001 — "The archivist did not look up when she passed." [character-behavior / main]
   hint_002 — ...
   ```
   Ask: "Which hint was resolved? (Enter the ID)"

5. **Ask for resolution details** one at a time:
   - "Which chapter resolved this hint?"
   - "Which scene?"
   - "Any note about how the payoff landed?"

6. **Update the hint:**
   - Set `status` to `"resolved"`
   - Fill `resolved.chapter`, `resolved.scene`, `resolved.note`

7. **Write** updated `hints.json`.

8. **Regenerate** `wiki/hints.md`.

9. **Confirm:**
   > "`hint_001` marked as resolved in chapter X. Well played."
