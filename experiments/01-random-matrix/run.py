"""
Run the three experiments and write raw results to results/*.json.

  A. Reproduce May's bound: does the stability transition sit at sigma*sqrt(SC) = 1?
  B. Test P4 as written: at equal complexity, does compartmentalization move it?
  C. Ask the question P4 should have asked: does compartmentalization contain damage?

Every number this prints comes from SEED. Change nothing else and it reproduces.
"""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
import json
import time

import numpy as np

from suc import may

SEED = 20260918
C = 0.2          # connectance, held fixed everywhere
M = 4            # compartments in experiments B and C
GRID = np.linspace(0.5, 1.5, 41)   # values of sigma*sqrt(SC) to sweep


def sigma_for(target: float, S: int, c: float = C) -> float:
    """The sigma that puts this draw at a given value of May's quantity."""
    return target / np.sqrt(S * c)


def experiment_a(replicates: int = 150) -> dict:
    """May 1972, reproduced at three system sizes."""
    out = {"grid": GRID.tolist(), "C": C, "replicates": replicates, "sizes": {}}
    for S in (50, 100, 200):
        rng = np.random.default_rng(SEED + S)
        p, lead = zip(
            *[
                may.stability_probability(S, C, sigma_for(t, S), replicates, rng)
                for t in GRID
            ]
        )
        out["sizes"][str(S)] = {
            "p_stable": list(p),
            "leading": list(lead),
            "crossing": may.crossing(GRID, np.array(p)),
        }
        print(f"  A: S={S:>3}  transition at sigma*sqrt(SC) = {out['sizes'][str(S)]['crossing']:.3f}")
    return out


def experiment_b(S: int = 100, replicates: int = 200) -> dict:
    """P4 as written: modular versus integrated at an identical link budget."""
    levels = [0.0, 0.5, 0.9, 1.0]
    out = {"grid": GRID.tolist(), "S": S, "C": C, "m": M,
           "replicates": replicates, "levels": {}}
    for q in levels:
        rng = np.random.default_rng(SEED + int(q * 1000))
        p, lead = zip(
            *[
                may.stability_probability(S, C, sigma_for(t, S), replicates, rng, m=M, q=q)
                for t in GRID
            ]
        )
        cross = may.crossing(GRID, np.array(p))
        out["levels"][f"{q:.2f}"] = {"p_stable": list(p), "leading": list(lead),
                                     "crossing": cross}
        print(f"  B: q={q:.2f}  transition at sigma*sqrt(SC) = {cross:.3f}")
    return out


def experiment_c(S: int = 100, replicates: int = 150) -> dict:
    """
    Damage containment across the whole stable range.

    Experiment B shows modularity does not decide whether the system fails.
    This asks the other question: when a species is pressed, how much of the
    community moves with it? A fully compartmentalized community has a hard
    ceiling here, because -A^-1 is block diagonal and damage cannot leave the
    compartment it started in. That ceiling is (n - 1) / (S - 1).
    """
    targets = np.linspace(0.30, 0.95, 14)
    ceiling = (may.block_sizes(S, M)[0] - 1) / (S - 1)
    out = {"S": S, "C": C, "m": M, "replicates": replicates,
           "targets": targets.tolist(), "ceiling": float(ceiling), "levels": {}}
    for q in (0.0, 0.5, 0.9, 0.99, 1.0):
        mean_spread, worst_spread, kept = [], [], []
        for t in targets:
            rng = np.random.default_rng(SEED + 7777 + int(q * 1000) + int(t * 100))
            sigma = sigma_for(t, S)
            per_source = []
            for _ in range(replicates):
                A = may.community_matrix(S, C, sigma, rng, m=M, q=float(q))
                if may.leading_real_part(A) >= 0:
                    continue          # unstable draws have no press equilibrium
                per_source.append(may.damage_spread_profile(A))
            per_source = np.array(per_source)
            kept.append(len(per_source))
            mean_spread.append(float(per_source.mean()))
            worst_spread.append(float(per_source.max(axis=1).mean()))
        out["levels"][f"{q:.2f}"] = {"mean": mean_spread, "worst": worst_spread,
                                     "n_stable": kept}
        print(f"  C: q={q:.2f}  mean spread {mean_spread[0]:.3f} -> {mean_spread[-1]:.3f}"
              f"   worst-case {worst_spread[0]:.3f} -> {worst_spread[-1]:.3f}")
    print(f"  C: compartment ceiling = {ceiling:.3f}")
    return out


def spectra(S: int = 100, target: float = 1.15) -> dict:
    """Two spectra at identical S, C and sigma, drawn just past May's bound."""
    sigma = sigma_for(target, S)
    out = {"S": S, "C": C, "m": M, "sigma": sigma, "target": target, "sets": {}}
    for q in (0.0, 1.0):
        rng = np.random.default_rng(SEED + 31337)
        A = may.community_matrix(S, C, sigma, rng, m=M, q=q)
        ev = np.linalg.eigvals(A)
        out["sets"][f"{q:.1f}"] = {"re": ev.real.tolist(), "im": ev.imag.tolist(),
                                   "radius": target}
    return out


if __name__ == "__main__":
    t0 = time.time()
    print("Experiment A: reproducing May's bound")
    a = experiment_a()
    print("\nExperiment B: P4 as written, at equal complexity")
    b = experiment_b()
    print("\nExperiment C: damage containment")
    c = experiment_c()
    s = spectra()
    for name, payload in (("a_may", a), ("b_modularity", b), ("c_containment", c), ("spectra", s)):
        with open(f"results/{name}.json", "w") as fh:
            json.dump(payload, fh)
    print(f"\nDone in {time.time() - t0:.0f}s. Raw results in results/")
