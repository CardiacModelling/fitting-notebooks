#!/usr/bin/env python
from __future__ import print_function, division
import numpy as np
import pints
import myokit
import matplotlib.pyplot as plt

class MyokitModel(pints.ForwardModel):
    """
    This is a pints model, i.e. a statistical model that takes parameters and
    times as input, and returns simulated values.
    """
    def __init__(self):
        m, p, _ = myokit.load('beeler-1977.mmt')
        self.simulation = myokit.Simulation(m, p)

    def n_parameters(self):
        return 5

    def n_outputs(self):
        return 2

    def simulate(self, parameters, times):

        self.simulation.reset()
        self.simulation.set_constant('ina.gNaBar', parameters[0])
        self.simulation.set_constant('ina.gNaC', parameters[1])
        self.simulation.set_constant('isi.gsBar', parameters[2])
        self.simulation.set_constant('ik1.gK1', parameters[3])
        self.simulation.set_constant('ix1.gx1', parameters[4])

        log = self.simulation.run(
            times[-1] + 1,
            log_times = times,
            log = ['engine.time', 'membrane.V', 'calcium.Cai'],
        )
        return np.vstack((log['membrane.V'], log['calcium.Cai'])).T


# Create a model
model = MyokitModel()

# Generate some 'experimental' data
x_true = np.array([4, 0.003, 0.09, 0.35, 0.8])
times = np.linspace(0, 600, 601)
values = model.simulate(x_true, times)
print(values.shape)

# Add noise
noisy_values = np.array(values, copy=True)
noisy_values[:, 0] += np.random.normal(0, 1, values[:, 0].shape)
noisy_values[:, 1] += np.random.normal(0, 5e-7, values[:, 1].shape)

plt.figure()
plt.suptitle('Generated data')
plt.subplot(2, 1, 1)
plt.xlabel('Time (ms)')
plt.ylabel('Vm (mV)')
plt.plot(times, noisy_values[:, 0])
plt.plot(times, values[:, 0])
plt.subplot(2, 1, 2)
plt.xlabel('Time (ms)')
plt.ylabel('[Ca]i (mol/L)')
plt.plot(times, noisy_values[:, 1])
plt.plot(times, values[:, 1])
#plt.show()

# Create an object with links to the model and time series
problem = pints.MultiOutputProblem(model, times, noisy_values)

# Create a score function
weights = [1 / 70, 1 / 0.000006]
score = pints.SumOfSquaresError(problem, weights=weights)

# Select some boundaries
lower = x_true / 2
upper = x_true * 2
boundaries = pints.RectangularBoundaries(lower, upper)

# Perform an optimization
x0 = x_true * 1.2
optimiser = pints.Optimisation(
    score, x0, boundaries=boundaries, method=pints.CMAES)

print('Running...')
x_found, score_found = optimiser.run()

# Compare parameters with original
print('Found solution:          True parameters:' )
for k, x in enumerate(x_found):
    print(pints.strfloat(x) + '    ' + pints.strfloat(x_true[k]))

fitted_values = problem.evaluate(x_found)

plt.figure()
plt.suptitle('Generated data + simulation with fit parameters')
plt.subplot(2, 1, 1)
plt.xlabel('Time (ms)')
plt.ylabel('Vm (mV)')
plt.plot(times, noisy_values[:, 0])
plt.plot(times, fitted_values[:, 0])
plt.subplot(2, 1, 2)
plt.xlabel('Time (ms)')
plt.ylabel('[Ca]i (mol/L)')
plt.plot(times, noisy_values[:, 1])
plt.plot(times, fitted_values[:, 1])
plt.show()

