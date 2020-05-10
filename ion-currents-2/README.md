# Estimating parameters of ion current models from whole-cell voltage-clamp data

In this tutorial, we look at the problem of estimating the parameters of an ion current model from whole-cell voltage-clamp data.
Starting from a synthetic data study, we add features step by step.
The final result is a fitting method that can be applied to real-world problems.


## Table of contents

1. Introduction
   - Provides background on the model we'll use throughout the tutorial
   - Introduces a simplified variant of the "staircase protocol"
   
2. Basic simulations
   - Shows how to run simulations and plot the results
   - Shows how to change model parameters
   - Shows how to set initial conditions

3. Basic fitting
    - Forward model
    - Generating synthetic data (and choosing a noise model)
    - Setting up a problem
    - Running an optimisation
    
4. Fitting to different protocols
    - Multiple protocols: Repeat, and combine
    - Sine wave: modify the model?
    - AP signal: use data clamp
    - Hint at ways to implement Chon's staircase
8. Choosing the right simulation type
    - See the current examples

5. Setting boundaries on parameters
    - Guess bounds on parameters themselves
    - Rates
    
6. Choosing starting points
    - Sampling from within boundaries

7. Searching in a transformed space
    - Reasons unclear

9. Speeding things up with parallelisation
    - Windows
    
10. Dealing with real data
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

11. Checking reliability of the results
    - Repeats from different starting points
    - MCMC has limited use, if the noise model is gaussian
    - Plot line near optimum?

12. Interpreting the final fit
    - Noise model
    - Discrepancy
    
