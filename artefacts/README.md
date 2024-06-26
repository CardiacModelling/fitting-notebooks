
# Modelling patch-clamp experiments

When analysing data from whole-cell patch-clamp experiments, it can be useful to have a model of both the biological system of interest _and_ the experimental set up.
In these notebooks we retrace the steps taken in the supplement to [Lei et al., 2020](https://doi.org/10.1098/rsta.2019.0348), and construct (1) a model of a patch-clamp experiment with various experimental artefacts, and (2) a model of the corrections applied by patch-clamp amplifiers to mitigate these effects.
Both models and their exposition draw heavily on a book chapter by [Sigworth (1995a)](https://doi.org/10.1007/978-1-4419-1229-9_4).

I have tried to keep things as to-the-point as possible, but a lot of extra detail is provided in the appendices.

## Modelling patch-clamp experiments [![github](../img/github.svg)](artefacts-1-modelling-patch-clamp.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts/artefacts-1-modelling-patch-clamp.ipynb)

The first notebook] describes the uncompensated patch-clamp set up, and shows how to derive both an electrical schematic and an ODE model.

## Modelling electronic compensation [![github](../img/github.svg)](artefacts-2-compensation.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts/artefacts-2-compensation.ipynb)

In this notebook we update the model to include the compensation circuitry commonly used in patch-clamp amplifiers.

## Simulating a manual patch clamp experiment [![github](../img/github.svg)](artefacts-3-simulations.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts/artefacts-3-simulations.ipynb)

(Unfinished) In this notebook, we walk through the steps of a manual patch-clamp experiment.

## Simplified models [![github](../img/github.svg)](artefacts-4-simplified.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/tree/artefacts/artefacts/artefacts-4-simplified.ipynb)

In this notebook we derive simplified models of the compensated voltage clamp setup, which can be used in fitting.

