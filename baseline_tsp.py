import networkx as nx
import time


class BaselineTSP:

    def __init__(self, G):

        self.G = G

    def solve(self, start="N1"):

        print("\n" + "=" * 70)
        print("BASELINE TSP (Nearest Neighbor)")
        print("=" * 70)

        start_time = time.time()

        visited = set()

        current = start

        route = [current]

        visited.add(current)

        total_distance = 0
        total_time = 0
        total_energy = 0
        total_penalty = 0

        while len(visited) < self.G.number_of_nodes():

            neighbors = []

            for neighbor in self.G.neighbors(current):

                if neighbor not in visited:

                    edge = self.G[current][neighbor]

                    neighbors.append(

                        (
                            edge["distance"],
                            neighbor,
                            edge
                        )

                    )

            if len(neighbors) == 0:

                # Go to nearest unvisited node using shortest path

                remaining = list(

                    set(self.G.nodes()) - visited

                )

                shortest = None

                best_path = None

                for node in remaining:

                    try:

                        path = nx.shortest_path(

                            self.G,

                            current,

                            node,

                            weight="distance"

                        )

                        dist = nx.shortest_path_length(

                            self.G,

                            current,

                            node,

                            weight="distance"

                        )

                        if shortest is None or dist < shortest:

                            shortest = dist

                            best_path = path

                    except:

                        pass

                if best_path is None:
                    break

                for i in range(len(best_path) - 1):

                    u = best_path[i]
                    v = best_path[i + 1]

                    edge = self.G[u][v]

                    total_distance += edge["distance"]
                    total_time += edge["time"]
                    total_energy += edge["energy"]
                    total_penalty += edge["obstacle_penalty"]

                    if v not in visited:

                        visited.add(v)

                    route.append(v)

                    current = v

            else:

                neighbors.sort()

                _, next_node, edge = neighbors[0]

                total_distance += edge["distance"]
                total_time += edge["time"]
                total_energy += edge["energy"]
                total_penalty += edge["obstacle_penalty"]

                current = next_node

                visited.add(current)

                route.append(current)

                print(

                    f"{route[-2]} --> {current}"

                    f" | Distance={edge['distance']}"

                )

        execution_time = time.time() - start_time

        print("\nBaseline Finished")

        return {

            "algorithm": "Nearest Neighbor TSP",

            "route": route,

            "visited_nodes": len(visited),

            "distance": round(total_distance, 2),

            "time": round(total_time, 2),

            "energy": round(total_energy, 2),

            "penalty": round(total_penalty, 2),

            "execution_time": round(execution_time, 5)

        }