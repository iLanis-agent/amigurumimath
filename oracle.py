#!/usr/bin/env python3
"""Independent oracle for Amigurumi math. Mirrors engine.js float ops exactly."""
import json, math

EYE_PART = 6
GAP_PART = 2
FILL_PER_L = 12

def r1(x): return math.floor(x * 10 + 0.5) / 10

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def eye_size(head_cm):
    if not (isinstance(head_cm, (int, float)) and math.isfinite(head_cm) and head_cm > 0):
        return {"error": "head size must be positive"}
    diam_mm = head_cm * 10 / math.pi
    return {"headCm": r1(head_cm), "headMm": r1(diam_mm),
            "eyeMm": r1(diam_mm / EYE_PART), "gapMm": r1(diam_mm / GAP_PART)}

def render_eye(r):
    if "error" in r: return r["error"]
    return (f"Head about {num(r['headMm'])} mm across - try {num(r['eyeMm'])} mm safety eyes, placed about "
            f"{num(r['gapMm'])} mm apart (labeled ratios, your pattern wins).")

def stuffing(l, w, h):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (l, w, h)):
        return {"error": "toy dimensions must be positive"}
    vol_ml = math.pi / 6 * l * w * h
    return {"volMl": r1(vol_ml), "grams": r1(vol_ml / 1000 * FILL_PER_L)}

def render_stuff(r):
    if "error" in r: return r["error"]
    return (f"Toy volume about {num(r['volMl'])} ml - plan on {num(r['grams'])} g of fiberfill "
            f"(labeled {FILL_PER_L} g per liter, ellipsoid estimate).")

def bag_count(toys, per_toy_g, bag_g):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (toys, per_toy_g, bag_g)):
        return {"error": "inputs must be positive"}
    need = r1(toys * per_toy_g)
    bags = math.ceil(need / bag_g)
    return {"toys": toys, "perToyG": r1(per_toy_g), "need": need, "bags": bags,
            "leftover": r1(bags * bag_g - need), "bagG": r1(bag_g)}

def render_bag(r):
    if "error" in r: return r["error"]
    s = "" if r["bags"] == 1 else "s"
    return (f"{r['toys']} toys at {num(r['perToyG'])} g each need {num(r['need'])} g - {r['bags']} bag{s} of "
            f"{num(r['bagG'])} g, leaving {num(r['leftover'])} g spare.")

cases = []
for c in [20, 12, 8, 15, 25, 30, 6.5, 40, 0, -3, 18.2, 9.9]:
    res = eye_size(c)
    cases.append({"fn": "eyeSize", "args": [c], "result": res, "render": render_eye(res)})
for l, w, h in [(12, 8, 8), (25, 15, 15), (8, 5, 5), (30, 20, 18), (6, 4, 3),
                (15.5, 10.2, 9.8), (50, 35, 30), (0, 8, 8), (12, -2, 8), (12, 8, 0), (18, 12, 10)]:
    res = stuffing(l, w, h)
    cases.append({"fn": "stuffing", "args": [l, w, h], "result": res, "render": render_stuff(res)})
for t, p, b in [(3, 4.8, 200), (10, 52.9, 200), (1, 12, 100), (5, 35.3, 250),
                (12, 8.5, 150), (2, 95, 200), (20, 22.4, 400), (0, 5, 200),
                (3, -1, 200), (3, 5, 0), (7, 15.7, 100)]:
    res = bag_count(t, p, b)
    cases.append({"fn": "bagCount", "args": [t, p, b], "result": res, "render": render_bag(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
