---
name: hint-list
description: "View the foreshadowing hint ledger. Invoke with /hint-list."
---

# hint-list — View the Hint Ledger

Use this skill when the user invokes `/hint-list`.

## Steps

1. **Read** `../hint-core/hint-core.md` for shared rules.

2. **Detect project root** using the project detection algorithm in hint-core.md.

3. **Read** `wiki/hints.json`. If it doesn't exist or has no hints, respond:
   > "No hints registered yet. Use `/hint-add` to register your first hint."
   Then stop.

4. **Group hints by status:**
   - `planted` → 🌱 Planted (awaiting resolution)
   - `resolved` → ✅ Resolved
   - `planned` → 📋 Planned
   - `abandoned` → ❌ Abandoned

5. **Output each group** as a markdown table. Use the hints.md format from hint-core.md as a template. Show ALL fields relevant to each status group.

6. At the end, print a summary line:
   > "Total: X hints — Y planted, Z resolved, W planned, V abandoned."
