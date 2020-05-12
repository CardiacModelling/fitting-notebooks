# Fitting electrophysiology models with Myokit & PINTS

This repository contains examples showing how to fit [Myokit](https://github.com/MichaelClerx/myokit/) models to data using the [Pints](https://github.com/pints-team/pints) optimisation & inference framework.




## General approach

- [Models are written in Myokit's MMT syntax](https://myokit.readthedocs.io/syntax/index.html), usually by [downloading a CellML model](https://models.cellml.org/electrophysiology) and then [importing it](https://myokit.readthedocs.io/api_formats/cellml.html).
- [Simulations are run](https://myokit.readthedocs.io/api_simulations/Simulation.html) using the `Simulation` class, which uses CVODE to solve the ODEs.
  - For ion-channel stuff with piecewise constant voltage-step protocols (no ramps or sine waves) it's usually faster to use Myokit's [Hodgkin-Huxley model](https://myokit.readthedocs.io/api_library/hh.html) or [Markov model](https://myokit.readthedocs.io/api_library/markov.html) classes to run analytical simulations)
- [A pints.ForwardModel](https://nbviewer.jupyter.org/github/pints-team/pints/blob/master/examples/writing-a-model.ipynb) is wrapped around a Myokit simulation.
- [A pints.ErrorMeasure](https://pints.readthedocs.io/en/latest/error_measures.html) or [pints.LogLikelihood](https://pints.readthedocs.io/en/latest/log_likelihoods.html) is defined
- [Optimisation](https://nbviewer.jupyter.org/github/pints-team/pints/blob/master/examples/optimisation-first-example.ipynb) or [Bayesian inference](https://nbviewer.jupyter.org/github/pints-team/pints/blob/master/examples/sampling-first-example.ipynb) is run.

## Examples: Inference using Myokit and PINTS

1. [Fitting conductances in a whole-cell model](https://github.com/MichaelClerx/myokit-pints-examples/tree/master/whole-cell-conductances)
2. [A real-life example](https://github.com/CardiacModelling/FourWaysOfFitting/blob/master/python/model.py) of a ForwardModel class used for sine-wave siulations as well as analytical step-protocol simulations
3. An example of a [parameter transform](https://github.com/CardiacModelling/FourWaysOfFitting/blob/master/python/transformation.py). This could be used in a forward model implementation, so that the parameters the model presents to the optimiser/sampler are in a transformed space.
4. [Example code](https://pints.readthedocs.io/en/latest/boundaries.html) for a [pints.Boundaries](https://pints.readthedocs.io/en/latest/boundaries.html) object for a hERG model. This could be adapted to be a [pints.LogPrior](https://pints.readthedocs.io/en/latest/log_priors.html).

## Some recommendations for fitting

1. Whenever possible, fit to **time-series data**, not to processed values such as time constants, IV-, or (in)activation curves. [
   This figure](https://www.biorxiv.org/content/10.1101/609875v1.full#F11) shows why: A score function defined on processed values (method 2 in the paper) can have a complex surface, full of local minima, while similar functions defined on the underlying time-series data (methods 3 and 4 in the paper) are convex and smooth.
2. Define prior expectations on transition rates as well as parameters.
   See [this figure](https://www.biorxiv.org/content/10.1101/609875v1.full#F3) and the [supplementary materials](https://www.biorxiv.org/content/10.1101/609875v1.supplementary-material).
3. Searching in a log-transformed parameter space [can make your problem more convex](https://dx.doi.org/10.1093/bioinformatics/btz020) (which is a good thing).
4. Use an analytic solver if possible, if using an adaptive ODE solver make sure you [set very fine tolerances](https://mirams.wordpress.com/2018/10/17/ode-errors-and-optimisation/).
   In Myokit, this can be done with [`Simulation.set_tolerance()`](https://myokit.readthedocs.io/api_simulations/Simulation.html#myokit.Simulation.set_tolerance).
5. Test the reliability of your fit by running repeated fits from different starting points (e.g. sampled uniformly from your prior).
6. Before doing any experiments, test the whole set-up with simulated data (and simulated noise).


## Papers

**Overview papers**
-   *Calibration of ionic and cellular cardiac electrophysiology models*.
    Dominic G. Whittaker, Michael Clerx, Chon Lok Lei, David J. Christini, Gary R. Mirams.
    2020, WIREs Systems Biology and Medicine.
    [doi:10.1002/wsbm.1482](https://doi.org/10.1002/wsbm.1482)
    | [code](https://github.com/CardiacModelling/WIRES)
-   *Four ways to fit an ion channel model*.
    Michael Clerx, Kylie A. Beattie, David J. Gavaghan, Gary R. Mirams.
    2019, Biophysical Journal.
    [doi:10.1016/j.bpj.2019.08.001](https://doi.org/10.1016/j.bpj.2019.08.001)
    | [code](https://github.com/CardiacModelling/FourWaysOfFitting)
**Fitting papers**
-   *Sinusoidal voltage protocols for rapid characterisation of ion channel kinetics*
    Kylie A. Beattie, Adam P. Hill, Rémi Bardenet, Yi Cui, Jamie I. Vandenberg, David J. Gavaghan, Teun P. de Boer, Gary R. Mirams
    2018, Journal of Physiology
    [doi:10.1113/JP275733](https://doi.org/10.1113/JP275733)
    | [code](https://github.com/mirams/sine-wave)
-   *Rapid characterisation of hERG channel kinetics I: using an automated high-throughput system*.
    Chon Lok Lei, Michael Clerx, David J. Gavaghan, Liudmila Polonchuk, Gary R. Mirams, Ken Wang.
    2019, Biophysical Journal.
    [doi:j.bpj.2019.07.029](https://doi.org/10.1016/j.bpj.2019.07.029)
    | [code](https://github.com/CardiacModelling/hERGRapidCharacterisation)
-   *Rapid characterisation of hERG channel kinetics II: temperature dependence*.
    Chon Lok Lei, Michael Clerx, Kylie A. Beattie, Dario Melgari, Jules C. Hancox, David J. Gavaghan, Liudmila Polonchuk, Ken Wang, Gary R. Mirams.
    2019, Biophysical Journal
    [doi:j.bpj.2019.07.030](https://doi.org/10.1016/j.bpj.2019.07.030)
    | [code](https://github.com/CardiacModelling/hERGRapidCharacterisation)
**Software papers**
-   *Probabilistic Inference on Noisy Time Series (PINTS)*
    Michael Clerx, Martin Robinson, Ben Lambert, Chon Lok Lei, Sanmitra Ghosh, Gary R. Mirams, David J. Gavaghan.
    2019, Journal of Open Research Software.
    [doi:10.5334/jors.252](https://doi.org/10.5334/jors.252)
    | [examples](https://github.com/pints-team/pints/blob/master/examples/README.md) 
    | [documentation](https://pints.readthedocs.io/)
    | [installation](https://github.com/pints-team/pints/)
    | [code](https://github.com/pints-team/pints/)
-   *Myokit: A simple interface to cardiac cellular electrophysiology*.
    Michael Clerx, Pieter Collins, Enno de Lange, Paul G.A. Volders.
    2016, Progress in Biophysics and Molecular Biology.
    [10.1016/j.pbiomolbio.2015.12.008](https://doi.org/10.1016/j.pbiomolbio.2015.12.008)
    | [examples](http://myokit.org/examples/)
    | [documentation](https://myokit.readthedocs.io)
    | [installation](http://myokit.org/install)
    | [website](http://myokit.org)
    | [code](https://github.com/MichaelClerx/myokit/)

