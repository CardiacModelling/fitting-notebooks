
# Modelling patch-clamp experiments

When analysing data from whole-cell patch-clamp experiments, it can be useful to have a model of both the biological system of interest, and the experimental set up.
In these notebooks we retrace the steps taken in the supplement to [Lei et al., 2020](https://doi.org/10.1098/rsta.2019.0348), and construct (1) a model of a patch-clamp experiment with artefacts due to capacitance and series resistance, and (2) a model of the circuitry used in patch-clamp amplifiers to compensate for these effects.
Both models draw heavily on the chapter by [Sigworth 1995a](https://doi.org/10.1007/978-1-4419-1229-9_4) and a recent paper from the same group by [Weerakoon et al., 2009](https://doi.org/10.1109/TBCAS.2008.2005419).

I have tried to keep things as to-the-point as possible, but 


1. [The first notebook](./artefacts-1-modelling-patch-clamp.ipynb) describes the uncompensated patch-clamp set up, and shows how to derive both an electrical schematic and an ODE model.
2. [The second](./artefacts-2-compensation.ipynb) adds (heavily simplified) equations that describe the corrections commonly applied _on-line_ during a patch-clamp experiment.


Possible to-do:
- [ ] Endogeneous currents
- [ ] Gating currents? (~100x smaller than ionic currents)
- [ ] Info loss when cutting out artefacts
- [ ] Subtraction protocol
- [ ] Leak ramp
- [ ] Reversal potential ramp

