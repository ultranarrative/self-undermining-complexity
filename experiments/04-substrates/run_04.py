"""
Experiment 04. Is this complexification, or is it ecology?

Three substrates that share no mechanism, each accreting elements under a filter
that is about function rather than stability, each reporting a normalised
distance to its own critical point. The claim under test is that accretion drives
that margin to zero regardless of what the system is made of.

  Lotka-Volterra   species arrive; those that cannot hold a positive abundance
                   are dropped. Margin: leading eigenvalue over the bulk.
  Hopfield         memories arrive; those that can no longer be recalled are
                   dropped. Margin: recall headroom of the WORST retained memory,
                   which is the fair analogue of the leading eigenvalue.
  Boolean network  nodes arrive; those that have stopped computing anything are
                   dropped. Margin: distance of average sensitivity from s = 1.

A second measurement runs alongside, testing a candidate explanation for whatever
the first one finds: **interference**, the degree to which adding one element
degrades the elements already present. Species compete for finite carrying
capacity and memories compete for the same finite set of weights, so both should
interfere. Boolean nodes do not obviously share anything, so they should not.
"""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import json, time
import numpy as np

from suc import assembly, substrates as sub

SEED, REPS = 20260918, 4


def glv_history(rep):
    rng = np.random.default_rng(SEED + rep)
    POOL, MU, SIGMA = 400, 0.5, 1.2
    A = assembly.interaction_pool(POOL, MU, SIGMA, rng)
    K = np.ones(POOL)
    resident = np.array([], dtype=int)
    order = rng.permutation(POOL)
    frac, margin, interf = [], [], []
    prevN = None
    for t in range(1000):
        cand = int(order[t % POOL])
        if cand in resident:
            continue
        before = resident.copy()
        N, surv = assembly.saturated_equilibrium(A, K, np.append(resident, cand))
        if before.size > 2 and N.size and prevN is not None:
            # resident is not sorted (the candidate is appended at the end), so
            # position maps rather than searchsorted
            pos_b = {int(v): i for i, v in enumerate(before)}
            pos_s = {int(v): i for i, v in enumerate(surv)}
            common = [int(v) for v in before if int(v) in pos_s]
            if len(common) > 2:
                old = np.array([prevN[pos_b[v]] for v in common])
                new = np.array([N[pos_s[v]] for v in common])
                interf.append(float(np.mean(np.abs(new - old) / np.maximum(np.abs(old), 1e-9))))
        resident, prevN = surv, N
        if resident.size > 2 and t % 3 == 0:
            lead, bulk = assembly.spectrum_shape(A, N, resident)
            frac.append(t / 1000.0)
            margin.append(abs(lead / bulk))
    return frac, margin, interf


def hopfield_history(rep):
    rng = np.random.default_rng(SEED + rep)
    N, THRESH = 400, 0.9
    stored = np.zeros((0, N))
    frac, margin, interf = [], [], []
    for t in range(1000):
        cand = rng.choice([-1.0, 1.0], size=(1, N))
        before = stored
        if before.shape[0] > 2:
            ov_before = sub.recall_overlap(sub.hopfield_weights(before, N), before)
        trial = np.vstack([before, cand])
        W = sub.hopfield_weights(trial, N)
        keep = sub.recallable(W, trial)
        stored = trial[keep]
        if before.shape[0] > 2 and stored.shape[0] > 2:
            surviving = keep[:before.shape[0]]
            if surviving.sum() > 2:
                ov_after = sub.recall_overlap(sub.hopfield_weights(stored, N),
                                              stored)[:surviving.sum()]
                old = ov_before[surviving]
                interf.append(float(np.mean(np.abs(ov_after - old) /
                                            np.maximum(np.abs(old), 1e-9))))
        if stored.shape[0] > 2 and t % 3 == 0:
            ov = sub.recall_overlap(sub.hopfield_weights(stored, N), stored)
            frac.append(t / 1000.0)
            margin.append(max(0.0, float((ov.min() - THRESH) / (1.0 - THRESH))))
    return frac, margin, interf


def rbn_history(rep, K=3):
    """
    Interference here is zero by construction and that is the point. Adding a
    node to a Boolean network leaves every existing node's inputs and truth
    table untouched, so no element already present is degraded by the arrival.
    Species and memories have no such luxury: both are drawing on something
    finite that the newcomer also draws on.
    """
    rng = np.random.default_rng(SEED + rep)
    h = sub.rbn_accretion(400, K, rng, record_every=5)
    if not h["s"]:
        return [], [], []
    n = len(h["s"])
    frac = [i / n for i in range(n)]
    margin = [abs(1.0 - v) for v in h["s"]]
    return frac, margin, [0.0]


def sweep():
    """
    The test for self-organisation is whether the endpoint is independent of the
    parameter you started from. A system that self-organises to its critical
    point arrives there whatever it was built like. A system that merely sits
    where its parameters put it will show endpoints that track the parameter.

    Lotka-Volterra passed this in experiment 02: every interaction strength
    reached the same margin near 0.03 while reaching very different richness.
    """
    out = {}

    glv = []
    for sigma in (0.6, 0.9, 1.2, 1.5):
        ends = []
        for rep in range(2):
            rng = np.random.default_rng(SEED + rep*17 + int(sigma*100))
            A = assembly.interaction_pool(400, 0.5, sigma, rng)
            K = np.ones(400); resident = np.array([], dtype=int)
            order = rng.permutation(400); last = None
            for t in range(900):
                cand = int(order[t % 400])
                if cand in resident: continue
                N, surv = assembly.saturated_equilibrium(A, K, np.append(resident, cand))
                resident = surv
                if resident.size > 2:
                    lead, bulk = assembly.spectrum_shape(A, N, resident)
                    last = abs(lead / bulk)
            ends.append(last)
        glv.append({"param": sigma, "ends": ends, "mean": float(np.mean(ends))})
    out["lotka-volterra"] = {"param_name": "interaction spread sigma", "levels": glv}

    hop = []
    for N in (200, 400, 800):
        ends = []
        for rep in range(2):
            rng = np.random.default_rng(SEED + rep*23 + N)
            stored = np.zeros((0, N)); vals = []
            for t in range(3*N):
                cand = rng.choice([-1.0, 1.0], size=(1, N))
                trial = np.vstack([stored, cand])
                stored = trial[sub.recallable(sub.hopfield_weights(trial, N), trial)]
                if t > 2.4*N and t % 10 == 0 and stored.shape[0] > 2:
                    ov = sub.recall_overlap(sub.hopfield_weights(stored, N), stored)
                    vals.append(max(0.0, (ov.min() - 0.9) / 0.1))
            ends.append(float(np.mean(vals)) if vals else float("nan"))
        hop.append({"param": N, "ends": ends, "mean": float(np.mean(ends))})
    out["hopfield"] = {"param_name": "network size N", "levels": hop}

    rbn = []
    for K in (2, 3, 4):
        ends = []
        for rep in range(3):
            h = sub.rbn_accretion(400, K, np.random.default_rng(SEED + rep*29 + K),
                                  record_every=5)
            ends.append(abs(1.0 - h["s"][-1]) if h["s"] else float("nan"))
        rbn.append({"param": K, "ends": ends, "mean": float(np.mean(ends))})
    out["boolean network"] = {"param_name": "inputs per node K", "levels": rbn}
    return out


if __name__ == "__main__":
    t0 = time.time()
    out = {"substrates": {}}
    for name, fn in (("lotka-volterra", glv_history),
                     ("hopfield", hopfield_history),
                     ("boolean network", rbn_history)):
        runs = [fn(r) for r in range(REPS)]
        grid = np.linspace(0.05, 1.0, 20)
        curves = []
        for frac, margin, _ in runs:
            if len(frac) > 3:
                curves.append(np.interp(grid, frac, margin))
        curve = np.mean(curves, axis=0) if curves else np.full_like(grid, np.nan)
        # Per-replicate endpoints as well as the mean curve: averaging the mean
        # curve alone hid how much the Boolean endpoint varies between runs,
        # which is the whole finding for that substrate.
        ends = [float(c[-1]) for c in curves]
        interf = np.concatenate([np.array(r[2]) for r in runs if len(r[2])])
        out["substrates"][name] = {
            "progress": grid.tolist(),
            "margin": curve.tolist(),
            "start": float(curve[0]), "end": float(curve[-1]),
            "ends": ends, "end_spread": float(np.ptp(ends)) if ends else float("nan"),
            "interference": float(np.median(interf)) if interf.size else float("nan"),
        }
        print(f"{name:>16}  margin {curve[0]:.3f} -> {curve[-1]:.3f}   "
              f"per-run endpoints {[round(e,3) for e in ends]}   "
              f"interference {out['substrates'][name]['interference']:.4f}")
    print()
    print("Is the endpoint independent of the parameter, or does it track it?")
    sw = sweep()
    out["sweep"] = sw
    for name, d in sw.items():
        means = [lv["mean"] for lv in d["levels"]]
        spread = float(np.nanmax(means) - np.nanmin(means))
        d["endpoint_spread"] = spread
        print(f"  {name:>16}  ({d['param_name']})")
        for lv in d["levels"]:
            print(f"      {lv['param']:>6}  endpoint margin {lv['mean']:.3f}   "
                  f"runs {[round(e,3) for e in lv['ends']]}")
        print(f"      spread across parameters: {spread:.3f}  "
              f"{'CONVERGES' if spread < 0.06 else 'TRACKS THE PARAMETER'}")
    json.dump(out, open("results/k_substrates.json", "w"))
    print(f"\ndone in {time.time()-t0:.0f}s")
