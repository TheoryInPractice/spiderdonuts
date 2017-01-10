# Chatper 2: Spectral analysis of graph minor ancestors


## Random Minor Ancestor Graph Generator (RMAGG)

### Create function `ancestor, map = minor_top_ancestrify(minor, p_subdivision, d_shallowness)`

Given graph `minor`, this function outputs graph `ancestor` that has `minor` as a topological minor, and `map` which maps the nodes/edges of `ancestor` to those of `minor` to prove that `minor` is in fact a minor of `ancestor`.

* `minor` -- networkx graph
* `p_subdivision` -- scalar in (0,1], probability of each edge being subdivided.
* `d_shallowness` -- a probability vector, d. d[j] gives the probability that a particular edge subdivision is of shallowness j.

The input `parameters` should quantify how many modifications to `A` must be made to obtain `M`, i.e. how many edge contractions.


## Outline of Random Minor Ancestor Graph Generator (RMAGG)
INPUT:  `M`, the desired graph minor, and parameters that either (a) gives `G` as an input graph, or (b) specifies how a random graph `G` should be produced using a call to some other function.

OUTPUT: `G`, created according to input specifications, with `M` as a graph minor.

OVERVIEW:

1. Given minor `M`, perform randomized edge sub-divisions to create `A`, a minor-ancestor of `M`
2. Randomly generate `G` with `n` nodes and `e` edges. [The "random process" can be an input option of RMAGG]
3. Randomly embed `A` in `G`.
4. Output `G` and the list of nodes in `G` from which we can recover `M`.


Note the "randomly" part of each of those steps needs to be pinned down more precisely.

### Random modifications to `M`

This should be its own function: `A = minor_ancestrify(M, parameters)`
where `parameters` enable us to dictate how many edge sub-divisions there are, and maybe even how shallow the sub-divisions are.

Given `M` we want to output `A`, a graph that has `M` as a "shallow" minor, meaning we need not contract long paths of `A` in order to produce `M` as a minor. (We'll make this more precise later).

INPUTS:  `M` -- a graph, `r` -- a parameter that quantifies how many edge sub-divisions there are

OUTPUTS: `A` -- a minor-ancestor of `M`

### Generate the sparse large graph `G`

The function should accept two types of input:

1. Input type 1: pass the desired graph `G` into the function as an input.
2. Input type 2: pass an option to the function that specifies a type of random graph generator to use:

Erdos-Renyi, or the k-core generator, or networkx's random graphs.
This step should use the input `e` as a parameter to determine edge density.
It is acceptable if `e` determines the number of edges, or if it simply specifices the *expected number*  of edges.
For example, if we use Erdos-Renyi then `e` would be converted to a probability of edges existing -- which means `e` would only dictate the expected number of edges, not the actual number of edges.

### Plant A inside G
Randomly assign the nodes of `A` to nodes in `G`. Then "add" the edges of `A` to `G`.

### Output
Output the graph `G` as a networkx graph, and output a list of nodes of `G` that will enable efficient recovery of `M`. The best way to do this will probably be

* output list of nodes of `A` in `G`
* output list of nodes that must be contracted in `A` to produce `M`.



## Old notes

* I've been looking through the literature at possible ways to randomly generate a class of graphs with minor structure that is in some way controlled. I found at paper for randomly generating outerplanar graphs, from Bodirsky and Kang. I have to search a bit more to see if there are algorithms more interesting classes, but I'm having trouble finding anything else.

* I need to write up formally the specifics we've developed on how we'll generate graphs with some desired minor structure.
  * Fix a set of desired minors that we want to scan for (cliques and bicliques of different sizes?)
  * Fix a collection of graph-families with varying density: random trees, random outerplanar, sparse erdos reyni, sparse random prescribed-core
  * pin down details of forming minor ancestor from a given prescribed minor
  * pin down details of planting/attaching the minor ancestor to the random graph
