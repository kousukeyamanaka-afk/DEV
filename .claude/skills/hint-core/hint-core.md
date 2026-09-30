# hint-core — Shared Rules for All Hint Skills

## Project Detection

When any hint skill starts, detect the novel project root:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask the user: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

All hint operations use `<project_root>/wiki/hints.json` and `<project_root>/wiki/hints.md`.

---

## hints.json Structure

The file contains a single JSON object with a `hints` array:

```json
{
  "hints": [
    {
      "id": "hint_001",
      "surface": "The text the reader sees — written subtly, no emphasis",
      "truth": "What it actually means — author-only knowledge",
      "type": "world-rule",
      "importance": "main",
      "status": "planted",
      "planted": {
        "chapter": 2,
        "scene": "Marketplace at dusk",
        "note": "Mentioned casually in passing"
      },
      "resolved": {
        "chapter": null,
        "scene": null,
        "note": null
      },
      "created_at": "2026-05-06T10:00:00"
    }
  ]
}
```

**type** (pick one): `object` | `prophecy` | `character-behavior` | `world-rule` | `dialogue` | `symbol`

**importance** (pick one): `main` | `subplot` | `easter-egg`

**status** (pick one): `planned` | `planted` | `resolved` | `abandoned`

---

## ID Generation

IDs are sequential strings: `hint_001`, `hint_002`, `hint_003`, ...

To assign the next ID: find the highest existing numeric suffix and add 1. If no hints exist, start at `hint_001`.

---

## Invariants (enforce on every write)

1. Always read `hints.json` before any write operation.
2. Always regenerate `hints.md` after any write operation.
3. Never instruct the user to edit `hints.md` — it is always derived from JSON.
4. `resolved.chapter`, `resolved.scene`, `resolved.note` MUST be `null` unless `status == "resolved"`.
5. `planted.chapter`, `planted.scene`, `planted.note` MUST be `null` unless `status == "planted"` or `"resolved"`.
6. When setting `status` to `"abandoned"`, always ask the user for a reason and store it in `planted.note`.

---

## hints.md Generation Format

After every write, regenerate `wiki/hints.md` with this exact structure:

```markdown
# Hint Ledger

## 🌱 Planted (awaiting resolution)
| ID | Surface | Truth | Type | Importance | Planted Ch. |
|----|---------|-------|------|------------|-------------|
| hint_001 | The crystals were warmer... | East wall crystals are Ruin's doing | world-rule | main | ch.2 |

## ✅ Resolved
| ID | Surface | Truth | Type | Importance | Planted Ch. | Resolved Ch. |
|----|---------|-------|------|------------|-------------|--------------|

## 📋 Planned (not yet written into a chapter)
| ID | Surface idea | Truth | Type | Importance |
|----|-------------|-------|------|------------|

## ❌ Abandoned
| ID | Surface | Reason | Type |
|----|---------|--------|------|

_Last updated: YYYY-MM-DD HH:MM:SS_
```

If a section has no entries, still show the header and an italic line: `_None yet._`
