# Myokit & Pints examples

This repository contains examples showing how to fit [Myokit](https://github.com/MichaelClerx/myokit/) models to data using the [Pints](https://github.com/pints-team/pints) optimisation & inference framework.

## How it works

- Models are written in Myokit's [MMT syntax](https://myokit.readthedocs.io/syntax/index.html)
  - Many project start by [downloading a CellML model](https://models.cellml.org/electrophysiology) and then [importing it into Myokit](https://myokit.readthedocs.io/api_formats/cellml.html).
- Simulations are run with Myokit's [Simulation](https://myokit.readthedocs.io/api_simulations/Simulation.html) class, which uses CVODE to solve the ODEs.
  - For ion-channel stuff with voltage-step protocols (no ramps or sine waves) it's usually faster to use Myokit's [Hodgkin-Huxley model](https://myokit.readthedocs.io/api_library/hh.html) or [Markov model](https://myokit.readthedocs.io/api_library/markov.html) classes to run analytical simulations)
- A [Pints ForwardModel](https://github.com/pints-team/pints/blob/master/examples/writing-a-model.ipynb) is wrapped around a Myokit simulation.
- A Pints [error measure](https://pints.readthedocs.io/en/latest/error_measures.html) or [likelihood function](https://pints.readthedocs.io/en/latest/log_likelihoods.html) is defined
- Using this function, [optimisation](https://github.com/pints-team/pints/blob/master/examples/optimisation-first-example.ipynb) or [Bayesian inference](https://github.com/pints-team/pints/blob/master/examples/sampling-first-example.ipynb) is run

## More details

Pints comes with [examples](https://github.com/pints-team/pints/blob/master/examples/README.md) and [API documentation](https://pints.readthedocs.io/). [This pre-print](https://arxiv.org/abs/1812.07388) describes Pints' design, information on citing it is given [here](https://github.com/pints-team/pints/blob/master/CITATION).

Similarly, Myokit comes with some [example models](http://myokit.org/examples/) and [API docs](https://myokit.readthedocs.io). [This publication in PBMB](https://doi.org/10.1016/j.pbiomolbio.2015.12.008) describes Myokit, and can be cited using the information [here](https://github.com/MichaelClerx/myokit/blob/master/CITATION).

## Installation

Please see the [Myokit](https://github.com/MichaelClerx/myokit/) and [Pints](https://github.com/pints-team/pints) repos for installation instructions for both tools.





