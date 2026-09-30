---
name: research
description: "Worldbuilding research: search the web on a topic or summarize a given URL into project notes. Invoke with /research."
---

# research — Worldbuilding Research Tool

Use this skill when the user invokes `/research`.

Two-mode worldbuilding research tool. Mode A: searches the web on a topic and
synthesizes findings. Mode B: ingests a URL directly. Saves notes to
`wiki/research/<topic>.md`.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm. If `hint-core.md` cannot be read, use the algorithm below directly:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

Store the resolved project root as an absolute path. Use this absolute path for ALL file reads and writes.

---

## Step 2: Choose mode

If the user provided a topic or URL directly in the `/research` invocation (e.g., `/research medieval blacksmithing` or `/research url https://...`), pre-select the appropriate mode and skip this prompt.

Ask:
> "Research mode — topic search or URL?
> A) Topic search — I'll search the web and synthesize findings
> B) URL ingest — paste a URL and I'll extract key worldbuilding facts"

---

## Step 3: Topic search (Mode A)

Note: `WebSearch` and `WebFetch` are standard Claude Code tools. If they are unavailable in this session, inform the user and suggest switching to Mode B (URL ingest) instead.

1. Ask: "What topic do you want to research? (e.g., medieval blacksmithing, Norse burial customs)"
2. Use `WebSearch` to find 3–5 relevant sources for the topic.
3. For each source URL returned, read the page with `WebFetch`. If `WebFetch` fails on a URL, skip it and continue with the remaining sources. Note any skipped URLs in the output.
4. Synthesize a research note from the successfully fetched pages.
5. Slugify the topic name: lowercase, replace spaces and special characters with hyphens (e.g., "Medieval Blacksmithing" → `medieval-blacksmithing`).
6. Check if `[resolved_project_root]/wiki/research/[slug].md` exists:
   - If it does NOT exist: proceed to save.
   - If it DOES exist: ask "A research note already exists for '[topic]'. Append new findings or overwrite? (append / overwrite)"
     - **append:** Read the existing file, then add new findings under a new `## Update YYYY-MM-DD` section.
     - **overwrite:** Replace the file entirely.
7. If the slug would collide with an existing file for a different topic (judge by reading the file's `# Title` line), append `-2` to the slug (e.g., `medieval-blacksmithing-2.md`).
8. Create `[resolved_project_root]/wiki/research/` if it does not already exist.
9. Save the note (see Research Note Format below).
10. Confirm: "Saved to [resolved_project_root]/wiki/research/[slug].md"

---

## Step 4: URL ingest (Mode B)

1. Ask: "Paste the URL to ingest."
2. Read the page with `WebFetch`. If it fails, report: "Could not fetch [URL]. Check that it's publicly accessible and try again." Stop.
3. Extract key facts relevant to worldbuilding: setting, culture, technology, history, social structures, lore.
4. Derive a slug from the page title: lowercase, replace spaces with hyphens, remove special characters.
   If the page has no title or the title is too generic (e.g., "Home", "Index"), derive the slug from the last path segment of the URL instead.
5. Check if `[resolved_project_root]/wiki/research/[slug].md` exists:
   - If it does NOT exist: proceed to save.
   - If it DOES exist: ask "A research note already exists for '[derived title]'. Append new findings or overwrite? (append / overwrite)"
     - **append:** Read existing file, add new findings under `## Update YYYY-MM-DD`.
     - **overwrite:** Replace the file.
6. Create `[resolved_project_root]/wiki/research/` if it does not already exist.
7. Save the note (see Research Note Format below).
8. Confirm: "Saved to [resolved_project_root]/wiki/research/[slug].md"

---

## Research Note Format

```markdown
# [Topic Title]
_Source(s): [URL or list of URLs]_
_Date: YYYY-MM-DD_

## Key Facts
- [fact]
- [fact]

## Terminology
- **[term]**: [definition]

## Common Misconceptions
- [misconception and correction, or "_None noted._"]

## Story-Relevant Details
- [detail applicable to fiction writing — sensory, cultural, procedural]
```

Replace `YYYY-MM-DD` with today's actual date.

All sections are required. If a section has no content, write `_None noted._`.

---

## Edge Cases

- **All WebFetch calls fail (topic search):** Save a stub note with the search query and a warning: "⚠️ All sources failed to load. Note saved as stub — retry or paste a URL manually."
- **No useful worldbuilding content found in a URL:** Save a stub note: "⚠️ No clear worldbuilding content extracted from this URL. Review manually."
- **Ambiguous topic:** Proceed without asking for clarification unless the user's intent is completely unclear.
