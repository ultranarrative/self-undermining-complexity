"""
May's stability-complexity bound, and a test of whether modularity moves it.

May, R. M. (1972). Will a large complex system be stable? Nature 238, 413-414.

The model is May's original: a community matrix A of S species with -d on the
diagonal (self-regulation), off-diagonal entries nonzero with probability C
(connectance) and drawn from N(0, sigma^2). A_ij and A_ji are drawn
independently. The system is locally stable iff every eigenvalue of A has
negative real part, which happens iff sigma * sqrt(S * C) < d.

The extension here adds compartments while holding the link budget fixed, so
that "modular" and "integrated" systems are compared at equal complexity.
"""
from __future__ import annotations

import numpy as np


def block_sizes(S: int, m: int) -> np.ndarray:
    """Split S species into m compartments as evenly as possible."""
    base, extra = divmod(S, m)
    return np.array([base + (1 if i < extra else 0) for i in range(m)])


def within_fraction(S: int, m: int) -> float:
    """Fraction of off-diagonal cells that fall inside a compartment."""
    n = block_sizes(S, m)
    return float((n * (n - 1)).sum() / (S * (S - 1)))


def connectance_split(C: float, S: int, m: int, q: float) -> tuple[float, float]:
    """
    Within- and between-compartment connectance at modularity q, holding the
    expected number of links fixed at C * S * (S - 1).

    q = 0  ->  C_in = C_out = C, which is May's original random community
    q = 1  ->  C_out = 0, a fully compartmentalized community

    Holding the budget fixed is what makes this a test of P4 rather than a
    test of "fewer links are more stable", which May already answers.
    """
    if m == 1:
        return C, C
    p_in = within_fraction(S, m)
    C_out = C * (1.0 - q)
    C_in = (C - (1.0 - p_in) * C_out) / p_in
    if C_in > 1.0:
        raise ValueError(
            f"C_in = {C_in:.3f} exceeds 1: a budget of C = {C} does not fit into "
            f"{m} compartments at q = {q}. Lower C or lower m."
        )
    return C_in, C_out


def community_matrix(
    S: int,
    C: float,
    sigma: float,
    rng: np.random.Generator,
    m: int = 1,
    q: float = 0.0,
    d: float = 1.0,
) -> np.ndarray:
    """One draw of a community matrix with m compartments at modularity q."""
    C_in, C_out = connectance_split(C, S, m, q)
    labels = np.repeat(np.arange(m), block_sizes(S, m))
    same = labels[:, None] == labels[None, :]
    P = np.where(same, C_in, C_out)
    A = rng.normal(0.0, sigma, size=(S, S)) * (rng.random((S, S)) < P)
    np.fill_diagonal(A, -d)
    return A


def leading_real_part(A: np.ndarray) -> float:
    """Largest real part across the spectrum. Negative means locally stable."""
    return float(np.linalg.eigvals(A).real.max())


def stability_probability(
    S: int,
    C: float,
    sigma: float,
    replicates: int,
    rng: np.random.Generator,
    m: int = 1,
    q: float = 0.0,
    d: float = 1.0,
) -> tuple[float, float]:
    """Fraction of draws that are locally stable, and the mean leading real part."""
    leading = np.array(
        [
            leading_real_part(community_matrix(S, C, sigma, rng, m=m, q=q, d=d))
            for _ in range(replicates)
        ]
    )
    return float((leading < 0).mean()), float(leading.mean())


def crossing(x: np.ndarray, y: np.ndarray, level: float = 0.5) -> float:
    """Linear interpolation of where a monotone-ish curve y(x) crosses `level`."""
    above = np.where(y >= level)[0]
    below = np.where(y < level)[0]
    if above.size == 0 or below.size == 0:
        return float("nan")
    i = above[-1]
    if i + 1 >= x.size:
        return float("nan")
    x0, x1, y0, y1 = x[i], x[i + 1], y[i], y[i + 1]
    if y0 == y1:
        return float(x0)
    return float(x0 + (level - y0) * (x1 - x0) / (y1 - y0))


def net_effects(A: np.ndarray) -> np.ndarray:
    """
    Press-perturbation net effects, -A^-1.

    Bender, Case & Gilpin (1984). Column k is the long-run change in every
    species when species k is held under sustained pressure.
    """
    return -np.linalg.inv(A)


def damage_spread(A: np.ndarray, threshold: float = 0.1) -> float:
    """
    Fraction of the community measurably moved by a sustained press on one
    species, averaged over which species is pressed.

    A species counts as affected if its response is at least `threshold` times
    the response of the species being pressed. This measures how far damage
    travels, which is a different question from whether the system is stable.
    """
    N = np.abs(net_effects(A))
    S = A.shape[0]
    relative = N / np.diag(N)[None, :]
    affected = (relative > threshold).sum(axis=0) - 1
    return float((affected / (S - 1)).mean())


def damage_spread_profile(A: np.ndarray, threshold: float = 0.1) -> np.ndarray:
    """
    Per-source version of `damage_spread`: entry k is the fraction of the rest
    of the community measurably moved by a sustained press on species k.

    Keeping the profile rather than its mean lets the worst source be reported,
    which is the quantity that matters for containment.
    """
    N = np.abs(net_effects(A))
    S = A.shape[0]
    relative = N / np.diag(N)[None, :]
    return ((relative > threshold).sum(axis=0) - 1) / (S - 1)
