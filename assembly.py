"""
Community assembly under generalized Lotka-Volterra dynamics.

    dN_i/dt = N_i * (K_i - sum_j A_ij N_j),   A_ii = 1

Species arrive one at a time from a fixed pool. After each arrival the community
is re-solved to its saturated equilibrium and whatever cannot hold a positive
abundance is dropped. Nothing tunes the system toward the stability boundary, so
if it ends up there it got there on its own.

This is the piece the random-matrix experiments could not supply: here complexity
is grown rather than drawn, which is what the Maintenance Thesis is actually about.

Bunin (2017) Phys. Rev. E 95, 042414; Biroli, Bunin & Cammarota (2018) NJP 20, 083051.
"""
from __future__ import annotations

import numpy as np


def interaction_pool(S_pool: int, mu: float, sigma: float,
                     rng: np.random.Generator) -> np.ndarray:
    """Random competitive interaction matrix, self-limitation normalised to 1."""
    A = rng.normal(mu/S_pool, sigma/np.sqrt(S_pool), size=(S_pool, S_pool))
    np.fill_diagonal(A, 1.0)
    return A


def saturated_equilibrium(A: np.ndarray, K: np.ndarray,
                          idx: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Equilibrium of the sub-community `idx`, dropping species that cannot hold a
    positive abundance. Returns (abundances, surviving indices).

    This is the standard removal algorithm: solve, drop the most negative, repeat.
    """
    idx = np.asarray(idx, dtype=int)
    while idx.size:
        sub = A[np.ix_(idx, idx)]
        try:
            N = np.linalg.solve(sub, K[idx])
        except np.linalg.LinAlgError:
            idx = idx[:-1]
            continue
        if (N > 1e-12).all():
            return N, idx
        idx = np.delete(idx, int(np.argmin(N)))
    return np.array([]), idx


def leading_eigenvalue(A: np.ndarray, N: np.ndarray, idx: np.ndarray) -> float:
    """
    Largest real part of the Jacobian at equilibrium.

    J = -diag(N) * A_sub, so the sign structure of A and the standing abundances
    together set how close the community sits to losing stability.
    """
    if idx.size == 0:
        return float("nan")
    J = -np.diag(N) @ A[np.ix_(idx, idx)]
    return float(np.linalg.eigvals(J).real.max())


def press_spread(A: np.ndarray, idx: np.ndarray, threshold: float = 0.1) -> float:
    """
    Worst-case share of the community moved by a sustained press on one species.

    A press on species k shifts its carrying capacity, so the response is column k
    of A_sub^-1. This is the same measure used in the random-matrix experiments,
    and it is an operational reading of the propagation scale.
    """
    n = idx.size
    if n < 2:
        return 0.0
    try:
        inv = np.abs(np.linalg.inv(A[np.ix_(idx, idx)]))
    except np.linalg.LinAlgError:
        return float("nan")
    rel = inv / np.diag(inv)[None, :]
    per_source = ((rel > threshold).sum(axis=0) - 1) / (n - 1)
    return float(per_source.max())


def assemble(S_pool: int, mu: float, sigma: float, steps: int,
             rng: np.random.Generator, record_every: int = 1) -> dict:
    """Run one assembly history and record what happens to it."""
    A = interaction_pool(S_pool, mu, sigma, rng)
    K = np.ones(S_pool)
    resident = np.array([], dtype=int)
    order = rng.permutation(S_pool)

    hist = {"step": [], "richness": [], "leading": [], "spread": [],
            "avalanche": [], "invaded": [], "total_abundance": []}

    for t in range(steps):
        cand = int(order[t % S_pool])
        if cand in resident:
            continue
        trial = np.append(resident, cand)
        N, survivors = saturated_equilibrium(A, K, trial)
        lost = np.setdiff1d(resident, survivors).size
        invaded = cand in survivors
        resident = survivors

        if t % record_every == 0 and resident.size:
            hist["step"].append(t)
            hist["richness"].append(int(resident.size))
            hist["leading"].append(leading_eigenvalue(A, N, resident))
            hist["spread"].append(press_spread(A, resident))
            hist["avalanche"].append(int(lost))
            hist["invaded"].append(bool(invaded))
            hist["total_abundance"].append(float(N.sum()))
    return hist


def spectrum_shape(A: np.ndarray, N: np.ndarray, idx: np.ndarray) -> tuple[float, float]:
    """
    (leading real part, mean real part) of the Jacobian.

    The ratio of these two is the scale-free reading. J = -diag(N) A_sub, so if
    abundances shrink as the community fills up, every eigenvalue shrinks with
    them and the leading one drifts toward zero for reasons that have nothing to
    do with stability. Dividing by the bulk removes that.
    """
    if idx.size == 0:
        return float("nan"), float("nan")
    J = -np.diag(N) @ A[np.ix_(idx, idx)]
    re = np.linalg.eigvals(J).real
    return float(re.max()), float(re.mean())


def drawn_null(A: np.ndarray, k: int, rng: np.random.Generator,
               threshold: float = 0.1) -> float:
    """
    Press spread for k species taken at random from the same pool, with no
    assembly filtering. The control for "is spread just tracking richness?"
    """
    if k < 2:
        return 0.0
    idx = rng.choice(A.shape[0], size=k, replace=False)
    return press_spread(A, idx, threshold)
