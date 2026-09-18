"""
Two substrates that share no mechanism with Lotka-Volterra, for testing whether
accretion under a viability filter drives a system to its own critical point.

The design rule throughout: **the filter must never be a stability filter.** In
the ecological model the filter is "a species that cannot hold a positive
abundance is dropped", which is about feasibility, and marginal stability then
emerges. A substrate whose filter said "stay stable" would assume the conclusion.
So here the filters are about function: a memory that can no longer be recalled
is dropped, a node that has stopped computing anything is dropped. Neither filter
knows where its substrate's critical point is.

Each substrate reports a normalised distance to that critical point, so the three
can be compared on one axis:

    margin = (x_c - x) / x_c

which is 1 far from criticality and 0 at it.
"""
from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------
# Substrate A: Hopfield associative memory
# --------------------------------------------------------------------------
# Spin glass, discrete states, no dynamics in continuous time and no interaction
# matrix whose eigenvalues decide anything. The critical point is the storage
# capacity alpha_c = 0.138, derived by replica theory and known independently of
# anything measured here.

ALPHA_C = 0.138


def hopfield_weights(patterns: np.ndarray, N: int) -> np.ndarray:
    """Hebbian weights from the stored set, self-connections removed."""
    if patterns.shape[0] == 0:
        return np.zeros((N, N))
    W = (patterns.T @ patterns) / N
    np.fill_diagonal(W, 0.0)
    return W


def recall_overlap(W: np.ndarray, patterns: np.ndarray, steps: int = 4) -> np.ndarray:
    """How well each stored pattern still recalls itself, in [-1, 1]."""
    if patterns.shape[0] == 0:
        return np.zeros(0)
    S = patterns.copy()
    for _ in range(steps):
        nxt = np.sign(S @ W.T)
        nxt[nxt == 0] = 1
        if np.array_equal(nxt, S):
            break
        S = nxt
    return (S * patterns).mean(axis=1)


def recallable(W: np.ndarray, patterns: np.ndarray, steps: int = 4,
               overlap_min: float = 0.9) -> np.ndarray:
    """
    Which stored patterns can still be recalled.

    Start the network at each pattern, let it run, and keep the pattern if the
    state it settles into still overlaps the original. This asks whether the
    memory works, not whether the network is stable.
    """
    if patterns.shape[0] == 0:
        return np.zeros(0, dtype=bool)
    S = patterns.copy()
    for _ in range(steps):
        nxt = np.sign(S @ W.T)
        nxt[nxt == 0] = 1
        if np.array_equal(nxt, S):
            break
        S = nxt
    overlap = (S * patterns).mean(axis=1)
    return overlap > overlap_min


def hopfield_accretion(N: int, steps: int, rng: np.random.Generator,
                       record_every: int = 2) -> dict:
    """Propose random memories one at a time, keep the ones that still recall."""
    stored = np.zeros((0, N))
    thresh = 0.9
    hist = {"step": [], "count": [], "alpha": [], "margin": [], "dropped": [],
            "overlap": []}
    for t in range(steps):
        cand = rng.choice([-1.0, 1.0], size=(1, N))
        trial = np.vstack([stored, cand])
        keep = recallable(hopfield_weights(trial, N), trial)
        dropped = int(trial.shape[0] - keep.sum())
        stored = trial[keep]
        if t % record_every == 0 and stored.shape[0]:
            alpha = stored.shape[0] / N
            ov = float(recall_overlap(hopfield_weights(stored, N), stored).mean())
            hist["step"].append(t)
            hist["count"].append(int(stored.shape[0]))
            hist["alpha"].append(float(alpha))
            hist["overlap"].append(ov)
            # How much recall quality is left above the point where a memory
            # stops counting as recalled. 1 = perfect, 0 = every memory is
            # barely holding on, which is this substrate's marginal state.
            hist["margin"].append(float((ov - thresh) / (1.0 - thresh)))
            hist["dropped"].append(dropped)
    return hist


# --------------------------------------------------------------------------
# Substrate B: random Boolean network
# --------------------------------------------------------------------------
# Discrete time, Boolean state, no abundances and no energy function. The order
# parameter is the average sensitivity s, which is below 1 in the ordered regime
# and above 1 in the chaotic one. Criticality is s = 1, a result about Boolean
# dynamics that owes nothing to the two substrates above.

def node_sensitivity(table: np.ndarray, K: int) -> float:
    """
    Summed influence of a node's inputs: how often flipping one input flips the
    output, averaged over input states and summed over inputs.
    """
    if K == 0:
        return 0.0
    idx = np.arange(1 << K)
    total = 0.0
    for j in range(K):
        total += float((table[idx] != table[idx ^ (1 << j)]).mean())
    return total


def rbn_accretion(steps: int, K: int, rng: np.random.Generator, n_init: int = 8,
                  T: int = 24, record_every: int = 2, cap: int = 240) -> dict:
    """
    Nodes arrive with K random inputs and a random Boolean function. A node that
    has stopped changing state is doing no computation and is removed, which
    costs its downstream neighbours an input and so lowers their sensitivity.
    Nothing in this rule refers to s = 1.
    """
    inputs: list[np.ndarray] = []
    tables: list[np.ndarray] = []
    hist = {"step": [], "n": [], "s": [], "margin": [], "dropped": []}

    for t in range(steps):
        n = len(inputs)
        if n < K + 1:                       # seed the network
            inputs.append(rng.integers(0, max(n, 1), size=min(K, max(n, 1))))
            tables.append(rng.integers(0, 2, size=1 << len(inputs[-1])))
            continue
        if n < cap:
            src = rng.choice(n, size=K, replace=False)
            inputs.append(src)
            tables.append(rng.integers(0, 2, size=1 << K))

        n = len(inputs)
        changed = np.zeros(n, dtype=bool)
        for _ in range(n_init):             # who is doing any computation?
            state = rng.integers(0, 2, size=n)
            seen = np.zeros(n, dtype=bool)
            first = state.copy()
            for step in range(T):
                nxt = np.empty(n, dtype=np.int64)
                for i in range(n):
                    src = inputs[i]
                    code = 0
                    for b, j in enumerate(src):
                        code |= int(state[j]) << b
                    nxt[i] = tables[i][code]
                if step > T // 3:
                    seen |= (nxt != first)
                state = nxt
            changed |= seen

        keep = np.where(changed)[0]
        dropped = n - keep.size
        if keep.size >= K + 1 and dropped:
            remap = -np.ones(n, dtype=int)
            remap[keep] = np.arange(keep.size)
            new_inputs, new_tables = [], []
            for i in keep:
                src, tab = inputs[i], tables[i]
                alive = [b for b, j in enumerate(src) if remap[j] >= 0]
                if len(alive) == len(src):
                    new_inputs.append(remap[src]); new_tables.append(tab)
                    continue
                # marginalise the lost inputs by fixing them to a random value,
                # which is what losing an upstream node actually does
                fixed = {b: int(rng.integers(0, 2)) for b in range(len(src))
                         if b not in alive}
                Kn = len(alive)
                tab2 = np.empty(1 << Kn, dtype=tables[i].dtype)
                for code in range(1 << Kn):
                    full = 0
                    for pos, b in enumerate(alive):
                        full |= ((code >> pos) & 1) << b
                    for b, v in fixed.items():
                        full |= v << b
                    tab2[code] = tab[full]
                new_inputs.append(remap[np.array(src)[alive]] if Kn else np.array([], int))
                new_tables.append(tab2)
            inputs, tables = new_inputs, new_tables

        if t % record_every == 0 and len(inputs) > K:
            s = float(np.mean([node_sensitivity(tables[i], len(inputs[i]))
                               for i in range(len(inputs))]))
            hist["step"].append(t)
            hist["n"].append(len(inputs))
            hist["s"].append(s)
            hist["margin"].append(float((1.0 - s) / 1.0))
            hist["dropped"].append(int(dropped))
    return hist
