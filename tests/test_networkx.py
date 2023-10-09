from pathlib import Path

import networkx as nx


def test_networkx():
    # Create an empty graph
    G = nx.DiGraph()

    # Add nodes with metadata
    G.add_node(1, name="Node 1", color="red")
    G.add_node(2, name="Node 2", color="blue")
    G.add_node(3, name="Node 3", color="green")

    # Add edges between nodes
    G.add_edge(1, 2, weight=0.5)
    G.add_edge(2, 3, weight=0.8)

    # Serialize the graph to disk in a common graph format (e.g., GraphML)
    output_folder = "./_output/"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    nx.write_graphml(G, f"{output_folder}/___test_graph.di.graphml")

    print(f"{G.nodes=}")
    print(f"{list(G.nodes)=}")
    print(f"{G.nodes.items()=}")
    print(f"{list(G.nodes.items())=}")
