"""Generate a table of walk classes for pyramid prisms."""

# Imports
from tabulate import tabulate
import code.common.generators as gen
import code.struckpod.walks as walks
import numpy as np


# CONSTANTS
MIN_FACES = 2
MAX_FACES = 8
MIN_LAYERS = 0
MAX_LAYERS = 5
PWFF = 'Pair-Wise Flip-Flopping '
DFF = 'Dominant Flip-Flopping'
ACFF = 'Average-Condition Flip-Flopping'
ECM = 'Each Class Max'


# Number of rows and columns
num_faces = (MAX_FACES - MIN_FACES) + 1
num_layers = (MAX_LAYERS - MIN_LAYERS) + 1

# Create results lists
shape = (num_faces, num_layers)
pwff = np.zeros(dtype=bool, shape=shape)
dff = np.zeros(dtype=bool, shape=shape)
acff = np.zeros(dtype=bool, shape=shape)
ecm = np.zeros(dtype=bool, shape=shape)

# Check each combination
for faces in range(MIN_FACES, MAX_FACES):
    for layers in range(MIN_LAYERS, MAX_LAYERS):

        # Generate the graph
        g = gen.pyramid_prism(faces, layers)

        # Analyze classes
        w_obj = walks.walk_classes(g)

        # Get the unique walk matrix w
        w = w_obj['uniq_matrix']

        # Get results row and cell
        row = faces - MIN_FACES
        col = layers - MIN_LAYERS

        # Check which properties it holds
        pwff[row][col] = walks.pair_wise_flip_flopping(w)
        dff[row][col] = walks.dominant_flip_flopping(w)
        acff[row][col] = walks.average_condition_flip_flopping(w)
        ecm[row][col] = walks.each_class_max(w)


def _annotate(array):
    # Annotate with number of faces
    arr = [
        ['{} Faces'.format(i + MIN_FACES)] + row
        for i, row in enumerate(array.tolist())
    ]

    # Annotate with number of layers
    arr.insert(0, [
        '',
        *['{} Layers'.format(i + MIN_LAYERS) for i in range(num_layers)]
    ])

    return arr

# Print
print(PWFF)
print(tabulate(_annotate(pwff), tablefmt='grid'))

print(DFF)
print(tabulate(_annotate(dff), tablefmt='grid'))

print(ACFF)
print(tabulate(_annotate(acff), tablefmt='grid'))

print(ECM)
print(tabulate(_annotate(ecm), tablefmt='grid'))