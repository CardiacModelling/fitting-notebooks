[↩ back to index](../README.md)
# Estimating parameters of ion current models from whole-cell voltage-clamp data

In these notebooks, we look at the problem of estimating the parameters of an ion current model from whole-cell voltage-clamp data.

As we go along, we'll create some classes and utility functions that may be useful in general.
These are all stored in [library.py](./library.py).

The follow topics are covered:

## [Introduction](introduction.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/introduction.ipynb)

This notebook provides some background on the model we'll use in all examples.
It also introduces a first voltage-protocol (a simplified variant of the "staircase protocol").

## [Basic simulations](basic-simulations.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/basic-simulations.ipynb)

This notebook shows how Myokit can be used to simulate patch-clamp experiments.
It shows you how to create a simulation from a model and protocol stored on disk, and discusses how to change model parameters.
Finally, it shows how steady-states can be calculated and set as initial conditions.

## [Basic fitting](basic-fitting.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/basic-fitting.ipynb)

In this notebook we link Myokit to PINTS.
Noise models are discussed and synthetic data is generated, after which an error measure is defined and minimised.
Inspecting the results, we show how tight solver tolerances are needed for fitting, and how the finite size of our experimental time series can cause a slight bias in the results.

## Fitting to different voltage protocols

The next four notebooks discuss different voltage protocols, and the simulation methods appropriate to each one.

- [Combining step protocols with sine waves or ramps](more-protocols-1-steps-and-ramps.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-1-steps-and-ramps.ipynb)
- [Simulating an AP protocol with "data clamp"](more-protocols-2-data-clamp.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-2-data-clamp.ipynb)
- [Analytical solvers for simple step protocols](more-protocols-3-analytic-solvers.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-3-analytic-solvers.ipynb)
- [Fitting to multiple simple step protocols](more-protocols-4-multiple-protocols.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-4-multiple-protocols.ipynb)

## [Setting boundaries on model parameters](boundaries.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/boundaries.ipynb)

In this notebook we show how some parameters can cause numerical issues during simulation, and how we can catch and report these errors.
We then inspect the model equations and use previous estimates of our parameters (or quantities related to the parameters) to define some very wide boundaries, or "prior estimates".
Finally, we show how we can use this kind of reasoning to define univariate boundaries (one on each parameter), and multivariate boundaries (which restrict the maximum rate coefficients seen during a simulation).

## [Selecting starting points for an optimisation](starting-points.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/starting-points.ipynb)

Continuing from the previous chapters, this notebook shows how we can sample from within the (univariate and multivariate) boundaries to select starting points for an optisiation.
At the end of this notebook we briefly discuss a "repeated-fits" strategy which allows you to test the reliability of results obtained on real data, where the "true" parameters are not known.

## [Searching in a transformed space](transformations.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/transformations.ipynb)

This notebook shows how you can create wrappers around models and boundaries to run optimisations on a transformed parameter space.

## [Running big fitting experiments](big-fitting.ipynb) - [nbviewer](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/big-fitting.ipynb)

This notebook focusses on the practical side of fitting.
It introduces methods to store simulation results to disk, load and analyse them, and shows a way to "reserve" filenames when multiple processes are running at once.
It ends with a brief note on multiprocessing.

## (TODO) Validating modelling results

- Repeated runs (see previous notebook) validates fitting
- Training, validation, and test sets validates modelling?

## (TODO) Dealing with real data

Blah blah blah

These are sequential, not independent notebooks

- [Introduction, and additive noise](real-data-1-noise.ipynb)
- [Capacitance and series resistance](real-data-2-capacitance-and-resistance.ipynb)

- One
  - Four strategies
  - Noise model
  - Stochastic noise
  - Periodic noise
- Two
  - Pipette capacitance
  - Membrane capacitance

Sources:
- [x] Thermal, shot, mains, etc.
- [x] Stray capacitance
- [ ] Membrane capacitance
- [ ] Series resistance
- [ ] Leak
- [ ] Endogeneous currents
- [ ] Gating currents? (~100x smaller than ionic currents)

Things to be uncertain about
- [ ] Concentrations
- [ ] Reversal potential (Nernst/GHK graph?)
- [ ] Temperature
- [ ] Model discrepancy

Methods
- [x] Low-pass filter
- [x] Modelling noise
- [x] Stray cap correction
- [ ] Cm correction
- [ ] Artefact filtering
- [ ] Rs correction
- [ ] Subtraction protocol
- [ ] Leak correction
- [ ] Leak ramp
- [ ] Reversal potential ramp

