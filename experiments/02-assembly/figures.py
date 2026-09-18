"""Figures for experiment 02, grown communities. Run from this directory."""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import matplotlib.pyplot as plt
import numpy as np

from suc.figstyle import (SURFACE, INK, INK_2, MUTED, GRID,
                          RAMP_5, RAMP_4, RAMP_3, dress, load)


def fig_assembly():
    """Does a community that grows its own complexity walk to the edge?"""
    h = load("h_assembly")
    sigmas = [f"{s:.1f}" for s in h["sigmas"]]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 4.3))

    def series(d, key):
        x = np.array(d["richness"]); y = np.array(d[key])
        ok = ~np.isnan(x)
        return x[ok], y[ok]

    # 1. Scale-free distance to the boundary against the complexity it grew.
    for colour, s in zip(RAMP_4, sigmas):
        x, y = series(h["data"][s], "ratio")
        ax1.plot(x, y, color=colour, linewidth=2, marker="o", markersize=5,
                 markerfacecolor=colour, markeredgecolor=SURFACE, markeredgewidth=1.4,
                 label=f"$\\sigma$ = {s}", zorder=3)
    ax1.set_yscale("log")
    ax1.legend(loc="lower left", fontsize=8.5, labelcolor=INK_2,
               title="interaction spread", title_fontsize=8.5)
    dress(ax1, "species richness", "leading Re / bulk Re",
          "Assembly walks a community to its own edge",
          "Scale-free, so shrinking abundances cannot fake it")

    # 2. The size of the largest extinction cascade.
    for colour, s in zip(RAMP_4, sigmas):
        x, y = series(h["data"][s], "aval_max")
        ax2.plot(x, y, color=colour, linewidth=2, marker="o", markersize=5,
                 markerfacecolor=colour, markeredgecolor=SURFACE, markeredgewidth=1.4,
                 label=f"$\\sigma$ = {s}", zorder=3)
    ax2.legend(loc="upper left", fontsize=8.5, labelcolor=INK_2,
               title="interaction spread", title_fontsize=8.5)
    dress(ax2, "species richness", "largest cascade from one arrival",
          "And the largest failures grow with it",
          "Species lost when a single new arrival is admitted")

    # 3. Reach rises, but assembly is not what raises it.
    for colour, s in zip(RAMP_4, sigmas):
        x, y = series(h["data"][s], "spread")
        _, yn = series(h["data"][s], "null")
        ax3.plot(x, y, color=colour, linewidth=2, label=f"$\\sigma$ = {s}", zorder=3)
        ax3.plot(x, yn, color=colour, linewidth=1.6, linestyle=(0, (2, 2.5)), zorder=2)
    ax3.set_ylim(0, 1.0)
    ax3.legend(loc="upper left", fontsize=8.5, labelcolor=INK_2,
               title="solid assembled, dashed drawn", title_fontsize=8.5)
    dress(ax3, "species richness", "worst-case share of community moved",
          "Reach rises, but assembly does not cause it",
          "Dashed: the same number of species drawn at random from the same pool")

    fig.tight_layout()
    fig.savefig("figures/fig6_assembly.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_assembly()
    print("wrote figures/fig6_assembly.png")
