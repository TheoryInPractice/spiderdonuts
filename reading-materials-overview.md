
## Reading materials

I will be maintaining both an introductory text as well as a glossary in the "background-reading" subdirectory. I would be grateful if you point out any typos as we go along, and if you identify any new terminology so we can keep the glossary as comprehensive as possible! :-)



## Related Papers

### Structural sparsity

* Bodlaender, [A Tourist Guide through Treewidth](http://www.inf.u-szeged.hu/actacybernetica/edb/vol11n1_2/pdf/Bodlaender_1993_ActaCybernetica.pdf)

Has a good example of a tree decomposition and path decomposition to give more concrete understandings of those objects; includes applications of these decompositions and approaches for obtaining such decompositions, as well as a wealth of citations of related works. Sections 1,2, and 4 are the most useful, but the others provide details that are good to have. Also includes a discussion of fixed-parameter-tractability.


* [A linear algorithm for Cores Decomposition of Networks](http://vlado.fmf.uni-lj.si/pub/networks/doc/cores/cores.pdf)

Contains a good concrete example of a cores decomposition, and a nice linear algorithm for computing these decompositions.


### Matrix functions and walk-entropy

* Higham and Estrada, [Network Properties Revealed through Matrix Functions](http://epubs.siam.org/doi/pdf/10.1137/090761070)

Describes some basic properties of graph matrices that make matrix functions useful for analyzing network structure.

* Estrada and de la Pena, [Maximum walk entropy implies walk regularity](https://arxiv.org/abs/1406.5056)

This paper is difficult to read (uses notation from another field), but is necessary to cite for work related to walk entropy: the main result is that the matrix exponential guarantees "diag(exp(A)) is constant iff A is walk-regular"


### Papers that could be relevant

* Baur, et al. [Generating Graphs with Predefined k-Core Structure](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.164.8551&rep=rep1&type=pdf)

* Pittel, Spencer, Wormald, [Sudden emergence of a giant k-core in a random graph](https://www.cs.nyu.edu/spencer/papers/k-core.pdf)

Erdos Reyni graphs with n nodes and m edges (in expectation) have O(n)-size 2- and 3-cores with large probability. Not clear that this will be useful for our purposes.
