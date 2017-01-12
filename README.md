# spiderdonuts

Exploring deceptive graphs and deceptive functions.

In general, all code will be in Python interfacing with the networkx module.

## Table of Contents

* [Reading Materials](reading-materials-overview.md)
* [Code](code/README.md)

## Main research focuses

The idea of "Walk Entropy" is concerned with the information about a graph encoded by the graph's walk structure. In this project, we study a graph's walk structure by looking at polynomials and functions of graph matrices.
The main focus is understanding when a non--walk-regular graph can "appear to be" walk-regular. The adjacency matrix M of a walk-regular graph will always have constant diagonal, no matter what function (or polynomial) we apply to the matrix, f(M). We study non--walk-regular graphs for which there exist functions (which we call "deceptive" functions) such that f(M) is constant-diagonal even though the graph is not walk-regular. Graphs for which such functions exist we call "deceptive graphs".

As part of this project we have developed some necessary and some sufficient conditions for graphs to be deceptive, as well as algorithms for constructing deceptive functions in some circumstances. This repository includes codes both for generating classes of graphs, some of which we have verified to be deceptive, as well as for checking whether or not a given graph is deceptive.
