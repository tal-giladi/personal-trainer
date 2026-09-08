"""Schema-check every yaml in the repo. Same logic as .github/workflows/validate.yml.
Run:  py tools/validate.py
"""
import glob, json, os, sys
import yaml, jsonschema


class StrDatesLoader(yaml.SafeLoader):
    """Keep `2026-09-08` a string so JSON Schema `format: date` can check it."""


StrDatesLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

pairs = {
    "profile.yaml": "schemas/profile.schema.json",
    "exercises/catalogue.yaml": "schemas/catalogue.schema.json",
}
for f in glob.glob("plans/*.yaml") + glob.glob("plans/archive/*.yaml"):
    pairs[f] = "schemas/plan.schema.json"
if os.path.exists("plans/next.yaml"):
    pairs["plans/next.yaml"] = "schemas/next.schema.json"
for f in glob.glob("logs/**/*.yaml", recursive=True):
    pairs[f] = "schemas/log.schema.json"

bad = 0
for f, s in pairs.items():
    try:
        with open(f, encoding="utf-8") as fh, open(s, encoding="utf-8") as sh:
            jsonschema.validate(yaml.load(fh, Loader=StrDatesLoader), json.load(sh),
                                format_checker=jsonschema.FormatChecker())
        print("ok  ", f)
    except Exception as e:  # noqa: BLE001
        bad += 1
        print("FAIL", f, "->", str(e).splitlines()[0])
sys.exit(1 if bad else 0)
