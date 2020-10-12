# Fitting ion channel models with Myokit & PINTS

This repository contains examples showing how to fit Myokit models to data using the PINTS optimisation & inference framework.

A part on fitting AP models is planned, but for now the repository contains:

- a [detailed tutorial](ion-currents-tutorial/README.md) showing how to fit kinetic parameters of ion current models.

## General recommendations

**Start with a synthetic data study:**
Before going to the lab, work out what data you expect to get, simulate this data and add noise, prepare your analysis code, and test that it can recover the parameters you used to generate the data.

**Fit to time-series data:**
Whenever possible, fit to time-series data, not to "summary statistics" or "biomarkers" such as time constants, IV-, or (in)activation curves.
Contacting experimenters, digging in archives, or even repeating experiments is a better use of time than trying to fit to data not suitable for fitting to.

**Define expected ranges for the parameters:**
Define boundaries on the parameters (or on e.g. rates derived from the parameters).
These speed up your search, but are also used to..

**Verify the reliability of your results:** by running repeated fits.
Restart your fit several (50?) times from different positions sampled from within the feasible ranges of the parameters.
If only a handful of fits find the same "best result", it's likely this isn't the true optimum.

**Check your solver tolerances**: if using an adaptive step-size solver, make sure you use strict tolerances.
If you're not sure, plot the error measure along a line between two nearby points: if it's nice and smooth the optimiser will love it.

**Search in a log-transformed parameter space**: This can often make the problem much easier for whatever optimisation algorithm you're using.

**Use the CMA-ES optimiser**: It performs much better on these problems than anything else we've tested.

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
  [doi:10.1016/j.pbiomolbio.2015.12.008](https://doi.org/10.1016/j.pbiomolbio.2015.12.008)
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

### Advanced topics in fitting

- **Accounting for variability in ion current recordings using a mathematical model of artefacts in voltage-clamp experiments**
  Chon Lok Lei, Michael Clerx, Dominic G. Whittaker, David J. Gavaghan, Teun P. de Boer, Gary R. Mirams
  [doi:10.1098/rsta.2019.0348](https://doi.org/10.1098/rsta.2019.0348)
  | [code](https://github.com/CardiacModelling/VoltageClampModel)

- **Considering discrepancy when calibrating a mechanistic electrophysiology model**
  Chon Lok Lei, Sanmitra Ghosh, Dominic G. Whittaker, Yasser Aboelkassem, Kylie A. Beattie, Chris D. Cantwell, Tammo Delhaas, Charles Houston, Gustavo Montes Novaes, Alexander V. Panfilov, Pras Pathmanathan, Marina Riabiz, Rodrigo Weber dos Santos, John Walmsley, Keith Worden, Gary R. Mirams, Richard D. Wilkinson
  2020, Phil. Trans. R. Soc. A.
  [doi:10.1098/rsta.2019.0349](http://doi.org/10.1098/rsta.2019.0349)
  | [code](https://github.com/CardiacModelling/fickleheart-method-tutorials)

