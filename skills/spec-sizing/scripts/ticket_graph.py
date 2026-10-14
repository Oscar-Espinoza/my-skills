#!/usr/bin/env python3
"""Validate a ticket graph and print its critical chain and parallel waves.

Usage: ticket_graph.py TRACKER.json [--list-key features] [--group GROUP] [--prefix F23-] [--open todo,in_progress]

Considers tickets whose status is in --open (default: todo) and that match --group/--prefix if given.
Deps on tickets that are not open (merged, done) are treated as satisfied; open deps outside the selection are
reported as external blockers. Exits 1 on unknown deps or cycles.
"""
import argparse, json, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tracker")
    ap.add_argument("--list-key", default="features")
    ap.add_argument("--group")
    ap.add_argument("--prefix")
    ap.add_argument("--open", default="todo")
    a = ap.parse_args()
    raw = json.load(open(a.tracker))
    feats = raw if isinstance(raw, list) else raw[a.list_key]
    byid = {f["id"]: f for f in feats}
    open_st = set(a.open.split(","))
    sel = [f["id"] for f in feats if f.get("status") in open_st
           and (not a.group or f.get("group") == a.group) and (not a.prefix or f["id"].startswith(a.prefix))]
    errors = [f"{i}: unknown dep {d}" for i in sel for d in byid[i]["deps"] if d not in byid]
    memo, onstack = {}, set()

    def depth(i):
        if i in memo:
            return memo[i]
        if i in onstack:
            errors.append(f"cycle through {i}")
            return (0, None)
        onstack.add(i)
        ds = [d for d in byid[i]["deps"] if d in byid and byid[d].get("status") in open_st]
        best = max(ds, key=lambda d: depth(d)[0]) if ds else None
        r = (1 + (depth(best)[0] if best else 0), best)
        onstack.discard(i)
        memo[i] = r
        return r

    sys.setrecursionlimit(100000)
    for i in sel:
        depth(i)
    if errors:
        print("ERRORS:\n" + "\n".join(sorted(set(errors))))
        sys.exit(1)
    if not sel:
        print("no open tickets selected")
        return
    end = max(sel, key=lambda i: memo[i][0])
    chain = []
    while end:
        chain.append(end)
        end = memo[end][1]
    print(f"open tickets: {len(sel)}")
    print(f"critical chain ({len(chain)}): " + " -> ".join(reversed(chain)))
    waves = {}
    for i in sel:
        waves.setdefault(memo[i][0], []).append(i)
    for k in sorted(waves):
        print(f"wave {k}: " + ", ".join(sorted(waves[k])))
    ext = sorted({d for i in sel for d in byid[i]["deps"] if d in byid and d not in sel
                  and byid[d].get("status") in open_st})
    if ext:
        print("external open blockers: " + ", ".join(ext))


if __name__ == "__main__":
    main()
