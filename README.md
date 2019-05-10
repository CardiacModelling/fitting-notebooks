# Myokit & Pints examples

This repository contains examples showing how to fit [Myokit](https://github.com/MichaelClerx/myokit/) models to data using the [Pints](https://github.com/pints-team/pints) optimisation & inference framework.

## How it works

- Models are written in Myokit's MMT syntax (typically imported from CellML)
- Simulations are run with Myokit's `Simulation` class, which uses CVODE internally (but note that for ion-channel stuff it's usually faster to use Myokit's HH or Markov modules to obtain analytical simulations)
- A Pints statistical model is wrapped around a Myokit simulation (in inference terms, this wrapped simulation is our _forward model_)
- A Pints [error measure](https://pints.readthedocs.io/en/latest/error_measures.html) or [likelihood function](https://pints.readthedocs.io/en/latest/log_likelihoods.html) is defined
- Using this function, optimisation or Bayesian inference is run

## More details

Pints comes with [examples](https://github.com/pints-team/pints/blob/master/examples/README.md) and [API documentation](https://pints.readthedocs.io/). [This pre-print](https://arxiv.org/abs/1812.07388) describes Pints' design, information on citing it is given [here](https://github.com/pints-team/pints/blob/master/CITATION).

Similarly, Myokit comes with some [example models](http://myokit.org/examples/) and [API docs](https://myokit.readthedocs.io). [This publication in PBMB](https://doi.org/10.1016/j.pbiomolbio.2015.12.008) describes Myokit, and can be cited using the information [here](https://github.com/MichaelClerx/myokit/blob/master/CITATION).

## Installation

Please see the [Myokit](https://github.com/MichaelClerx/myokit/) and [Pints](https://github.com/pints-team/pints) repos for installation instructions for both tools.





