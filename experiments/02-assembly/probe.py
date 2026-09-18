import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
import numpy as np
from suc import assembly
print("larger pool, so the ceiling is set by the dynamics and not by supply")
print(f"{'sigma':>6} {'pool':>6} {'rich':>6} {'lead Re':>10} {'spread':>8} {'aval/step':>10} {'max aval':>9}")
for sigma in (0.6, 0.9, 1.2, 1.5, 1.8):
    rng = np.random.default_rng(11)
    h = assembly.assemble(500, 0.5, sigma, 2000, rng)
    tail = slice(-200, None)
    print(f"{sigma:>6.1f} {500:>6} {np.mean(h['richness'][tail]):>6.1f} "
          f"{np.mean(h['leading'][tail]):>10.4f} {np.mean(h['spread'][tail]):>8.3f} "
          f"{np.mean(h['avalanche'][tail]):>10.2f} {max(h['avalanche']):>9}")

print()
print("trajectory within one history at sigma = 1.2: does it walk to the edge?")
rng = np.random.default_rng(11)
h = assembly.assemble(500, 0.5, 1.2, 2000, rng)
r = np.array(h["richness"]); l = np.array(h["leading"]); s = np.array(h["spread"])
for lo, hi in [(1, 20), (20, 40), (40, 60), (60, 80), (80, 100), (100, 130), (130, 500)]:
    sel = (r >= lo) & (r < hi)
    if sel.sum() > 5:
        print(f"  richness {lo:>3}-{hi:<3}  n={sel.sum():>4}  "
              f"lead Re {l[sel].mean():>8.4f}   spread {s[sel].mean():>6.3f}")
