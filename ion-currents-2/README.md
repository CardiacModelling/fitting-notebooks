# Estimating parameters of ion current models from whole-cell voltage-clamp data

In this tutorial, we look at the problem of estimating the parameters of an ion current model from whole-cell voltage-clamp data.
Starting from a synthetic data study, we add features step by step.
The final result is a fitting method that can be applied to real-world problems.

1. Introduction
    - Model
    - Staircase protocol
    

2. First steps: a synthetic data study
    - Sim
    - Forward model
    - Data, times
    - Log selected variables only

    - Initial conditions?
    - Noise model
    
    
2. Fitting to multiple protocols


2. Setting boundaries on parameters
    - Rates

3. Searching in a transformed space
    - Reasons unclear
    
4. Choosing the right simulation type
    - Current stuff

5. Speeding things up with parallelisation
    - Windows
    
6. Dealing with real data
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

8. Checking reliability of the results
    - Repeats
    - MCMC has limited use, if the noise model is gaussian
    - Plot line near optimum?

9. Interpreting the final fit
    - Noise model
    - Discrepancy
    
