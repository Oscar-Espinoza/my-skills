#!/usr/bin/env python3
"""Apply a splits file to a ticket tracker JSON and refuse on any coverage or graph error.

Usage:
  apply_splits.py TRACKER.json SPLITS.json [--write] [--list-key features] [--gate-regex '^pnpm check passes']
                  [--group GROUP] [--umbrella UMBRELLA_ID] [--date 2026-10-14]

TRACKER.json: a list of tickets, or an object holding the list under --list-key. Each ticket has at least
  id, title, description, acceptance (list of strings), deps (list of ids), status.

SPLITS.json:
{
  "splits": {
    "<original id>": {
      "subs": [{"id", "title", "shortTitle"?, "note" | "description", "acceptance": [1-based original line numbers],
                "deps": [...], "flow"?: "...", "surface"?: "..."}],
      "shared": {"<line no>": "which part each sub verifies"}   # required for a non-gate line on >1 sub
    }
  },
  "downstream": {"<original id>": ["<sub ids a dependent takes by default>"]},
  "overrides": {"<dependent id>": {"<original id>": ["<sub ids>"]}},
  "setDeps":   {"<ticket id>": ["<deps>"]},      # explicit deps for kept tickets
  "notes":     {"<ticket id>": "text appended to its description"},
  "flows":     {"<ticket id>": "<flow>"}
}
A sub with "note" gets: original description + blank line + note. A sub with "description" replaces it.
The gate line (matched by --gate-regex) is added to every sub automatically.
Checks: every original line covered, lines in order, duplicates only for the gate or with a 'shared' reason,
deps exist, no runnable ticket depends on a superseded one, no cycles. Prints a report; writes only with --write.
"""
import argparse, copy, json, re, sys

RUNTIME_KEYS = ("pid", "pidStart", "foremanPid", "sha", "branch", "pausedFrom", "pausedAt", "lastFeedback", "plan", "stop")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tracker")
    ap.add_argument("splits")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--list-key", default="features")
    ap.add_argument("--gate-regex", default=None, help="regex for the final checks/gate acceptance line")
    ap.add_argument("--group", default=None, help="group to set on subs and to collect umbrella members from")
    ap.add_argument("--umbrella", default=None, help="umbrella ticket whose deps become every open group member")
    ap.add_argument("--date", default="")
    a = ap.parse_args()

    raw = json.load(open(a.tracker))
    feats = raw if isinstance(raw, list) else raw[a.list_key]
    for f in feats:
        f.setdefault("deps", [])
    spec = json.load(open(a.splits))
    gate_re = re.compile(a.gate_regex) if a.gate_regex else None
    byid = {f["id"]: f for f in feats}
    errors, report = [], []
    split_ids = set(spec["splits"])
    for o in split_ids:
        if o not in byid:
            errors.append(f"unknown original {o}")
    sub_ids = [s["id"] for v in spec["splits"].values() for s in v["subs"]]
    dup = (set(sub_ids) & set(byid)) | {i for i in sub_ids if sub_ids.count(i) > 1}
    if dup:
        errors.append(f"sub ids already exist or repeat: {sorted(dup)}")

    out = []
    for f in feats:
        oid = f["id"]
        if oid not in spec["splits"]:
            out.append(f)
            continue
        sp = spec["splits"][oid]
        acc = f["acceptance"]
        n = len(acc)
        gate = [i for i, x in enumerate(acc, 1) if gate_re and gate_re.search(x)]
        if gate_re and len(gate) != 1:
            errors.append(f"{oid}: expected 1 gate line, found {gate}")
        seen, subs = {}, []
        for s in sp["subs"]:
            lines = list(s["acceptance"])
            if lines != sorted(lines):
                errors.append(f"{s['id']}: acceptance not in original order {lines}")
            if gate and gate[0] not in lines:
                lines = sorted(lines + [gate[0]])
            for i in lines:
                if not 1 <= i <= n:
                    errors.append(f"{s['id']}: line {i} out of range 1..{n}")
                seen.setdefault(i, []).append(s["id"])
            g = copy.deepcopy(f)
            for k in RUNTIME_KEYS:
                g.pop(k, None)
            g.update({
                "id": s["id"], "title": s["title"],
                "description": s["description"] if "description" in s else f["description"] + "\n\n" + s["note"],
                "acceptance": [acc[i - 1] for i in lines if 1 <= i <= n],
                "deps": s["deps"], "status": "todo",
            })
            for k in ("shortTitle", "flow", "surface"):
                if k in s:
                    g[k] = s[k]
            if "attempts" in g:
                g["attempts"] = 0
            if "costUsd" in g:
                g["costUsd"] = 0
            if a.group:
                g["group"] = a.group
            subs.append(g)
        for i in range(1, n + 1):
            owners = seen.get(i, [])
            if not owners:
                errors.append(f"{oid}: acceptance line {i} lost")
            elif len(owners) > 1 and i not in gate and str(i) not in sp.get("shared", {}):
                errors.append(f"{oid}: line {i} on {owners} without a 'shared' reason")
        names = [s["id"] for s in sp["subs"]]
        listed = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
        f = copy.deepcopy(f)
        f["status"] = "paused"
        when = f" ({a.date})" if a.date else ""
        f["description"] += f"\n\nSUPERSEDED: split into {listed}{when}. Do not run."
        out.append(f)
        out.extend(subs)
        report.append(f"split {oid} -> {names}")

    byid = {f["id"]: f for f in out}
    down, over = spec.get("downstream", {}), spec.get("overrides", {})
    for o in split_ids - set(down):
        errors.append(f"no downstream mapping for {o}")
    for f in out:
        if f["id"] == a.umbrella or f["id"] in split_ids:
            continue
        new = []
        for d in f["deps"]:
            if d in split_ids:
                rep = over.get(f["id"], {}).get(d, down.get(d, []))
                report.append(f"rewire {f['id']}: {d} -> {rep}")
                new.extend(rep)
            else:
                new.append(d)
        f["deps"] = [d for i, d in enumerate(new) if d not in new[:i] and d != f["id"]]
    for key, apply in (("setDeps", lambda t, v: t.__setitem__("deps", v)),
                       ("notes", lambda t, v: t.__setitem__("description", t["description"] + "\n\n" + v)),
                       ("flows", lambda t, v: t.__setitem__("flow", v))):
        for tid, v in spec.get(key, {}).items():
            if tid not in byid:
                errors.append(f"{key}: unknown {tid}")
            else:
                apply(byid[tid], v)
                report.append(f"{key} {tid}")
    if a.umbrella:
        if a.umbrella not in byid:
            errors.append(f"unknown umbrella {a.umbrella}")
        else:
            byid[a.umbrella]["deps"] = [f["id"] for f in out if f.get("group") == a.group
                                        and f["id"] != a.umbrella and f["status"] != "paused"]

    superseded = {f["id"] for f in out if f["status"] == "paused" and "SUPERSEDED" in f.get("description", "")}
    for f in out:
        for d in f["deps"]:
            if d not in byid:
                errors.append(f"{f['id']}: unknown dep {d}")
            elif d in superseded and f["id"] not in superseded:
                errors.append(f"{f['id']}: depends on superseded {d}")
    color = {}

    def dfs(u, path):
        color[u] = 1
        for v in byid[u]["deps"]:
            if v in byid:
                if color.get(v) == 1:
                    errors.append("cycle: " + " -> ".join(path + [u, v]))
                elif not color.get(v):
                    dfs(v, path + [u])
        color[u] = 2

    sys.setrecursionlimit(100000)
    for f in out:
        if not color.get(f["id"]):
            dfs(f["id"], [])

    print("\n".join(report))
    if errors:
        print("ERRORS:\n" + "\n".join(errors))
        sys.exit(1)
    print(f"OK: {len(feats)} -> {len(out)} entries")
    if a.write:
        if isinstance(raw, list):
            raw = out
        else:
            raw[a.list_key] = out
        text = open(a.tracker).read()
        indent = 2 if text.startswith("{\n  ") or text.startswith("[\n  ") else None
        open(a.tracker, "w").write(json.dumps(raw, indent=indent, ensure_ascii=False) + "\n")
        print("written", a.tracker)


if __name__ == "__main__":
    main()
