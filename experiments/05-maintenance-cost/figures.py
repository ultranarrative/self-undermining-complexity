"""Figures for experiment 05. Run from this directory."""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import matplotlib.pyplot as plt
import numpy as np

from suc.figstyle import SURFACE, INK, INK_2, MUTED, RAMP_3, CAT_3, dress, load


def fig_maintenance():
    g = load("l_maintenance")["grid"]
    p2 = load("m_p2_power")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    betas = [1.0, 1.2, 1.5]
    for colour, beta in zip(RAMP_3, betas):
        for mode, style in (("legacy", "-"), ("per-capita", (0, (2, 2.5)))):
            rows = [r for r in g if r["mode"] == mode and r["beta"] == beta]
            rows.sort(key=lambda r: r["m"])
            xs = [r["m"] for r in rows]; ys = [r["peak"] for r in rows]
            ax1.plot(xs, ys, color=colour, linewidth=2 if style == "-" else 1.7,
                     linestyle=style, zorder=3,
                     label=f"beta = {beta}" if mode == "legacy" else None)
            for r in rows:
                if r["collapse_rate"] > 0.5:
                    ax1.plot(r["m"], r["peak"], marker="X", markersize=11,
                             color=CAT_3[1], markeredgecolor=SURFACE,
                             markeredgewidth=1.5, zorder=5)
    ax1.plot([], [], marker="X", linestyle="none", color=CAT_3[1], markersize=9,
             label="collapsed")
    ax1.legend(loc="lower left", fontsize=8.5, labelcolor=INK_2,
               title="solid: legacy cost    dashed: per-capita", title_fontsize=8.5)
    ax1.set_ylim(0, 155)
    dress(ax1, "maintenance cost m", "peak complexity reached  (C*)",
          "P1: superlinear cost is not enough on its own",
          "Collapse needs beta = 1.5 and a cost the survivors carry. Otherwise it just shrinks")

    labels = ["variance\nbefore collapse", "variance\nno collapse",
              "autocorrelation\nbefore collapse", "autocorrelation\nno collapse"]
    vals = [p2["collapsing"]["rise_var"], p2["surviving"]["rise_var"],
            p2["collapsing"]["rise_ar1"], p2["surviving"]["rise_ar1"]]
    cols = [CAT_3[1], MUTED, CAT_3[1], MUTED]
    ax2.bar(labels, vals, color=cols, width=0.6, zorder=3)
    ax2.axhline(0.5, color=INK_2, linewidth=1.3, linestyle=(0, (4, 3)), zorder=4)
    ax2.text(3.42, 0.515, "chance", color=INK_2, fontsize=8.5, ha="right")
    for i, v in enumerate(vals):
        ax2.annotate(f"{v:.2f}", (i, v), xytext=(0, 5), textcoords="offset points",
                     ha="center", color=INK_2, fontsize=9)
    ax2.set_ylim(0, 0.72)
    ax2.tick_params(axis="x", labelsize=8)
    dress(ax2, None, "share of runs where the signal rises",
          "P2: neither signal tells collapse from survival",
          f"n = {p2['collapsing']['n']} collapsing, {p2['surviving']['n']} surviving, same detector on both")
    fig.tight_layout()
    fig.savefig("figures/fig9_maintenance.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_maintenance()
    print("wrote figures/fig9_maintenance.png")
