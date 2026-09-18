# Does modularity move May's bound?

**At a fixed link budget, compartmentalizing a random community does not make it
more likely to be stable. It drifts slightly the other way.** What compartments do
instead is cap the size of a failure: near the stability boundary, the worst single
perturbation moves 91% of an integrated community and 24% of a fully
compartmentalized one, which is exactly the share of the community inside one
compartment.

![Main result](figures/fig2_main.png)

## Why this matters

The Maintenance Thesis predicts that at equal complexity, modular systems outlast
integrated ones (P4). That prediction is false if "outlast" means local stability,
and the experiment below says so. It is true, and sharply so, if "outlast" means
bounded damage. P4 needs restating in those terms before it is worth testing on
anything harder.

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

### 2. P4 as written is false

Same sweep, `S = 100`, four compartments, link budget fixed:

| modularity `q` | transition |
|---|---|
| 0.00 | 1.045 |
| 0.50 | 1.040 |
| 0.90 | 1.000 |
| 1.00 | 0.972 |

Modularity buys no stability, and full compartmentalization is marginally worse.
The reason is visible in the spectra: packing the same links into smaller blocks
raises within-block density by exactly enough to cancel the size reduction, so the
eigenvalue disk has the same radius. Taking the worst of four blocks then costs a
little. ([figure](figures/fig3_spectra.png))

### 3. Containment is where modularity pays, and it is all-or-nothing

Worst-case share of the community moved by a sustained press on one species, at
`sigma*sqrt(SC) = 0.95`:

| modularity `q` | worst-case spread |
|---|---|
| 0.00 | 0.910 |
| 0.50 | 0.910 |
| 0.90 | 0.913 |
| 0.99 | 0.686 |
| 1.00 | 0.242 |

The compartment ceiling is 0.242, and `q = 1.00` sits exactly on it: damage cannot
leave the compartment it started in, because `-A^-1` is block diagonal.

The surprise is `q = 0.99`. Ninety-nine percent of the walls are sealed, roughly
15 links remain out of 1500, and the worst perturbation still reaches 69% of the
community. Partial compartmentalization is not partial containment. The barrier has
to be complete.

## Limits

Worth being explicit, because each of these is a way the result could be wrong or
too narrow:

- **Local stability only.** This is linear stability at a fixed point, not
  persistence under nonlinear dynamics. Stouffer and Bascompte (2011) measured
  persistence in dynamical food-web models, which is a harder and different
  question. This result does not contradict them. It shows that the local-stability
  route does not reproduce their conclusion, so whatever drives it is dynamical.
- **No sign structure.** `A_ij` and `A_ji` are independent, so the matrix contains
  no predator-prey pairs. Allesina and Tang (2012) showed sign structure moves the
  bound substantially. Adding it is the obvious next experiment and may well change
  the answer to question 2.
- **Uniform self-regulation.** Every species gets the same `d`. Heterogeneous
  self-regulation is known to matter.
- **One size.** Experiments 2 and 3 use `S = 100`, `m = 4` only.

## Next

1. Repeat experiment 2 with predator-prey sign structure (Allesina & Tang 2012).
2. Sweep compartment count `m` and compartment size, to see whether the ceiling
   trades against anything.
3. Locate the containment threshold in experiment 3 properly. It sits somewhere
   between `q = 0.99` and `q = 1.00`, which suggests a percolation threshold in the
   between-compartment graph rather than a smooth effect.

## Running it

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python run.py       # ~3 min, writes results/*.json
.venv/bin/python figures.py   # redraws figures/ from saved results
```

`may.py` is the model and the measures. `run.py` is the experiments. `figures.py`
only draws.

## References

Allesina, S. & Tang, S. (2012). Stability criteria for complex ecosystems. *Nature* 483, 205-208.
Bender, E. A., Case, T. J. & Gilpin, M. E. (1984). Perturbation experiments in community ecology. *Ecology* 65, 1-13.
May, R. M. (1972). Will a large complex system be stable? *Nature* 238, 413-414.
McCann, K. S. (2000). The diversity-stability debate. *Nature* 405, 228-233.
Stouffer, D. B. & Bascompte, J. (2011). Compartmentalization increases food-web persistence. *PNAS* 108, 3648-3652.
