import networkx as nx
import time

from battery_manager import BatteryManager
from traffic_manager import TrafficManager
from task_scheduler import TaskScheduler


class ADMOR:

    def __init__(self, G, tasks, sensor_logs, traffic):

        self.G = G

        self.scheduler = TaskScheduler(tasks)

        self.battery = BatteryManager(sensor_logs)

        self.traffic = TrafficManager(traffic)

    # ==========================================================
    # Priority Score
    # ==========================================================

    def priority_score(self, priority):

        if priority == "High":
            return 30

        elif priority == "Medium":
            return 15

        else:
            return 5

    # ==========================================================
    # Adaptive Cost
    # ==========================================================

    def adaptive_cost(
        self,
        edge,
        battery_penalty,
        traffic_penalty,
        priority
    ):

        score = self.priority_score(priority)

        cost = (

            0.30 * edge["distance"]

            + 0.20 * edge["time"]

            + 0.15 * edge["energy"]

            + 0.15 * edge["obstacle_penalty"]

            + 0.10 * battery_penalty

            + 0.10 * traffic_penalty

            - 0.10 * score

        )

        return round(cost, 2)

    # ==========================================================
    # Solve
    # ==========================================================

    def solve(self, start="N1"):

        print("\n" + "=" * 70)
        print("ADMOR ALGORITHM")
        print("=" * 70)

        start_clock = time.time()

        current = start

        route = [current]

        total_distance = 0

        total_time = 0

        total_energy = 0

        total_penalty = 0

        total_cost = 0

        completed = []

        tasks = self.scheduler.get_pending_tasks()

        for _, task in tasks.iterrows():

            pickup = task["Pickup_Node"]

            destination = task["Destination_Node"]

            priority = task["Priority"]

            print("\n---------------------------------------")
            print("Task :", task["Task_ID"])
            print("Priority :", priority)
            print("Pickup :", pickup)
            print("Destination :", destination)

            # ==================================================
            # Go to Pickup
            # ==================================================

            try:

                pickup_path = nx.shortest_path(

                    self.G,

                    current,

                    pickup,

                    weight="cost"

                )

            except nx.NetworkXNoPath:

                print("No path to pickup.")

                continue

            for i in range(len(pickup_path)-1):

                u = pickup_path[i]

                v = pickup_path[i+1]

                edge = self.G[u][v]

                battery_level, battery_penalty = self.battery.battery_penalty()

                traffic_level, traffic_penalty = self.traffic.current_traffic()

                adaptive = self.adaptive_cost(

                    edge,

                    battery_penalty,

                    traffic_penalty,

                    priority

                )

                total_distance += edge["distance"]

                total_time += edge["time"]

                total_energy += edge["energy"]

                total_penalty += edge["obstacle_penalty"]

                total_cost += adaptive

                if v not in route:

                    route.append(v)

            current = pickup

            print("Reached Pickup")

            # ==================================================
            # Deliver
            # ==================================================

            try:

                delivery_path = nx.shortest_path(

                    self.G,

                    pickup,

                    destination,

                    weight="cost"

                )

            except nx.NetworkXNoPath:

                print("No path to destination.")

                continue

            for i in range(len(delivery_path)-1):

                u = delivery_path[i]

                v = delivery_path[i+1]

                edge = self.G[u][v]

                battery_level, battery_penalty = self.battery.battery_penalty()

                traffic_level, traffic_penalty = self.traffic.current_traffic()

                adaptive = self.adaptive_cost(

                    edge,

                    battery_penalty,

                    traffic_penalty,

                    priority

                )

                total_distance += edge["distance"]

                total_time += edge["time"]

                total_energy += edge["energy"]

                total_penalty += edge["obstacle_penalty"]

                total_cost += adaptive

                if v not in route:

                    route.append(v)

            current = destination

            completed.append(task["Task_ID"])

            print("Delivered Successfully")

        end_clock = time.time()

        print("\n" + "=" * 70)
        print("ADMOR FINISHED")
        print("=" * 70)

        return {

            "algorithm": "ADMOR",

            "tasks_completed": len(completed),

            "route": route,

            "visited_nodes": len(route),

            "distance": round(total_distance,2),

            "time": round(total_time,2),

            "energy": round(total_energy,2),

            "penalty": round(total_penalty,2),

            "cost": round(total_cost,2),

            "execution_time": round(end_clock-start_clock,5)

        }