---
name: daily-write
description: "Set up a recurring daily writing reminder. Invoke with /daily-write."
---

# daily-write — Daily Writing Reminder

Use this skill when the user invokes `/daily-write`.

Sets up a daily writing reminder using the `/schedule` skill. Prompts the user
to run `/novel-write` for the current chapter at a chosen time each day.

---

## Step 1: Read shared rules and detect project

Read `../hint-core/hint-core.md` for the project detection algorithm.

Run the project detection algorithm. If `hint-core.md` cannot be read, use the algorithm below directly:
1. Check if the CURRENT directory contains a `wiki/` folder.
2. If not, check parent directory. Repeat up to 3 levels.
3. If still not found, ask: "I couldn't find a wiki/ folder. Please provide the path to your novel project root."

Get the novel title from `wiki/project.md` if it exists (first `# ` heading or `title:` frontmatter; fall back to folder name).

---

## Step 2: Check for existing reminder

Before asking for settings, invoke the `/schedule` skill using the `Skill` tool with `skill: 'schedule'` to list existing scheduled routines (ask it to list). If a daily-write reminder already exists, show it to the user and ask: "A daily-write reminder already exists. Replace it? (yes / no)" If no, stop: "Keeping your existing reminder." If yes, ask `/schedule` to delete it, then continue to get new settings.

If `/schedule` cannot list routines or is unavailable, skip this check and proceed.

---

## Step 3: Get reminder settings

Ask:
> "What time each day should I remind you to write? (e.g., 9:00am, 8:30pm)"

If the user provides a vague answer like "morning" or "evening", ask: "What specific time? (e.g., 9:00am)"

Accept formats: 12-hour (e.g., 9:00am, 8:30pm) or 24-hour (e.g., 21:30). If still unrecognizable after one follow-up, default to 9:00am and confirm: "I'll use 9:00am — is that okay?"

Ask:
> "Which chapter are you currently working on? (e.g., Chapter 3)"

Ask:
> "What timezone are you in? (e.g., America/New_York, Asia/Taipei, UTC+8) — needed so the reminder fires at the right local time."

---

## Step 4: Schedule the reminder

Invoke the `/schedule` skill using the `Skill` tool with `skill: 'schedule'`. Describe the schedule as: daily at [time] the user provided, with the message above. Follow the `/schedule` skill's prompts to complete the setup. If `/schedule` returns an error or is unavailable, fall through to the edge case below.

- **Schedule:** daily at the time the user provided
- **Message:**

> "Time to write! Open your novel project and run `/novel-write` for **[Novel Title]** — Chapter [N] is waiting."

Replace [Novel Title] with the detected title and [N] with the chapter number the user provided.

---

## Step 5: Confirm and instruct

After the schedule is set, confirm:

> "Daily writing reminder set for [time]. I'll prompt you every day to work on Chapter [N] of [Novel Title]."

Then tell the user:

> "When you finish a chapter, run `/daily-write` again to update the chapter number."

Tell the user: "You can run `/schedule` and ask it to list your reminders to verify it was created correctly."

---

## Edge Cases

- **`/schedule` skill unavailable:** Tell the user: "The /schedule skill isn't available in this session. To set a manual reminder, add a daily alarm on your phone or calendar at [time] with the note: 'Run /novel-write for [Novel Title] — Chapter [N].'"
- **`wiki/project.md` missing:** Use the project folder name as the novel title.
- **User provides no chapter number:** Ask once more: "Which chapter are you working on?" If still no answer, use "the next chapter" as a placeholder in the reminder message.
