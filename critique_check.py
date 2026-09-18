"""Test the three empirical claims in the critique against the model."""
import json
import numpy as np
import may

SEED = 20260918
C, M, S = 0.2, 4, 100
GRID = np.linspace(0.5, 1.5, 41)
sig_for = lambda t, s=S, c=C: t / np.sqrt(s * c)

print("=" * 72)
print("CLAIM 1: the q=1 worsening is an extreme-value effect, P_m4 = (p_block)^4")
print("=" * 72)
C_in, _ = may.connectance_split(C, S, M, 1.0)
n_b = may.block_sizes(S, M)[0]
print(f"block size {n_b}, within-block connectance {C_in:.4f}")
reps = 400
p_block, p_m4 = [], []
for t in GRID:
    rng = np.random.default_rng(SEED + 991 + int(t * 100))
    pb, _ = may.stability_probability(n_b, C_in, sig_for(t), reps, rng)
    rng2 = np.random.default_rng(SEED + 5150 + int(t * 100))
    pm, _ = may.stability_probability(S, C, sig_for(t), reps, rng2, m=M, q=1.0)
    p_block.append(pb); p_m4.append(pm)
p_block, p_m4 = np.array(p_block), np.array(p_m4)
pred = p_block ** 4
print(f"  transition, single block          : {may.crossing(GRID, p_block):.3f}")
print(f"  transition, (single block)^4       : {may.crossing(GRID, pred):.3f}")
print(f"  transition, measured m=4 q=1       : {may.crossing(GRID, p_m4):.3f}")
print(f"  max |measured - (p_block)^4|       : {np.abs(p_m4 - pred).max():.3f}")
print(f"  mean |measured - (p_block)^4|      : {np.abs(p_m4 - pred).mean():.3f}")
json.dump({"grid": GRID.tolist(), "p_block": p_block.tolist(),
           "p_pred": pred.tolist(), "p_m4": p_m4.tolist()},
          open("results/d_extreme_value.json", "w"))

print()
print("=" * 72)
print("CLAIM 2: 'all-or-nothing' is threshold-dependent; q=0.99 leaves the")
print("         ceiling as criticality is approached")
print("=" * 72)
targets = np.linspace(0.30, 0.95, 14)
thresholds = [0.01, 0.05, 0.10, 0.30]
ceiling = (n_b - 1) / (S - 1)
print(f"compartment ceiling = {ceiling:.3f}")
out2 = {"targets": targets.tolist(), "ceiling": float(ceiling),
        "thresholds": thresholds, "levels": {}}
for q in (0.99, 1.0):
    rows = {f"{th:.2f}": [] for th in thresholds}
    for t in targets:
        rng = np.random.default_rng(SEED + 4242 + int(q * 1000) + int(t * 100))
        acc = {f"{th:.2f}": [] for th in thresholds}
        for _ in range(120):
            A = may.community_matrix(S, C, sig_for(t), rng, m=M, q=float(q))
            if may.leading_real_part(A) >= 0:
                continue
            N = np.abs(may.net_effects(A))
            rel = N / np.diag(N)[None, :]
            for th in thresholds:
                prof = ((rel > th).sum(axis=0) - 1) / (S - 1)
                acc[f"{th:.2f}"].append(prof.max())
        for th in thresholds:
            rows[f"{th:.2f}"].append(float(np.mean(acc[f"{th:.2f}"])))
    out2["levels"][f"{q:.2f}"] = rows
    print(f"\n  q = {q:.2f}  worst-case spread by detection threshold")
    print(f"    {'sqrt(SC)':>9} " + "".join(f"{('th='+format(th,'.2f')):>10}" for th in thresholds))
    for i, t in enumerate(targets):
        print(f"    {t:>9.2f} " + "".join(f"{rows[f'{th:.2f}'][i]:>10.3f}" for th in thresholds))
json.dump(out2, open("results/e_threshold.json", "w"))

print()
print("=" * 72)
print("CLAIM 3: stable-draw conditioning differs across q; compare at matched")
print("         distance to the boundary instead")
print("=" * 72)
pairs = {}
for q in (0.0, 0.5, 0.99, 1.0):
    lead, spread = [], []
    for t in np.linspace(0.30, 1.05, 26):
        rng = np.random.default_rng(SEED + 8080 + int(q * 1000) + int(t * 100))
        for _ in range(90):
            A = may.community_matrix(S, C, sig_for(t), rng, m=M, q=float(q))
            lr = may.leading_real_part(A)
            if lr >= 0:
                continue
            lead.append(lr)
            spread.append(may.damage_spread_profile(A).max())
    pairs[f"{q:.2f}"] = {"lead": lead, "spread": spread}
    print(f"  q={q:.2f}  {len(lead)} stable draws, leading Re from {min(lead):.3f} to {max(lead):.3f}")

edges = np.array([-0.60, -0.40, -0.25, -0.15, -0.09, -0.05, -0.02, 0.0])
print(f"\n  worst-case spread at MATCHED distance to the boundary")
hdr = "  " + "".join(f"{f'[{edges[i]:.2f},{edges[i+1]:.2f})':>16}" for i in range(len(edges)-1))
print(f"  {'q':>5}" + hdr)
binned = {}
for q in ("0.00", "0.50", "0.99", "1.00"):
    lead = np.array(pairs[q]["lead"]); spread = np.array(pairs[q]["spread"])
    row = []
    for i in range(len(edges) - 1):
        sel = (lead >= edges[i]) & (lead < edges[i + 1])
        row.append(float(spread[sel].mean()) if sel.sum() >= 12 else float("nan"))
    binned[q] = row
    print(f"  {q:>5}" + "".join(f"{v:>16.3f}" if v == v else f"{'-':>16}" for v in row))
json.dump({"edges": edges.tolist(), "binned": binned}, open("results/f_matched.json", "w"))
