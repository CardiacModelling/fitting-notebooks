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

## More simulation

The next four notebooks discuss different voltage protocols, and the simulation methods appropriate to each one.

- [Combining step protocols with sine waves or ramps](more-simulation-1-steps-and-ramps.ipynb)
- [Simulating an AP protocol with "data clamp"](more-simulation-2-data-clamp.ipynb)
- [Analytical solvers for simple step protocols](more-simulation-3-analytic-solvers.ipynb)
- [Fitting to multiple simple step protocols](more-simulation-4-multiple-protocols.ipynb)

## Setting boundaries on parameters
- Guess bounds on parameters themselves
- Rates
    
## Choosing starting points
- Sampling from within boundaries

## Searching in a transformed space
- Reasons unclear
  
## Dealing with real data
- Capacitance filtering
    - Manual
    - Using step protocol
- Subtraction protocol
- Leak correction
    - We don't know!
    - But could add ramps
- Reversal potential
    - Could add ramps
    - But links to leak!

## Checking reliability of the results
- Repeats from different starting points
- MCMC has limited use, if the noise model is gaussian

## Speeding things up with parallelisation
- Windows
- GPUs?
