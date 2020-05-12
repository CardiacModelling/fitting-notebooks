# Fitting electrophysiology models with Myokit & PINTS

This repository contains examples showing how to fit Myokit models to data using the PINTS optimisation & inference framework.
It includes:

- a [brief example](action-potential-example) of fitting (whole-cell) conductances to an action potential (AP) trace; and
- a [detailed tutorial](io-currents-tutorial) showing how to fit kinetic parameters of ion current models.

The AP model example is a great place to start if you've done fitting before, and would like to spend five minutes seeing how it can be done with Myokit and PINTS.
The ion current tutorial goes into much more depth, and includes topics that are useful in AP model fitting too, such as defining boundaries and parameter transformations.

## General recommendations

A definition list?
: Who knows
: It might even work

It might not work
: But that is a risk we're willing to take

1. Whenever possible, fit to **time-series data**, not to processed values such as time constants, IV-, or (in)activation curves. [
   This figure](https://www.biorxiv.org/content/10.1101/609875v1.full#F11) shows why: A score function defined on processed values (method 2 in the paper) can have a complex surface, full of local minima, while similar functions defined on the underlying time-series data (methods 3 and 4 in the paper) are convex and smooth.
2. Define prior expectations on transition rates as well as parameters.
   See [this figure](https://www.biorxiv.org/content/10.1101/609875v1.full#F3) and the [supplementary materials](https://www.biorxiv.org/content/10.1101/609875v1.supplementary-material).
3. Searching in a log-transformed parameter space [can make your problem more convex](https://dx.doi.org/10.1093/bioinformatics/btz020) (which is a good thing).
4. Use an analytic solver if possible, if using an adaptive ODE solver make sure you [set very fine tolerances](https://mirams.wordpress.com/2018/10/17/ode-errors-and-optimisation/).
   In Myokit, this can be done with [`Simulation.set_tolerance()`](https://myokit.readthedocs.io/api_simulations/Simulation.html#myokit.Simulation.set_tolerance).
5. Test the reliability of your fit by running repeated fits from different starting points (e.g. sampled uniformly from your prior).
6. Before doing any experiments, test the whole set-up with simulated data (and simulated noise).

## More information

### Fitting software

- **Probabilistic Inference on Noisy Time Series (PINTS)**.
  Michael Clerx, Martin Robinson, Ben Lambert, Chon Lok Lei, Sanmitra Ghosh, Gary R. Mirams, David J. Gavaghan.
  2019, Journal of Open Research Software.
  [doi:10.5334/jors.252](https://doi.org/10.5334/jors.252)
  | [examples](https://github.com/pints-team/pints/blob/master/examples/README.md) 
  | [documentation](https://pints.readthedocs.io/)
  | [installation](https://github.com/pints-team/pints/)
  | [code](https://github.com/pints-team/pints/)
    
- **Myokit: A simple interface to cardiac cellular electrophysiology**.
  Michael Clerx, Pieter Collins, Enno de Lange, Paul G.A. Volders.
  2016, Progress in Biophysics and Molecular Biology.
  [10.1016/j.pbiomolbio.2015.12.008](https://doi.org/10.1016/j.pbiomolbio.2015.12.008)
  | [examples](http://myokit.org/examples/)
  | [documentation](https://myokit.readthedocs.io)
  | [installation](http://myokit.org/install)
  | [website](http://myokit.org)
  | [code](https://github.com/MichaelClerx/myokit/)

### Fitting papers

- **Calibration of ionic and cellular cardiac electrophysiology models**.
  Dominic G. Whittaker, Michael Clerx, Chon Lok Lei, David J. Christini, Gary R. Mirams.
  2020, WIREs Systems Biology and Medicine.
  [doi:10.1002/wsbm.1482](https://doi.org/10.1002/wsbm.1482)
  | [code](https://github.com/CardiacModelling/WIRES)

- **Four ways to fit an ion channel model**.
  Michael Clerx, Kylie A. Beattie, David J. Gavaghan, Gary R. Mirams.
  2019, Biophysical Journal.
  [doi:10.1016/j.bpj.2019.08.001](https://doi.org/10.1016/j.bpj.2019.08.001)
  | [code](https://github.com/CardiacModelling/FourWaysOfFitting)

- **Rapid characterisation of hERG channel kinetics I: using an automated high-throughput system**.
  Chon Lok Lei, Michael Clerx, David J. Gavaghan, Liudmila Polonchuk, Gary R. Mirams, Ken Wang.
  2019, Biophysical Journal.
  [doi:j.bpj.2019.07.029](https://doi.org/10.1016/j.bpj.2019.07.029)
  | [code](https://github.com/CardiacModelling/hERGRapidCharacterisation)

- **Rapid characterisation of hERG channel kinetics II: temperature dependence**.
  Chon Lok Lei, Michael Clerx, Kylie A. Beattie, Dario Melgari, Jules C. Hancox, David J. Gavaghan, Liudmila Polonchuk, Ken Wang, Gary R. Mirams.
  2019, Biophysical Journal.
  [doi:j.bpj.2019.07.030](https://doi.org/10.1016/j.bpj.2019.07.030)
  | [code](https://github.com/CardiacModelling/hERGRapidCharacterisation)

- **Sinusoidal voltage protocols for rapid characterisation of ion channel kinetics**
  Kylie A. Beattie, Adam P. Hill, Rémi Bardenet, Yi Cui, Jamie I. Vandenberg, David J. Gavaghan, Teun P. de Boer, Gary R. Mirams
  2018, The Journal of Physiology.
  [doi:10.1113/JP275733](https://doi.org/10.1113/JP275733)
  | [code](https://github.com/mirams/sine-wave)

