---
name: workout
description: Show the planned next session from plans/next.yaml. Use when Tal says "workout", "what's today", "show me the plan". If the plan is missing or stale, runs /checkin instead.
---

# /workout

1. Read `plans/next.yaml`. If missing, or its `date` is before today, or a newer log exists
   than the plan was made for → run `/checkin` instead.
2. Print it compactly, one line per exercise, the reason as a trailing parenthesis:

```
Wed → push + core · ~45 min
dumbbell bench press 4x8 @ 20
shoulder press 3x10 @ 12
push up 3x15
plank 3x45s
tabata 1 block: burpee / high knees
(legs recovering, push fresh, cardio 3/3 this week)
```

3. If he asks to change it ("no HIIT today", "shoulder hurts") → adjust with the CLAUDE.md
   rules, rewrite `plans/next.yaml`, validate, commit `plan: 2026-09-09 adjusted`, push,
   reprint.
