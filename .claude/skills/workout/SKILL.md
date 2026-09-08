---
name: workout
description: Tell Tal what to do today. Use when he says "workout", "what's today", "מה היום", or asks for a session.
---

# /workout

1. Read `profile.yaml` → `active_plan`; read `plans/<active_plan>.yaml`.
2. Today's weekday (Asia/Jerusalem) → `schedule` → day letter. If Tal names a day letter or
   says "swap", use his.
3. Read the last 4 weeks of `logs/` (only files that exist; do not invent). For each exercise
   in today's day, find its last two logged performances.
4. Apply the plan's `progression` rules mechanically:
   - `reps_kg`: last two sessions hit all target reps at rpe ≤ 8 → `+step_kg`; one miss → hold;
     `misses_before_deload` misses → `-deload_pct`%.
   - `kg: TODO` and no history → ask ONE question: "goblet squat — what weight?" and stop.
     Never propose a starting load yourself.
   - tabata: if last block completed all rounds → `+1 round` up to 8, then `+1 block` up to max.
5. Week number since `starts` divisible by `deload_every_n_weeks` → cut sets by ~30%, say
   "deload week".
6. If the last log lists `pain` for a muscle used today → use the catalogue `substitute` and
   say so in one clause.
7. Output — compact, one line per exercise, nothing else:

```
Mon A lower · 45 min
goblet squat 4x8 @ 22 kg   (+2, hit 8/8/8/8 twice)
romanian deadlift 3x10 @ 20 kg
split squat 3x8/leg @ 12 kg
calf raise 3x15 @ 20 kg
plank 3x45s
```

No warm-up lecture, no motivation. When he says he's done, hand off to `/log`.
