---
name: log
description: Record a finished session from Tal's own words into logs/ and commit. Use when he says "log", "done", "I did ...", or dictates sets.
---

# /log

1. Parse what Tal said. Map names through `exercises/catalogue.yaml` (names + aliases).
   Unknown name → ask ONE question ("`skater` isn't in the catalogue — add it, or did you
   mean X?"). Never silently rename.
2. Shorthand you accept:
   - `squat 22 8 8 8 7` → 4 sets, kg 22, reps 8/8/8/7
   - `squat 4x8 @22` → 4 sets of 8 at 22 kg
   - `plank 45 45 40` → sec
   - `tabata 3 blocks, last block 6 rounds` → sets: 8/8/6 rounds
   - `run 4.2 22min` → km 4.2, min 22
   - `rpe 8`, `52 min`, `knee hurt on split squat` → rpe, duration_min, pain[]
3. Missing values stay missing. Do not fill reps, kg or rpe from the plan. Ask only if the
   entry would be useless without it (an exercise with zero sets).
4. Write `logs/YYYY/MM/YYYY-MM-DD.yaml` (second session → `-2`). Shape:

```yaml
date: 2026-09-08
plan: 2026-09-current
day: A
duration_min: 52
rpe: 7
exercises:
  - name: goblet squat
    sets: [{reps: 8, kg: 22}, {reps: 8, kg: 22}, {reps: 8, kg: 22}, {reps: 7, kg: 22}]
  - name: tabata
    sets: [{rounds: 8, work_sec: 20, rest_sec: 10, moves: [burpee, jump squat]}]
pain: [{area: knee, note: "split squat, set 2"}]
notes: "felt strong"
```

5. Run `py tools/validate.py`; fix until every file prints `ok`.
6. If any `kg` in the active plan is `TODO` for an exercise now logged with a weight, set it
   in the plan file in the same commit.
7. Commit: `git add -A && git commit -m "log: 2026-09-08 A" && git push`.
8. Reply with exactly one line: `Logged 2026-09-08 A · 5 exercises · 52 min · rpe 7.`
   If push failed, say that instead.
