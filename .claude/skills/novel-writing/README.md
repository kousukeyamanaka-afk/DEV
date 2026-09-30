# 📖 Novel Writing Skill

A comprehensive AI-assisted novel writing skill that organizes a novel project into 10 modular components — covering the full lifecycle from world-building to manuscript drafting and review.

Designed for use with Claude Code (or any agent that supports the Skill format defined in `SKILL.md`).

---

## ✨ Features

- **Modular structure** — 10 numbered directories, each handling one stage of the writing pipeline
- **Top-down workflow** — set up the project → world → characters → plot → outlines → drafts → reviews
- **Consistency-first** — every module references project-level metadata and world settings
- **Version-safe** — manuscripts are never overwritten; new versions are saved as new files
- **Reusable prompts** — `09_prompt_templates/` collects prompt templates for common writing tasks

---

## 📂 Directory Structure

```
writing-skill/
├── SKILL.md                  # Master skill instructions
├── 00_project_control/       # Project metadata & global settings
├── 01_world_settings/        # World-building & setting details
├── 02_characters/            # Character profiles & relationships
├── 03_plot_control/          # Main plot arcs & story beats
├── 04_volume_outlines/       # Volume-level outlines (macro structure)
├── 05_chapter_outlines/      # Chapter-level outlines (micro structure)
├── 06_manuscripts/           # Drafted chapter manuscripts
├── 07_chapter_reviews/       # Review notes & revision records
├── 08_style_control/         # Writing style guides & tone rules
└── 09_prompt_templates/      # Reusable AI prompt templates
```

Each subdirectory contains its own `README.md` with detailed instructions for that module.

---

## 🚀 Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/EchoAI-Design/novel-writing-skill.git
   ```

2. **Install as a Claude Code skill** (optional)

   Place the directory under your Claude Code skills folder, e.g.:

   ```
   ~/.claude/skills/novel-writing/
   ```

3. **Initialize your novel project**

   - Fill out `00_project_control/` with title, author, genre, target word count, etc.
   - Populate `01_world_settings/` with world-building details
   - Create character profiles in `02_characters/`
   - Continue through the numbered modules in order

---

## 📝 Workflow

1. **Initialize** — fill out `00_project_control` with project metadata
2. **World-build** — populate `01_world_settings`
3. **Characters** — create profiles in `02_characters`
4. **Plot** — lay out the macro plot in `03_plot_control`
5. **Volume Outline** — break the story into volumes in `04_volume_outlines`
6. **Chapter Outline** — detail each chapter in `05_chapter_outlines`
7. **Draft** — write manuscripts in `06_manuscripts`, using prompts from `09_prompt_templates`
8. **Review** — evaluate drafts in `07_chapter_reviews`, applying rules from `08_style_control`
9. **Revise** — update manuscripts based on reviews; repeat steps 7–8 until approved
10. **Finalize** — mark chapters as approved; update project status

---

## 📐 Conventions

- **File naming**: lowercase with underscores; chapter files use zero-padded numbers (e.g., `ch_001.md`)
- **Language**: content files should be written in the same language as the novel
- **Cross-references**: always check `00_project_control` and `01_world_settings` before drafting
- **Versioning**: never overwrite a manuscript — create a new version file instead
- **Reviews**: every chapter must complete at least one review cycle before approval

---

## 📄 License

MIT — see `LICENSE` if included, otherwise free to use and modify.

---

## 🔗 Links

- Repository: https://github.com/EchoAI-Design/novel-writing-skill
- Skill specification: see [`SKILL.md`](./SKILL.md)
