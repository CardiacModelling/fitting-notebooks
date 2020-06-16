#!/usr/bin/env python3
#
#
# Code library for use in the ion currents fitting tutorial.
#
#
import matplotlib.pyplot as plt
import numpy as np

import pints
import myokit
import myokit.lib.hh


class Boundaries(pints.Boundaries):
    """
    A boundaries class that implements the maximum-rate boundaries used in Beattie et al.

    Parameters
    ----------
    g_min
        A cell-specific lower boundary on the conductance.
    """

    # Limits for a-type parameters (untransformed)
    a_min = 1e-7
    a_max = 1e3

    # Limits for g-type parameters
    b_min = 1e-7
    b_max = 0.4

    # Limits for maximum rate coefficients
    km_min = 1.67e-5
    km_max = 1e3

    # Voltages used when determining maximum rate coefficients
    v_low = -120
    v_high = 60

    def __init__(self, g_min=0.1):

        self.g_min = g_min
        self.g_max = 10 * g_min

        # Univariate paramater bounds
        self.lower = np.array([
            self.a_min, self.b_min,
            self.a_min, self.b_min,
            self.a_min, self.b_min,
            self.a_min, self.b_min,
            self.g_min,
        ])
        self.upper = np.array([
            self.a_max, self.b_max,
            self.a_max, self.b_max,
            self.a_max, self.b_max,
            self.a_max, self.b_max,
            self.g_max,
        ])

    def n_parameters(self):
        return 9

    def check(self, parameters):

        # Check parameter boundaries
        if np.any(parameters <= self.lower) or np.any(parameters >= self.upper):
            return False

        # Check rate boundaries
        k1m = parameters[0] * np.exp(parameters[1] * self.v_high)
        if k1m <= self.km_min or k1m >= self.km_max:
            return False
        k2m = parameters[2] * np.exp(-parameters[3] * self.v_low)
        if k2m <= self.km_min or k2m >= self.km_max:
            return False
        k3m = parameters[4] * np.exp(parameters[5] * self.v_high)
        if k3m <= self.km_min or k3m >= self.km_max:
            return False
        k4m = parameters[6] * np.exp(-parameters[7] * self.v_low)
        if k4m <= self.km_min or k4m >= self.km_max:
            return False

        # All tests passed!
        return True

    def _sample_partial(self, v):
        """Samples a pair of kinetic parameters"""
        for i in range(100):
            a = np.exp(np.random.uniform(np.log(self.a_min), np.log(self.a_max)))
            b = np.random.uniform(self.b_min, self.b_max)
            km = a * np.exp(b * v)
            if km > self.km_min and km < self.km_max:
                return a, b
        raise ValueError('Too many iterations')

    def sample(self, n=1):
        points = np.zeros((n, 9))
        for i in range(n):
            points[i, 0:2] = self._sample_partial(self.v_high)
            points[i, 2:4] = self._sample_partial(-self.v_low)
            points[i, 4:6] = self._sample_partial(self.v_high)
            points[i, 6:8] = self._sample_partial(-self.v_low)
            points[i, 8] = np.random.uniform(self.g_min, self.g_max)
        return points


def univariate_boundary_plot(a_log=False, b_log=False):
    """
    Plots the univariate boundaries, as defined in the boundaries tutorial.

    The limits plotted are obtained from the :class:`Boundaries` class.

    Parameters
    ----------
    a_log
        Set to True to plot a-type parameters on a logarithmic scale.
    b_log
        Set to True to plot b-type parameters on a logarithmic scale.
    """
    # Create some boundaries, to get lower and upper limits from
    b = Boundaries()

    # Create a figure
    fig = plt.figure(figsize=(16, 2.6))
    fig.subplots_adjust(wspace=0.4)

    def prepare_panel(ax):
        if a_log:
            ax.set_xscale('log')
            ax.set_xlim(0.1 * b.a_min, 7 * b.a_max)
        else:
            ax.set_xlim(b.a_min - 200, b.a_max + 200)
        if b_log:
            ax.set_yscale('log')
            ax.set_ylim(0.2 * b.b_min, 5 * b.b_max)
        else:
            ax.set_ylim(b.b_min - 0.1, b.b_max + 0.1)
        ax.axvline(b.a_min, color='#bbbbbb')
        ax.axvline(b.a_max, color='#bbbbbb')
        ax.axhline(b.b_min, color='#bbbbbb')
        ax.axhline(b.b_max, color='#bbbbbb')

    ax1 = fig.add_subplot(1, 5, 1)
    prepare_panel(ax1)
    ax1.set_xlabel('p1')
    ax1.set_ylabel('p2')

    ax2 = fig.add_subplot(1, 5, 2)
    prepare_panel(ax2)
    ax2.set_xlabel('p3')
    ax2.set_ylabel('p4')

    ax3 = fig.add_subplot(1, 5, 3)
    prepare_panel(ax3)
    ax3.set_xlabel('p5')
    ax3.set_ylabel('p6')

    ax4 = fig.add_subplot(1, 5, 4)
    prepare_panel(ax4)
    ax4.set_xlabel('p7')
    ax4.set_ylabel('p8')

    ax5 = fig.add_subplot(1, 5, 5)
    ax5.set_xlabel('p9')
    ax5.set_xlim(0, b.g_max * 1.1)
    ax5.set_ylim(-2.2, 2.2)
    ax5.axvline(b.g_min, color='#bbbbbb')
    ax5.axvline(b.g_max, color='#bbbbbb')

    return ax1, ax2, ax3, ax4, ax5


def multivariate_boundary_plot(a_log=False):
    """
    Plots the multivariate boundaries, as defined in the boundaries tutorial.

    Parameters
    ----------
    a_log
        Set to True to plot a-type parameters on a logarithmic scale.

    """
    # Create some boundaries, to get lower and upper limits from
    b = Boundaries()

    # Define a range on which to plot the rate coefficient boundaries
    if a_log:
        # We use a range that's linear in the log-transformed space
        px = np.exp(np.linspace(np.log(b.a_min), np.log(b.a_max), 200))
    else:
        px = np.linspace(b.a_min, b.a_max, 200)

    # Calculate the lower and upper boundaries on p2 and p4 (which are the same as those on p6 and p8)
    p2_min = np.log(b.km_min / px) / 60
    p2_max = np.log(b.km_max / px) / 60
    p4_min = np.log(b.km_min / px) / 120
    p4_max = np.log(b.km_max / px) / 120

    # But p2,p6 and p4,p8 are also bounded by the parameter boundaries, so add that in too:
    p2_min = np.maximum(p2_min, b.b_min)
    p4_min = np.maximum(p4_min, b.b_min)

    # Create a figure
    fig = plt.figure(figsize=(16, 2.6))
    fig.subplots_adjust(wspace=0.4)

    def prepare_panel(ax):
        if a_log:
            ax.set_xscale('log')
            ax.set_xlim(0.3 * b.a_min, 3 * b.a_max)
        else:
            ax.set_xlim(b.a_min - 50, b.a_max + 50)
        ax.set_ylim(b.b_min - 0.02, b.b_max + 0.02)
        ax.axvline(b.a_min, color='#bbbbbb')
        ax.axvline(b.a_max, color='#bbbbbb')
        ax.axhline(b.b_min, color='#bbbbbb')
        ax.axhline(b.b_max, color='#bbbbbb')

    ax1 = fig.add_subplot(1, 5, 1)
    prepare_panel(ax1)
    ax1.set_xlabel('p1')
    ax1.set_ylabel('p2')
    ax1.plot(px, p2_min)
    ax1.plot(px, p2_max)
    ax1.fill_between(px, p2_min, p2_max, color='#dddddd')

    ax2 = fig.add_subplot(1, 5, 2)
    prepare_panel(ax2)
    ax2.set_xlabel('p3')
    ax2.set_ylabel('p4')
    ax2.plot(px, p4_min)
    ax2.plot(px, p4_max)
    ax2.fill_between(px, p4_min, p4_max, color='#dddddd')

    ax3 = fig.add_subplot(1, 5, 3)
    prepare_panel(ax3)
    ax3.set_xlabel('p5')
    ax3.set_ylabel('p6')
    ax3.plot(px, p2_min)
    ax3.plot(px, p2_max)
    ax3.fill_between(px, p2_min, p2_max, color='#dddddd')

    ax4 = fig.add_subplot(1, 5, 4)
    prepare_panel(ax4)
    ax4.set_xlabel('p7')
    ax4.set_ylabel('p8')
    ax4.plot(px, p4_min)
    ax4.plot(px, p4_max)
    ax4.fill_between(px, p4_min, p4_max, color='#dddddd')

    ax5 = fig.add_subplot(1, 5, 5)
    ax5.set_xlabel('p9')
    ax5.set_xlim(0, b.g_max * 1.1)
    ax5.set_ylim(-2.2, 2.2)
    ax5.axvline(b.g_min, color='#bbbbbb')
    ax5.axvline(b.g_max, color='#bbbbbb')

    return ax1, ax2, ax3, ax4, ax5


class ModelHHSolver(pints.ForwardModel):
    """
    A forward model that runs simulations on step protocols, using an
    analytical solving method for Hodgkin-Huxley models.
    """

    def __init__(self, protocol):

        # Load a model, and isolate the HH ion current model part
        model = myokit.load_model('resources/beattie-2017-ikr-hh.mmt')
        parameters = ['ikr.p' + str(1 + i) for i in range(9)]
        hh_model = myokit.lib.hh.HHModel.from_component(
            model.get('ikr'), parameters=parameters)

        # Create an analytical simulation
        self.sim = myokit.lib.hh.AnalyticalSimulation(hh_model, protocol)

        # Set the -80mV steady state as the default state
        self.sim.set_default_state(hh_model.steady_state(-80))

    def n_parameters(self):
        return 9

    def simulate(self, parameters, times):

        # Reset, apply parameters, and run
        self.sim.reset()
        self.sim.set_parameters(parameters)
        tmax = times[-1] + (times[-1] - times[-2])
        log = self.sim.run(tmax, log_times=times)
        return log['ikr.IKr']

