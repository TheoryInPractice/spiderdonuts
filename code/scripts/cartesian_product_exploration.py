"""Compare cartesian products.

The goal is to see if the product of two known
deceptive graphs leads to a 3 class graph which
has a nonnegative solution to `Wx = gamma * e - g`.
"""


# Imports
from code.common import generators as gen
from code.struckpod import walks
from itertools import combinations_with_replacement
from tabulate import tabulate
import networkx as nx

# Generate known 2 class graphs
graphs = {
    'pyramid_prism_4':        gen.pyramid_prism(4, 0),
    # 'chamfered_dodecahedron': gen.chamfered_dodecahedron(),
    'orthobicupola_3':        gen.orthobicupola(3),
    # 'orthobicupola_4':        gen.orthobicupola(4),
    # 'orthobicupola_6':        gen.orthobicupola(6)
}

flip_flops = [
    walks.pair_wise_flip_flopping,
    walks.average_condition_flip_flopping,
    walks.dominant_flip_flopping,
    walks.each_class_max
]

# Generate pairs
pairs = combinations_with_replacement(graphs.keys(), 2)

# Analysis results
results = []

# Check pairs
for g1, g2 in pairs:

    # Generate the cartesian product
    g = nx.cartesian_product(graphs[g1], graphs[g2])

    # Analyze
    w_obj = walks.walk_classes(g)
    res = walks.positive_linear_system(w_obj, False, 10)

    # Create the result row
    results.append([
        g1,
        g2,
        w_obj['num_classes'],
        *[ff(w_obj['eig_matrix']) for ff in flip_flops],
        res.x
    ])

print(tabulate(
    results,
    tablefmt='grid',
    headers=[
        'Graph 1',
        'Graph 2',
        'Num Classes',
        'PW FF',
        'ACFF',
        'DFF',
        'ECM',
        'Nonnegative Solution'
    ]
))
