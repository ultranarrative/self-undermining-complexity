"""
The assembly experiment: does a community that grows its own complexity walk
itself toward the stability boundary?

Every measure here is reported scale-free or against a matched null, because the
obvious version of each is an artefact waiting to happen.
"""
from __future__ import annotations
import json, time
import numpy as np
import assembly

SEED, POOL, MU, STEPS, REPS = 20260918, 400, 0.5, 1200, 5
SIGMAS = [0.6, 0.9, 1.2, 1.5]
BINS = [(2,20),(20,40),(40,60),(60,90),(90,130),(130,180),(180,250),(250,400)]


def one_history(sigma, rep):
    rng = np.random.default_rng(SEED + rep*31 + int(sigma*100))
    A = assembly.interaction_pool(POOL, MU, sigma, rng)
    K = np.ones(POOL)
    resident = np.array([], dtype=int)
    order = rng.permutation(POOL)
    rows = []
    for t in range(STEPS):
        cand = int(order[t % POOL])
        if cand in resident:
            continue
        N, surv = assembly.saturated_equilibrium(A, K, np.append(resident, cand))
        lost = np.setdiff1d(resident, surv).size
        resident = surv
        if resident.size < 2 or t % 3:
            continue
        lead, bulk = assembly.spectrum_shape(A, N, resident)
        rows.append((resident.size, lead, bulk, N.sum(),
                     assembly.press_spread(A, resident),
                     assembly.drawn_null(A, resident.size, rng), lost))
    return np.array(rows)


if __name__ == "__main__":
    t0 = time.time()
    out = {"pool": POOL, "mu": MU, "steps": STEPS, "reps": REPS,
           "bins": BINS, "sigmas": SIGMAS, "data": {}}
    for sigma in SIGMAS:
        allr = np.vstack([one_history(sigma, r) for r in range(REPS)])
        rich, lead, bulk, tot, spread, null, aval = allr.T
        rec = {k: [] for k in ("richness","ratio","lead","spread","null",
                               "aval_mean","aval_max","total","n")}
        for lo, hi in BINS:
            s = (rich >= lo) & (rich < hi)
            if s.sum() < 15:
                for k in rec: rec[k].append(float("nan"))
                continue
            rec["richness"].append(float(rich[s].mean()))
            rec["ratio"].append(float((lead[s]/bulk[s]).mean()))
            rec["lead"].append(float(lead[s].mean()))
            rec["spread"].append(float(spread[s].mean()))
            rec["null"].append(float(null[s].mean()))
            rec["aval_mean"].append(float(aval[s].mean()))
            rec["aval_max"].append(float(aval[s].max()))
            rec["total"].append(float(tot[s].mean()))
            rec["n"].append(int(s.sum()))
        out["data"][f"{sigma:.1f}"] = rec
        print(f"sigma = {sigma:.1f}  max richness {int(rich.max()):>3}  "
              f"lead/bulk {rec['ratio'][0]:.3f} -> {[v for v in rec['ratio'] if v==v][-1]:.3f}")
    json.dump(out, open("results/h_assembly.json","w"))

    print(f"\n{'sigma':>6} {'richness':>9} {'lead/bulk':>10} {'spread':>8} {'null':>8} "
          f"{'aval mean':>10} {'aval max':>9} {'total N':>9}")
    for sigma in SIGMAS:
        d = out["data"][f"{sigma:.1f}"]
        for i in range(len(BINS)):
            if d["richness"][i] != d["richness"][i]:
                continue
            print(f"{sigma:>6.1f} {d['richness'][i]:>9.1f} {d['ratio'][i]:>10.4f} "
                  f"{d['spread'][i]:>8.3f} {d['null'][i]:>8.3f} {d['aval_mean'][i]:>10.3f} "
                  f"{d['aval_max'][i]:>9.0f} {d['total'][i]:>9.1f}")
        print()
    print(f"done in {time.time()-t0:.0f}s")
