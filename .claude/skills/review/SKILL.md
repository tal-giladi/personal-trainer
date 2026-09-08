---
name: review
description: Weekly review — adherence, volume, PRs, and next week's plan changes. Use when Tal says "review", "how was the week", or a weekly-review issue is open.
---

# /review

1. Week = last Mon–Sun (Asia/Jerusalem) unless Tal names one (`2026-W37`).
2. Read every log in that week. Compute (with `trainer stats` when it exists, else by hand):
   - adherence: sessions logged / 7
   - per strength exercise: top set (kg × reps), total volume (Σ kg×reps), vs previous week
   - tabata: blocks × rounds completed vs planned
   - cardio: km, min
   - PRs: any top set heavier or more reps at same kg than any earlier log
   - flags: rpe ≥ 9 days, pain entries, exercises skipped 2+ weeks
3. Write `reports/weekly/YYYY-Www.md`:

```
# 2026-W37
adherence 6/7 · avg rpe 7.4 · 3 PRs · 0 pain

| exercise | top set | volume | Δ vs W36 |
|---|---|---|---|
| goblet squat | 24×8 | 768 | +8% |

flags: rpe 9 on Thu (D); pull up skipped 2 weeks
next week: +2 kg goblet squat, RDL; hold bench; tabata D → 4 blocks
```

4. Propose next week's changes (from the plan's progression rules + flags) as one short list.
   **Wait for Tal's yes.** He edits, you apply.
5. On yes: if changes touch targets, write `plans/YYYY-MM-<name>.yaml`, move the old plan to
   `plans/archive/`, update `profile.yaml` → `active_plan`. Small load bumps go in the same
   plan file.
6. Commit: `review: 2026-W37` and push. If a GitHub issue "review 2026-W37" exists, close it
   with the report body (`gh issue close`).
7. Reply in one line: `W37: 6/7, 3 PRs, plan bumped. Next review Mon.`
