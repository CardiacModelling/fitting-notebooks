
# Modelling patch-clamp experiments

When analysing data from whole-cell patch-clamp experiments, it can be useful to have a model of both the biological system of interest _and_ the experimental set up.
In these notebooks we retrace the steps taken in the supplement to [Lei et al., 2020](https://doi.org/10.1098/rsta.2019.0348), and construct (1) a model of a patch-clamp experiment with various experimental artefacts, and (2) a model of the various corrections applied by patch-clamp amplifiers to mitigate these effects.
Both models and the exposition here draw heavily on a book chapter by [Sigworth (1995a)](https://doi.org/10.1007/978-1-4419-1229-9_4), as well as a recent paper from the same group ([Weerakoon et al., 2009](https://doi.org/10.1109/TBCAS.2008.2005419)).

I have tried to keep things as to-the-point as possible, but a lot of extra detail is provided in the appendices.


## Modelling patch-clamp experiments [![github](../img/github.svg)](artefacts-1-modelling-patch-clamp.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts/artefacts-1-modelling-patch-clamp.ipynb)

The first notebook] describes the uncompensated patch-clamp set up, and shows how to derive both an electrical schematic and an ODE model.
It first introduces a basic op-amp based current measuring device, then adds in the effects of stray and parasitic  (pipette) capacitance, before briefly discussing the finite speed of the amplifier.
It then adds series resistance and membrane capacitance, a voltage offset, and leak current, culminating in a 3-state ODE model of whole-cell voltage clamp.

## Modelling patch-clamp experiments: compensation [![github](../img/github.svg)](artefacts-2-compensation.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts/artefacts-2-compensation.ipynb)

This notebook adds (heavily simplified) equations that describe the corrections commonly applied _on-line_ during a patch-clamp experiment.


Possible to-do:
- [ ] Endogeneous currents
- [ ] Gating currents? (~100x smaller than ionic currents)
- [ ] Info loss when cutting out artefacts
- [ ] Subtraction protocol
- [ ] Leak ramp
- [ ] Reversal potential ramp

