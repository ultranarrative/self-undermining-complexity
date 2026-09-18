"""
A bigger sample for P2 specifically. The grid run produced only 12 collapsing
histories, which is too few to rest a claim on, so this generates collapsing and
surviving runs deliberately and scores both with the same detector.
"""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import json
import numpy as np

from suc import maintenance as mt

SEED, POOL, MU, SIGMA, STEPS = 20260918, 300, 0.5, 1.2, 700
WINDOW, LEAD = 40, 120


def score(h):
    total = np.array(h["total"], dtype=float)
    end = h["collapse_step"] if h["collapsed"] else len(total)
    seg = total[max(0, end - LEAD):end]
    if seg.size < WINDOW + 12:
        return float("nan"), float("nan")
    var, ar1 = mt.early_warnings(seg, WINDOW)
    return mt.trend(var), mt.trend(ar1)


rows = {"collapsing": [], "surviving": []}
for mode in ("legacy", "per-capita"):
    for m in (0.08, 0.10, 0.12, 0.15):
        for rep in range(22):
            rng = np.random.default_rng(SEED + 9000 + rep*11 + int(m*1000) + len(mode))
            h = mt.assemble_with_cost(POOL, MU, SIGMA, m, 1.5, mode, STEPS, rng)
            a, b = score(h)
            if a != a or b != b:
                continue
            rows["collapsing" if h["collapsed"] else "surviving"].append((a, b))

out = {}
for k, v in rows.items():
    arr = np.array(v)
    out[k] = {"n": int(arr.shape[0]),
              "tau_var": float(arr[:, 0].mean()), "tau_ar1": float(arr[:, 1].mean()),
              "rise_var": float((arr[:, 0] > 0).mean()),
              "rise_ar1": float((arr[:, 1] > 0).mean())}

c, s = out["collapsing"], out["surviving"]
print(f"{'':>12} {'n':>4} {'mean tau(var)':>14} {'mean tau(ar1)':>14} {'rises var':>10} {'rises ar1':>10}")
for k in ("collapsing", "surviving"):
    d = out[k]
    print(f"{k:>12} {d['n']:>4} {d['tau_var']:>14.3f} {d['tau_ar1']:>14.3f} "
          f"{d['rise_var']:>10.2f} {d['rise_ar1']:>10.2f}")
out["discrimination_var"] = c["rise_var"] - s["rise_var"]
out["discrimination_ar1"] = c["rise_ar1"] - s["rise_ar1"]
print()
print(f"  variance        separates collapse from survival by {out['discrimination_var']:+.2f}")
print(f"  autocorrelation separates collapse from survival by {out['discrimination_ar1']:+.2f}")
json.dump(out, open("results/m_p2_power.json", "w"))
