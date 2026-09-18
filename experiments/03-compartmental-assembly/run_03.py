"""
Experiment 03. Grown into compartments.

Experiment 01 found that containment, modularity's only real benefit, weakens as a
system approaches criticality. Experiment 02 found that a system which grows its own
complexity ends up at criticality without being put there. Each used a different model,
so the obvious joint claim had no way to be tested.

This runs both in one model: assemble a community whose pool has compartment
structure, and ask whether containment still holds at the endpoint assembly picks
for itself.

The prediction, if 01 and 02 both transfer, is that partial compartmentalization buys
nothing at the assembly endpoint, and only complete decoupling holds.
"""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import json, time
import numpy as np

from suc import assembly

SEED, POOL, M, MU, SIGMA, STEPS, REPS = 20260918, 400, 4, 0.5, 1.2, 1200, 5
QS = [0.0, 0.5, 0.9, 1.0]
COUPLE_MEAN = __import__("os").environ.get("COUPLE_MEAN") == "1"


def one_history(q, rep):
    rng = np.random.default_rng(SEED + rep*97 + int(q*1000))
    A, label = assembly.modular_pool(POOL, M, MU, SIGMA, q, rng,
                                     couple_mean=COUPLE_MEAN)
    K = np.ones(POOL)
    resident = np.array([], dtype=int)
    order = rng.permutation(POOL)
    rows = []
    for t in range(STEPS):
        cand = int(order[t % POOL])
        if cand in resident:
            continue
        N, surv = assembly.saturated_equilibrium(A, K, np.append(resident, cand))
        resident = surv
        if resident.size < 2 or t % 3:
            continue
        lead, bulk = assembly.spectrum_shape(A, N, resident)
        rows.append((resident.size, lead, bulk,
                     assembly.press_spread(A, resident),
                     assembly.compartment_ceiling(label, resident)))
    return np.array(rows)


if __name__ == "__main__":
    t0 = time.time()
    print("compartments coupled through the mean:" , COUPLE_MEAN)
    out = {"pool": POOL, "m": M, "mu": MU, "sigma": SIGMA, "reps": REPS,
           "qs": QS, "by_richness": {}, "by_margin": {}}

    RBINS = [(2,20),(20,40),(40,60),(60,90),(90,130),(130,180),(180,260)]
    # Bins of scale-free distance to the boundary, so every q is compared at the
    # same proximity to criticality rather than at the same richness.
    MBINS = [(0.40,1.0),(0.20,0.40),(0.10,0.20),(0.06,0.10),(0.04,0.06),(0.0,0.04)]

    store = {}
    for q in QS:
        allr = np.vstack([one_history(q, r) for r in range(REPS)])
        store[q] = allr
        rich, lead, bulk, spread, ceil = allr.T
        ratio = lead / bulk

        rec = {k: [] for k in ("richness","ratio","spread","ceiling","n")}
        for lo, hi in RBINS:
            s = (rich >= lo) & (rich < hi)
            if s.sum() < 15:
                for k in rec: rec[k].append(float("nan"))
                continue
            rec["richness"].append(float(rich[s].mean()))
            rec["ratio"].append(float(ratio[s].mean()))
            rec["spread"].append(float(spread[s].mean()))
            rec["ceiling"].append(float(ceil[s].mean()))
            rec["n"].append(int(s.sum()))
        out["by_richness"][f"{q:.2f}"] = rec

        rec2 = {k: [] for k in ("ratio","spread","ceiling","richness","n")}
        for lo, hi in MBINS:
            s = (ratio >= lo) & (ratio < hi)
            if s.sum() < 15:
                for k in rec2: rec2[k].append(float("nan"))
                continue
            rec2["ratio"].append(float(ratio[s].mean()))
            rec2["spread"].append(float(spread[s].mean()))
            rec2["ceiling"].append(float(ceil[s].mean()))
            rec2["richness"].append(float(rich[s].mean()))
            rec2["n"].append(int(s.sum()))
        out["by_margin"][f"{q:.2f}"] = rec2

        print(f"q = {q:.2f}  max richness {int(rich.max()):>3}  "
              f"lead/bulk {ratio.max():.3f} -> {ratio.min():.4f}  "
              f"final spread {rec['spread'][-1] if rec['spread'][-1]==rec['spread'][-1] else float('nan'):.3f}")

    out["mbins"] = MBINS; out["rbins"] = RBINS
    tag = "j_meancoupled" if COUPLE_MEAN else "i_compartmental"
    out["couple_mean"] = COUPLE_MEAN
    json.dump(out, open(f"results/{tag}.json","w"))

    print(f"\nDoes the walk to the edge still happen with compartments?")
    print(f"{'q':>6} " + "".join(f"{f'rich {lo}-{hi}':>14}" for lo,hi in RBINS))
    for q in QS:
        d = out["by_richness"][f"{q:.2f}"]
        print(f"{q:>6.2f} " + "".join(
            f"{v:>14.4f}" if v==v else f"{'-':>14}" for v in d["ratio"]))

    print(f"\nAt MATCHED distance to the boundary: spread, and the ceiling it must beat")
    print(f"{'q':>6} " + "".join(f"{f'{lo}-{hi}':>16}" for lo,hi in MBINS))
    for q in QS:
        d = out["by_margin"][f"{q:.2f}"]
        cells = []
        for sp, ce in zip(d["spread"], d["ceiling"]):
            cells.append(f"{sp:.2f}/{ce:.2f}".rjust(16) if sp == sp else "-".rjust(16))
        print(f"{q:>6.2f} " + "".join(cells))
    print(f"\ndone in {time.time()-t0:.0f}s")
