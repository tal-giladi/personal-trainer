---
name: checkin
description: Daily check-in - ask what Tal did, log it, recompute muscle-group recovery, plan the next session, commit. Use when he says hi, checkin, what's next, "I did ...", or starts a conversation with no other ask.
---

# /checkin

1. `git pull -q`. Read `profile.yaml`, the active plan, `plans/next.yaml` (may not exist).
2. Find the last logged date. If yesterday (Asia/Jerusalem) has no log, ask exactly:
   `What did you do yesterday (Tue 2026-09-08)?` — one line, then stop and wait.
   If he already described it in his message, skip the question.
   "Rest" / "nothing" → write a log with `exercises: []`? No — no log means rest. Just move on.
3. Log what he said via the `/log` steps. Set `followed_plan` by comparing with
   `plans/next.yaml` (same type and same groups → true). Unknown exercise → add to the
   catalogue (muscles + group) in the same commit; ask only if the muscles are unclear.
4. Run `py tools/muscles.py`. Read the table: which groups are fresh / recovering / STALE,
   sets per group in 7 days, what the last 7 days looked like.
5. Choose the next session with the CLAUDE.md planning rules. Write it down before looking
   at templates: `type` (strength|hiit|cardio|recovery), `groups`, one-clause `reason`.
6. Build the exercise list: start from the matching template in the plan, drop/add to fit the
   chosen groups, then set loads from history with the progression rules. `kg: TODO` with
   no history → ask `goblet squat — what weight will you use?` and stop.
7. Write `plans/next.yaml`:

```yaml
date: 2026-09-09
type: strength
groups: [push, core]
template: C
reason: "legs done yesterday, push fresh since Fri, cardio at 3/3 for the week"
exercises:
  - { name: dumbbell bench press, sets: 4, reps: 8, kg: 20 }
  - { name: shoulder press,       sets: 3, reps: 10, kg: 12 }
  - { name: push up,              sets: 3, reps: 15 }
  - { name: plank,                sets: 3, sec: 45 }
  - { name: tabata, blocks: 1, rounds: 8, work_sec: 20, rest_sec: 10, moves: [burpee, high knees] }
```

8. `py tools/validate.py` → all ok. `git add -A && git commit -m "checkin: 2026-09-08" && git push`.
9. Reply, nothing else:

```
Logged Tue: legs (4 exercises, rpe 8).
Wed → push + core · ~45 min
dumbbell bench press 4x8 @ 20
shoulder press 3x10 @ 12
push up 3x15
plank 3x45s
tabata 1 block: burpee / high knees
(legs recovering, push fresh, cardio 3/3 this week)
```
