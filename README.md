# personal-trainer

Tal's exercise trainer. Claude is the coach, this repo is the memory. See `PLAN.md`.

- `profile.yaml` — who / equipment / goals
- `plans/` — the programme (`active_plan` in profile)
- `logs/YYYY/MM/` — one yaml per session, one commit per session
- `exercises/catalogue.yaml` — names, aliases, substitutes
- `schemas/` — JSON Schema for every yaml type
- `/workout`, `/log`, `/review` — Claude Code skills in `.claude/skills/`
