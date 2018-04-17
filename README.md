<img align="right" src="spiderdonuts-logo.png">

# spiderdonuts

This project explores connections between walk-regularity and the behavior of functions on graphs.

## Table of Contents

README
* [Main Research Focuses](#main-research-focuses)
* [Dependencies](#dependencies)
* [Code](#code)
* [Examples](#examples)
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

## Dependencies

To use the spiderdonuts repo, all that is required is a compatible version of python and a few python packages.
We can verify all code in the spiderdonuts repo is compatible with python 3.5, but any python 3.X should work.
Specific dependencies are listed in `requirements.txt`.

To install the python dependencies use `pip`:
```bash
$ pip3 install -r requirements.txt
```
WARNING: Newer versions of `scipy` cause errors with the current implementations of this repo---be sure to use `scipy==0.18.0` as listed in `requirements.txt`.


## Code

Spiderdonuts is split into two main modules: `generators` and `polygraph`.

The module `generators` contains functions for creating a number of different graphs (all networkx type objects), including the deceptive graphs that we found. [Examples](#examples) below shows how to use a number of functions in `generators` to create graphs, including graphs of the families we designed in our search for deceptive graphs.

The module `polygraph` contains functions for computing walk-classes, checking flip-flop conditions, and
checking for deceptiveness of an input graph. We give examples of usage in [Examples](#examples) below. For in-
depth details on individual functions, see their documentation in `/code/polygraph.py`. Here is a brief overview:

| Function | Description |
| -------- | ----------- |
| walk_classes | Returns metadata about a graph\'s walk-classes |
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

Here are examples of using our codes for

1. generating graphs
   * pyramid prism
   * spidertorus
2. analyzing walk-classes of an input graph
3. checking whether an input graph satisfies necessary conditions for deceptiveness

### Generating a Pyramid Prism

Pyramid prisms are a graph family we designed in an attempt to produce deceptive graphs.
A pyramid prism has two parameters: faces and layers.
Our graph generator can be used to generate networkx pyramid prism graphs with face and layer
values specified as inputs. This code produces a pyramid prism with 4 faces and 0 layers:

```python
# Import generators
from code import generators as gen

# Construct a pyramid prism with 4 faces and 0 layers
pyramid_prism = gen.pyramid_prism(4, 0)
```
After running the above code, `pyramid_prism` will be a networkx object,
so running `pyramid_prism.nodes()` will output a list of the graph\'s nodes:

  `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`

### Generating a Spidertorus

`generators.spider_torus()` takes three parameters for the construction of a spidertorus graph: degree, length, and number of copies in each ring starting from the first level and working outwards. The `spider_torus()` function returns a
dictionary object containing the graph and some other metadata. Here's how to create a spidertorus
of degree 4, length 2, with an inner ring of 5 and outer ring of 3.

```python
# Import generators
from code import generators as gen

# Construct
spidertorus = gen.spider_torus(4, 2, [5, 3])
```
In contrast with most of our graph generating functions, this function does not output a networkx object.
Instead, this outputs a dict containing a networkx representation of the graph as well as additional information.
Running the above code and then calling `print(spidertorus)`will output
```python
{'graph': <networkx.classes.graph.Graph object at 0x7f0e80aeb710>, 'representatives': [0, 4, 8], 'degree': 4, 'length': 2, 'copies': [5, 3]}
```
You can then obtain the networkx object by calling `graph = spidertorus['graph']`.

In addition to a networkx object representation of the graph, the dict output by `gen.spidertorus` also contains a list of nodes that represent the distinct walk-classes of that spider-torus. Calling `list_of_reps = spidertorus['representatives']` creates a list of nodes, each node representing a distinct walk-class of the spidertorus.
For the above example, the output of `print(spidertorus['representatives'])` is `[0, 4, 8]`, indicating that nodes 0, 4, and 8 each represent a distinct walk-class of nodes.

### Analyzing Walk Classes

We now turn to functionalities in our `polygraph` module.
First we introduce our function for determining the distinct walk-classes of an input graph,
`polygraph.walk_classes()`.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a pyramid prism
pyramid_prism = gen.pyramid_prism()

# Analyze walk classes
pyramid_prism_walk_class_dict = polygraph.walk_classes(pyramid_prism)
```
The function `polygraph.walk_classes()` outputs a dict containing information about the input graph.
Running the above code and then calling `print(pyramid_prism_walk_class_dict.keys())` will print the following:
```python
dict_keys(['num_classes', 'classes', 'diag_matrix', 'uniq_rows', 'uniq_matrix', 'eig_matrix', 'graph'])
```
For a detailed description of each object, see the documentation in `code/polygraph.py`.
The key `'classes'` will return a dict that contains a list of nodes that are in each walk class. For the current example, calling `pyramid_prism_walk_class_dict['classes']` will print
```python
{0: [0, 7], 1: [1, 2, 3, 4, 5, 6]}
```

We remark that the `walk_classes()` function can be a little slow in practice for large graphs as its worst case runtime is `O(n^4)` where `n` is the number of nodes in the graph.
For a faster algorithm for analyzing spidertorus graphs, see the specialized `spider_torus_walk_classes` in the `polygraph` module.


### Checking for Deceptiveness - Not Deceptive by Pair-Wise Flip-Flopping

Pair-Wise Flip-Flopping is a necessary condition for a graph to be deceptive.
Here is an example of a graph that does not pass the pair-wise metric.

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
Running this code will print `False`, indicating the pyramid prism with 2 sides and 3 layers
does not meet the necessary criterion to be deceptive.

### Checking for Deceptiveness - Not Deceptive by Average-Condtion Flip-Flopping

Average-Condition Flip-Flopping is a necessary condition for a graph to be deceptive that can complement the pair-wise condition.
Here is an example of a graph that passes the pair-wise condition, but does not pass the average-condition metric.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 4-sided, 1-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(4, 1)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# First Check for Pair-Wise Flip-Flopping, which will return True
print(polygraph.pair_wise_flip_flopping(walk_obj['eig_matrix']))
```
Running the above code will print `True`, indicating the graph satisfies the pair-wise flip-flop condition.
However, running
```python
print(polygraph.average_condition_flip_flopping(walk_obj['eig_matrix']))
```
will instead return `False`, proving that this graph does not satisfy the necessary average-condition, and so must not be deceptive.


### Checking for Deceptiveness - Deceptive by Positive Linear System Check

The above conditions were merely necessary conditions for deceptiveness---satisfying those conditions does not guarantee the input graph is deceptive. Now we turn to conditions that are sufficient for proving deceptiveness.

The positive linear system check is a linear program we designed to be
a sufficient condition for the deceptiveness of an input graph.
Here is an example of calling our function that implements the check:
```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a 4-sided, 0-layer pyramid prism using provided graph generators
pyramid_prism = gen.pyramid_prism(4, 0)

# Compute walk class info
walk_obj = polygraph.walk_classes(pyramid_prism)

# Check for a solution to the system Wx = e
print(polygraph.positive_linear_system_check(walk_obj))
```
Running the above code will print output similar to, if not identical to, the following:
```python
     fun: 0.0015427388310380642
 message: 'Optimization terminated successfully.'
     nit: 8
   slack: array([ 0.        ,  0.        ,  0.        ,  0.        ,  0.00132889,
        0.00021384])
  status: 0
 success: True
       x: array([  1.00000000e-10,   1.00000000e-10,   1.00000000e-10,
         1.00000000e-10,   1.32889351e-03,   2.13844921e-04])
```
The positive linear system check returns a result from `scipy.optimize.linprog`. Successful
optimization will return `True` for success with a solution set for `x`, which indicates the input graph is provably deceptive.
Different solutions, and hence different values of `x` and `fun`, might be returned; the important detail is whether `success` is `True` or not.


### Checking for Deceptiveness - Deceptive by Nonnegative Linear System Check

The nonnegative linear system check is another linear program we designed to be
a sufficient condition for the deceptiveness of an input graph.
A significant difference from the positive linear system is this check is capable of producing an actual instance of a deceptive function so that the deceptiveness can be observed.
Here is an example of calling our function that implements the check:

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

Running the above code will print the following:
```python     fun: 880.04893632916662
 message: 'Optimization terminated successfully.'
     nit: 9
   slack: array([   0.        ,    0.        ,    0.        ,    0.        ,
          1.00267957,    0.        ,  878.04625676])
  status: 0
 success: True
       x: array([  1.66666667e-01,   1.66666667e-01,   1.66666667e-01,
         1.66666667e-01,   1.16934623e+00,   1.66666667e-01,
         8.78046257e+02])
```

Similar to the positive linear system check, the nonnegative linear system check returns a result from `scipy.optimize.linprog`. Successful optimization will return `True` for success, and the solution set for `x` will contain coefficients that can be used to make a deceptive function for the input graph. Again, different solutions, and hence different values of `x` and `fun`, might be returned; the important detail is whether `success` is `True` or not.

### Checking for Deceptiveness - Inconclusive

When either linear system check returns `True`, then we know for sure the input graph is deceptive.
However, if either linear system check returns `False`, we cannot conclude whether or not the input graph is deceptive.
In the following code, the linear system check fails:

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a deceptive snowflakecycle
snowflakecycle = gen.snowflakecycle(5, 3, 3)

# Compute walk class info
walk_obj = polygraph.walk_classes(snowflakecycle)

# Check for a solution to the system Wx = e
polygraph.nonnegative_linear_system_check(walk_obj)
```
Running the above code outputs the following:
```python
     fun: 5.0444295204524199
 message: 'Optimization failed. Unable to find a feasible starting point.'
     nit: 5
  status: 2
 success: False
       x: nan

```
The failure of the optimization program, and hence the nonnegative linear system check, is indicated by `Success: False`. When this occurs, no conclusion can be drawn about the deceptiveness of the input graph using our current theory.

### Analyzing a Deceptive Spidertorus

The spidertorus graphs we designed grow large rather quickly, but they are sparse and specially structured graphs. We designed special functions to compute their walk classes and analyze their deceptiveness efficiently. Here is an example of how to efficiently compute the walk classes of a spidertorus graph, and use the walk class information to check for deceptiveness.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a deceptive spidertorus
spidertorus_obj = gen.spider_torus(4, 2, [5, 3])

# Compute walk class info
walk_obj = polygraph.spider_torus_walk_classes(spidertorus_obj)

# Check for a solution to the system Wx = (gamma * e) - g
polygraph.nonnegative_linear_system_check(walk_obj)
```
Similar to the above successful call to a linear system check, the output of this code block should be of the form:
```python
fun: 8.993326346058371
 message: 'Optimization terminated successfully.'
     nit: 8
   slack: array([ 0.        ,  0.50365524,  0.        ,  0.01374805,  7.7592564 ])
  status: 0
 success: True
       x: array([ 0.5       ,  0.6703219 ,  0.04166667,  0.02208138,  7.7592564 ])
```
As before, the important element here is that `success` is set to `True`.

### Printing a Graph With Node IDs
To output an image of a graph with its nodes labeled with node IDs, run the following code on the desired graph.
```python
# Import spiderdonuts modules
from code import graphs, generators as gen

# Generate a Chamfered Dodecahedron
cd = gen.chamfered_dodecahedron()

# Draw
graphs.draw_with_id(cd, 'out.png')
```

### Printing a Graph With Node Classes
To output an image of a graph with its nodes labeled with their walk-class numbers, run the following code on the desired graph.
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

----------

## Reproducing results from paper
Here we use our codes to reproduce claims made about explicit deceptive graphs in our paper *When Centrality Measures Deceive Us* by Eric Horton, Kyle Kloster, and Blair D. Sullivan.

### Analyzing Deceptive Spidertorus with positive
This is the spidertorus graph from Figure 3.1 in the paper; our code establishes deceptiveness using Corollary 3.6 from the paper.

```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate a deceptive spidertorus
spidertorus_obj = gen.spider_torus(4, 2, [5, 3])

# Compute walk class info
walk_obj = polygraph.spider_torus_walk_classes(spidertorus_obj)

# Check for a solution to the system Wx = e
print(polygraph.positive_linear_system_check(walk_obj))
```
Running the above code will print output similar to, if not identical to, the following:
```python
     fun: 0.0015427388310380642
 message: 'Optimization terminated successfully.'
     nit: 8
   slack: array([ 0.        ,  0.        ,  0.        ,  0.        ,  0.00132889,
        0.00021384])
  status: 0
 success: True
       x: array([  1.00000000e-10,   1.00000000e-10,   1.00000000e-10,
         1.00000000e-10,   1.32889351e-03,   2.13844921e-04])
```
As noted in our code examples above, the optimization returning `True` for success indicates the linear solver produced a positive solution to the equation `W*x=e`. By Corollary 3.6, this demonstrates the graph is *f*-deceptive for some analytic function f with positive power-series coefficients.


### Analyzing KKS graph
The graph `G(4,5)` was first shown to be deceptive in the paper *Walk-regularity and walk entropy* by Kyle Kloster, Dan Kral, and Blair D. Sullivan. In our manuscript we generalized this graph to the graph `G(c,m)`, depicted in Figure 6.1, which consists of an independent set of size `m` connected by a perfect matching to each of `m` different cliques of size `c`.

Both `G(4,5)` and `G(5,6)` are members of an entire family of graphs which we prove are deceptive in our manuscript. Here we show how to use our function `kks_graph(c,m)` for producing members of that family, `G(c,m)`. We then show both `G(4,5)` and `G(5,6)` are deceptive using Corollary 3.6 from our manuscript.


```python
# Import spiderdonuts modules
from code import polygraph, generators as gen

# Generate kks graphs
kks_graph = gen.kks_graph(4,5)
kks_graph2 = gen.kks_graph(5,6)

# Compute walk class info
walk_obj = polygraph.walk_classes(kks_graph)
walk_obj2 = polygraph.walk_classes(kks_graph2)

# Check for a solution to the system Wx = e
print(polygraph.positive_linear_system_check(walk_obj))
print(polygraph.positive_linear_system_check(walk_obj2))
```

Running the above code will print output similar to, if not identical to, the following:
```python
     fun: 0.0019244211908294355
 message: 'Optimization terminated successfully.'
     nit: 8
   slack: array([ 0.        ,  0.        ,  0.        ,  0.        ,  0.0016449 ,
        0.00027952])
  status: 0
 success: True
       x: array([  1.00000000e-10,   1.00000000e-10,   1.00000000e-10,
         1.00000000e-10,   1.64489600e-03,   2.79524793e-04])

     fun: 0.091666754746666676
 message: 'Optimization terminated successfully.'
     nit: 14
   slack: array([ 0.08333344,  0.        ,  0.00833332,  0.        ,  0.        ,  0.        ])
  status: 0
 success: True
       x: array([  8.33334381e-02,   1.00000000e-10,   8.33331621e-03,
         1.00000000e-10,   1.00000000e-10,   1.00000000e-10])
```
As noted in our code examples above, the optimization returning `True` for success indicates the linear solver produced a positive solution to the equation `W*x=e`. By Corollary 3.6, this demonstrates that the graphs G(4,5) and G(5,6) are *f*-deceptive for some analytic function f with positive power-series coefficients.


----------

## License

**Important**: spiderdonuts is *research software*, so you should cite us when you use it in scientific publications! Please see the CITATION file for citation information.

Spiderdonuts is released under the BSD license; see the LICENSE file.
Distribution, modification and redistribution, and incorporation into other
software is allowed.



## Acknowledgements

Development of the spiderdonuts software package was funded in part by
the [Gordon & Betty Moore Foundation Data-Driven Discovery Initiative](https://www.moore.org/programs/science/data-driven-discovery),
through a [DDD Investigator Award](https://www.moore.org/programs/science/data-driven-discovery/investigators)
to Blair D. Sullivan ([grant GBMF4560](https://www.moore.org/grants/list/GBMF4560)).
