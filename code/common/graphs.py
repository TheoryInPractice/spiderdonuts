"""Sparkstruck module for shared graph functions."""

# Imports
import matplotlib.pyplot as plot
import networkx as nx


def draw_with_category(graph, path):
    """Draw a graph using matplotlib, labeled with node property `category`.

    Parameters
    ----------
    graph : Networkx Graph
        The networkx graph to be plotted.
    path : String
        The filepath that the plot will be saved to.
    """
    # Create a new figure
    plot.figure()

    # Draw networkx graph
    nx.draw(
        graph,
        with_labels=True,
        labels=nx.get_node_attributes(graph, 'category')
    )

    # Save and close
    plot.savefig(path)
    plot.close()


def draw_with_id(graph, path):
    """Draw a graph using matplotlib, labeled with node id.

    Parameters
    ----------
    graph : Networkx Graph
        The networkx graph to be plotted.
    path : String
        The filepath that the plot will be saved to.
    """
    # Create a new figure
    plot.figure()

    # Draw networkx graph
    nx.draw(
        graph,
        with_labels=True
    )

    # Save and close
    plot.savefig(path)
    plot.close()
