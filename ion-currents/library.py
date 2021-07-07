#!/usr/bin/env python3
#
#
# Code library for use in the ion currents fitting notebooks.
#
#
import fnmatch
import glob
import os

import matplotlib.pyplot as plt
import numpy as np

import pints
import myokit
import myokit.lib.hh


class Boundaries(pints.Boundaries):
    """
    A boundaries class that implements the maximum-rate boundaries used in
    Beattie et al.

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
        if (np.any(parameters <= self.lower)
                or np.any(parameters >= self.upper):
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
            a = np.exp(np.random.uniform(
                np.log(self.a_min), np.log(self.a_max)))
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
    Plots the univariate boundaries, as defined in the boundaries notebook.

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
    Plots the multivariate boundaries, as defined in the boundaries notebook.

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

    # Calculate the lower and upper boundaries on p2 and p4 (which are the same
    # as those on p6 and p8)
    p2_min = np.log(b.km_min / px) / 60
    p2_max = np.log(b.km_max / px) / 60
    p4_min = np.log(b.km_min / px) / 120
    p4_max = np.log(b.km_max / px) / 120

    # But p2,p6 and p4,p8 are also bounded by the parameter boundaries, so add
    # that in too:
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


def boundary_plot_point(axes, x, *args, **kwargs):
    """
    Adds one or multiple points to a univariate or multivariate boundary plot.
    """
    if len(x.shape) == 1:
        x = x.reshape((1, len(x)))

    axes[0].plot(x[:, 0], x[:, 1], *args, **kwargs)
    axes[1].plot(x[:, 2], x[:, 3], *args, **kwargs)
    axes[2].plot(x[:, 4], x[:, 5], *args, **kwargs)
    axes[3].plot(x[:, 6], x[:, 7], *args, **kwargs)
    axes[4].plot(x[:, 8], 0 * x[:, 8], *args, **kwargs)


class ModelCVODESolver(pints.ForwardModel):
    """A forward model that runs simulations with CVODE."""

    def __init__(self, protocol):

        # Load a model, and isolate the HH ion current model part
        model = myokit.load_model('resources/beattie-2017-ikr-hh.mmt')
        parameters = ['ikr.p' + str(1 + i) for i in range(9)]
        hh_model = myokit.lib.hh.HHModel.from_component(
            model.get('ikr'), parameters=parameters)

        # Create a CVODE Simulation
        self.sim = myokit.Simulation(model, protocol)

        # Set the -80mV steady state as the default state
        self.sim.set_default_state(hh_model.steady_state(-80))

    def n_parameters(self):
        return 9

    def simulate(self, parameters, times):

        # Reset to default time and state
        self.sim.reset()

        # Apply parameters
        for i, p in enumerate(parameters):
            self.sim.set_constant('ikr.p' + str(1 + i), p)

        # Run
        tmax = times[-1] + (times[-1] - times[-2])
        try:
            log = self.sim.run(tmax, log_times=times, log=['ikr.IKr'])
            return log['ikr.IKr']
        except myokit.SimulationError:
            print('Error evaluating with parameters: ' + str(parameters))
            return np.nan * times


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


class LogTransform(object):
    """
    Performs forward and backward transformations on the alpha-parameters used
    in the Beattie et al. model.
    """

    def to_search(self, x):
        """Transforms from model to search space."""
        q = np.copy(x)
        q[0] = np.log(x[0])
        q[2] = np.log(x[2])
        q[4] = np.log(x[4])
        q[6] = np.log(x[6])
        return q

    def to_model(self, q):
        """Transforms from search to model space."""
        x = np.copy(q)
        x[0] = np.exp(q[0])
        x[2] = np.exp(q[2])
        x[4] = np.exp(q[4])
        x[6] = np.exp(q[6])
        return x


class TransformedForwardModel(pints.ForwardModel):
    """
    Wraps around a ``pints.ForwardModel`` and applies parameter
    transformations.
    """

    def __init__(self, model, transform):
        self._model = model
        self._transform = transform

    def n_parameters(self):
        return self._model.n_parameters()

    def simulate(self, search_parameters, times):
        model_parameters = self._transform.to_model(search_parameters)
        return self._model.simulate(model_parameters, times)


class TransformedErrorMeasure(pints.ErrorMeasure):
    """
    Wraps around a ``pints.ErrorMeasure`` and applies parameter
    transformations.
    """

    def __init__(self, error, transform):
        self._error = error
        self._transform = transform

    def n_parameters(self):
        return self._error.n_parameters()

    def __call__(self, search_parameters):
        return self._error(self._transform.to_model(search_parameters))


class TransformedBoundaries(pints.Boundaries):
    """
    Wraps around a ``pints.Boundaries`` object and applies parameter
    transformations.
    """
    def __init__(self, boundaries, transform):
        self._boundaries = boundaries
        self._transform = transform

    def check(self, search_parameters):
        model_parameters = self._transform.to_model(search_parameters)
        return self._boundaries.check(model_parameters)

    def n_parameters(self):
        return self._boundaries.n_parameters()

    def sample(self, n):
        model_parameters = self._boundaries.sample(n)
        search_parameters = np.zeros(model_parameters.shape)
        for i, p in enumerate(model_parameters):
            search_parameters[i] = self._transform.to_search(p)
        return search_parameters


class reserve_base_name(object):
    """
    Context manager that reserves a location for storing results, but deletes
    any partial results if an error occurs.

    A template path is specified by the user, for example
    ``output/result.txt``. Upon entering, this is converted to a numbered path,
    for example ``output/result-i.txt``, such that ``i`` equals one plus the
    highest indice already found in the same directory. To "reserve" the path,
    a file is placed at ``output/result-i.txt``, which can be overwritten by
    the user. Finally, the path to the numbered file is returned.

    If an exception occurs within the manager's context, the numbered file is
    deleted, **along with any files starting with the same basename as the
    numbered path**. For example, if the numbered path is ``result-001.txt``,
    files such as ``result-001-log.dat`` will also be deleted.

    Example::

        with reserve_base_name('output/result.txt') as basename:
            # Write to output/result-001.txt
            with open(basename + '.txt', 'w') as f:
                f.write('Writing stuff')

        with reserve_base_name('output/result.txt') as basename:
            # Write to output/result-002-log.txt
            with open(basename + '-log.txt', 'w') as f:
                f.write('Writing stuff')

    Parameters
    ----------
    template_path
        A template for the path to store results at: to store results such as
        ``results-1.txt``, ``results-2.txt`` etc., pass in the template
        ``name='results.txt'``.

    """
    def __init__(self, template_path):

        # Split path into directory, basename, and extension
        dirname, basename = os.path.split(template_path)
        self._dirname = dirname
        self._basename, self._extension = os.path.splitext(basename)

        # Indice, as integer
        self._indice = None

        # Indice formatting (must be fixed width and start with hyphen)
        self._format = '-{:03d}'
        self._nformat = 4

    def __enter__(self):

        # Find potential indice
        fs = glob.glob(os.path.join(self._dirname, self._basename + '*'))
        if fs:
            i1 = len(self._basename) + 1
            i2 = i1 + self._nformat - 1
            fs = [int(os.path.basename(f)[i1:i2]) for f in fs]
            indice = max(fs)
        else:
            indice = 0

        # Make reservation
        running = True
        while running:
            indice += 1
            path = self._basename + self._format.format(indice)
            path = os.path.join(self._dirname, path + self._extension)
            f = None
            try:
                f = open(path, 'x')     # Note: Python 3.3+ only
                f.write('Reserved\n')
                running = False
            except FileExistsError:
                # File already exists, try next indice
                pass
            finally:
                if f is not None:
                    f.close()

        # Store indice
        self._indice = indice

        # Update stored basename
        self._basename += self._format.format(indice)

        # Return numbered path
        return os.path.join(self._dirname, self._basename + self._extension)

    def __exit__(self, exc_type, exc_val, exc_tb):

        # No exception? Then exit without deleting
        if exc_type is None:
            return

        # Delete files matching pattern
        pattern = os.path.join(self._dirname, self._basename + '*')
        for path in glob.glob(pattern):
            print('Removing unfinished result file: ' + path)
            os.remove(path)

        # Don't suppress the exception
        return False


def save(path, parameters, error, time, iterations, evaluations):
    """
    Stores a result at the given ``path``.

    Parameters
    ----------
    path
        The path to store the result at, e.g. ``output/result-123.txt``.
    parameters
        A list of paramater values.
    error
        The corresponding error (or likelihood or score).
    time
        The time taken to reach the result.
    iterations
        The number of iterations performed.
    evaluations
        The number of function evaluations performed.

    """
    error = float(error)
    time = float(time)
    iterations = int(iterations)
    evaluations = int(evaluations)

    print('Writing results to ' + str(path))
    with open(path, 'w') as f:
        f.write('error: ' + pints.strfloat(error).strip() + '\n')
        f.write('time: ' + pints.strfloat(time).strip() + '\n')
        f.write('iterations: ' + str(iterations) + '\n')
        f.write('evaluations: ' + str(evaluations) + '\n')
        f.write('parameters:\n')
        for p in parameters:
            f.write('    ' + pints.strfloat(p) + '\n')
    print('Done')


def load(template_path, n_parameters=9):
    """
    Loads and returns all results stored at a given ``template_path``.

    Parameters
    ----------
    template_path
        A template path, e.g. ``output/results.txt``, such that results can be
        found at ``output/results-001.txt``, ``output/results-002.txt``, etc.

    Returns
    -------
    A tuple ``(parameters, info)``, where ``parameters`` is a numpy array
    (with shape ``(n_entries, n_parameters)``) containing all obtained
    parameter sets, and where ``info`` is a numpy array containing one row per
    entry, and each row is structured as ``(run, error, time, iterations,
    evaluations)``. Both arrays are ordered by error (lowest error first).
    """
    # Split path into directory, base ('results'), and extension ('.txt')
    dirname, filename = os.path.split(template_path)
    basename, ext = os.path.splitext(filename)

    # Create pattern to find result files
    pattern = os.path.join(dirname, basename + '-*.txt')

    # Create empty lists
    parameters = []
    info = []

    # Find and process matching files
    for path in glob.glob(pattern):

        # Get run index from filename
        filename = os.path.split(path)[1]
        run = os.path.splitext(filename)[0]
        try:
            run = int(run.rsplit('-', 1)[1])
        except ValueError:
            print('Unable to parse filename, skipping ' + filename)
            continue

        # Naively parse file, warn and skip unparseable files
        error = time = iters = evals = params = None
        try:
            todo = 5
            with open(path, 'r') as f:
                for i in range(100):    # Give up after 100 lines
                    line = f.readline().strip()
                    if line.startswith('error:'):
                        error = float(line[6:])
                        todo -= 1
                    elif line.startswith('time:'):
                        time = float(line[5:])
                        todo -= 1
                    elif line.startswith('iterations:'):
                        iters = int(line[11:])
                        todo -= 1
                    elif line.startswith('evaluations:'):
                        evals = int(line[12:])
                        todo -= 1
                    elif line == 'parameters:':
                        params = [
                            float(f.readline()) for j in range(n_parameters)]
                        todo -= 1
                    if todo == 0:
                        break
                if todo:
                    print('Unable to find all information, skipping '
                          + filename)
                    continue

        except Exception as e:
            print('Error when parsing file, skipping ' + filename)
            print(e)
            continue

        # Store
        parameters.append(params)
        info.append(np.array([run, error, time, iters, evals]))

    # Convert to arrays
    parameters = np.array(parameters)
    info = np.array(info)

    # Sort by error
    if len(parameters) > 0:
        order = np.argsort(info[:, 1])
        parameters = parameters[order]
        info = info[order]

    return parameters, info


def count(template_path, n_parameters=9, parse=True):
    """
    Counts the number of results matching the given ``template_path``.

    Parameters
    ----------
    template_path
        A template path, e.g. using ``result.txt`` will count the number of
        files named ``result-x.txt`` where ``x`` can be parsed to an integer.
    n_parameters
        The expected number of parameters in each result file. This will be
        ignored if ``parse`` is ``False``.
    parse
        If set to ``True``, this method will read all files matching the
        template, and so count the number of valid, parseable files. If set to
        false any files matching the template will be counted, regardless of
        their content.
    """
    # Load and count all files
    if parse:
        parameters, info = load(template_path, n_parameters)
        return len(parameters)

    # Scan for files matching the template
    n = 0
    base, ext = os.path.splitext(template_path)
    pattern = base + '-*' + ext
    for path in glob.glob(pattern):
        # Chop off extension, and start of path
        path = os.path.splitext(path)[0]
        path = path[len(base) + 1:]

        # Attempt to parse as number
        try:
            run = int(path)
        except ValueError:
            continue
        n += 1

    return n


def fit(name, error, boundaries, transformation=None, repeats=1, cap=None):
    """
    Minimises the given ``error``, and stores the results in the directory
    ``name``.

    All files are called ``results-i.txt``, with ``i`` automatically increased
    until an available filename is found. Optimisations are run until either
    (1) the requested number of ``repeats`` is reached, or (2) until the
    specified directory contains ``cap`` results.

    Parameters
    ----------
    name
        The directory to store results in (a string).
    error
        A ``pints.ErrorMeasure`` to minimise (or a ``pints.LogLikelihood`` to
        maximise).
    boundaries
        A boundaries object, used to constrain the search and to sample initial
        starting points.
    transformation
        An optional transformation, to wrap around the error and boundaries.
    repeats
        The maximum number of optimisations to run (default is 1).
    cap
        The maximum number of results to obtain in the given directory (default
        is ``None``, for unlimited).

    """
    debug = False

    # Create a template path
    template_path = os.path.join(name, 'result.txt')

    # Get the number of parameters
    n_parameters = error.n_parameters()

    # Apply transformation, if given
    if transformation is not None:
        error = TransformedErrorMeasure(error, transformation)
        boundaries = TransformedBoundaries(boundaries, transformation)

    # Check the number of repeats
    repeats = int(repeats)
    if repeats < 1:
        raise ValueError('Number of repeats must be at least 1.')

    # Check the cap on total number of runs
    if cap is not None:
        cap = int(cap)
        if cap < 1:
            raise ValueError(
                'Cap on total number of runs must be at least 1 (or None).')

    # Run
    for i in range(repeats):

        # Cap the maximum number of runs
        cap_info = ''
        if cap:
            n = count(template_path, n_parameters=n_parameters, parse=False)
            if n >= cap:
                print()
                print('Maximum number of runs reached: terminating.')
                print()
                return
            cap_info = ' (run ' + str(n + 1) + ', capped at ' + str(cap) + ')'

        # Show configuration
        print()
        print('Repeat ' + str(1 + i) + ' of ' + str(repeats) + cap_info)
        print()

        # Get base filename to store results in
        with reserve_base_name(template_path) as path:
            print('Storing results in ' + path)

            # Choose starting point
            # Allow resampling, in case error calculation fails
            print('Choosing starting point')
            q0 = s0 = float('inf')
            while not np.isfinite(s0):
                q0 = boundaries.sample(1)[0]  # Search space
                s0 = error(q0)                # Initial score

            # Create a file path to store the optimisation log in
            log_path = os.path.splitext(path)
            log_path = log_path[0] + '-log.csv'

            # Create optimiser
            opt = pints.OptimisationController(
                error, q0, boundaries=boundaries, method=pints.CMAES)
            opt.set_log_to_file(log_path, csv=True)
            opt.set_max_iterations(3 if debug else None)
            opt.set_parallel(True)

            # Run optimisation
            print('Running')
            with np.errstate(all='ignore'): # Ignore numpy warnings
                q, s = opt.run()            # Search space

            # Transform back to model space
            if transformation is None:
                p = q
            else:
                p = transformation.to_model(q)

            # Store results for this run
            time = opt.time()
            iters = opt.iterations()
            evals = opt.evaluations()
            save(path, p, s, time, iters, evals)

    # Show best results
    parameters, info = load(template_path, n_parameters)
    print('Total results found: ' + str(len(parameters)))
    if len(parameters) > 0:
        print('Best score : ' + str(info[0, 1]))
        print('Worst score: ' + str(info[-1, 1]))
        print('Mean: ' + str(np.mean(info[:, 1])))
        print('Std : ' + str(np.std(info[:, 1])))

