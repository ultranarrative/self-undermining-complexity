"""
Shared figure style.

Ordinal blue ramps rather than categorical hues, because every series in this
repository is ordered (system size, modularity, interaction spread) and a value
ramp is the right encoding for an ordered quantity. Validated for monotone
lightness, single hue and light-end contrast against the surface.
"""
from __future__ import annotations

import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e8e7e3"

RAMP_5 = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
RAMP_4 = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
RAMP_3 = ["#86b6ef", "#2a78d6", "#0d366b"]

RC = {
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "text.color": INK,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "font.size": 9,
    "axes.titlesize": 10,
    "legend.frameon": False,
    "figure.dpi": 200,
}
plt.rcParams.update(RC)


def dress(ax, xlabel=None, ylabel=None, title=None, subtitle=None):
    """Recessive grid, no top or right spine, left-aligned title and standfirst."""
    ax.grid(True, color=GRID, linewidth=0.8, linestyle="-")
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, loc="left", color=INK, fontweight="bold",
                     pad=14 if subtitle else 8)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, color=INK_2,
                fontsize=8.5, va="bottom")


def load(name, base="results"):
    """Load a saved result set. Experiment scripts run from their own directory."""
    with open(f"{base}/{name}.json") as fh:
        return json.load(fh)
