[↩ back to index](../README.md)
# Estimating parameters of ion current models from whole-cell voltage-clamp data

In these notebooks, we look at the problem of estimating the parameters of an ion current model from whole-cell voltage-clamp data.

As we go along, we'll create some classes and utility functions that may be useful in general.
These are all stored in [library.py](./library.py).

The covered topics are listed below.
Each notebook can be viewed either using github's built-in viewer, or using [Jupyter nbviewer](https://nbviewer.jupyter.org/), which usually provides nicer rendering.

## Introduction [![github](../img/github.svg)](introduction.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/introduction.ipynb)

This notebook provides some background on the model we'll use in all examples.
It also introduces a first voltage-protocol (a simplified variant of the "staircase protocol").

## Basic simulations [![github](../img/github.svg)](basic-simulations.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/basic-simulations.ipynb)

This notebook shows how Myokit can be used to simulate patch-clamp experiments.
It shows you how to create a simulation from a model and protocol stored on disk, and discusses how to change model parameters.
Finally, it shows how steady-states can be calculated and set as initial conditions.

## Basic fitting [![github](../img/github.svg)](basic-fitting.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/basic-fitting.ipynb)

In this notebook we link Myokit to PINTS.
Noise models are discussed and synthetic data is generated, after which an error measure is defined and minimised.
Inspecting the results, we show how tight solver tolerances are needed for fitting, and how the finite size of our experimental time series can cause a slight bias in the results.

## Simulating different voltage protocols

The next four notebooks discuss different voltage protocols, and the simulation methods appropriate to each one.

- Combining step protocols with sine waves or ramps [![github](../img/github.svg)](more-protocols-1-steps-and-ramps.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-1-steps-and-ramps.ipynb)
- Simulating an AP protocol with "data clamp" [![github](../img/github.svg)](more-protocols-2-data-clamp.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-2-data-clamp.ipynb)
- Analytical solvers for simple step protocols [![github](../img/github.svg)](more-protocols-3-analytic-solvers.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-3-analytic-solvers.ipynb)
- Fitting to multiple simple step protocols [![github](../img/github.svg)](more-protocols-4-multiple-protocols.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/more-protocols-4-multiple-protocols.ipynb)

## Setting boundaries on model parameters [![github](../img/github.svg)](boundaries.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/boundaries.ipynb)

In this notebook we show how some parameters can cause numerical issues during simulation, and how we can catch and report these errors.
We then inspect the model equations and use previous estimates of our parameters (or quantities related to the parameters) to define some very wide boundaries, or "prior estimates".
Finally, we show how we can use this kind of reasoning to define univariate boundaries (one on each parameter), and multivariate boundaries (which restrict the maximum rate coefficients seen during a simulation).

## Selecting starting points for an optimisation [![github](../img/github.svg)](starting-points.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/starting-points.ipynb)

Continuing from the previous chapters, this notebook shows how we can sample from within the (univariate and multivariate) boundaries to select starting points for an optisiation.
At the end of this notebook we briefly discuss a "repeated-fits" strategy which allows you to test the reliability of results obtained on real data, where the "true" parameters are not known.

## Searching in a transformed space [![github](../img/github.svg)](transformations.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/transformations.ipynb)

This notebook shows how you can use PINTS Transformation class to run optimisations in a transformed parameter space.

## Running big fitting experiments [![github](../img/github.svg)](big-fitting.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/big-fitting.ipynb)

This notebook focusses on the practical side of fitting.
It introduces methods to store simulation results to disk, load and analyse them, and shows a way to "reserve" filenames when multiple processes are running at once.
It ends with a brief note on multiprocessing.

## Checking your fitting results [![github](../img/github.svg)](reliability.ipynb) [![nbviewer](../img/nbviewer.svg)](https://nbviewer.jupyter.org/github/CardiacModelling/fitting-notebooks/blob/main/ion-currents/reliability.ipynb)

In this notebook we discuss using synthetic data to test your optimisation set-up, using repeated fits to check the reliability of your real-data fits, and using an independent data set to test the usefulness of your fitted model.

