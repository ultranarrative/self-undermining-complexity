# 01. The drawn random community matrix

Does compartmentalization move May's stability bound, and what does it do instead?

**Headline: no, and this was already known.** At a fixed link budget, walls do not raise
the stability threshold. Grilli, Rogers and Allesina (2016) proved that analytically.
What compartments do instead is cap the reach of a failure, and that cap is graded and
weakens as the system approaches criticality.

![Main result](figures/fig2_main.png)

## The model

May's original community matrix. `S` species, `-d` on the diagonal, off-diagonal
entries nonzero with probability `C` and drawn from `N(0, sigma^2)`, with `A_ij`
and `A_ji` drawn independently. The system is locally stable iff every eigenvalue
has negative real part, which for large `S` happens iff `sigma*sqrt(SC) < d`.

The extension adds `m` compartments and a modularity knob `q`:

| `q` | within-compartment | between-compartment | links across walls |
|---|---|---|---|
| 0.00 | C | C | ~1500 |
| 0.50 | 2.1C | 0.5C | ~750 |
| 0.90 | 3.7C | 0.02C | ~150 |
| 0.99 | 4.1C | 0.002C | ~15 |
| 1.00 | 4.1C | 0 | 0 |

`q` redistributes links inward while holding the **expected total link count
constant**. That constraint is what makes this a test of structure rather than a
restatement of May's result that fewer links are more stable.

## Results

All numbers from seed `20260918`. `python run.py` reproduces them exactly.

### 1. The bound reproduces

Transition point (where P(stable) crosses 0.5) against system size, predicted at 1:

| S | transition |
|---|---|
| 50 | 1.092 |
| 100 | 1.036 |
| 200 | 1.026 |

Converging on 1 from above as finite-size effects shrink. ([figure](figures/fig1_may_bound.png))

### 2. Compartments do not move the threshold

Same sweep, `S = 100`, four compartments, link budget fixed:

| modularity `q` | transition |
|---|---|
| 0.00 | 1.045 |
| 0.50 | 1.040 |
| 0.90 | 1.000 |
| 1.00 | 0.972 |

**Superseded analytically.** Patil, Aguirre-Lopez and Bouchaud (2024) derive the boundary
of the eigenvalue spectrum, including the eigenvalues of extremal real part, for a block
ensemble considerably more general than the one simulated here. Stefano Allesina pointed
this out in correspondence. What follows is a numerical special case of a solved problem,
and is retained because it validates the instrument, not because it establishes anything.

This follows from the construction, and saying so is the honest framing. Packing the
same links into smaller blocks raises within-block density by exactly enough to cancel
the size reduction, so `sigma*sqrt(S_b C_w)` is invariant and the eigenvalue disk keeps
its radius. The spectra show it directly. ([figure](figures/fig3_spectra.png))

The shortfall at `q = 1` is not a separate finding. It is an extreme-value effect: four
independent blocks are all stable with probability `p^4`, so the aggregate curve crosses
0.5 where each block is at `p = 0.841`, which is earlier. Tested directly, a single block
of 25 species at the rescaled connectance, raised to the fourth power, predicts a
transition at 0.981 against a measured 0.978, with mean absolute error 0.009 across the
sweep. ([figure](figures/fig5_extreme_value.png))

### 3. Compartments cap the reach of a failure, and the cap is graded

Worst-case share of the community moved by a sustained press on one species, compared
at **matched distance to the stability boundary** rather than at matched
`sigma*sqrt(SC)`, because conditioning on stable draws is a stronger filter at high `q`
and would otherwise bias the comparison:

| leading Re(λ) | q = 0.00 | q = 0.50 | q = 0.99 | q = 1.00 |
|---|---|---|---|---|
| -0.50 | 0.211 | 0.198 | 0.157 | 0.156 |
| -0.20 | 0.718 | 0.701 | 0.312 | 0.229 |
| -0.07 | 0.943 | 0.940 | 0.581 | 0.240 |
| -0.01 | 0.991 | 0.992 | 0.813 | 0.242 |

Three things read off this. Far from the boundary, structure barely matters. Only
`q = 1` gives a hard cap, and it is exact rather than statistical, because `-A^-1` is
block diagonal and damage cannot leave the compartment it started in. And the
containment advantage of partial separation is real but **degrades as the system
approaches criticality**: `q = 0.99` holds damage to 31% at a comfortable margin and
loses it to 81% at the edge. ([figure](figures/fig4_correction.png))

An earlier version of this README claimed containment was all-or-nothing, on the basis
that `q = 0.99` tracked the compartment ceiling and then left it. That was an artefact
of the detection threshold. At a threshold of 0.01 rather than 0.10, `q = 0.99` sits
above the ceiling at every point in the sweep. The mechanism is gain, not connectivity:
one cross link makes the inverse dense, so influence always reaches everywhere, and what
changes near the boundary is magnitude, since `||A^-1||` diverges as the leading
eigenvalue approaches zero. There is no percolation threshold between `q = 0.99` and
`q = 1.00` to locate. The only structural discontinuity is at exactly zero cross links.

## Limits

- **Local stability only.** Linear stability at a fixed point, not persistence under
  nonlinear dynamics. Stouffer and Bascompte (2011) measured persistence in dynamical
  food-web models. This result does not contradict them. It shows the local-stability
  route does not reproduce their conclusion, so whatever drives it is dynamical.
- **No sign structure.** `A_ij` and `A_ji` are independent, so there are no
  predator-prey pairs. Allesina and Tang (2012) showed sign structure moves the bound
  substantially, and repeating result 2 with it may change the answer.
- **The spread measure carries a threshold.** "Moved" means a response at least 10% of
  the pressed species' own response. The absolute numbers depend on that choice, as
  section 3 shows. The ordering across `q` does not.
- **Uniform self-regulation, one size.** Every species gets the same `d`, and
  sections 2 and 3 use `S = 100`, `m = 4` only.
- **Nothing here complexifies.** The matrix is drawn, not grown, which is why
  [experiment 02](../02-assembly/) exists.

## Running it

```bash
python run.py             # sections 1 to 3, ~3 min, writes results/
python robustness_checks.py  # the three checks behind sections 2 and 3
python figures.py         # redraws figures/ from saved results
```
