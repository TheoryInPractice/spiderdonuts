#
# This file is part of spiderdonuts, https://github.com/TheoryInPractice/spiderdonuts/,
# and is Copyright (C) North Carolina State University, 2017. It is licensed
# under the three-clause BSD license; see LICENSE.
#
"""Module for adhoc linear algebra computation."""

# Imports
import numpy as np
from math import exp


def adhoc_expm(A):
    """Calculate the matrix exponential.

    Parameters
    ----------
    A : Numpy Matrix
        A square, real-valued, symmetric matrix

    Returns
    -------
    Numpy Matrix
        The matrix exponential of `A`
    """

    # Get the eigen values and vectors of the matrix
    eig_vals, eig_vecs = np.linalg.eigh(A)

    # Generate the list of exponentials of eigenvalues
    exp_eigs = np.diag([exp(val) for val in eig_vals])

    # Return
    return eig_vecs * exp_eigs * eig_vecs.T
