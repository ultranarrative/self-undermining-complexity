# Self-undermining complexity

Does complexity generate its own fragility? This is the working repository for that
question: models, experiments, negative results and corrections, kept in one place so
the reasoning stays auditable.

## The thesis

In systems whose complexity is sustained by finite throughput, the growth of complexity
tends to undermine the processes that sustain it.

One candidate formalization, the Maintenance Thesis, stipulates three ingredients:
the benefit of complexity levels off, maintenance cost grows faster than linearly, and
coupling between components rises with complexity. Together these give a threshold `C*`
past which net returns turn negative and large failures become more likely, with
modularity as the escape clause.

**Experiment 02 suggests that formalization is over-specified.** A model with none of
those three ingredients, and no maintenance cost at all, still drives itself to marginal
stability. The mechanism appears to be simpler and more general than the thesis proposes.

## Status of each prediction

| Claim | Status | Where |
|---|---|---|
| P1. Maintenance cost grows superlinearly, so marginal returns fall past `C*` | **Untested.** No model here has a maintenance cost in it yet | |
| P2. Variance and autocorrelation rise before collapse | **Untested** | |
| P3. Large failures become more common as coupling rises | **Supported.** Largest cascade per arrival grows with richness at every interaction strength | [02](experiments/02-assembly/) |
| P4. At equal complexity, modular systems outlast integrated ones | **False as stated**, and already known false analytically | [01](experiments/01-random-matrix/) |
| Complexification drives a system to its own stability boundary | **Supported.** Scale-free distance falls from 0.84 to 0.03 during assembly | [02](experiments/02-assembly/) |
| Modularity caps failure size | **Supported**, at roughly `1/m`, but the cap is graded and degrades toward criticality | [01](experiments/01-random-matrix/) |
| Assembly raises the propagation scale | **Not supported.** Reach rises with complexity as a size effect; a matched random draw has the same reach | [02](experiments/02-assembly/) |

## The claim the two experiments make together

Neither experiment establishes this on its own, and it is the most interesting thing
here, so it is stated as an open hypothesis rather than a result:

> **Modularity's protection fails precisely at the state that assembly selects for.**
> Experiment 01 shows that containment, modularity's only real benefit, weakens as a
> system approaches criticality. Experiment 02 shows that a system which grows its own
> complexity ends up at criticality without being put there. If both hold in one model,
> then walls stop working exactly where complexification lands.

The two halves currently use different models, a random community matrix and generalized
Lotka-Volterra, so their eigenvalue scales are not comparable and this is a qualitative
convergence rather than a computed result. **The experiment that would settle it is
assembly into compartments:** run the grown model with block structure and measure
whether containment still holds at the endpoint the community picks for itself. That is
experiment 03.

## Experiments

| | Question | Answer |
|---|---|---|
| [**01. Drawn**](experiments/01-random-matrix/) | Does compartmentalization move May's stability bound? | No, and it was already known. It caps damage instead, gradedly |
| [**02. Grown**](experiments/02-assembly/) | Does a community that grows its own complexity walk to the edge? | Yes, and with no help |
| **03. Grown into compartments** | Does containment survive at the endpoint assembly picks? | Not yet run |

Each experiment directory is self-contained: its own README stating what it asked and
what it found, its own scripts, saved results and figures.

## Layout

```
src/suc/          models and shared measures, imported by every experiment
  may.py          random community matrix, stability, press perturbation
  assembly.py     generalized Lotka-Volterra assembly
  figstyle.py     shared figure style
experiments/      one directory per experiment, self-contained
site/             the password-gated lab note built from experiment 01
```

## Running it

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Then run any experiment from its own directory. Scripts put `src/` on the path
themselves, so nothing needs installing:

```bash
cd experiments/02-assembly && ../../.venv/bin/python run_assembly.py
```

## House rules for this repository

- **Every result gets a control before it gets believed.** Both headline measures in
  experiment 02 have one: a scale-free reading so shrinking abundances cannot fake the
  walk to the edge, and a matched random draw so community size cannot fake reach. The
  second control killed a result I wanted.
- **Negative results stay in**, with the same prominence as positive ones.
- **Corrections are commits, not edits.** Experiment 01's containment claim was wrong in
  the first version and the history says so.
- **Check the literature before claiming novelty.** Result 2 of experiment 01 turned out
  to be a numerical instance of a theorem proved in 2016.

## References

Allesina, S. & Tang, S. (2012). Stability criteria for complex ecosystems. *Nature* 483, 205-208.
Bender, E. A., Case, T. J. & Gilpin, M. E. (1984). Perturbation experiments in community ecology. *Ecology* 65, 1-13.
Biroli, G., Bunin, G. & Cammarota, C. (2018). Marginally stable equilibria in critical ecosystems. *New J. Phys.* 20, 083051.
Bunin, G. (2017). Ecological communities with Lotka-Volterra dynamics. *Phys. Rev. E* 95, 042414.
Grilli, J., Rogers, T. & Allesina, S. (2016). Modularity and stability in ecological communities. *Nat. Commun.* 7, 12031.
May, R. M. (1972). Will a large complex system be stable? *Nature* 238, 413-414.
McCann, K. S. (2000). The diversity-stability debate. *Nature* 405, 228-233.
Stouffer, D. B. & Bascompte, J. (2011). Compartmentalization increases food-web persistence. *PNAS* 108, 3648-3652.
