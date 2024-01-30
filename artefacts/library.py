#!/usr/bin/env python3
"""
Shared functions for the artefact notebooks.
"""
import numpy as np


def _fit_exponential(t, I, Iss, i1, i2, cutoff, invert, plot=False):
    """
    Fits a single exponential to ``I - Iss`` on the segment ``i1:i2``.
    
    The exponential is assumed to be decreasing. For an increasing exponential,
    set ``invert=True``.
    
    If the signal on ``i1:i2`` dips below ``cutoff``, the upper bound ``i2``
    will be reduced.
    
    Returns ``tau, I0``.
    """

    # Find points for exponential
    ilog = I[i1:i2] - Iss
    if invert:
        ilog = -ilog

    # If any zeroes are found, this is almost certainly due to noise.
    if np.any(ilog < 0):
        # Find where the signal dips below a set signal-to-noise ratio
        i = np.where(ilog < cutoff)[0][0]
        # Cut off values after that point, and update i2 accordingly
        ilog = ilog[:i]
        i2 = i1 + i
    tlog = t[i1:i2]
    ilog = np.log(ilog)

    # Calculate means, residuals, coefficients
    mx = np.mean(tlog)
    my = np.mean(ilog)
    rx = tlog - mx
    ry = ilog - my
    b = np.sum(rx * ry) / np.sum(rx ** 2)
    a = my - b * mx

    # Get tau and I0 estimates
    tau = -1 / b
    if invert:
        I0 = -np.exp(a) + Iss
    else:
        I0 = np.exp(a) + Iss

    if plot:
        print(f'Tau* = {tau:.3f} ms')
        print(f'I0* = {I0:.3f} pA')

        fig = plt.figure()
        ax = fig.add_subplot()
        ax.plot(tlog, ilog, lw=3, label='Data')
        ax.plot(tlog, a + b * tlog, '--', label='Least squares fit')
        ax.legend()
        plt.show()

    return tau, I0
    
    
def _integrate_current(t, I, Iss, i0, i3, cutoff, dt, invert):
    """
    Integrates the I[i0:i3] and returns the result.
    
    If the initial points are below cutoff, ``i0`` will be increased.
    """
    # Get segment containing transient
    iup = I[i0:i3] - Iss
    if invert:
        iup = -iup

    # Increase i0 if necessary    
    i = np.where(iup > cutoff)[0][0]
    iup = iup[i:]
    i0 += i
    
    # Integrate
    if dt is None:
        return np.trapz(iup, t[i0:i3])
    return np.trapz(iup, dx=dt)
    

def estimate_cell_parameters(
        t, I, T, dV, dt=None, f1=0.05, f2=0.8, f3=0.8, f4=1):
    """
    
    Arguments:
    
    ``t``
        A time vector, starting at 0 and going up to and/or including time 2T.
    ``I``
        The corresponding current vector.
    ``T``
        The duration of both steps (each has duration T).
    ``dV``
        The difference ``V1 - V2``, where ``V1`` is the command voltage during
        the first, and ``V2`` during the second step.
    ``dt``
        Sampling interval, or ``None`` to assume irregular sampling.
    ``f1=0.1``
        The start of the segment where an exponential is fit, as a fraction of
        ``T``.
    ``f2=0.8``
        The end of the segment where an exponential is fit, as a fraction of 
        ``T``. If the given signal is noisy, a shorter interval may be used.
    ``f3=0.8``
        The start of the segment used to estimate the steady-state current, as
        a fraction of ``T``.
    ``f4=1.0``
        The end of the segment used to estimate the steady-state current, as
        a fraction of ``T``.

    Returns:
    
    ``Rs``
        The estimated series (or access) resistance.
    ``Rm``
        The estimated membrane resistance.
    ``Cm``
        The estimated membrane capacitance.
    ``points``
        A tuple ``(tau, I01, a1, b1, Iss1, c1, d1, I02, a2, b2, Iss2, c2, d2)``
        where ``tau`` is the estimated time constant, ``Iss`` are current
        steady-state values, ``I0`` are initial values for the fitted
        transients, and where the remaining numbers give array indices suitable
        for drawing fitted transients and steady states.
       
    """
    # Get indices
    f = np.array((f1, f2, f3, f4, 1, 1 + f1, 1 + f2, 1 + f3, 1 + f4)) * T
    if dt is None:
        i = np.searchsorted(t, f)
    else:
        i = np.rint(f / dt).astype(int)
    i1, i2, i3, i4, iT, i5, i6, i7, i8 = i        
        
    # Estimate I1 and I2
    I1 = np.mean(I[i3:i4])
    I2 = np.mean(I[i7:i8])
    dI = I1 - I2
    
    # Estimate the noise
    cutoff = np.std(I[i3:i4]) + np.std(I[i7:i8])
        
    # Estimate tau and I0
    tau1, I01 = _fit_exponential(t, I, I1, i1, i2, cutoff, False)
    tau2, I02 = _fit_exponential(t - T, I, I2, i5, i6, cutoff, True)
    tau = 0.5 * (tau1 + tau2)
    
    # Estimate charge
    Q11 = _integrate_current(t, I, I1, 0, i3, cutoff, dt, False)
    Q12 = _integrate_current(t, I, I2, iT, i7, cutoff, dt, True)
    Qm = 0.5 * (Q11 + Q12) + tau * dI

    # Estimate rest
    Rs = tau * dV / Qm
    Rm = dV / dI - Rs
    Cm = Qm * (Rm + Rs) / (Rm * dV)
    
    # Gather points for drawing
    points = (tau, I01, i1, i2, I1, i3, i4, I02, i5, i6, I2, i7, i8)
    
    return Rs, Rm, Cm, points


def _test_one_shot():
    """ Generates data and shows the results of a one-shot test. """

    import myokit
    import matplotlib.pyplot as plt
    
    m = myokit.parse_model('''
        [[model]]
        amp.Vm = -70

        [engine]
        time = 0 [ms] in [ms] bind time
        pace = 0 bind pace

        [amp]
        Rs = 11.7e-3 [GOhm] in [GOhm]
        Cm = 31.89 [pF] in [pF]
        Rm = 0.5003 [GOhm] in [GOhm]
        Vc = 1 [mV] * engine.pace
            in [mV]
        dot(Vm) = (Rm * I_obs - Vm) / (Rm * Cm)
            in [mV]
        I_obs = (Vc - Vm) / Rs
            in [pA]
        ''')
    m.check_units(myokit.UNIT_STRICT)

    T = 10
    V1 = -60
    V2 = -70
    dV = V1 - V2

    p = myokit.Protocol()
    p.schedule(start=0, level=V1, duration=T, period=2*T)
    p.schedule(start=T, level=V2, duration=T, period=2*T)
    
    if True:
        N = 2000
        dt = (2 * T) / N
        print(f'Using dt={dt} for a total of {N} samples')
    else:
        dt=None
        print('Using adaptive time steps')
    
    s = myokit.Simulation(m, p)
    s.set_tolerance(1e-12, 1e-12)
    s.pre(2 * T)
    s.reset()
    d = s.run(2 * T, log_interval=dt).npview()
    t, I = d.time(), d['amp.I_obs']
    
    #I += np.random.normal(0, 5, size=t.shape)
    
    Rs, Rm, Cm, points = estimate_cell_parameters(t, I, T, dV, dt)
    print(f'Estimated Rs {1e3 * Rs:>5.1f} MOhm')
    print(f'Estimated Rm {1e3 * Rm:>5.1f} MOhm')
    print(f'Estimated Cm {Cm:>5.2f} pF')
    
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot()
    ax.plot(t, I, label='$Iobs$')
    kw = dict(color='tab:orange', lw=2)
    tau, I01, a1, b1, I1, c1, d1, I02, a2, b2, I2, c2, d2 = points
    ax.plot((t[c1], t[d1 - 1]), (I1, I1), **kw)
    ax.plot((t[c2], t[d2 - 1]), (I2, I2), **kw)
    te = t[a1:(b1 + a1) // 3]
    ax.plot(te, I1 - (I1 - I01) * np.exp(-te / tau), **kw)
    ax.plot(T + te, I2 - (I2 - I02) * np.exp(-te / tau), **kw)
    ax.legend(loc='lower right')
    plt.show()


    
if __name__ == '__main__':
    _test_one_shot()
