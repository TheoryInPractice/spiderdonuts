#
# This file is part of spiderdonuts, https://github.com/TheoryInPractice/spiderdonuts/,
# and is Copyright (C) North Carolina State University, 2017. It is licensed
# under the three-clause BSD license; see LICENSE.
#
"""Calculate Linear Systems `Wx = e` for pyramid prisms."""

# Imports
from code import generators as gen
from code import polygraph
import numpy as np
from tabulate import tabulate


# Constants
NUM_PYRAMID_FACES = 4
MIN_PYRAMID_LAYERS = 0
MAX_PYRAMID_LAYERS = 3
MIN_BCP_FACES = 3
MAX_BCP_FACES = 6


def _analyze(graph):
    # Get the walk object
    w_obj = polygraph.walk_classes(graph)

    # Solve the linear system involving the eig_matrix
    res = polygraph.positive_linear_system_check(w_obj)

    # Check to see if x is positive
    return np.all(res.x >= 0)


# Accumulated results
results = [[] for layer in range(MIN_PYRAMID_LAYERS, MAX_PYRAMID_LAYERS + 1)]

# Check pyramid prisms
for layers in range(MIN_PYRAMID_LAYERS, MAX_PYRAMID_LAYERS + 1):

    # Get result index
    idx = layers - MIN_PYRAMID_LAYERS

    # Set Layer result header
    results[idx].append('Pyramid Prism (4, {})'.format(layers))

    # Create a pyramid prism
    g = gen.pyramid_prism(NUM_PYRAMID_FACES, layers)

    # Analyze g
    results[idx].append(_analyze(g))


# Check chamfered dodecahedron
g = gen.chamfered_dodecahedron()
results.append(['Chamfered Dodecahedron', _analyze(g)])


# Check orthobicupola
for faces in range(MIN_BCP_FACES, MAX_BCP_FACES + 1):
    # Generate the graph
    g = gen.orthobicupola(faces)

    results.append([
        'Orthobicupola ({})'.format(faces),
        _analyze(g)
    ])


# Print
print(tabulate(results, tablefmt='grid', headers=['Graph', 'Is Positive']))
