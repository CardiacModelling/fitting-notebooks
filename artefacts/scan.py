#!/usr/bin/env python3
print('Starting')
import sys
import timeit

import myokit
import numpy as np
import matplotlib.pyplot as plt


print('Creating simulation')
m = myokit.parse_model('''
[[model]]
desc: Compensated model
amp.Vm = -80
amp.Vp = -80
amp.Vo = -80
amp.Ve = -80
amp.Vr = -80

[amp]
alpha = 0.6
beta = 0.6
time = 0 [ms] in [ms] bind time
I = 50 [pA] in [pA]
E = 1 [mV] in [mV]
Vc = -20 [mV] in [mV]
Cm = 40 [pF] in [pF]
Cmf = 1
Cp = 4.5 [pF] in [pF]
Cpf = 1
Cf = 0.3 [pF] in [pF]
Rs = 0.01 [GOhm] in [GOhm]
Rsf = 1
Rf = 0.025 [GOhm] in [GOhm]
tau_amp = 50e-6 [ms] in [ms]
tau_sum = 40e-3 [ms] in [ms]
Cp_est = Cp * Cpf
    in [pF]
Cm_est = Cm * Cmf
    in [pF]
Rs_est = Rs * Rsf
    in [GOhm]
dot(Vm) = (Vp + E - Vm) / (Rs * Cm) - I / Cm
    in [mV]
dot(Vp) = ((Vo - Vp) / Rf - (Vp + E - Vm) / Rs +
            Cf * dot(Vo) + Cm * dot(Ve) + Cp * dot(Vr)
          ) / (Cp + Cf) : Eq 2a
    in [mV]
dot(Vo) = (Vr - Vp) / tau_amp
    in [mV]
dot(Ve) = (Vc - Ve) / if(tau < 1e-12 [ms], 1e-12 [ms], tau)
    in [mV]
    tau = (1 - beta) * Rs_est * Cm_est
        in [ms]
dot(Vr) = (Vc + alpha * Rs_est * I_obs 
              + beta * Rs_est * Cm_est * dot(Ve) - Vr) / tau_sum
    in [mV]
I_obs = (Vo - Vr) / Rf
    in [pA]
''')
m.check_units(myokit.UNIT_STRICT)
s = myokit.Simulation(m)

# Generate Latin Hypercube samples, for Gary
print('Generating samples')
parameters = {
#    'alpha': (0, 1),        # True range
#    'beta': (0, 1),         # True rage
    'I': (0, 1000),         # Guesstimate
    'Cm': (10, 40),         # No cell to small cell
    'Cmf': (0, 1.2),        # No compensation to overcompensation
    'Cp': (0, 10),          # Based on ex293 cells
    'Cpf': (0, 1.2),        # No compensation to overcompensation
    'Rs': (0, 60),          # Based on ex293 cells
    'Rsf': (0, 1.2),        # No compensation to overcompensation
    'Cf': (0.01, 1),            # Based on appendix B
    'Rf': (0.01, 1),            # Based on appendix B
    'tau_amp': (10e-6, 100e-6), # Based on appendix C
    'tau_sum': (5e-6, 70e-6),   # Based on Lei 2020
}

def lhs(parameters, n):
    ps = []
    a = np.arange(n)
    w = 1 / n
    for p, bounds in parameters.items():
        lo, hi = bounds
        np.random.shuffle(a)
        x = lo + (hi - lo) * (a + np.random.uniform(size=n)) * w
        ps.append(x)
    return np.array(ps).T

n = 20000
psets = lhs(parameters, n)
alpha = max((1 + n)**(-0.6), 1e-3)
print(alpha)

'''
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot()
bounds = list(parameters.values())[:2]
print(bounds)
padding = [0.05 * (b[1] - b[0]) for b in bounds]
ax.set_xlim(bounds[0][0] - padding[0], bounds[0][1] + padding[0])
ax.set_ylim(bounds[1][0] - padding[1], bounds[1][1] + padding[1])
if n < 50:
    for i in np.arange(n):
        ax.axhline((i + 1) / n, ls='--', color='#cccccc')
        ax.axvline((i + 1) / n, ls='--', color='#cccccc')
for i in range(m):
    ps = lhs(parameters, n)
    ax.plot(ps[0], ps[1], 'x')
plt.show()
'''

# Create figure
print('Creating figure')
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14, 7))
ax1 = fig.add_subplot(1, 2, 1)
ax1.set_xlabel('Time (ms')
ax1.set_ylabel('Vm (mV)')
ax2 = fig.add_subplot(1, 2, 2)
ax2.set_xlabel('Time (ms')
ax2.set_ylabel('$I_{obs}$ (pA)')

# Run
print('Running simulations')
tsim = 5
log_vars = ['amp.time', 'amp.Vm', 'amp.I_obs']


j = 0
dt = 0.05
tn = timeit.default_timer() + dt
for i, pset in enumerate(psets):
    s.reset()
    for k, p in zip(parameters, pset):
        s.set_constant(f'amp.{k}', p)
    d = s.run(tsim, log=log_vars)

    ax1.plot(d.time(), d['amp.Vm'], color='blue', alpha=alpha)
    ax2.plot(d.time(), d['amp.I_obs'], color='red', alpha=alpha)
    
    if timeit.default_timer() >= tn:
        print('.', end='')
        j += 1
        if j == 76:
            print(f' {(100*i)//n}%')
            j = 0
        else:
            sys.stdout.flush()
        tn += dt
print()


TODO
- Calculate area under curves
- Calculate min & max of curves
- Calculate min & max of derivatives
- Calculate min & max of 2nd derivatives
- Split results per variables


plt.show()
