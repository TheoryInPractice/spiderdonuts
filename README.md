<img align="right" src="spiderdonuts-logo.png">

# spiderdonuts

This project explores connections between walk-regularity and the behavior of functions on graphs.

## Table of Contents

README
* [Main Research Focuses](#main-research-focuses)
* [Code](#code)
* [Examples](#examples)
* [Dependencies](#dependencies)
* [License](#license)
* [Acknowledgements](#acknowledgements)

## Main Research Focuses

The idea of "Walk Entropy" measures how structured/symmetric/uniform a graph is in terms of its
walk structure---a graph that has regular walk structure (i.e. a graph that is walk-regular) has maximum walk-entropy.
In this project, we study the relationship of a graph's walk structure to the behavior of a special class of functions applied to the graph adjacency matrix.

The main focus is understanding when a non--walk-regular graph can "appear to be" walk-regular. The
adjacency matrix M of a walk-regular graph will always have constant diagonal, no matter what
function (or polynomial) we apply to the matrix, f(M). We study non--walk-regular graphs for which
there exist functions (which we call "deceptive" functions) such that f(M) is constant-diagonal even
though the graph is not walk-regular. Graphs for which such functions exist we call "deceptive
graphs".

As part of this project we have developed some necessary and some sufficient conditions for graphs
to be deceptive, as well as algorithms for constructing deceptive functions in some circumstances.
This repository includes codes for generating classes of graphs (some of which we have verified
to be deceptive), checking whether or not a given graph meets our necessary criteria for deceptiveness, and for constructing deceptive functions.


## Code

Spiderdonuts is split into two main modules: `generators` and `polygraph`.

The module `generators` contains functions for creating a number of different graphs (all networkx type objects), including the deceptive graphs that we found. See [Examples](#examples) below for examples of how to call some of the graph generator functions in `generators`.

The module `polygraph` contains functions for analyzing graph walk-classes, checking flip-flop conditions, and
checking for deceptiveness.

| Function | Description |
| -------- | ----------- |
| walk_classes | Returns metadata about a graphs walk-classes |
| spider_torus_walk_classes | A version of walk_classes optimized for spidertori |
| positive_linear_system_check | Check for deceptiveness by solving for `Wx = e` |
| nonnegative_linear_system_check | Check for deceptiveness by solving for `Wx = (gamma * e) - diag(expm(A))` |
| pair_wise_flip_flopping | Check for pair-wise flip-flopping property |
| dominant_flip_flopping | Check for dominant flip-flopping property |
| average_condition_flip_flopping | Check for average-condition flip-flopping property |
| each_class_max | Check for each-class-max property |

### Verbose Mode

Several of the functions in Spiderdonuts can be slow for graphs larger than one or two thousand
nodes. When verbose mode is enabled, progress will be logged to standard output. To toggle verbose
mode, use `code.verbose`.

```python
import code

# Toggle On
code.verbose(True)

# Toggle Off
code.verbose(False)
```

If running through Jupyter Notebook (IPython), the root python logger must be correctly configured
to see logging per cell (within the notebook, logging will still go to standard output on the
console jupyter was started from without configuration).

```python
import logging, code
logging.basicConfig(format='[%(asctime)s] %(message)s')
code.verbose(True)
```

## Examples

### Generating a Pyramid Prism

Pyramid prisms have two parameters, faces and layers. Our graph generator can be used to
generate networkx pyramid prism graphs.

```python
# Import generators
from code import generators as gen

# Construct a pyramid prism with 4 faces and 0 layers
pyramid_prism = gen.pyramid_prism(4, 0)
```

### Generating a Spidertorus

Spidertori take three parameters for construction: degree, length, and number of copies in each
ring starting from the first level and working outwards. The generator for spidertori returns a
dictionary object containing the graph and some other metadata. Here's how to create a spidertorus
of degree 4, length 2, with an inner ring of 5 and outer ring of 3.

```python
# Import generators
from code import generators as gen

# Construct
spidertorus = gen.spider_torus(4, 2, [5, 3])
```

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

### Checking for Deceptiveness - Not Deceptive by Pair-Wise Flip-Flopping

Pair-Wise Flip-Flopping is a necessary condition for a graph to be deceptive. Here is an example
of a graph that does not pass the pair-wise metric.

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

### Checking for Deceptiveness - Not Deceptive by Average-Condtion Flip-Flopping

Average-Condtion Flip-Flopping is a necessary condition for a graph to be deceptive. Here is an
example of a graph that does not pass the average-condition metric.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 2-sided, 3-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(2, 3)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# Check for Average-Condtion Flip-Flopping, which will return false
polygraph.pair_wise_flip_flopping(walk_obj['eig_matrix'])
```

### Checking for Deceptiveness - Deceptive by Positive Linear System Check

The positive linear system check returns a result from `scipy.optimize.linprog`. Successful
optimization will return `True` for success with a solution set for `x`.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 4-sided, 0-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(4, 0)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# Check for a solution to the system Wx = e
polygraph.positive_linear_system_check(walk_obj)
```

### Checking for Deceptiveness - Deceptive by Nonnegative Linear System Check

The nonnegative linear system check returns a result from `scipy.optimize.linprog`. Successful
optimization will return `True` for success with a solution set for `x`.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 4-sided, 0-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(4, 0)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# Check for a solution to the system `Wx = (gamma * e) - diag(expm(A))`
polygraph.nonnegative_linear_system_check(walk_obj)
```

### Checking for Deceptiveness - Inconclusive

Failure of a linear system check to return an optimization without further information is
inconclusive about a graphs deceptiveness.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a deceptive snowflakecycle
snowflakecycle = gen.snowflakecycle(5, 5, 3)

# Compute walk class info
walk_obj = polygraph.walk_classes(spidertorus)

# Check for a solution to the system Wx = e
polygraph.nonnegative_linear_system_check(walk_obj)
```

### Analyzing a Deceptive Spidertorus

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

## Dependencies

All code is compatible with python 3.5. Specific dependencies are listed in `requirements.txt`.

Install python dependencies using `pip`:
```bash
$ pip3 install -r requirements.txt
```

Updating dependencies with `pip`:
```bash
$ pip3 freeze > requirements.txt
```

## License

<!---
**Important**: spiderdonuts is *research software*, so you should cite us when you use it in scientific publications! Please see the CITATION file for citation information.
[![DOI](https://zenodo.org/...)](https://zenodo.org/badge/...)

-->

Spiderdonuts is released under the BSD license; see the LICENSE file.
Distribution, modification and redistribution, and incorporation into other
software is allowed.


## Acknowledgements

Development of the spiderdonuts software package was funded in part by
the [Gordon & Betty Moore Foundation Data-Driven Discovery Initiative](https://www.moore.org/programs/science/data-driven-discovery),
through a [DDD Investigator Award](https://www.moore.org/programs/science/data-driven-discovery/investigators)
to Blair D. Sullivan ([grant GBMF4560](https://www.moore.org/grants/list/GBMF4560)).
