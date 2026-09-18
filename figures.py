"""Draw the figures from results/*.json. Re-run after run.py."""
from __future__ import annotations

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e8e7e3"

# Ordinal blue ramp (validated: monotone L, single hue, light end clears surface).
RAMP_5 = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]
RAMP_3 = ["#86b6ef", "#2a78d6", "#0d366b"]

plt.rcParams.update({
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
})


def dress(ax, xlabel=None, ylabel=None, title=None, subtitle=None):
    ax.grid(True, color=GRID, linewidth=0.8, linestyle="-")
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, loc="left", color=INK, fontweight="bold", pad=14 if subtitle else 8)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, color=INK_2,
                fontsize=8.5, va="bottom")


def load(name):
    return json.load(open(f"results/{name}.json"))


def fig_may():
    a = load("a_may")
    g = np.array(a["grid"])
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.axvline(1.0, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    ax.text(1.02, 0.97, "May's bound", color=MUTED, fontsize=8.5, va="top")
    for colour, S in zip(RAMP_3, ("50", "100", "200")):
        d = a["sizes"][S]
        ax.plot(g, d["p_stable"], color=colour, linewidth=2, label=f"S = {S}", zorder=3)
    # No direct labels here: all three curves converge on zero, so end-labels collide.
    ax.set_xlim(g[0], g[-1])
    ax.set_ylim(-0.03, 1.03)
    ax.legend(loc="lower left", fontsize=8.5, labelcolor=INK_2)
    dress(ax, r"$\sigma\sqrt{SC}$", "P(locally stable)",
          "The transition sharpens on May's bound as the system grows",
          f"Random community matrices, connectance C = {a['C']}, "
          f"{a['replicates']} draws per point")
    fig.tight_layout()
    fig.savefig("figures/fig1_may_bound.png", bbox_inches="tight")
    plt.close(fig)
    return a


def fig_main():
    b, c = load("b_modularity"), load("c_containment")
    g = np.array(b["grid"])
    t = np.array(c["targets"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # Left: P4 as written. The curves collapse.
    ax1.axvline(1.0, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    qs_b = ["0.00", "0.50", "0.90", "1.00"]
    for colour, q in zip([RAMP_5[0], RAMP_5[2], RAMP_5[3], RAMP_5[4]], qs_b):
        ax1.plot(g, b["levels"][q]["p_stable"], color=colour, linewidth=2,
                 label=f"q = {q}", zorder=3)
    ax1.set_xlim(g[0], g[-1])
    ax1.set_ylim(-0.03, 1.03)
    ax1.legend(loc="lower left", fontsize=8.5, labelcolor=INK_2, title="modularity",
               title_fontsize=8.5)
    dress(ax1, r"$\sigma\sqrt{SC}$", "P(locally stable)",
          "Modularity does not move the bound",
          f"S = {b['S']}, C = {b['C']}, {b['m']} compartments, link budget held fixed")

    # Inset: the transition point against modularity, which drifts the wrong way.
    ins = ax1.inset_axes([0.60, 0.56, 0.37, 0.34])
    xs = [float(q) for q in qs_b]
    ys = [b["levels"][q]["crossing"] for q in qs_b]
    ins.axhline(1.0, color=MUTED, linewidth=0.9, linestyle=(0, (3, 2.5)))
    ins.plot(xs, ys, color=RAMP_5[3], linewidth=1.6, marker="o", markersize=5,
             markerfacecolor=RAMP_5[3], markeredgecolor=SURFACE, markeredgewidth=1.4)
    ins.set_ylim(0.94, 1.08)
    ins.set_xlabel("q", fontsize=7.5, labelpad=1)
    ins.set_title("transition point", fontsize=7.5, color=INK_2, loc="left", pad=3)
    ins.tick_params(labelsize=7)
    for side in ("top", "right"):
        ins.spines[side].set_visible(False)
    ins.spines["left"].set_color(GRID)
    ins.spines["bottom"].set_color(GRID)
    ins.set_facecolor(SURFACE)

    # Right: what modularity actually does.
    ceiling = c["ceiling"]
    ax2.axhline(ceiling, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    ax2.text(t[0], ceiling + 0.022, "compartment ceiling", color=MUTED, fontsize=8.5)
    qs_c = ["0.00", "0.50", "0.90", "0.99", "1.00"]
    for colour, q in zip(RAMP_5, qs_c):
        ax2.plot(t, c["levels"][q]["worst"], color=colour, linewidth=2,
                 label=f"q = {q}", zorder=3)
    for q, colour, dy in (("1.00", RAMP_5[4], -11), ("0.99", RAMP_5[3], 0)):
        y = c["levels"][q]["worst"][-1]
        ax2.annotate(f"q = {q}", (t[-1], y), xytext=(6, dy), textcoords="offset points",
                     color=colour, fontsize=8.5, va="center", fontweight="bold")
    ax2.annotate("q $\\leq$ 0.90", (t[-1], c["levels"]["0.90"]["worst"][-1]),
                 xytext=(6, 0), textcoords="offset points", color=RAMP_5[2],
                 fontsize=8.5, va="center", fontweight="bold")
    ax2.set_xlim(t[0], t[-1] + 0.14)
    ax2.set_ylim(0, 1.0)
    ax2.legend(loc="upper left", fontsize=8.5, labelcolor=INK_2, title="modularity",
               title_fontsize=8.5)
    dress(ax2, r"$\sigma\sqrt{SC}$", "worst-case share of community moved",
          "It bounds how far one failure travels",
          "Sustained press on the worst single species, stable draws only")
    fig.tight_layout()
    fig.savefig("figures/fig2_main.png", bbox_inches="tight")
    plt.close(fig)
    return b, c


def fig_spectra():
    s = load("spectra")
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.3), sharey=True)
    titles = {"0.0": "Integrated  (q = 0)", "1.0": "Compartmentalized  (q = 1)"}
    for ax, q in zip(axes, ("0.0", "1.0")):
        ev = s["sets"][q]
        r = ev["radius"]
        circle = plt.Circle((-1, 0), r, fill=False, color=MUTED, linewidth=1.2,
                            linestyle=(0, (4, 3)), zorder=2)
        ax.add_patch(circle)
        ax.axvline(0, color=INK_2, linewidth=1.0, zorder=2)
        ax.scatter(ev["re"], ev["im"], s=22, color=RAMP_5[2], zorder=3,
                   edgecolors=SURFACE, linewidths=0.9)
        ax.set_aspect("equal")
        ax.set_xlim(-2.6, 0.9)
        ax.set_ylim(-1.6, 1.6)
        dress(ax, "Re", "Im" if q == "0.0" else None)
        ax.tick_params(left=(q == "0.0"))
        ax.set_title(titles[q], loc="left", color=INK, fontweight="bold", pad=6)
        unstable = sum(1 for x in ev["re"] if x > 0)
        word = "eigenvalue" if unstable == 1 else "eigenvalues"
        ax.text(0.04, 0.03, f"{unstable} {word} right of zero",
                transform=ax.transAxes, fontsize=8.5, color=INK_2)
    fig.suptitle("Why the bound does not move: the same disk, however you wire it",
                 x=0.045, ha="left", color=INK, fontweight="bold", fontsize=10)
    fig.text(0.045, 0.905, f"S = {s['S']}, C = {s['C']}, identical $\\sigma$, "
             f"drawn at $\\sigma\\sqrt{{SC}}$ = {s['target']}. Dashed circle is the "
             f"predicted radius.", ha="left", color=INK_2, fontsize=8.5)
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    fig.savefig("figures/fig3_spectra.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_may()
    fig_main()
    fig_spectra()
    print("wrote figures/fig1_may_bound.png, fig2_main.png, fig3_spectra.png")


def fig_correction():
    """The two checks that overturned the original 'all-or-nothing' reading."""
    e, f = load("e_threshold"), load("f_matched")
    t = np.array(e["targets"])
    ceiling = e["ceiling"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # Left: the ceiling agreement at q = 0.99 is an artefact of the threshold.
    ax1.axhline(ceiling, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    ax1.text(t[0], ceiling + 0.022, "compartment ceiling", color=MUTED, fontsize=8.5)
    ths = ["0.01", "0.05", "0.10", "0.30"]
    ramp = [RAMP_5[4], RAMP_5[3], RAMP_5[2], RAMP_5[0]]
    for colour, th in zip(ramp, ths):
        ax1.plot(t, e["levels"]["0.99"][th], color=colour, linewidth=2,
                 label=f"detect > {th}", zorder=3)
    ax1.set_xlim(t[0], t[-1])
    ax1.set_ylim(0, 1.0)
    ax1.legend(loc="upper left", fontsize=8.5, labelcolor=INK_2,
               title="threshold, q = 0.99", title_fontsize=8.5)
    dress(ax1, r"$\sigma\sqrt{SC}$", "worst-case share of community moved",
          "The ceiling agreement was an artefact",
          "At a finer detection threshold, q = 0.99 sits above the ceiling everywhere")

    # Right: compare at matched distance to the boundary, not matched sigma.
    edges = np.array(f["edges"])
    mids = (edges[:-1] + edges[1:]) / 2
    for colour, q in zip([RAMP_5[0], RAMP_5[1], RAMP_5[3], RAMP_5[4]],
                         ["0.00", "0.50", "0.99", "1.00"]):
        ax2.plot(mids, f["binned"][q], color=colour, linewidth=2,
                 marker="o", markersize=5, markerfacecolor=colour,
                 markeredgecolor=SURFACE, markeredgewidth=1.4,
                 label=f"q = {q}", zorder=3)
    ax2.axhline(ceiling, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    ax2.set_xlim(mids[0] - 0.03, 0.02)
    ax2.set_ylim(0, 1.05)
    ax2.legend(loc="upper left", fontsize=8.5, labelcolor=INK_2, title="modularity",
               title_fontsize=8.5)
    ax2.annotate("criticality", (0.0, 0.04), xytext=(-6, 0), textcoords="offset points",
                 color=MUTED, fontsize=8.5, ha="right")
    dress(ax2, r"leading Re($\lambda$), matched across q", "worst-case share of community moved",
          "Containment is graded, not all-or-nothing",
          "Same distance to the boundary for every q, so stability is not confounded")
    fig.tight_layout()
    fig.savefig("figures/fig4_correction.png", bbox_inches="tight")
    plt.close(fig)


def fig_extreme_value():
    d = load("d_extreme_value")
    g = np.array(d["grid"])
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.axvline(1.0, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    ax.plot(g, d["p_block"], color=RAMP_3[0], linewidth=2, label="one block, S = 25")
    ax.plot(g, d["p_pred"], color=RAMP_3[1], linewidth=2.6,
            label="(one block)$^4$, predicted")
    ax.plot(g, d["p_m4"], color=RAMP_3[2], linewidth=2, linestyle=(0, (2, 2)),
            label="measured, m = 4, q = 1")
    ax.set_xlim(g[0], g[-1])
    ax.set_ylim(-0.03, 1.03)
    ax.legend(loc="lower left", fontsize=8.5, labelcolor=INK_2)
    dress(ax, r"$\sigma\sqrt{SC}$", "P(locally stable)",
          "The q = 1 shortfall is an extreme-value effect",
          "Four blocks are all stable with probability $p^4$, so the curve moves left")
    fig.tight_layout()
    fig.savefig("figures/fig5_extreme_value.png", bbox_inches="tight")
    plt.close(fig)


RAMP_4 = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]


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
