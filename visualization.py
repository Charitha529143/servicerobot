import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Visualization:

    def __init__(self):
        pass

    def animate_robot(self, G, route, charging=None, obstacles=None):

        if charging is None:
            charging = []

        if obstacles is None:
            obstacles = []

        fig, ax = plt.subplots(figsize=(12, 8))

        pos = {}

        for node in G.nodes():

            pos[node] = (
                G.nodes[node]["x"],
                G.nodes[node]["y"]
            )

        def update(frame):

            ax.clear()

            # Background graph
            nx.draw_networkx_edges(
                G,
                pos,
                ax=ax,
                edge_color="lightgray",
                width=1
            )

            # Nodes
            nx.draw_networkx_nodes(
                G,
                pos,
                node_size=250,
                node_color="skyblue",
                ax=ax
            )

            nx.draw_networkx_labels(
                G,
                pos,
                font_size=7,
                ax=ax
            )

            # Charging Stations
            if len(charging):

                nx.draw_networkx_nodes(
                    G,
                    pos,
                    nodelist=charging,
                    node_color="green",
                    node_size=450,
                    ax=ax,
                    label="Charging"
                )

            # Obstacles
            if len(obstacles):

                nx.draw_networkx_nodes(
                    G,
                    pos,
                    nodelist=obstacles,
                    node_color="red",
                    node_size=400,
                    ax=ax,
                    label="Obstacle"
                )

            # Traversed Path
            if frame > 0:

                travelled = []

                for i in range(frame):

                    travelled.append(
                        (route[i], route[i+1])
                    )

                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=travelled,
                    edge_color="orange",
                    width=4,
                    ax=ax
                )

            # Robot
            current = route[frame]

            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[current],
                node_color="purple",
                node_size=700,
                ax=ax
            )

            battery = max(0, 100 - frame * 2)

            ax.set_title(
                f"Service Robot Simulation\n"
                f"Current Node : {current}    "
                f"Battery : {battery}%"
            )

            ax.set_xlim(-5, 105)
            ax.set_ylim(-5, 105)

        ani = FuncAnimation(
            fig,
            update,
            frames=len(route),
            interval=700,
            repeat=False
        )

        plt.show()