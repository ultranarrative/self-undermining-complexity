"""Figures for experiment 03. Run from this directory."""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import matplotlib.pyplot as plt
import numpy as np

from suc.figstyle import SURFACE, INK, INK_2, MUTED, RAMP_5, dress, load

QC = {"0.00": RAMP_5[0], "0.50": RAMP_5[1], "0.90": RAMP_5[3], "1.00": RAMP_5[4]}


def fig_compartmental():
    a, b = load("i_compartmental"), load("j_meancoupled")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # Left: compartments do not stop the walk to criticality.
    for q, colour in QC.items():
        d = a["by_richness"][q]
        x, y = np.array(d["richness"]), np.array(d["ratio"])
        ok = ~np.isnan(x)
        ax1.plot(x[ok], y[ok], color=colour, linewidth=2, marker="o", markersize=5,
                 markerfacecolor=colour, markeredgecolor=SURFACE, markeredgewidth=1.4,
                 label=f"q = {q}", zorder=3)
    ax1.set_yscale("log")
    ax1.legend(loc="lower left", fontsize=8.5, labelcolor=INK_2, title="modularity",
               title_fontsize=8.5)
    dress(ax1, "species richness", "leading Re / bulk Re",
          "Walls do not stop the walk to the edge",
          "Every level of compartmentalization reaches the same marginal state")

    # Right: does containment hold there? Spread as a multiple of its own ceiling.
    ax2.axhline(1.0, color=MUTED, linewidth=1.3, linestyle=(0, (4, 3)), zorder=1)
    ax2.text(0.62, 0.86, "containment holds below this line", color=MUTED,
             fontsize=8.5, va="top")
    for src, style, width in ((a, "-", 2.0), (b, (0, (2, 2.5)), 1.7)):
        for q, colour in QC.items():
            d = src["by_margin"][q]
            x = np.array(d["ratio"]); y = np.array(d["spread"]) / np.array(d["ceiling"])
            ok = ~np.isnan(x)
            ax2.plot(x[ok], y[ok], color=colour, linewidth=width, linestyle=style,
                     zorder=3 if style == "-" else 2,
                     label=f"q = {q}" if style == "-" else None)
    ax2.set_xscale("log")
    ax2.invert_xaxis()
    ax2.set_ylim(0, 2.1)
    # Explicit ticks: the default log locator stacks minor labels on top of each
    # other on an inverted axis and the result is unreadable.
    ticks = [0.6, 0.3, 0.15, 0.08, 0.05, 0.02]
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([f"{t:g}" for t in ticks])
    ax2.xaxis.set_minor_locator(plt.NullLocator())
    ax2.xaxis.set_minor_formatter(plt.NullFormatter())
    ax2.legend(loc="upper left", fontsize=8.5, labelcolor=INK_2,
               title="solid: walls complete   dashed: mean coupling survives",
               title_fontsize=8.5)
    ax2.annotate("criticality", (a["by_margin"]["0.00"]["ratio"][-1], 0.08),
                 xytext=(8, 0), textcoords="offset points", color=MUTED,
                 fontsize=8.5, ha="left")
    dress(ax2, "leading Re / bulk Re  (approaching criticality to the right)",
          "worst-case spread  /  compartment ceiling",
          "And containment fails exactly where assembly lands",
          "Only complete separation holds, and a uniform background coupling undoes it")

    fig.tight_layout()
    fig.savefig("figures/fig7_compartmental.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_compartmental()
    print("wrote figures/fig7_compartmental.png")
