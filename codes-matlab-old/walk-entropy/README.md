# walk-entropy

Studying the relationship between the walk behavior of nodes and the diagonal entries of f(A), a function of the adjacency matrix.

* a result from Estrada and de la Pena states that exp(A)_jj is constant (for all j) if and only if the graph is walk-regular.
* Benzi conjectured that or any function f(x) with strictly positive power-series coefficients, that a connected graph has constant diagonal f(A)_jj iff G is walk regular.


## Counter examples

We have constructed two counter examples:

* chamfered dodecahedron
* "double sided dreidel"

In both cases, the graphs have two classes of nodes (literally, two orbits), and each node class is contained in k-cycles of different lengths.
More concretely, the dreidel graph has nodes incident to only triangles, and nodes incident to both triangles and 4-cycles. (The chamfered dodecahedron has a node class incident to pentagons and hexagons and a node class incident to hexagons only). 

This difference in cycles enables the two node classes to "flip-flop":
there exists a walk length K1 such that class-A nodes have *more* length-K1 walks than class-B nodes have,
and another walk length K2 such that class-A nodes have *fewer* length-K2 walks than class-B nodes have.


## Theoretical explanation

THEOREM (rough draft):
(Blair and I haven't written this up precisely and double checked, but I am confident we can.)

For any graph with exactly two node classes, such that there exist at least two lengths K1 and K2 for which the node classes flip-flop,
we can construct a Benzi-type function f(x) such that f(A)_jj is constant.


Remark:

Graphs of the type constructed in the theorem above (i.e. flip-flop graphs) are not walk-regular (by definition of walk-regular).

## Questions to answer

* can we construct an infinite family of these highly symmetric graphs? (i.e. polyhedra with exactly two node classes determined by incidence to cycles of different lengths.)
* are there conditions on the counter-example functions that we construct that we can identify that make them "weird" ?
	* the f(x) that we construct are of the form f(x) = exp(A) + p(x), for a degree two polynomial. So they're infinitely differentiable!
* can we prove statements of the following forms?
	* "For each f(x) = exp(x) + p(x), does there exist some non-walk-regular graph such that f(A)_jj is constant? " (possibly with conditions on p(x) ? )
	* "For each non-walk-regular graph, does there exist an f(x) with f(A)jj constant" -- NO, this statement is not true. Any graph containing at least one node that does not flip-flop (MAKE THIS PRECISE) does not have any functions f(x) such that f(A)jj is constant.

* linear algebra for k node-classes, for k > 2.


<<<<<<< HEAD
## Generalizing to k node-classes

In our proof for the case of 2 node classes we simply showed a 2-by-2 linear system always had strictly postive solutions. We did so constructively, and merely required that the two rows off the nonnegative linear system "flip flopped", i.e. A(1,1) > A(2,1) but A(1,2) < A(2,2).

What conditions are necessary to guarantee a positive solution in the case of 3 node-classes? k node-classes? Note the linear system is going to be k-by-t where k is the number of distinct node classes, and t is the number of different walk-lengths we consider -- k is fixed, whereas t we can change (you can include any finite number of different walk lengths to try to get things to work; the questions are "how many do we need" and "what *kind* do we need in order to use the minimum possible t?"

In the k = 2 case, it sufffieced to use t = 2 different walk lengths, as long as the two flip-flopped. For k = 3, will it suffice to use t = 3 different terms if those three column vectors satisfy some property?

Properties to consider:

* MAX : use large enough t such that each node class has at least one column in which that node class is the largest value, i.e. for each i in [1,k] there exists some j in [1,t] such that A(i,j) = max(  A(:,j)  ). (Note this property reduces to the flip-flop property in the 2-by-2 case.) Does this property guarantee existence of a positive solution? (I don't think so, not sure)

* "Point-wise flip-flop" : it is definitely a necessary condition that for each pair of nodes u and v, there must exist at least one term j for which A(u,j) < A(v,j) and at least one term i for which A(u,i) > A(v,i) .
	* this condition alone is not sufficient though. Consider the matrix A = [ [ 5 2 1 ]^T ; [ 1 2 5 ]^T ]. No matter its coefficients, it can never produce Ax = a constant vector.

* "All-subsets flip-flop" : Fix two distjoint subsets of node classes, I and J. Suppose it is the case that for all columns c we have sum(A(I,c)) > sum(A(J,c)).

=======
## Graphs with 2 < k node classes

* Still trying to construct / find a graph with exactly 3 node classes.
* The linear algebra in for this is rich, requires some work:
	* It is unclear exactly what conditions must hold for the 2 < k to "flip flop" in such a way that guarantees a counter-example function exists.
	* 
>>>>>>> b8f587d4f8f44dc7b6038ecf551d6598f13065be
