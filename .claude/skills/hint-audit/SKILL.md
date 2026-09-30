---
name: hint-audit
description: "Audit chapters for foreshadowing health: unplanted, orphaned or overdue hints. Invoke with /hint-audit."
---

# hint-audit — Audit Chapters for Hint Health

Use this skill when the user invokes `/hint-audit`.

## Steps

1. **Read** `../hint-core/hint-core.md` for shared rules.

2. **Detect project root** using the project detection algorithm in hint-core.md.

3. **Read** `wiki/hints.json`.

4. **Ask the user:**
   - "Which chapter range should I audit? (e.g., '1-10' or 'all')"
   - "How many chapters without reinforcement before flagging a planted hint? (default: 5)"

5. **Read the chapter files** in the specified range. Look for files named:
   - `wiki/chapter_01.md`, `wiki/chapter_02.md`, ... (zero-padded)
   - or `chapters/chapter_01.md` — try both locations

6. **For each `planted` hint**, scan all chapter files for the surface text (or paraphrases). Track which chapters mention it. Flag the hint if:
   - It was planted in chapter N and the current audit range extends beyond chapter N+5 with no reinforcement

7. **For each `planned` hint**, check if the user's stated resolution chapter (if known) is within 3 chapters of the audit range's end. If so, flag it as urgent to plant.

8. **Scan for contradictions**: look for any sentence in the chapters that directly contradicts a hint's `truth`. Report suspected contradictions for human review.

9. **Output the audit report:**

   ```
   ## Hint Audit Report — Chapters 1–10

   ### ⚠️ At Risk of Being Forgotten (planted but unreinforced for 5+ chapters)
   - hint_001 "The archivist did not look up..." — planted ch.1, last seen ch.1, now at ch.7. Consider a callback.

   ### 🚨 Urgent: Plant Now (planned, resolve coming soon)
   - hint_003 — planned but not yet in a chapter; resolution target approaching.

   ### 🔍 Possible Contradictions (review manually)
   - Ch.4 says "all archivists rotate weekly" — but hint_001 implies the archivist is a permanent fixture.

   ### ✅ Healthy Hints
   - hint_002 — planted ch.2, reinforced ch.5. On track.
   ```

10. Do NOT write to `hints.json` or `hints.md` — audit is read-only.
