"""
Experiment 05. The two predictions that had never been tested.

P1 says maintenance cost growing faster than linearly with complexity produces a
threshold C* past which returns turn negative. No model in this repository had a
maintenance cost in it, so P1 had stood untested from the start.

P2 says variance and autocorrelation rise before collapse. Testing it needs
collapses, which is why it waited for P1.

There is a prior worth stating before the numbers arrive. Experiment 02 showed
these systems sit permanently at marginal stability, and critical slowing down is
exactly what early-warning signals detect. If a system is always at the edge, its
warning signals may be permanently elevated and therefore useless. That makes the
FALSE POSITIVE rate the real test of P2, not the true positive rate, and this
experiment measures both.
"""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import json, time
import numpy as np

from suc import maintenance as mt

SEED, POOL, MU, SIGMA, STEPS, REPS = 20260918, 300, 0.5, 1.2, 700, 5
WINDOW, LEAD = 40, 120


def score(h):
    """Early-warning trends over the window running up to the end of the run."""
    total = np.array(h["total"], dtype=float)
    end = h["collapse_step"] if h["collapsed"] else len(total)
    seg = total[max(0, end - LEAD):end]
    if seg.size < WINDOW + 12:
        return float("nan"), float("nan")
    var, ar1 = mt.early_warnings(seg, WINDOW)
    return mt.trend(var), mt.trend(ar1)


if __name__ == "__main__":
    t0 = time.time()
    out = {"grid": [], "window": WINDOW, "lead": LEAD}
    print(f"{'mode':>11} {'beta':>5} {'m':>6} {'peak C*':>8} {'collapsed':>10} "
          f"{'tau(var)':>9} {'tau(ar1)':>9}")
    for mode in ("per-capita", "legacy"):
        for beta in (1.0, 1.2, 1.5):
            for m in (0.02, 0.05, 0.08, 0.12):
                peaks, coll, tv, ta = [], [], [], []
                for rep in range(REPS):
                    rng = np.random.default_rng(SEED + rep*13 + int(m*1000) + int(beta*100))
                    h = mt.assemble_with_cost(POOL, MU, SIGMA, m, beta, mode, STEPS, rng)
                    peaks.append(h["peak"]); coll.append(h["collapsed"])
                    a, b = score(h)
                    if a == a: tv.append(a)
                    if b == b: ta.append(b)
                row = {"mode": mode, "beta": beta, "m": m,
                       "peak": float(np.mean(peaks)),
                       "collapse_rate": float(np.mean(coll)),
                       "tau_var": float(np.mean(tv)) if tv else float("nan"),
                       "tau_ar1": float(np.mean(ta)) if ta else float("nan")}
                out["grid"].append(row)
                print(f"{mode:>11} {beta:>5.1f} {m:>6.2f} {row['peak']:>8.0f} "
                      f"{row['collapse_rate']:>10.1f} {row['tau_var']:>9.3f} "
                      f"{row['tau_ar1']:>9.3f}")

    # P2 proper: do the signals separate collapsing runs from surviving ones?
    coll_v, coll_a, surv_v, surv_a = [], [], [], []
    for mode in ("per-capita", "legacy"):
        for m in (0.02, 0.05, 0.08, 0.12):
            for rep in range(8):
                rng = np.random.default_rng(SEED + 500 + rep*7 + int(m*1000))
                h = mt.assemble_with_cost(POOL, MU, SIGMA, m, 1.5, mode, STEPS, rng)
                a, b = score(h)
                if a != a or b != b:
                    continue
                (coll_v if h["collapsed"] else surv_v).append(a)
                (coll_a if h["collapsed"] else surv_a).append(b)
    out["p2"] = {
        "collapsing": {"n": len(coll_v), "tau_var": float(np.mean(coll_v)) if coll_v else float("nan"),
                       "tau_ar1": float(np.mean(coll_a)) if coll_a else float("nan")},
        "surviving": {"n": len(surv_v), "tau_var": float(np.mean(surv_v)) if surv_v else float("nan"),
                      "tau_ar1": float(np.mean(surv_a)) if surv_a else float("nan")},
        "false_positive_var": float(np.mean(np.array(surv_v) > 0)) if surv_v else float("nan"),
        "false_positive_ar1": float(np.mean(np.array(surv_a) > 0)) if surv_a else float("nan"),
        "true_positive_var": float(np.mean(np.array(coll_v) > 0)) if coll_v else float("nan"),
        "true_positive_ar1": float(np.mean(np.array(coll_a) > 0)) if coll_a else float("nan"),
    }
    p2 = out["p2"]
    print(f"\nP2: do the signals tell collapse from survival?")
    print(f"  collapsing runs (n={p2['collapsing']['n']:>2}): tau(var) {p2['collapsing']['tau_var']:+.3f}  tau(ar1) {p2['collapsing']['tau_ar1']:+.3f}")
    print(f"  surviving  runs (n={p2['surviving']['n']:>2}): tau(var) {p2['surviving']['tau_var']:+.3f}  tau(ar1) {p2['surviving']['tau_ar1']:+.3f}")
    print(f"  rising-signal rate   collapsing: var {p2['true_positive_var']:.2f}  ar1 {p2['true_positive_ar1']:.2f}")
    print(f"  rising-signal rate   surviving : var {p2['false_positive_var']:.2f}  ar1 {p2['false_positive_ar1']:.2f}")
    json.dump(out, open("results/l_maintenance.json", "w"))
    print(f"\ndone in {time.time()-t0:.0f}s")
