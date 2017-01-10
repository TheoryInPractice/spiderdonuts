# Struckpod

A module for generating the highly symmetric, polyhedral graphs for use in testing walk-entropy ideas

## Walks

Contains code for working with the walk properties of graphs.

Example Usage
```py
import code.common.generators as gen
import code.struckpod.walks as walks

res = walks.walk_classes(gen.chamfered_dodecahedron())
```
