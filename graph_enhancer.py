import networkx as nx
import math


def node_distance(G, node1, node2):

    x1 = G.nodes[node1]["x"]
    y1 = G.nodes[node1]["y"]

    x2 = G.nodes[node2]["x"]
    y2 = G.nodes[node2]["y"]

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def connect_graph(G):

    print("\n" + "=" * 60)
    print("GRAPH ENHANCEMENT")
    print("=" * 60)

    components = list(nx.connected_components(G))

    print(f"\nConnected Components Before : {len(components)}")

    while len(components) > 1:

        c1 = list(components[0])
        c2 = list(components[1])

        best_u = None
        best_v = None
        best_distance = float("inf")

        # Find closest pair of nodes
        for u in c1:

            for v in c2:

                d = node_distance(G, u, v)

                if d < best_distance:

                    best_distance = d
                    best_u = u
                    best_v = v

        # Add bridge edge
        G.add_edge(

            best_u,

            best_v,

            distance=round(best_distance, 2),

            time=round(best_distance / 2, 2),

            energy=round(best_distance / 8, 2),

            obstacle_penalty=0,

            cost=round(best_distance, 2)

        )

        print(f"Added Bridge : {best_u} ---- {best_v}")

        components = list(nx.connected_components(G))

    print(f"\nConnected Components After : {len(components)}")

    if nx.is_connected(G):

        print("\nGraph is Fully Connected!")

    return G