"""Muscle-group recovery state from the logs. Facts only - the decision is Claude's.

Run:  py tools/muscles.py [--days 14] [--today YYYY-MM-DD]
Prints a table and writes state/muscles.md (committed, so GitHub shows it too).
"""
import argparse, datetime as dt, glob, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


class StrDatesLoader(yaml.SafeLoader):
    pass


StrDatesLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load(p):
    with open(p, encoding="utf-8") as fh:
        return yaml.load(fh, Loader=StrDatesLoader)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today)

    cat = load("exercises/catalogue.yaml")
    groups = cat["groups"]                       # group -> [muscles]
    muscle_to_group = {m: g for g, ms in groups.items() for m in ms}
    ex = {}
    for e in cat["exercises"]:
        ex[e["name"]] = e
        for al in e.get("aliases", []):
            ex[al] = e

    plan_name = load("profile.yaml")["active_plan"]
    plan = load(f"plans/{plan_name}.yaml")
    sel = plan.get("selection", {})
    recovery = sel.get("recovery_hours", {})
    targets = sel.get("weekly_targets", {})

    since = today - dt.timedelta(days=a.days)
    logs = []
    for f in sorted(glob.glob("logs/**/*.yaml", recursive=True)):
        d = load(f)
        day = dt.date.fromisoformat(d["date"])
        if since <= day <= today:
            logs.append((day, d))

    # per group: last date, sessions in 7d, sets in 7d
    state = {g: {"last": None, "sessions7": set(), "sets7": 0} for g in groups}
    types = {}                                    # date -> session type(s)
    week_ago = today - dt.timedelta(days=6)
    for day, d in logs:
        seen = set()
        for item in d["exercises"]:
            e = ex.get(item["name"])
            if not e:
                print(f"?? unknown exercise '{item['name']}' in {day}", file=sys.stderr)
                continue
            gs = {muscle_to_group.get(e["muscles"][0])} - {None}   # primary muscle only
            nsets = len(item.get("sets", []))
            for g in gs:
                st = state[g]
                if st["last"] is None or day > st["last"]:
                    st["last"] = day
                if day >= week_ago:
                    st["sessions7"].add(day)
                    st["sets7"] += nsets
            seen |= gs
        kind = "cardio" if seen <= {"cardio", "core"} and "cardio" in seen else "strength"
        types[day] = (kind, sorted(seen - {"cardio"}) if kind == "strength" else sorted(seen))

    lines = [f"# Muscle state as of {today}", "",
             "| group | last worked | hours ago | sessions 7d | sets 7d | target/wk | status |",
             "|---|---|---|---|---|---|---|"]
    for g in groups:
        st = state[g]
        if st["last"] is None:
            hours, last, status = None, "never", "fresh"
        else:
            hours = int((today - st["last"]).days * 24)
            last = st["last"].isoformat()
            need = recovery.get(g, 48)
            status = "fresh" if hours >= need else "recovering"
            if hours >= 24 * 5 and g != "cardio":
                status = "STALE"
        n7 = len(st["sessions7"])
        tgt = targets.get(g, "")
        if tgt != "" and n7 >= tgt:
            status += " (weekly target met)"
        lines.append(f"| {g} | {last} | {'' if hours is None else hours} | {n7} | {st['sets7']} | {tgt} | {status} |")

    lines += ["", "## Last 7 days", ""]
    for i in range(6, -1, -1):
        d = today - dt.timedelta(days=i)
        t = types.get(d)
        lines.append(f"- {d} {d.strftime('%a')}: " + (f"{t[0]} {', '.join(t[1])}" if t else "rest / not logged"))

    out = "\n".join(lines) + "\n"
    os.makedirs("state", exist_ok=True)
    with open("state/muscles.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    print(out)


if __name__ == "__main__":
    main()
