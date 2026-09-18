# Self-undermining complexity

Does complexity generate its own fragility? This is the working repository for that
question: models, experiments, negative results and corrections, kept in one place so
the reasoning stays auditable.

## The thesis

> Is the universe not merely capable of producing its own destruction, but structurally
> predisposed to do so by the very process through which complexity emerges?

That question is the motivation. It is not what gets tested here, and it does not need
to be, because it rests on a mechanistic claim that does get tested:

> **Does complexification generically drive systems toward their own instability?**

The relationship between the two is a necessary condition. If complexity does not
generically produce its own fragility, the cosmological thesis is dead whatever else is
true, because its whole content is that the universe inherits this property from the
process that builds structure in it. If complexity does produce its own fragility,
generically and across substrates, then the thesis is live and what remains is a question
about scope and cosmology rather than about mechanism.

So this repository is the science the thesis stands on. Three things have to hold.

**The mechanism has to be endogenous.** Fragility must come from the process that builds
complexity, not from wear, shock or exhaustion arriving afterwards. True in one model
class, shown by [experiment 02](experiments/02-assembly/) and established before that by
Biroli, Bunin and Cammarota (2018). Reproduced here, not discovered here.

**It has to be generic.** One model class is an existence proof, not a structural claim.
The mechanism has to recur in systems that share no physics with each other, and it has
to beat a null of the same size in each. This is experiment 04 and it is the central
deliverable of the whole programme, not a caveat on it. The word "structurally" in the
thesis is exactly this word.

**It has to survive the observer.** *The Epistemic Filter* argues that evolved observers
over-detect purpose, and "predisposed" is a purpose word. Stories of order consuming
itself recur in every end-of-days tradition, which is what the filter predicts whether or
not the cosmos cooperates. The defence is built into the method rather than argued: these
are formal systems with no observers inside them, and the measures are scale-free or
tested against matched nulls, so a result cannot be a projection.

### The common-cause objection, and what experiment 02 does to it

The strongest objection to the thesis is thermodynamic: complexity and destruction may
share a cause, the low-entropy past, rather than one
causing the other. Structure formation and its undoing would then be siblings, not parent
and child.

Experiment 02 bears on this directly. Generalized Lotka-Volterra has no thermodynamic
gradient in it. Nothing is being spent, no free energy is running down, there is no
low-entropy past. Complexity still drives itself to the edge of stability. Whatever
produces the fragility there, it is not the shared thermodynamic cause, because that
cause is absent from the model. The mechanism looks structural, a property of how
interacting systems accumulate, rather than a thermodynamic accounting identity.

That is one model class, which is why experiment 04 exists. But it is the right kind of
evidence against the strongest objection the thesis faces, and it was not available
before.

### One candidate formalization

The Maintenance Thesis stipulates three ingredients: the benefit of complexity levels off,
maintenance cost grows faster than linearly, and coupling rises with complexity. Together
they give a threshold `C*` past which returns turn negative, with modularity as the escape
clause.

**Experiment 02 suggests it is over-specified.** A model with none of those three
ingredients, and no maintenance cost at all, still reaches marginal stability. The
mechanism appears simpler and more general than this formalization proposes, which is
good news for the thesis and bad news for the formalization.

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
| **04. Other substrates** | Does self-driven criticality appear in systems with no ecology in them? | Not yet run |

Experiment 04 is the one that decides whether "structurally" is earned. The assembly
result has to be reproduced in at least two model classes that share no mechanism with
Lotka-Volterra, and where a null of the same size does not reproduce it. If it recurs,
the claim is about complexification. If it does not, it is a fact about ecology.

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
