"""Two controls on the assembly result, before it gets believed."""
import numpy as np, assembly

SEED, POOL, MU, SIGMA, STEPS = 20260918, 500, 0.5, 1.2, 2000
rng = np.random.default_rng(SEED)
A = assembly.interaction_pool(POOL, MU, SIGMA, rng)
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
    if resident.size < 2:
        continue
    lead, bulk = assembly.spectrum_shape(A, N, resident)
    rows.append((resident.size, lead, bulk, N.sum(), N.mean(),
                 assembly.press_spread(A, resident),
                 assembly.drawn_null(A, resident.size, rng)))

r = np.array(rows)
rich, lead, bulk, tot, mean_N, spread, null = r.T

print("CONTROL A: is the walk to the edge just abundances shrinking?")
print(f"{'richness':>10} {'lead Re':>9} {'bulk Re':>9} {'lead/bulk':>10} "
      f"{'total N':>9} {'mean N':>8}")
for lo, hi in [(2,20),(20,40),(40,60),(60,80),(80,100),(100,140),(140,200),(200,320)]:
    s = (rich >= lo) & (rich < hi)
    if s.sum() > 5:
        print(f"{f'{lo}-{hi}':>10} {lead[s].mean():>9.4f} {bulk[s].mean():>9.4f} "
              f"{(lead[s]/bulk[s]).mean():>10.4f} {tot[s].mean():>9.2f} {mean_N[s].mean():>8.4f}")

print()
print("CONTROL B: is spread just tracking community size?")
print(f"{'richness':>10} {'assembled':>11} {'drawn null':>11} {'difference':>11}")
for lo, hi in [(2,20),(20,40),(40,60),(60,80),(80,100),(100,140),(140,200),(200,320)]:
    s = (rich >= lo) & (rich < hi)
    if s.sum() > 5:
        print(f"{f'{lo}-{hi}':>10} {spread[s].mean():>11.3f} {null[s].mean():>11.3f} "
              f"{spread[s].mean()-null[s].mean():>+11.3f}")

np.save("results/g_controls.npy", r)
