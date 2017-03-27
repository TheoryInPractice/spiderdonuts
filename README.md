# spiderdonuts

Exploring deceptive graphs and deceptive functions.

In general, all code will be in Python interfacing with the networkx module.

## Table of Contents

* [Code](code/README.md)

## Main research focuses

The idea of "Walk Entropy" is concerned with the information about a graph encoded by the graph's walk structure. In this project, we study a graph's walk structure by looking at polynomials and functions of graph matrices.
The main focus is understanding when a non--walk-regular graph can "appear to be" walk-regular. The adjacency matrix M of a walk-regular graph will always have constant diagonal, no matter what function (or polynomial) we apply to the matrix, f(M). We study non--walk-regular graphs for which there exist functions (which we call "deceptive" functions) such that f(M) is constant-diagonal even though the graph is not walk-regular. Graphs for which such functions exist we call "deceptive graphs".

As part of this project we have developed some necessary and some sufficient conditions for graphs to be deceptive, as well as algorithms for constructing deceptive functions in some circumstances. This repository includes codes both for generating classes of graphs, some of which we have verified to be deceptive, as well as for checking whether or not a given graph is deceptive.

## Verbose Mode

Several of the functions in Spiderdonuts can be slow for graphs larger than one or two thousand nodes. When verbose mode is enabled, progress will be logged to standard output. To toggle verbose mode, use `code.verbose`.

```python
import code

# Toggle On
code.verbose(True)

# Toggle Off
code.verbose(False)
```

If running through Jupyter Notebook (IPython), the root python logger must be correctly configured to see logging per cell (within the notebook, logging will still go to standard output on the console jupyter was started from without configuration).

```python
import logging, code
logging.basicConfig(format='[%(asctime)s] %(message)s')
code.verbose(True)
```

## Code Examples

### Analyzing Walk Classes

This is slow for large graphs O(n^4). For spider torus graphs, see the specialized
spider_torus_walk_classes.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a pyramid prism
pyramid_prism = gen.pyramid_prism()

# Analyze walk classes
polygraph.walk_classes(pyramid_prism)
```

### Checking for Deceptiveness - Not Deceptive

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 2-sided, 3-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(2, 3)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# Check for Pair-Wise Flip-Flopping, which will return false
polygraph.pair_wise_flip_flopping(walk_obj['eig_matrix'])
```

### Checking for Deceptiveness - Deceptive

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 4-sided, 0-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(4, 0)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# Check for a solution to the system Wx = (gamma * e) - g
polygraph.positive_linear_system_check(walk_obj)
```

### Printing a Graph With Node IDs

```python
# Import spiderdonuts modules
from code import graphs, generators as gen

# Generate a Chamfered Dodecahedron
cd = gen.chamfered_dodecahedron()

# Draw
graphs.draw_with_id(cd, 'out.png')
```
### Printing a Graph With Node Classes

```python
# Import spiderdonuts modules
from code import graphs, polygraph, generators as gen

# Generate a Chamfered Dodecahedron
cd = gen.chamfered_dodecahedron()

# Compute walk class info
walk_obj = polygraph.walk_classes(cd)

# Draw
graphs.draw_with_category(walk_obj['graph'], 'out.png')
```

# Analyzing a Deceptive Spidertorus

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a deceptive spider torus
spidertorus_obj = gen.spider_torus(4, 2, [5, 3])

# Compute walk class info
walk_obj = polygraph.spider_torus_walk_classes(spidertorus_obj)

# Check for a solution to the system Wx = (gamma * e) - g
polygraph.nonnegative_linear_system_check(walk_obj)
```
