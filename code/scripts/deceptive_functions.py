"""Calculate deceptive functions for a set of graphs.

A deceptive function is formed as g(lambda) = (e^lambda) + p(lambda), where
p(lambda) = 0*lambda^0 + 0*lambda^1 + x_{1}lambda^2 + ... + x_{k-1}lambda^k
with x_1..x_{k-1} formed from the solutions to
`polygraph.nonnegative_linear_system_check` and lambda is an eigenvalue
of the graph.

Outputs
- Plot of (lambda, g(lambda)) for each graph.
- Table of (graph, min(g(lambda))) for all graphs.
"""


# Imports
from code import generators as gen, polygraph, SPIDERDONUTS, verbose
from functools import partial
from math import exp
from tabulate import tabulate
import io
import logging
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# Intermediate points
NUM_POINTS = 100
MAX_POWER = 6


def deceptive(y, coefficients):
    """Deceptive function.

    Parameters
    ----------
    y : Number
        Eigenvalue of a graph
    coefficients : list
        List of coefficients

    Returns
    -------
    Number
        e^y + coefficients[0]*y^2 + ... coefficients[k-1]*y^k
    """
    poly = np.poly1d(np.concatenate(([0, 0], coefficients)))
    return exp(y) + np.polyval(poly, y)


# Get logger
logger = logging.getLogger(SPIDERDONUTS)
verbose(True)

# A list of (graph_name, graph_generator) tuples.
# Each generator has its parameters already bound to it
graphs_generators = [
    ('chamfered_dodecahedron', gen.chamfered_dodecahedron),
    ('pyramid_prism(4,0)', partial(gen.pyramid_prism, 4, 0)),
    ('spider_torus(4,2,[5,3])', partial(gen.spider_torus, 4, 2, [5, 3])),
    ('spider_torus(4,3,[7,5,3])', partial(gen.spider_torus, 4, 3, [7, 5, 3])),
    ('snowflakecycle(5,5,3)', partial(gen.snowflakecycle, 5, 5, 3)),
    ('snowflakecycle(5,7,5)', partial(gen.snowflakecycle, 5, 7, 5)),
    ('snowflakecycle(5,7,3)', partial(gen.snowflakecycle, 5, 7, 3))
]

# Min lambda
min_lambda = [('Graph', 'Min g(lambda)', 'Number of Coefficients')]

# Analyze graphs
for name, generator in graphs_generators:

    logger.info('Analyzing graph {}'.format(name))

    # Construct graph
    logger.info('Generating graph')
    g = generator()

    # Analyze walk classes
    logger.info('Analyzing walk classes')
    if type(g) is dict:
        graph = g['graph']
        w_obj = polygraph.spider_torus_walk_classes(g)
    else:
        graph = g
        w_obj = polygraph.walk_classes(g, max_power=MAX_POWER)

    # Generate solutions to nonnegative linear system
    logger.info('Performing nonnegative system check')
    res = polygraph.nonnegative_linear_system_check(w_obj)

    # Check for success
    if not res.success:
        logger.warning('Failed nonnegative check on {} with {}'.format(
            name,
            res.message
        ))
    else:
        # Take solutions as coefficients
        coefficients = res.x[::-1]

        # Find graph eigenvalues
        logger.info('Finding graph eigenvalues')
        eigenvalues = np.linalg.eigvalsh(nx.adjacency_matrix(graph).todense())

        # Key points
        max_eig = max(eigenvalues)
        min_eig = min(eigenvalues)
        linspace = np.linspace(min_eig, max_eig, NUM_POINTS)

        # Evaluate the deceptive function at each eigenvalue
        logger.info('Evaluating deceptive function at eigenvalues')
        eig_results = [deceptive(x, coefficients) for x in eigenvalues]
        lin_results = [deceptive(x, coefficients) for x in linspace]

        # Append min result to table output
        min_result, min_idx = min(
            (val, idx)
            for (idx, val) in enumerate(eig_results)
        )
        min_lambda.append((name, min_result, len(coefficients)))

        # Generate plot
        logger.info('Generating (lambda, g(lambda)) plot')
        plt.figure()
        plt.suptitle(name)
        plt.xlabel('lambda (Eigenvalue)')
        plt.ylabel('g(lambda)')
        plt.scatter(eigenvalues, eig_results, marker='*', s=150)
        plt.scatter(linspace, lin_results, marker='.')
        plt.axvline(x=eigenvalues[min_idx], ymin=0, ymax=max(eig_results))
        plt.axhline(y=min_result, xmin=0, xmax=max_eig)
        plt.savefig('docs/tables-and-figures/{}'.format(name))
        plt.close()

    logger.info('Finished graph {}\n'.format(name))


# Generate (graph, min(g(lambda))) table
table = tabulate(min_lambda, tablefmt='grid')

# Write file
file = io.open('docs/tables-and-figures/lambda-table.txt', 'w')
file.write(table)
file.close()
