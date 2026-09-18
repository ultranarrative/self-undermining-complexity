"""
Assembly with a maintenance cost, for testing P1 and P2.

No model elsewhere in this repository has a maintenance cost in it, which is why
P1 has stood untested. The Maintenance Thesis says that cost is what produces a
threshold C* past which returns turn negative and the system comes apart.
Experiment 02 already showed the cost is not needed to reach marginal stability.
What is still open is whether it is what turns sitting at the edge into going
over it, because those are different outcomes and only the second is collapse.

Two ways for cost to scale, and they behave very differently:

  "per-capita"  every species pays a share that grows with richness, so
                K_eff = K0 - m * S^(beta-1). Negative feedback, self-limiting.

  "legacy"      the cost is of infrastructure already built, and it has to be
                carried by whoever is left, so K_eff = K0 - m * S_peak^beta / S.
                Losing a species raises the burden on the survivors. This is
                Tainter's mechanism and the only one of the two that can run away.

One thing has to be right or the whole model is inert. The Lotka-Volterra
equilibrium solves A N = K, so scaling K uniformly rescales every abundance and
leaves the composition exactly unchanged: feasibility is scale-invariant, and a
maintenance cost expressed as a reduction in K changes nothing at all. The first
version of this file did that and produced identical richness at every cost and
every exponent, which is how the error announced itself.

The cost bites only once something breaks that invariance. Here it is a minimum
viable abundance: a species holding less than N_min cannot persist. Lowering K
scales everyone down, the smallest cross the floor first, and in the legacy mode
their loss raises the burden on whoever is left.
"""
from __future__ import annotations

import numpy as np

from . import assembly


def effective_K(mode: str, S: int, S_peak: int, m: float, beta: float,
                K0: float = 1.0) -> float:
    if S < 1:
        return K0
    if mode == "per-capita":
        return K0 - m * S**(beta - 1.0)
    if mode == "legacy":
        return K0 - m * (S_peak**beta) / max(S, 1)
    raise ValueError(mode)


def assemble_with_cost(S_pool: int, mu: float, sigma: float, m: float, beta: float,
                       mode: str, steps: int, rng: np.random.Generator,
                       N_min: float = 0.2, margin_every: int = 5) -> dict:
    """
    Assembly where the carrying capacity every species sees is reduced by the
    community's own maintenance burden. Arrivals are random, as everywhere else,
    so any threshold has to come from the cost rather than from the schedule.
    """
    A = assembly.interaction_pool(S_pool, mu, sigma, rng)
    resident = np.array([], dtype=int)
    order = rng.permutation(S_pool)
    S_peak = 0
    h = {"step": [], "richness": [], "total": [], "K_eff": [], "margin": [],
         "collapsed": False, "collapse_step": None, "peak": 0}

    for t in range(steps):
        cand = int(order[t % S_pool])
        if cand not in resident:
            trial = np.append(resident, cand)
        else:
            trial = resident
        S_guess = max(trial.size, 1)
        K_eff = effective_K(mode, S_guess, S_peak, m, beta)
        if K_eff <= 0:                       # the burden exceeds what is available
            h["collapsed"] = True
            h["collapse_step"] = t
            resident = np.array([], dtype=int)
            h["step"].append(t); h["richness"].append(0); h["total"].append(0.0)
            h["K_eff"].append(float(K_eff)); h["margin"].append(float("nan"))
            break

        N, surv = assembly.saturated_equilibrium(A, np.full(S_pool, K_eff), trial)
        # Minimum viable abundance. Without this the cost cannot bite: the
        # equilibrium is scale-invariant in K, so composition would never change.
        if N.size:
            viable = N >= N_min
            if not viable.all():
                surv = surv[viable]
                N, surv = assembly.saturated_equilibrium(
                    A, np.full(S_pool, K_eff), surv)
        resident = surv
        S_peak = max(S_peak, resident.size)

        if resident.size >= 2 and t % margin_every == 0:
            lead, bulk = assembly.spectrum_shape(A, N, resident)
            margin = abs(lead / bulk)
        else:
            margin = float("nan")

        h["step"].append(t)
        h["richness"].append(int(resident.size))
        h["total"].append(float(N.sum()) if N.size else 0.0)
        h["K_eff"].append(float(K_eff))
        h["margin"].append(float(margin))

        if resident.size == 0 and t > 10:
            h["collapsed"] = True
            h["collapse_step"] = t
            break

    h["peak"] = int(max(h["richness"])) if h["richness"] else 0
    return h


def early_warnings(series: np.ndarray, window: int = 40) -> tuple[np.ndarray, np.ndarray]:
    """
    Rolling variance and lag-1 autocorrelation, the two standard early-warning
    signals (Scheffer et al. 2009). Autocorrelation rising toward 1 is critical
    slowing down: the system takes longer and longer to recover from a nudge.
    """
    n = series.size
    var = np.full(n, np.nan)
    ar1 = np.full(n, np.nan)
    t = np.arange(window)
    for i in range(window, n):
        w = series[i-window:i].astype(float)
        # Detrend linearly inside the window. Subtracting the mean alone leaves
        # the trend in, which inflates variance and autocorrelation on any
        # series that is going somewhere, collapse or not.
        if np.ptp(w) > 0:
            w = w - np.polyval(np.polyfit(t, w, 1), t)
        var[i] = w.var()
        if w.size > 2 and w.var() > 1e-12:
            ar1[i] = float(np.corrcoef(w[:-1], w[1:])[0, 1])
    return var, ar1


def trend(x: np.ndarray) -> float:
    """Kendall tau of a series against time, the usual way these are scored."""
    ok = ~np.isnan(x)
    if ok.sum() < 10:
        return float("nan")
    y = x[ok]; t = np.arange(y.size)
    yr = np.argsort(np.argsort(y)); tr = np.argsort(np.argsort(t))
    return float(np.corrcoef(yr, tr)[0, 1])
