#
# This file is part of spiderdonuts, https://github.com/TheoryInPractice/spiderdonuts/,
# and is Copyright (C) North Carolina State University, 2017. It is licensed
# under the three-clause BSD license; see LICENSE.
#
"""Tests for cartesian_product."""

from code import generators as gen
from code import polygraph
import networkx as nx
from tabulate import tabulate


MIN = 2
MAX_1 = 6
GRAPHS = {
    'Cycle': nx.cycle_graph,
    'Clique': nx.complete_graph,
    'hypercube': nx.hypercube_graph
}


pyramid = gen.pyramid_prism(4, 0)


pwff = []
acff = []
classes = []
for graph_type, generator in GRAPHS.items():
    pwrow = [graph_type]
    acrow = [graph_type]
    crow = [graph_type]
    for i in range(MIN, MAX_1):
        graph = nx.cartesian_product(pyramid, generator(i))
        w_obj = polygraph.walk_classes(graph)
        w = w_obj['eig_matrix']
        pwrow.append(polygraph.pair_wise_flip_flopping(w))
        acrow.append(polygraph.average_condition_flip_flopping(w))
        crow.append(w_obj['num_classes'])
    pwff.append(pwrow)
    acff.append(acrow)
    classes.append(crow)

print('Number of Walk Classes')
print(tabulate(
    classes,
    tablefmt='grid',
    headers=['Graph', *[i for i in range(MIN, MAX_1)]]
))
print('Pair-Wise Flip-Flopping')
print(tabulate(
    pwff,
    tablefmt='grid',
    headers=['Graph', *[i for i in range(MIN, MAX_1)]]
))
print('Average-Condtion Flip-Flopping')
print(tabulate(
    acff,
    tablefmt='grid',
    headers=['Graph', *[i for i in range(MIN, MAX_1)]]
))
