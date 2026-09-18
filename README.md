# Self-undermining complexity

Does complexity generate its own fragility? This is the working repository for that
question: models, experiments, negative results and corrections, kept in one place so
the reasoning stays auditable.

## The thesis

> Is the universe not merely capable of producing its own destruction, but structurally
> predisposed to do so by the very process through which complexity emerges?

That question is the motivation. It is not what gets tested here, and it does not need
to be, because it rests on a mechanistic claim that does get tested:

> **Do independent processes of complexification repeatedly produce a state in which the
> system's capacity to absorb perturbation approaches zero?**

Note the care in the wording. "Complexity generates its own fragility" sounds causal and
claims more than the measurements support. What the models actually show is that
complexification *drives systems toward marginal stability*, which may happen through
interaction density, coupling, dimensionality, correlated response or something else
again. Which of those is the invariant is precisely what experiment 04 is for.

The relationship between the two is a necessary condition, and it needs stating carefully.
If complexification does not generically produce its own fragility, then **the cosmological
argument from complexification fails.** Not the cosmological thesis outright: someone could
propose a different mechanism by which the universe is predisposed to undermine itself, and
nothing here would touch it. What dies is this argument for it, which is the one worth
defending because it is the one that can be tested. If complexification does produce
fragility, generically and across substrates, the argument is live and what remains is a
question about scope rather than about mechanism.

So this repository is the science the thesis stands on. Three things have to hold.

**The mechanism has to be endogenous.** Fragility must come from the process that builds
complexity, not from wear, shock or exhaustion arriving afterwards. True in one model
class, shown by [experiment 02](experiments/02-assembly/) and established before that by
Biroli, Bunin and Cammarota (2018). Reproduced here, not discovered here.

**It has to be generic.** One model class is an existence proof, not a structural claim.
Here, **"structurally" means the effect recurs across independent substrates rather than
being peculiar to one physical implementation.**
[Experiment 04](experiments/04-substrates/) tested this and the word is **partly earned**.
Associative memories share no mathematics with Lotka-Volterra and converge to criticality
anyway, so the phenomenon is not an artefact of ecology. But Boolean networks do not
converge, so accretion alone is not sufficient. What separates them is interference,
whether a new element degrades the elements already present, and that yields a sharper
claim than universality would have:

> **Accretion drives a system to its own critical point when new elements degrade
> existing ones, and not otherwise.**

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
cause is absent from the model.

Stated at the strength the evidence supports: **thermodynamic exhaustion is not necessary
for an endogenous, complexity-driven approach to instability.** That is narrower than
"therefore complexity destroys itself" and far more defensible, and it is enough to deny
the common-cause objection its claim to be the whole explanation.

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
candidate replacement, which experiment 04 would test:

> Maintenance costs are **sufficient but not necessary** for self-undermining
> complexification.

That is good news for the thesis and bad news for this formalization of it.

## Status of each prediction

| Claim | Status | Where |
|---|---|---|
| P1. Maintenance cost grows superlinearly, so marginal returns fall past `C*` | **Untested.** No model here has a maintenance cost in it yet | |
| P2. Variance and autocorrelation rise before collapse | **Untested** | |
| P3. Large failures become more common as coupling rises | **Supported.** Largest cascade per arrival grows with richness at every interaction strength | [02](experiments/02-assembly/) |
| P4. At equal complexity, modular systems outlast integrated ones | **False as stated**, and already known false analytically | [01](experiments/01-random-matrix/) |
| Complexification drives a system to its own stability boundary | **Supported.** Scale-free distance falls from 0.84 to 0.03 during assembly | [02](experiments/02-assembly/) |
| Modularity caps failure size | **Supported**, at roughly `1/m`, but the cap is graded and degrades toward criticality | [01](experiments/01-random-matrix/) |
| Modularity's protection fails at the state assembly selects | **Supported.** Tested directly in one model. Only complete separation holds, and a uniform background coupling undoes even that | [03](experiments/03-compartmental-assembly/) |
| Compartments slow the approach to criticality | **False.** Every level of compartmentalization reaches the same marginal state | [03](experiments/03-compartmental-assembly/) |
| Assembly raises the propagation scale | **Not supported.** Reach rises with complexity as a size effect; a matched random draw has the same reach | [02](experiments/02-assembly/) |
| The mechanism is not peculiar to ecology | **Supported.** Hopfield networks share no mathematics with Lotka-Volterra and converge to criticality anyway | [04](experiments/04-substrates/) |
| Accretion alone drives any system to criticality | **False.** Boolean networks do not converge; their endpoint tracks `K` | [04](experiments/04-substrates/) |
| Interference is what separates the substrates that converge from those that do not | **Supported by one contrast**, not established. Degradation per arrival: 0.0282, 0.0074, and exactly 0 | [04](experiments/04-substrates/) |

## The claim the two experiments make together

Neither experiment establishes this on its own, and it is the most interesting thing
here, so it is stated as an open hypothesis rather than a result:

> **Modularity's protection fails precisely at the state that assembly selects for.**

Stated as an open hypothesis before [experiment 03](experiments/03-compartmental-assembly/)
ran, because experiments 01 and 02 used different models and could only converge on it
qualitatively. Experiment 03 tested it directly in a single model and it held, with a
strengthening that was not predicted: complete separation of the fluctuating interactions
is not sufficient either. A uniform background coupling of 0.00125 per pair, with all of
the interaction variance moved inside the compartments, still breaks containment at
criticality. Walls have to stop everything.

Compartments also turn out not to slow the approach to criticality at all. Every level of
modularity reaches the same marginal state.

## Experiments

| | Question | Answer |
|---|---|---|
| [**01. Drawn**](experiments/01-random-matrix/) | Does compartmentalization move May's stability bound? | No, and it was already known. It caps damage instead, gradedly |
| [**02. Grown**](experiments/02-assembly/) | Does a community that grows its own complexity walk to the edge? | Yes, and with no help |
| [**03. Grown into compartments**](experiments/03-compartmental-assembly/) | Does containment survive at the endpoint assembly picks? | No. Walls do not slow criticality, and only complete separation contains damage there |
| [**04. Other substrates**](experiments/04-substrates/) | Does self-driven criticality appear in systems with no ecology in them? | In two of three. The one that fails shows what the necessary ingredient is |

### Where the programme has got to

The defensible claim is narrower than the thesis wanted and more useful than the thesis
had:

> Complexification drives systems to marginality **wherever complexity is built from
> elements that compete for something finite.** Where arrival is free, it does not.

That is a cross-domain statement formal enough to fail, which is what the original working
note said nobody had produced. Failing it is specific: find a substrate with interference
that does not converge, or one without interference that does.

What it does not reach, and no experiment here can, is whether the universe is such a
system.

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
