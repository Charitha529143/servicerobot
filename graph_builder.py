import networkx as nx
import math

from data_loader import DataLoader

# ==========================================================
# Load Dataset
# ==========================================================

loader = DataLoader()
data = loader.load()

environment = data["environment"]
routes = data["routes"]
obstacles = data["obstacles"]

# ==========================================================
# Create Graph
# ==========================================================

G = nx.Graph()

positions = {}

# ==========================================================
# Add Nodes
# ==========================================================

for _, row in environment.iterrows():

    node = f"N{int(row['Node_ID'])}"

    G.add_node(
        node,
        x=row["X"],
        y=row["Y"],
        floor=row["Floor"],
        zone=row["Zone"],
        room=row["Room_Type"]
    )

    positions[node] = (row["X"], row["Y"])

# ==========================================================
# Obstacle Penalty Function
# ==========================================================

def obstacle_penalty(start, goal):

    sx = environment.loc[
        environment["Node_ID"] == int(start.replace("N", "")),
        "X"
    ].values[0]

    sy = environment.loc[
        environment["Node_ID"] == int(start.replace("N", "")),
        "Y"
    ].values[0]

    gx = environment.loc[
        environment["Node_ID"] == int(goal.replace("N", "")),
        "X"
    ].values[0]

    gy = environment.loc[
        environment["Node_ID"] == int(goal.replace("N", "")),
        "Y"
    ].values[0]

    mx = (sx + gx) / 2
    my = (sy + gy) / 2

    penalty = 0

    for _, obs in obstacles.iterrows():

        d = math.sqrt(
            (obs["X"] - mx) ** 2 +
            (obs["Y"] - my) ** 2
        )

        if d < 15:

            if obs["Risk"] == "High":
                penalty += 30

            elif obs["Risk"] == "Medium":
                penalty += 20

            else:
                penalty += 10

    return penalty

# ==========================================================
# Cost Function
# ==========================================================

def calculate_cost(distance, time, energy, penalty):

    cost = (
        0.40 * distance +
        0.30 * time +
        0.20 * energy +
        0.10 * penalty
    )

    return round(cost, 2)

# ==========================================================
# Add Edges
# ==========================================================

for _, row in routes.iterrows():

    start = row["Start"]
    goal = row["Goal"]

    penalty = obstacle_penalty(start, goal)

    cost = calculate_cost(
        row["Distance"],
        row["Travel_Time"],
        row["Energy"],
        penalty
    )

    G.add_edge(
        start,
        goal,
        distance=row["Distance"],
        time=row["Travel_Time"],
        energy=row["Energy"],
        obstacle_penalty=penalty,
        cost=cost
    )

# ==========================================================
# Graph Summary
# ==========================================================

def graph_summary():

    print("\n" + "=" * 60)
    print("GRAPH CREATED")
    print("=" * 60)

    print("Nodes :", G.number_of_nodes())
    print("Edges :", G.number_of_edges())

    print("\nFirst 5 Nodes\n")

    for node, attr in list(G.nodes(data=True))[:5]:
        print(node, attr)

    print("\nFirst 5 Edges\n")

    for u, v, attr in list(G.edges(data=True))[:5]:

        print(f"{u} <--> {v}")
        print("Distance :", attr["distance"])
        print("Time     :", attr["time"])
        print("Energy   :", attr["energy"])
        print("Penalty  :", attr["obstacle_penalty"])
        print("Cost     :", attr["cost"])
        print("-" * 40)