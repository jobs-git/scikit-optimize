# -*- coding: utf-8 -*-
""" Inspired by https://github.com/jonathf/chaospy/blob/master/chaospy/
distributions/sampler/sequences/hammersley.py
"""
import numpy as np
from .halton import Halton
from ..space import Space
from .base import InitialPointGenerator


class Hammersly(InitialPointGenerator):
    """Creates `Hammersley` sequence samples.
    The Hammersley set is equivalent to the Halton sequence, except for one
    dimension is replaced with a regular grid. It is not recommended to
    generate a Hammersley sequence with more than 10 dimension.

    For ``dim == 1`` the sequence falls back to Van Der Corput sequence.

    References
    ----------
    T-T. Wong, W-S. Luk, and P-A. Heng, "Sampling with Hammersley and Halton
    Points," Journal of Graphics Tools, vol. 2, no. 2, 1997, pp. 9 - 24.

    Parameters
    ----------
    min_skip : int, default=-1
        minimum skipped seed number. When `min_skip != max_skip` and
        both are > -1, a random number is picked.
    max_skip : int, default=-1
        maximum skipped seed number. When `min_skip != max_skip` and
        both are > -1, a random number is picked.
    primes : tuple, default=None
        The (non-)prime base to calculate values along each axis. If
        empty, growing prime values starting from 2 will be used.
    """
    def __init__(self, min_skip=-1, max_skip=-1, primes=None):
        self.primes = primes
        self.min_skip = min_skip
        self.max_skip = max_skip

    def generate(self, dimensions, n_samples, random_state=None):
        """Creates samples from Hammersly set.

        Parameters
        ----------
        dimensions : list, shape (n_dims,)
            List of search space dimensions.
            Each search dimension can be defined either as

            - a `(lower_bound, upper_bound)` tuple (for `Real` or `Integer`
              dimensions),
            - a `(lower_bound, upper_bound, "prior")` tuple (for `Real`
              dimensions),
            - as a list of categories (for `Categorical` dimensions), or
            - an instance of a `Dimension` object (`Real`, `Integer` or
              `Categorical`).
        n_samples : int
            The order of the Hammersley sequence.
            Defines the number of samples.
        random_state : int, RandomState instance, or None (default)
            Set random state to something other than None for reproducible
            results.

        Returns
        -------
        np.array, shape=(n_dim, n_samples)
            Hammersley set
        """

        halton = Halton(min_skip=self.min_skip, max_skip=self.max_skip,
                        primes=self.primes)
        space = Space(dimensions)
        n_dim = space.n_dims
        space.set_transformer("normalize")
        if n_dim == 1:
            return halton.generate(dimensions, n_samples,
                                   random_state=random_state)
        out = np.empty((n_dim, n_samples), dtype=float)
        out[:n_dim - 1] = np.array(halton.generate(
            [(0., 1.), ] * (n_dim - 1), n_samples,
            random_state=random_state)).T

        out[n_dim - 1] = np.linspace(0, 1, n_samples + 2)[1:-1]
        return space.inverse_transform(out.T)
