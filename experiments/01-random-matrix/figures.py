"""Figures for experiment 01, the drawn random community matrix. Run from this directory."""
from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import matplotlib.pyplot as plt
import numpy as np

from suc.figstyle import (SURFACE, INK, INK_2, MUTED, GRID,
                          RAMP_5, RAMP_4, RAMP_3, dress, load)


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


if __name__ == "__main__":
    fig_may(); fig_main(); fig_spectra(); fig_correction(); fig_extreme_value()
    print("wrote figures/fig1..fig5")
