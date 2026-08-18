import networkx as nx
import time
from cost_function import CostFunction


class ProposedTSP:

    def __init__(self, graph):

        self.G = graph
        self.cost = CostFunction()

    def solve(self, start="N1"):

        print("\n" + "=" * 70)
        print("PROPOSED DYNAMIC MULTI-OBJECTIVE ROUTING")
        print("=" * 70)

        start_clock = time.time()

        current = start

        visited = set([start])

        route = [start]

        total_distance = 0
        total_time = 0
        total_energy = 0
        total_penalty = 0
        total_cost = 0

        while len(visited) < self.G.number_of_nodes():

            best_node = None
            best_score = float("inf")
            best_path = None
            best_metrics = None

            for node in self.G.nodes():

                if node in visited:
                    continue

                try:

                    path = nx.shortest_path(
                        self.G,
                        current,
                        node,
                        weight="cost"
                    )

                except nx.NetworkXNoPath:
                    continue

                distance = 0
                travel_time = 0
                energy = 0
                penalty = 0

                for i in range(len(path)-1):

                    edge = self.G[path[i]][path[i+1]]

                    distance += edge["distance"]
                    travel_time += edge["time"]
                    energy += edge["energy"]
                    penalty += edge["obstacle_penalty"]

                score = self.cost.calculate(
                    distance,
                    travel_time,
                    energy,
                    penalty
                )

                if score < best_score:

                    best_score = score
                    best_node = node
                    best_path = path

                    best_metrics = (
                        distance,
                        travel_time,
                        energy,
                        penalty
                    )

            if best_node is None:
                break

            print(
                f"{current} --> {best_node} | Score = {best_score:.2f}"
            )

            d, t, e, p = best_metrics

            total_distance += d
            total_time += t
            total_energy += e
            total_penalty += p
            total_cost += best_score

            for node in best_path[1:]:

                if node not in route:
                    route.append(node)

            visited.add(best_node)
            current = best_node

        execution_time = time.time() - start_clock

        print("\nRouting Finished")

        return {

            "route": route,

            "visited_nodes": len(visited),

            "distance": round(total_distance, 2),

            "time": round(total_time, 2),

            "energy": round(total_energy, 2),

            "penalty": round(total_penalty, 2),

            "cost": round(total_cost, 2),

            "execution_time": round(execution_time, 5)

        }