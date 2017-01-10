# Sparkctruck Common

A Python module for shared code, if any.

## Generators

Generators contains a set of functions which return premade networkx graphs.

Example usage
```py
import code.common.generators as gen

g = gen.chamfered_dodecahedron()
```

## Graphs

Graphs contains a set of shared functions for working with graphs.

Example usage
```py
import code.common.graphs as graphs

graphs.draw_with_category(g, 'out.png')
```
