# sparkstruck
Exploring the relationship of graph sparsity, structure, spectrum, and walks.

In general, all code will be in Python interfacing with the networkx module.

## Table of Contents

* [Reading Materials](reading-materials-overview.md)
* [Repo Overview](repo_overview.md)
* [Code](code/README.md)

## Main research focuses

* Walk-entropy

One pillar of this project, which we'll call "Walk Entropy", studies the information about a graph encoded by its walk structure, and studies a graph's walk structure by looking at polynomials and functions of graph matrices.

For now, the goal here is to better understand how a graphs' walks and matrix functions relate to each other, and design some Python codes for glueing together different kinds of graphs where we can test our findings in a concrete setting. The kinds of graphs we'll want to put together will be highly structured / symmetric, like hypercubes or polygons we fit together to make polyhedra.

Eric will be primarily working on this component of Sparkstruck.

* Spectrum and structured sparsity

The other pillar of this project is two-fold: assembling a code repository for generating graphs with differents kinds of structural aspects (small clique size, small tree width, bounded degeneracy), and writing codes to examine different aspects of a graph's eigenvalues.

Jean-Claude will be primarily working on this component of Sparkstruck.

There will be lots of opportunities to apply the two project threads to each other -- using spectrum codes to analyze the symmetric graphs generated in walk-entropy, e.g., so I want all codes to be somewhat consistent in their graph formatting / the way functions are called.


## Learning resources
