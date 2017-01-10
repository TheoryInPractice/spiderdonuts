
# Structure of repository:

In general, all codes will be on Python and stored in `/sparkstruck/code/`. Each project member should maintain their own git branch, and merge via github pull requests. For the time being, their ought to be a couple different modules that we are building, which I begin to outline below. We might merge them as submodules into a single `sparkstruck` module later on, depending on the directions the projects go.


## struckpod

A module for generating the highly symmetric, polyhedral graphs for use in testing walk-entropy ideas
	* this module ought to contain codes for generating these graphs, as well as ...
	* functions for analyzing properties of any input graph (Eric, we talked about computing the `node-walk-classes`" of a graph -- that function should go in this module)
	* should include function that will load the chamferred dodecahedron, and pyramidprism-3 and -4.

## sparkpod

A module for generating graphs that are more randomized than symmetric, but have specified sparsity properties
	* function for extracting k-cores
	* function for generating a random graph that is a k-core, of specified size n and value k
	* function for building a graph with treewidth bounded by an input parameter

### minors!

	* functions for generating small graphs that have specified minors
		* 5-cliques, 3-bicliques, etc
	* functions that take an input minor graph and make small perturbations
	* we'll expand this as the project continues

## specpod

This does not necessarily have to be a module, but we do want to organize in a coherent way that codes we develop for checking spectral properties of our graphs. Functionalities we want to have include

	* compute full eigendecomposition, including values and vectors
	* eigendecomposition of extracted subgraphs
	* Once we have the eigenvalues and vectors, we want to look at:
		* large gaps between specific, consecutive eigenvalues
		* clusters of eigenvalues near specific numbers
		* Absolutely we'll be exploring for new types of features to look for

### Eigen experiments

The `eigen-information` properties that we consider looking at -- we are trying to look for answer to questions like the following:

	* what effect does it have on the spectrum if we all of a sudden plant a clique somewhere
	* if we all of a sudden plant a k-core somewhere
	* if we start with a very small treewidth graph and introduce some larger treewidth feature, how does the spectrum of the larger treewidth feature (clique, grid, etc) effect the spectrum of the original graph?
