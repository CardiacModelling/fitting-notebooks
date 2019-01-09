# Myokit + Pints example

This example shows you how to fit [Myokit](https://github.com/MichaelClerx/myokit/) models to data using the [Pints](https://github.com/pints-team/pints) optimisation & inference tools.

## How it works

- Models are written in Myokit's MMT syntax (typically imported from CellML)
- Simulations are run with Myokit's `Simulation` class, which uses CVODE internally (but note that for ion-channel stuff it's usually faster to use Myokit's HH or Markov modules to obtain analytical simulations)
- A Pints statistical model is wrapped around a Myokit simulation
- A Pints error function or likelihood function is defined
- Using this function, optimisation or Bayesian inference is run

## Installation

Please see the [Myokit](https://github.com/MichaelClerx/myokit/) and [Pints](https://github.com/pints-team/pints) repos for installation instructions for both tools.
