#!/usr/bin/env python3
print('Starting')
import sys
import timeit

import myokit
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

n = 0
if len(sys.argv) > 1:
    n = int(sys.argv[1])
if n < 1:
    n = 200


np.random.seed(1)

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
Vc = 0 [mV] in [mV]
Cm = 40 [pF] in [pF]
Cmf = 0.95
Cp = 4.5 [pF] in [pF]
Cpf = 0.95
Cf = 0.3 [pF] in [pF]
Rs = 0.01 [GOhm] in [GOhm]
Rsf = 0.95
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
    #'alpha': (0, 0.8),          # Safe range
    #'beta': (0, 0.8),           # Safe rage
    #'I': (0, 1000),            # Guesstimate
    #'Cm': (5, 50),              # No cell to small cell
    #'Cmf': (0, 1.2),            # No compensation to overcompensation
    'Cp': (0.1, 10),            # Based on ex293 cells
    'Cpf': (0, 1.2),            # No compensation to overcompensation
    #'Rs': (5e-3, 60e-3),        # Based on ex293 cells
    #'Rsf': (0, 1.2),            # No compensation to overcompensation
    'Cf': (0.01, 1),            # Based on appendix B
    'Rf': (0.01, 1),            # Based on appendix B
    'tau_amp': (10e-6, 100e-6), # Based on appendix C
    #'tau_sum': (1e-3, 100e-3),  # Based on manuals
}
nparam = len(parameters)

def lhs(parameters, n):
    ps = np.zeros((n, len(parameters)))
    a = np.arange(n)
    w = 1 / n
    for i, bounds in enumerate(parameters.values()):
        lo, hi = bounds
        np.random.shuffle(a)
        x = lo + (hi - lo) * (a + np.random.uniform(size=n)) * w
        ps[:, i] = x
    return ps

psets = lhs(parameters, n)
alpha = max((1 + n)**(-0.6), 1e-4)
print(f'Alpha {alpha}')

if False:
    # Show parameters
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot()
    bounds = list(parameters.values())[:2]
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


def stat(d, ar):
    k = 'amp.Vm'
    v = d[k]
    ar[0] = d.integrate(k)[-1]
    ar[1] = np.max(v)
    ar[2] = np.mean(v)
    ar[3] = np.std(v)

    k = 'amp.I_obs'
    v = d[k]
    ar[4] = d.integrate(k)[-1]
    ar[5] = np.min(v)
    ar[6] = np.max(v)
    ar[7] = np.mean(v)
    ar[8] = np.std(v)


labels = [
    '$\Sigma$Vm',
    'max',
    'mean',
    'std',
    '$\Sigma$I',
    'min',
    'max',
    'mean',
    'std',
]


# Run
print('Running simulations')
tsim = 10
log_vars = ['amp.time', 'amp.Vm', 'amp.I_obs']

# Baseline simulation and stats
d0 = s.run(tsim, log=log_vars).npview()
nstat = len(labels)
stats0 = np.zeros(nstat)
stat(d0, stats0)

# Collect for all parameters
stats = np.zeros((n, nstat))
ds = []

j = 0
dt = 0.05
time = timeit.default_timer()
tn = time + dt
for i, pset in enumerate(psets):
    s.reset()
    for k, p in zip(parameters, pset):
        s.set_constant(f'amp.{k}', p)
    d = s.run(tsim, log=log_vars).npview()
    ds.append(d)

    k = 'amp.Vm'
    v = d[k]
    stats[i][0] = d.integrate(k)[-1]
    #stats[i][1] = np.min(v)
    stats[i][1] = np.max(v)
    stats[i][2] = np.mean(v)
    stats[i][3] = np.std(v)
    k = 'amp.I_obs'
    v = d[k]
    stats[i][4] = d.integrate(k)[-1]
    stats[i][5] = np.min(v)
    stats[i][6] = np.max(v)
    stats[i][7] = np.mean(v)
    stats[i][8] = np.std(v)

    if timeit.default_timer() >= tn:
        print('.', end='')
        j += 1
        if j == 76:
            print(f' {(100*i)//n}%')
            j = 0
        else:
            sys.stdout.flush()
        tn += dt

stats /= stats0
time = timeit.default_timer() - time
print(f'Ran {n} simulations in {time:.3f}s')

# Calculate correlation coefficients
rs = np.zeros((nparam, nstat))
for i in range(nparam):
    for j in range(nstat):
        rs[i][j] = r = np.corrcoef(psets[:, i], stats[:, j])[0, 1]


# Create figures
print('Creating figures')
cmap = matplotlib.cm.get_cmap('viridis')


def swarmx(y, nbins=None):
    """
    Returns x coordinates for the points in ``y``, so that plotting ``x`` and
    ``y`` results in a bee swarm plot.
    """
    nbins = len(y) // 6

    # Get upper bounds of bins
    y = np.asarray(y)
    x = np.zeros(len(y))
    ylo = np.min(y)
    yhi = np.max(y)
    dy = (yhi - ylo) / nbins
    ybins = np.linspace(ylo + dy, yhi - dy, nbins - 1)

    # Divide indices into bins
    i = np.arange(len(y))
    ibs = [0] * nbins
    ybs = [0] * nbins
    nmax = 0
    for j, ybin in enumerate(ybins):
        f = y <= ybin
        ibs[j], ybs[j] = i[f], y[f]
        nmax = max(nmax, len(ibs[j]))
        f = ~f
        i, y = i[f], y[f]
    ibs[-1], ybs[-1] = i, y
    nmax = max(nmax, len(ibs[-1]))

    # Assign x indices
    dx = 1 / (nmax // 2)
    for i, y in zip(ibs, ybs):
        if len(i) > 1:
            j = len(i) % 2
            i = i[np.argsort(y)]
            a = i[j::2]
            b = i[j + 1::2]
            x[a] = (0.5 + j / 3 + np.arange(len(a))) * dx
            x[b] = (0.5 + j / 3 + np.arange(len(b))) * -dx

    return x


if False:
    fig = plt.figure(figsize=(14, 7))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_xlabel('Time (ms')
    ax1.set_ylabel('Vm (mV)')
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_xlabel('Time (ms')
    ax2.set_ylabel('$I_{obs}$ (pA)')

    for d in ds:
        ax1.plot(d.time(), d['amp.Vm'], color='blue', alpha=alpha)
        ax2.plot(d.time(), d['amp.I_obs'], color='red', alpha=alpha)
    ax1.plot(d0.time(), d0['amp.Vm'], color='k')
    ax2.plot(d0.time(), d0['amp.I_obs'], color='k')




#
# Correlation coefficients
#
rsum = np.sum(np.abs(rs), axis=1)
rsum /= np.sum(rsum)

fig = plt.figure(figsize=(10, 10))
fig.subplots_adjust(0.1, 0.05, 0.90, 0.95)
ax = fig.add_subplot()
ax.invert_yaxis()
ax.set_xticks(range(nstat))
ax.set_yticks(range(nparam))
ax.set_xticklabels(labels)
ax.set_yticklabels(parameters.keys())
plt.xlim(-0.5, nstat - 0.5)
plt.ylim(-0.5, nparam - 0.5)
for i, row in enumerate(rs):
    for j, r in enumerate(row):
        x = 2 * i
        w, h = 2, 1
        ax.add_patch(plt.Rectangle(
            (j - 0.5, i - 0.5), 1, 1, facecolor=cmap(abs(r)), alpha=0.6))
        ax.text(j, i, f'{r:<1.2f}', ha='center', va='center')
    ax.text(j + 1, i, f'{rsum[i]:<1.2f}')
ax.text((nstat - 1) / 2, nparam - 0.25, f'n = {n}', ha='center', va='center')
plt.savefig('stats-coeff.png')


#
# All stats
#
n_striping = max(1, n // 2000)

xs = []
fig = plt.figure(figsize=(14, 7))
ax1 = fig.add_subplot()
ax1.set_xticks(np.arange(nstat, dtype=int))
ax1.set_xticklabels(labels)
for i in range(nstat):
    xs.append(0.45 * swarmx(stats[:, i][::n_striping]))
    ax1.plot(i + xs[i], stats[:, i][::n_striping].T, 'x', alpha=0.3)
    ax1.plot(i, 1, 'kx')
fig.savefig('stats.png')

#
# Stats, colour coded per parameter
#
for j, p in enumerate(parameters):
    norm = matplotlib.colors.Normalize(*parameters[p])
    colors = norm(psets[:, j][::n_striping])
    kwargs = dict(marker='x', c=colors, cmap=cmap, alpha=0.3)

    fig = plt.figure(figsize=(14, 7))
    fig.subplots_adjust(0.025, 0.05, 0.99, 0.95, 0.08)
    fig.text(0.5, 0.97, p, ha='center')
    ax1 = fig.add_subplot()
    ax1.set_xticks(np.arange(nstat, dtype=int))
    ax1.set_xticklabels(labels)
    for i in range(nstat):
        ax1.scatter(i + xs[i], stats[:, i][::n_striping].T, **kwargs)
        ax1.text(0.1 + 0.2 * i, 1.01, f'{rs[j][i]:.2f}', ha='center',
                 transform=ax1.transAxes)

    fig.savefig(f'stats-{1 + j}.png')

