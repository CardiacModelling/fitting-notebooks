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

- Robust ForwardModel (try/catch)
- Guess bounds on parameters themselves
- Rates

## [Selecting starting points for an optimisation](starting-points.ipynb)

- Sampling from within boundaries
- Repeats from different starting points

## [Searching in a transformed space](transformations.ipynb)
- Reasons unclear
  
## [Dealing with real data](real-data.ipynb)
- Capacitance filtering
- Subtraction protocol
- Leak correction
    - We don't know!
    - But could add ramps
- Reversal potential
    - Could add ramps
    - But links to leak!

