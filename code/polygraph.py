"""Spiderdonuts module for dealing with graph walks."""

# Imports
import networkx as nx
import numpy as np
import scipy as sp
from itertools import chain, combinations
from code import linalg


# Number of decimals used for floating point comparison
DECIMALS = 10


def _diag_matrix(graph, max_power, arbitrary_precision=False):
    """Calculate the matrix of diagonals for a graph.

    The matrix of diagonals is an n x (n - 1) matrix
    containing the diagonals of A**2 - A**n where
    A is the adjacency matrix of a graph and n is the
    number of nodes in the graph.

    Parameters
    ----------
    graph : Networkx Graph
        A networkx graph
    max_power: Number
        An optional maximum power to use in determining the walk matrix
        (default n).
    arbitrary_precision: Boolean
        Whether or not to compute the walk matrix using arbitrary
        precision arithmetic. Using it is slow, but avoids numerical
        difficulties. (Default False).

    Returns
    -------
    Numpy Matrix
        A numpy matrix with dtype=object where
        data elements are python arbitrary
        precision integer objects.
    """
    # Get the total number of nodes in the graph
    num_nodes = len(graph.nodes())

    # List of all diagonals computed
    diagonals = []

    # Get adjacency matrix
    a_1 = nx.adjacency_matrix(graph).todense()

    # Make a copy to accumulate the product of
    # the matrix from 2..n. Specify object
    # datatype to force numpy to use python's
    # default arbitrary precision integers.
    adj = np.matrix(
        a_1.copy(),
        dtype=object if arbitrary_precision else np.float64
    )

    # Set maximum power to n if not specified
    if not max_power:
        max_power = num_nodes

    # Calculate A**2 through max_power + 1
    for i in range(2, max_power + 1):

        # Calculate nth adj matrix
        adj = adj.dot(a_1)

        # Get the diagonal of the matrix
        diag = np.diagonal(adj)

        # Append to list of diagonals
        diagonals.append(diag)

    # Return the matrix of diagonals
    return np.matrix(diagonals).transpose()


def _eigenvalues(graph):
    """Calculate eigenvalues and eigenvectors of a graph.

    Parameters
    ----------
    graph : Networkx Graph
        A networkx graph

    Returns
    -------
    tuple
        A tuple containing
        - eigenvalues
        - eigenvectors
    """
    # Get the adjacency matrix
    adj = nx.adjacency_matrix(graph).todense()

    # Return the eigenvalues
    return np.linalg.eigh(adj)


def _flip_flop_subset(w):
    """Given a matrix, return a subset that has the same Flip-Flopping.

    Parameters
    ----------
    w : Numpy Matrix
        A reduced walk matrix as returned by `walk_classes`

    Returns
    -------
    Numpy Matrix
        A square matrix containing only the first N columns of `w`
        required to make a matrix which demonstrates the same
        Flip-Flopping properties as `w`.
    """
    # Keep a list of flip-flopping properties to check
    flip_flops = [
        pair_wise_flip_flopping,
        dominant_flip_flopping,
        average_condition_flip_flopping,
        each_class_max
    ]

    # Calculate original flip-flopping properties
    original_ff = np.array([ff(w) for ff in flip_flops])

    # Get matrix shape
    rows, cols = w.shape

    # Get list of lexicographically sorted combinations of indices
    # and test each of them. Return the subset that works.
    for indices in combinations(range(cols), rows):

        # Take the subset
        w_sub = w[:, indices]

        # Calculate the subset's flip-flopping properties
        new_ff = np.array([ff(w_sub) for ff in flip_flops])

        # Check for equivalence
        if np.all(original_ff == new_ff):
            return w_sub

    # Return None as a default. Should never actually happen.
    return None


def walk_classes(graph, max_power=None, arbitrary_precision=False):
    """Analyze a networkx graph to determine its walk classes.

    Walk classes are computed as the distinct rows of the matrix
    of diagonals.

    The general algorithm is to compute A**2 through A**n where n
    is the number of nodes in the graph. W, the matrix of diagonals,
    is constructed as the matrix whose columns are the diagonals of
    A**2 through A**n.

    The unique rows of W share a 1:1 correspondence with the walk classes
    of a graph. After W is calculated, the graph is parsed and nodes labeled
    with their appropriate category, starting at 0.

    Warning. This is slow for large graphs O(n^4).

    Parameters
    ----------
    graph : Networkx Graph
        The networkx graph that will be analyzed.
    max_power: Number
        An optional maximum power to use in determining the walk matrix
        (default n).
    arbitrary_precision: Boolean
        Whether or not to compute the walk matrix using arbitrary
        precision arithmetic. Using it is slow, but avoids numerical
        difficulties. (Default False).

    Returns
    -------
    dict
        A dict consisting of the following:
        num_classes - The number `N` of walk classes
        classes     - A dictionary keyed by class label where each value
                      is a list of nodes in that class
        diag_matrix - The matrix `W` of diagonals
        uniq_rows   - The indices of the first copy of each distinct row
                      from the matrix of diagonals
        uniq_matrix - The matrix of uique rows in `W`
        eig_matrix  - The matix formed by taking columns 1-d of `uniq_matrix`
                      where d is the number of distinct eigenvalues in the
                      adjacency matrix of `graph`
        graph       - A copy of the graph where each node has the property
                      `category` corresponding to the walk category computed
    """
    # Create `W` as the matrix of diagonals
    W = _diag_matrix(graph, max_power, arbitrary_precision)

    # Get the eigenvalues from the graph adjacency matrix
    eigenvalues, eigenvectors = _eigenvalues(graph)
    num_values = len(np.unique(eigenvalues.round(decimals=DECIMALS)))

    # List of all unique rows encountered
    unique_rows = []
    unique_row_idxs = []

    # Mapping of a row to a class label
    mapping = {}

    # Unique class label
    idx = 0

    # Mapping of class label to a list of nodes in that class
    classes = {}

    # Process unique elements
    for row, node in enumerate(graph.nodes()):

        # Get row from W as string of comma separated values
        bts = ','.join(map(str, W[row].tolist()[0]))

        # If bts has not been seen before, create a class label
        if bts not in mapping:

            # Create mapping
            mapping[bts] = idx
            classes[idx] = []

            # Increment idx
            idx += 1

            # Add to unique rows from list of diagonals
            unique_rows.append(np.array(W[row]).reshape((-1,)))
            unique_row_idxs.append(row)

        # Label graph node from mapping and record class
        graph.node[node]['category'] = mapping[bts]
        classes[mapping[bts]].append(node)

    # Create the unique matrix
    uniq_matrix = np.matrix(unique_rows, dtype=object)

    # Calculate number of classes
    num_classes = len(mapping.keys())

    # Take the subset for number of eigenvalues
    eig_matrix = uniq_matrix[0: num_classes, 0:num_values]

    # Return
    return {
        'num_classes': num_classes,
        'classes': classes,
        'diag_matrix': W,
        'uniq_rows': unique_row_idxs,
        'uniq_matrix': uniq_matrix,
        'eig_matrix': eig_matrix,
        'graph': graph
    }


def spider_torus_walk_classes(st_obj, arbitrary_precision=False):
    """Analyze the walk classes of a spider torus.

    The walk classes of a spider torus are determined
    by applying a specialized version of the general analysis
    algorithm. The diagonal matrix is constructed by the
    diagonals of the matricies A^2, A^k1, ... A^kn for k in
    copies.

    Parameters
    ----------
    st_obj : dict
        A dict as returned by `gen.spider_torus`
    arbitrary_precision : Boolean
        Whether or not to compute the walk matrix using arbitrary
        precision arithmetic. Using it is slow, but avoids numerical
        difficulties. (Default False).

    Returns
    -------
    dict
        A dict consisting of the following:
        num_classes - The number `N` of walk classes
        uniq_rows   - The indices of the distinct rows used to form the
                      matrix of diagonals
        uniq_matrix - The matrix of uique rows in `W`
        graph       - A copy of the graph
    """
    # Get arguments
    graph = st_obj['graph']
    representatives = st_obj['representatives']
    copies = st_obj['copies']

    # Add 2 to the list of copies, to be used as powers
    # powers = [2] + copies
    max_power = max(copies)

    # Get adjacency matrix
    adj = np.matrix(
        nx.adjacency_matrix(graph).todense(),
        dtype=object if arbitrary_precision else np.float64
    )

    # Copy the adjacency matrix
    w = adj.copy()

    # List of all diagonals
    diagonals = []

    # Build up the list of diagonals
    for k in range(2, max_power + 1):

        # Take the matrix power
        w = w.dot(adj)

        # Get the diagonal
        diagonals.append(np.diagonal(w))

    # Calculate the matrix of diagonals
    diag_matrix = np.matrix(diagonals).transpose()
    uniq_matrix = diag_matrix[representatives]

    # Return output
    return {
        'num_classes': len(copies) + 1,
        'uniq_rows': representatives,
        'uniq_matrix': uniq_matrix,
        'graph': graph
    }


def positive_linear_system_check(w_obj, epsilon=1e-10):
    """Solve a linear program.

    The system attempts to find a strictly positive solution
    to the problem `Wx = e`.

    Paremeters
    ----------
    w_obj : Dict
        Walk object returned by `walk_classes`
    epsilon : Number
        Small, nonzero number (default 1e-10)

    Returns
    -------
    Scipy Optimize Result
        The result from calling scipy.optimize.linprog
    """
    # Get the reduced walk matrix
    if 'eig_matrix' in w_obj:
        w = w_obj['eig_matrix']
    else:
        w = w_obj['uniq_matrix']

    # Get the number of rows and columns of w
    num_rows, num_cols = w.shape

    # Return result
    return sp.optimize.linprog(
        c=np.ones(num_cols),
        A_ub=-np.matrix(np.identity(num_cols)),
        b_ub=-np.ones(num_cols) * epsilon,
        A_eq=w,
        b_eq=np.ones(num_rows)
    )


def nonnegative_linear_system_check(w_obj, epsilon=1e-10, subset=False):
    """Solve a linear program.

    The system will attempt to find a nonnegative solution of the form
    `Wx = (gamma * e) - g` where `g = diag(expm(A))`, limited to the entries
    corresponding to the unique classes of `w`, and `(gamma * e) - g > 0`.

    Paremeters
    ----------
    w_obj : Dict
        Walk object returned by `walk_classes`
    epsilon : Number
        Small, nonzero number (default 1e-10)
    subset: Boolean | List
        If True, the minimal subset of the walk matrix which demonstrates the
        same flip-flopping conditions will be used. If a List, the column
        indices provided in the list will be used to form the subset. Otherwise
        (False), no subsetting will be performed.

    Returns
    -------
    Scipy Optimize Result
        The result from calling scipy.optimize.linprog
    """
    # Get the reduced walk matrix
    if 'eig_matrix' in w_obj:
        w = w_obj['eig_matrix']
    else:
        w = w_obj['uniq_matrix']

    # Take the subset of the matrix
    if subset is True:
        w = _flip_flop_subset(w)
    elif isinstance(subset, list):
        w = w[:, subset]

    # Get the shape of w
    num_rows, num_cols = w.shape

    # Get the graph adjacency matrix
    A = nx.adjacency_matrix(w_obj['graph']).todense()

    # Calcualte the diagonal matrix
    try:
        d = np.diag(sp.linalg.expm(A))
    except:
        d = np.diag(linalg.adhoc_expm(A))

    # Form g from the unique rows of d
    g = np.matrix([d[idx] for idx in w_obj['uniq_rows']])

    # Return result
    return sp.optimize.linprog(
        c=np.ones(num_cols + 1),
        A_ub=-np.identity(num_cols + 1),
        b_ub=np.concatenate((np.zeros(num_cols), np.array([-epsilon]))),
        A_eq=np.concatenate((w, -np.ones((num_rows, 1))), axis=1),
        b_eq=-g
    )


def pair_wise_flip_flopping(W):
    """Determine if a unique walk matrix demonstrates pair-wise flip-flopping.

    Pair-wise flip-flopping is defined as:
    For every pair of classes C[i] and C[j], there exist walk lengths L[x]
    and L[y], such that C[i] has more closed walks of length L[x] than
    C[j] and vice versa.

    Parameters
    ----------
    W : Numpy Matrix
        Unique walk matrix as returned by `walk_classes`

    Returns
    -------
    boolean
        True if pair-wise flip-flopping holds for `W`
    """
    # Work with an ndarray representation of W
    w = W.getA()

    # Get the number of rows and columns in W
    num_rows, num_cols = w.shape

    # Generate all possible pairs of classes and k-walks
    # A single pair is held as a tuple (x, y)
    classes, walks = ([
        (i, j)
        for i in range(0, num)
        for j in range(i + 1, num)
    ] for num in [num_rows, num_cols])

    # Iterate over all pairs of classes
    for cls1, cls2 in classes:

        # Whether these two classes flip-flop at any point
        flip_flops = False

        # Iterate over all pairs of walks
        for w1, w2 in walks:

            # Comparison of classes for k-walk 1
            n1 = w[cls1][w1] - w[cls2][w1]

            # Comparison of classes for k-walk 2
            n2 = w[cls1][w2] - w[cls2][w2]

            # Check to see if the classes flip-flopped
            if (n1 > 0 and n2 < 0) or (n1 < 0 and n2 > 0):
                flip_flops = True
                break

        # If the classes don't flip-flop, return false immediately
        if not flip_flops:
            return False

    # Return true if no counter examples are found
    return True


def dominant_flip_flopping(W):
    """Determine if a unique walk matrix demonstrates dominant flip-flopping.

    Dominant flip-flopping is defined as:
    For every class C[i], there exists a walk length L[x], such that C[i] has
    more closed walks of length L[x] than all other classes combined.

    Dominant flip-flopping implies all-subset flip-flopping.

    Parameters
    ----------
    W : Numpy Matrix
        Unique walk matrix as returned by `walk_classes`

    Returns
    -------
    boolean
        True if dominant flip-flopping holds for `W`
    """
    # Work with an ndarray representation of W
    w = W.getA()

    # Get the number of rows and columns in W
    num_rows, num_cols = w.shape

    # Generate the column-wise sum of w
    # This amounts to a 1darray where each item
    # is the sum of all walks of a length k for
    # all classes
    sums = w.sum(0)

    # Iterate over all classes
    for cls in range(0, num_rows):

        # Whether this class dominates any k-walk
        is_dominant = False

        # Iterate over all walks
        for walk in range(0, num_cols):

            # Check to see if is dominant
            # Sums includes the number of walks for the class
            # so it must be removed before checking that it
            # dominates the remainder
            if w[cls][walk] > sums[walk] - w[cls][walk]:
                is_dominant = True
                break

        # Return false immediately if this class does
        # not dominate a k-walk
        if not is_dominant:
            return False

    # Return true as default
    return True


def average_condition_flip_flopping(W):
    """Determine if a unique walk matrix demonstrates ACFF.

    Average-Condtion flip-flopping is defined as:

    For all pairs of subsets (S, T) where S and T are not equal to the empty
    set and do not intersect, the there exists a walk of length L[x] such that
    the average number of walks of length L[x] in S is greater than the average
    number of walks of the same length in T.

    A simpler, yet equivalent definition is that for every subset S, there is
    some walk length L[x] such that the average number of walks in S is greater
    than or equal to the maximum number of walks of any class in the compliment
    of S. This is the condition that is checked to determine ACFF.

    Parameters
    ----------
    W : Numpy Matrix
        Unique walk matrix as returned by `walk_classes`

    Returns
    -------
    boolean
        True if average-condition flip-flopping holds for `W`
    """
    # Work with an ndarray representation of W
    w = W.getA()

    # Get the number of rows and columns in W
    num_rows, num_cols = w.shape

    # Generate the set of classes
    classes = set([i for i in range(num_rows)])

    # Generatae a list of subsets of classes not including
    # the empty set or the original set
    subsets = list(map(
        set,
        chain.from_iterable(
            combinations(classes, i) for i in range(1, len(classes))
        )
    ))

    # For each subset, check that, for some walk length,
    # its average value is bigger than the max in the
    # compliment of the set
    for subset in subsets:

        # Whether flip-flipping is found
        flip_flops = False

        # Take the set compliment
        compliment = classes - subset

        # Check each walk length average vs max property
        for walk in range(0, num_cols):

            # Calculate average number of walks for the subset
            average = sum([w[cls][walk] for cls in subset]) / len(subset)

            # Calculate the max number of walks for the compliment
            maximum = max([w[cls][walk] for cls in compliment])

            # If the average is greater than the maximum
            # there is flip-flopping, stop checking
            if average >= maximum:
                flip_flops = True
                break

        # No flip flopping was found, return
        if not flip_flops:
            return False

    # If no counter examples are found return true
    return True


def each_class_max(W):
    """Determine if a unique walk matrix demonstrates each class max.

    Each class max is defined as:

    For each class C[i] in W there exists a walk length L[x] such that
    C[i] has larger number of walks of length L[x] than all other classes.

    Parameters
    ----------
    W : Numpy Matrix
        Unique walk matrix as returned by `walk_classes`

    Returns
    -------
    boolean
        True if each-class-max holds, false if not
    """
    # Work with an ndarray representation of W
    w = W.getA()

    # Get the number of rows and columns in W
    num_rows, num_cols = w.shape

    # Possible classes
    classes = [i for i in range(0, num_rows)]

    # Possible walks
    walks = [i for i in range(0, num_cols)]

    # Check all classes
    for cls in classes:

        # Whether class has a max
        has_max = False

        # Check all walks
        for walk in walks:

            # Find maximum of other classes for same walk
            maximum = max([w[cls2][walk] for cls2 in classes if cls2 != cls])

            # Set has max to true if number of walks is greater
            if w[cls][walk] > maximum:
                has_max = True
                break

        # If not max for some length return false
        if not has_max:
            return False

    # Return true if property is not violated
    return True
