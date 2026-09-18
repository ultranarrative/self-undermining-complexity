"""Figures for experiment 04. Run from this directory."""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import matplotlib.pyplot as plt
import numpy as np

from suc.figstyle import SURFACE, INK, INK_2, MUTED, CAT_3, dress, load

ORDER = ["lotka-volterra", "hopfield", "boolean network"]
LABEL = {"lotka-volterra": "Lotka-Volterra", "hopfield": "Hopfield",
         "boolean network": "Boolean network"}


def fig_substrates():
    d = load("k_substrates")
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.3))

    # 1. Margin over the course of accretion.
    for colour, name in zip(CAT_3, ORDER):
        s = d["substrates"][name]
        ax1.plot(s["progress"], s["margin"], color=colour, linewidth=2,
                 label=LABEL[name], zorder=3)
    ax1.set_ylim(0, 0.45)
    ax1.legend(loc="upper right", fontsize=8.5, labelcolor=INK_2)
    dress(ax1, "progress through accretion", "normalised distance to critical point",
          "All three fall. That is not the test",
          "Each substrate measured against its own critical point")

    # 2. The test: is the endpoint independent of what you built the system from?
    for i, (colour, name) in enumerate(zip(CAT_3, ORDER)):
        sw = d["sweep"][name]
        xs = np.arange(len(sw["levels"])) * 0.16 + i
        ys = [lv["mean"] for lv in sw["levels"]]
        ax2.plot(xs, ys, color=colour, linewidth=1.8, marker="o", markersize=7,
                 markerfacecolor=colour, markeredgecolor=SURFACE,
                 markeredgewidth=1.6, zorder=3)
        for j, (x, y, lv) in enumerate(zip(xs, ys, sw["levels"])):
            # Label below a local minimum, above otherwise, so the text never
            # lands on its own marker.
            lo = (0 < j < len(ys)-1) and y < ys[j-1] and y < ys[j+1]
            ax2.annotate(f"{lv['param']:g}", (x, y), xytext=(0, -16 if lo else 9),
                         textcoords="offset points", ha="center",
                         color=INK_2, fontsize=8)
        ax2.text(xs.mean(), -0.035, LABEL[name], ha="center", color=colour,
                 fontsize=9, fontweight="bold")
        ax2.text(xs.mean(), -0.062, sw["param_name"], ha="center", color=MUTED,
                 fontsize=7.8)
    ax2.set_xticks([])
    ax2.set_ylim(-0.075, 0.36)
    ax2.axhline(0, color=MUTED, linewidth=1, zorder=1)
    dress(ax2, None, "endpoint distance to critical point",
          "The test: does the endpoint depend on the build?",
          "Flat and low is self-organisation. Hopfield falls with size; Boolean tracks K")

    # 3. The candidate explanation.
    names = [LABEL[n] for n in ORDER]
    vals = [d["substrates"][n]["interference"] for n in ORDER]
    ax3.bar(names, vals, color=CAT_3, width=0.55, zorder=3)
    for i, v in enumerate(vals):
        ax3.annotate(f"{v:.4f}", (i, v), xytext=(0, 5), textcoords="offset points",
                     ha="center", color=INK_2, fontsize=9)
    ax3.set_ylim(0, 0.036)
    dress(ax3, None, "degradation of existing elements per arrival",
          "And the ingredient that separates them",
          "Zero for Boolean networks by construction: a new node degrades nothing")
    fig.tight_layout()
    fig.savefig("figures/fig8_substrates.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_substrates()
    print("wrote figures/fig8_substrates.png")
