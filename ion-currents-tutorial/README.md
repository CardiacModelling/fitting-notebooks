[↩ back to index](../README.md)
# Estimating parameters of ion current models from whole-cell voltage-clamp data

In this tutorial, we look at the problem of estimating the parameters of an ion current model from whole-cell voltage-clamp data.
The follow topics are covered:

## [Introduction](introduction.ipynb)

This tutorial provides some background on the model we'll use throughout the tutorial.
It also introduces a first voltage-protocol (a simplified variant of the "staircase protocol").

## [Basic simulations](basic-simulations.ipynb)

This tutorial shows how Myokit can be used to simulate patch-clamp experiments.
It shows you how to create a simulation from a model and protocol stored on disk, and discusses how to change model parameters.
Finally, it shows how steady-states can be calculated and set as initial conditions.

## [Basic fitting](basic-fitting.ipynb)

In this tutorial we link Myokit to PINTS.
Noise models are discussed and synthetic data is generated, after which an error measure is defined and minimised.
Inspecting the results, we show how tight solver tolerances are needed for fitting, and how the finite size of our experimental time series can cause a slight bias in the results.

## Fitting to different voltage protocols

The next four notebooks discuss different voltage protocols, and the simulation methods appropriate to each one.

- [Combining step protocols with sine waves or ramps](more-protocols-1-steps-and-ramps.ipynb)
- [Simulating an AP protocol with "data clamp"](more-protocols-2-data-clamp.ipynb)
- [Analytical solvers for simple step protocols](more-protocols-3-analytic-solvers.ipynb)
- [Fitting to multiple simple step protocols](more-protocols-4-multiple-protocols.ipynb)

## [Setting boundaries on model parameters](boundaries.ipynb)

In this tutorial we show how some parameters can cause numerical issues during simulation, and how we can catch and report these errors.
We then inspect the model equations and use previous estimates of our parameters (or quantities related to the parameters) to define some very wide boundaries, or "prior estimates".
Finally, we show how we can use this kind of reasoning to define univariate boundaries (one on each parameter), and multivariate boundaries (which restrict the maximum rate coefficients seen during a simulation).

## [Selecting starting points for an optimisation](starting-points.ipynb)

Continuing from the previous tutorial, this tutorial shows how we can sample from within the (univariate and multivariate) boundaries to select starting points for an optisiation.
At the end of this tutorial we briefly discuss a "repeated-fits" strategy which allows you to test the reliability of results obtained on real data, where the "true" parameters are not known.

## [Searching in a transformed space](transformations.ipynb)

This tutorial shows how you can create wrappers around models and boundaries to run optimisations on a transformed parameter space.

## [Running big fitting experiments](big-fitting.ipynb)

This tutorial focusses on the practical side of fitting.
It introduces methods to store simulation results to disk, load and analyse them, and shows a way to "reserve" filenames when multiple processes are running at once.
It ends with a brief note on multiprocessing.
  
## [Dealing with real data](real-data.ipynb)
- Capacitance filtering
- Subtraction protocol
- Leak correction
    - We don't know!
    - But could add ramps
- Reversal potential
    - Could add ramps
    - But links to leak!

