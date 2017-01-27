"""A collection of functions used to generate pre-existing graphs."""

# Imports
import networkx as nx
import numpy as np
import os


# Determine the base path to the current directory
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def abs_path(relative):
    """Resolve a relative path to an absolute path based on current directory.

    Parameters
    ----------
    relative : string
        A file path relative to the current working file.

    Returns
    -------
    string
        The absolute path to the relative file.
    """
    return os.path.join(BASE_PATH, relative)


def chamfered_dodecahedron():
    """Return a networkx graph of a Chamfered Dodecahedron.

    Returns
    -------
    Networkx Graph
        A Networkx Graph object of a Chamfered Dodecahedron.
    """
    return nx.read_gml(abs_path('gml/chamfered_dodecahedron.gml'))


def pyramid_prism_3():
    """Return a networkx graph of a Pyramid Prism 3.

    Returns
    -------
    Networkx Graph
        A Networkx Graph object of a Pyramid Prism 3.
    """
    return nx.read_gml(abs_path('gml/pyramid_prism_3.gml'))


def pyramid_prism_4():
    """Return a networkx graph of a Pyramid Prism 4.

    Returns
    -------
    Networkx Graph
        A Networkx Graph object of a Pyramid Prism 4.
    """
    return nx.read_gml(abs_path('gml/pyramid_prism_4.gml'))


def pyramid_prism(faces=3, layers=0):
    """Generate a Pyramid Prism with `faces` sides and `layers` extra layers.

    The graph will be generated programatically,
    rather than loading from a saved .gml file.

    Parameters
    ----------
    faces : int, optional
        Number of sides which the generated prism will have
        (The default is 3).
    layers : int, optional
        Number of additional layers added to the middle of
        the prism (The default is 0).

    Returns
    -------
    Networkx Graph
        A Pyramid Prism graph with `faces` sides and
        `layers` extra layers.

    Raises
    ------
    Exception
        Raised if faces is less than or equal to zero or
        if layers is less than zero.
    """
    # Raise if faces <= 0 or layers < 0
    if faces <= 0 or layers < 0:
        raise Exception('faces must be > 0, layers >= 0')

    # Create an empty graph.
    g = nx.Graph()

    # Number of rows needed is 2 + number of extra layers
    # len_row is equal to number of faces
    num_rows = 2 + layers
    len_row = faces

    # Set graph top and bottom node labels
    top = 0
    bottom = (num_rows * len_row) + 1

    # Create rows
    rows = [
        [
            (i * len_row) + j
            for j in range(1, len_row + 1)
        ]
        for i in range(0, num_rows)
    ]

    # Add nodes to g
    g.add_nodes_from([
        top,
        *[node for row in rows for node in row],
        bottom
    ])

    # Add edges to g
    g.add_edges_from([
        # All edges from the top node to the first row
        *[(top, node) for node in rows[0]],

        # All edges from a row to the row below it
        *[
            edge
            for i in range(0, len(rows) - 1)
            for edge in zip(rows[i], rows[i + 1])
        ],

        # All edges connecting edges on a row
        *[
            (row[i], row[(i + 1) % len(row)])
            for row in rows
            for i in range(0, len(row))
        ],

        # All edges from the bottom row to the bottom node
        *[(bottom, node) for node in rows[-1]]
    ])

    # Return g
    return g


def fan_graph():
    """Create a fan graph.

    Returns
    -------
    Networkx Graph
        A fan graph.
    """
    return nx.read_gml(abs_path('gml/fan.gml'))


def snowflake():
    """Create a snowflake graph.

    Returns
    -------
    Networkx Graph
        A snowflake graph.
    """
    return nx.read_gml(abs_path('gml/snowflake.gml'))


def tiered_pyramid_prism(k=3):
    """Generate a Tiered Pyramid Prism with K sides.

    The graph will be generated programatically,
    rather than loading from a saved .gml file.

    Parameters
    ----------
    k : int, optional
        Number of sides which the generated prism will have
        (The default is 3).

    Returns
    -------
    Networkx Graph
        A Tiered Pyramid Prism graph with k sides.

    Raises
    ------
    Exception
        Raised if k argument is less than or equal to zero
    """
    return nx.read_gml(abs_path('gml/tiered_pyramid_prism.gml'))


def hexagonal_pyramid_prism():
    """Generate a hexagonal pyramid prism.

    Returns
    -------
    Networkx Graph
        A networkx graph of a hexagonal pyramid prism
    """
    return nx.read_gml(abs_path('gml/hexagonal_pyramid_prism.gml'))


def triangular_prism():
    """Generate a 3-layer triangular_prism graph."""
    return nx.read_gml(abs_path('gml/triangular_prism.gml'))


def triangular_orthobicupola():
    """Generate a triangular orthobicupola."""
    return nx.read_gml(abs_path('gml/triangular_orthobicupola.gml'))


def square_orthobicupola():
    """Generate a square orthobicupola."""
    return nx.read_gml(abs_path('gml/square_orthobicupola.gml'))


def orthobicupola(sides=3):
    """Generate an orthobicupola.

    The number of sides is taken as the number of
    sides on the top polygon of the bicupola. I.E.
    sides=3 will produce a triangular orthobicupola.

    Parameters
    ----------
    sides : Number
        Number of sides on the bicupola (default is 3).

    Returns
    -------
    Networkx Graph
        Generated graph of an orthobicupola.
    """
    # Generate a new graph
    g = nx.Graph()

    # Generate layers
    top = [i for i in range(0, sides)]
    middle = [i for i in range(sides, 3 * sides)]
    bottom = [i for i in range(3 * sides, 4 * sides)]

    # Add nodes
    g.add_nodes_from([*top, *middle, *bottom])

    # Add edges
    g.add_edges_from([
        # Add all edges between nodes of the same row
        *[
            (row[i], row[(i + 1) % len(row)])
            for row in [top, middle, bottom]
            for i in range(0, len(row))
        ],

        # Add all edges between the middle row
        # and the top and bottom rows
        *[
            (middle[i], row[i // 2])
            for row in [top, bottom]
            for i in range(0, len(middle))
        ]
    ])

    # Return
    return g


def rhombicuboctahedron():
    """Generate a rhombicuboctahedron graph."""
    return nx.read_gml(abs_path('gml/rhombicuboctahedron.gml'))


def snowflakecycle(flake_number=5, inner_cycle=5, outer_cycle=3):
    """Generate a snowflake cycle.

    Cycle can be customized with flake_number different snowflake-sides,
    inner_cycle different snowflakes connected in a cycle by their inner nodes,
    and outer_cycle different copies connected in a cycle by their outer nodes.

    The total number of nodes is (1+2*flake_number)*inner_cycle*outer_cycle

    Parameters
    ----------
    flake_number : Number
        Number of sides of the snowflake (default is 5).
    inner_cycle : Number
        Length of cycle connecting inner nodes of snowflakes (default 5).
    outer_cycle : Number
        Length of cycle connecting outer nodes of snowflakes (default 3).
        Generated graph of a snowflake-cycle.

    Returns
    -------
    Networkx Graph
        Snowflake Cycle
    """
    # Construct (k+1)-node snow-flake graph:
    # A k-cycle with a single node connected to every other vertex
    num_flake_nodes = (1 + 2 * flake_number)
    Cn = nx.cycle_graph(2 * flake_number)
    Adj = nx.adjacency_matrix(Cn).toarray()
    A_snowflake = np.zeros((num_flake_nodes, num_flake_nodes))
    A_snowflake[1:(num_flake_nodes), 1:(num_flake_nodes)] = Adj

    # Construct vector to identify "every other node" in the cycle
    temp_vec = np.zeros((2 * flake_number, 1))
    a_mod = 0
    for j in range(len(temp_vec)):
        if j % 2 == (a_mod % 2):
            temp_vec[j] = 1

    A_snowflake[1:(num_flake_nodes), 0] = np.squeeze(temp_vec)
    A_snowflake[0, 1:(num_flake_nodes)] = np.squeeze(temp_vec.T)

    # Next link together inner_cycle of these
    # snowflakes by their inner flake nodes
    D = np.zeros((num_flake_nodes))
    D[1:(num_flake_nodes)] = np.squeeze(temp_vec)
    D = np.diag(D)

    cycle_inner_g = nx.cycle_graph(inner_cycle)
    cycle_inner = nx.adjacency_matrix(cycle_inner_g).toarray()
    I_inner = np.identity(inner_cycle)
    A_inner = np.kron(I_inner, A_snowflake) + np.kron(cycle_inner, D)

    # Now link together outer_cycle copies of the inner_cycle graphs
    cycle_outer_g = nx.cycle_graph(outer_cycle)
    cycle_outer = nx.adjacency_matrix(cycle_outer_g).toarray()

    temp_vec = np.zeros((2 * flake_number, 1))
    for j in range(len(temp_vec)):
        if j % 2 == (a_mod + 1 % 2):
            temp_vec[j] = 1
    temp_vec = np.squeeze(temp_vec)
    D = np.zeros(num_flake_nodes)
    D[1:(num_flake_nodes)] = temp_vec

    I_outer = np.identity(outer_cycle)
    AG = np.kron(I_outer, A_inner) + np.kron(
        cycle_outer,
        np.kron(I_inner, np.diag(D))
    )
    AG = np.asmatrix(AG)

    return nx.from_numpy_matrix(AG)


def spider(degree, length):
    """Create a spider graph.

    Parameters
    ----------
    degree : Integer
        Degree of the center node (number of pendants)
    length : Integer
        Length of each pendant (not including the center node)

    Returns
    -------
    Networkx Graph
        Spider graph
    """
    # Create a single spoke and get its adjacency matrix W
    spoke = nx.path_graph(length)
    spoke_adj = nx.adjacency_matrix(spoke).todense()

    # Create the identity matrix of size degree
    identity = np.identity(degree)

    # Create the adjacency matrix for the graph containing
    # `degree` number unconnected spokes
    spokes = np.matrix(np.kron(spoke_adj, identity))

    # Calculate the total number of desired nodes in the graph
    num_nodes = (degree * length) + 1

    # Create a num_nodes x num_nodes matrix, filled with zeroes.
    # This will eventually be the matrix of the spider graph
    spider = np.zeros((num_nodes, num_nodes))

    # Add the spokes to the spider
    spider[1:num_nodes, 1:num_nodes] = spokes

    # Connect each spoke to the center
    spider[0, 1:degree + 1] = 1
    spider[1:degree + 1, 0] = 1

    # Construct and return a networkx graph from the matrix
    return nx.from_numpy_matrix(spider)


def spider_torus(degree, length, copies):
    """Create a torus of spider graphs.

    A torus is formed with the folling process:

    Take `copies[0]` copies of a spider graph and link them
    together in a ring by connecting each node in the first
    level of each spider to the same node in the adjacent
    spider graphs in the ring.

    Take `copies[1]` copies of the original ring, and link them
    together in a new ring by connection each node in the second
    level of each spider to the same node in the adjacent spider
    graphs in the ring.

    ...

    Repeat until reaching the outer level of the spider.

    Parameters
    ----------
    degree : Integer
        The degree of the base spider graph
    length : Integer
        The length of each arm of the base spider graph
    copies : List
        A list containing the number of copies of the
        previous level to maek at each level of the
        hyperchain.

    Returns
    -------
    Dict
        Dictionary containing
        graph           - The full hyperchain graph
        representatives - An list of representative nodes from each class,
                          in ascending order by level.
        degree          - Degree of the base spider graph
        length          - Length of each pendant
        copies          - Number of copies in each ring
    """

    # Raise an exception if a number of copies is not
    # specified for each level
    if len(copies) != length:
        raise Exception('Invalid number of copies.')

    # Create the base spider graph
    spider_graph = spider(degree, length)

    # Get the adjacency matrix and shape of the base spider
    spider_adj = nx.adjacency_matrix(spider_graph).todense()
    spider_rows, spider_cols = spider_adj.shape

    # Copy the spider adjacency matrix. This will be the base
    # matrix that gets built up into the hyperchain.
    adj = spider_adj.copy()

    # Number of copies of the original spider that exist
    # within the hyperchain
    num_duplcates = 1

    # Iterate over each level, building up the resulting hyperchain
    for level in range(length):

        # Get the number of copies being made of the
        # previous level
        num_copies = copies[level]

        # Construct a diagonal matrix which has a 1 for every
        # pair of nodes that will be connected in this level.
        # This is determined by taking the nodes from the
        # original spider graph that exist at `level` and
        # tiling it `num_duplcates` times.
        min_node = 1 + (level * degree)
        max_node = 1 + ((level + 1) * degree)
        row = np.zeros(spider_rows)
        row[min_node:max_node] = 1
        diagonal = np.diag(np.tile(row, num_duplcates))

        # Create a cycle graph equal in size to the number of copies
        # being made for this level. Save its adjacency matrix.
        cycle = nx.adjacency_matrix(nx.cycle_graph(num_copies)).todense()

        # Calculate the edges being added to the set of duplicates
        # as the kronecker product of the cycle graph with the
        # diagonal matrix which links nodes together
        edges = np.kron(cycle, diagonal)

        # Use the kronecker product to create a single graph
        # containing n unconnected copies of the base adjacency
        # matrix
        duplicates = np.kron(np.identity(num_copies), adj)

        # Update the number of duplicates
        num_duplcates *= num_copies

        # Update the adjacency matrix to be the set of duplicates
        # plus the set of edges being added.
        adj = duplicates + edges

    # Return the graph formed from the final adjacency matrix
    return {
        'graph': nx.from_numpy_matrix(adj),
        'representatives': [level * degree for level in range(length + 1)],
        'degree': degree,
        'length': length,
        'copies': copies
    }
