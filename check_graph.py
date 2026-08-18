import networkx as nx
from graph_builder import G

print("=" * 60)
print("GRAPH ANALYSIS")
print("=" * 60)

print(f"Number of Nodes : {G.number_of_nodes()}")
print(f"Number of Edges : {G.number_of_edges()}")

# Check if graph is connected
connected = nx.is_connected(G)
print(f"\nIs Graph Connected? : {connected}")

# Find connected components
components = list(nx.connected_components(G))

print(f"\nNumber of Connected Components : {len(components)}")

for i, component in enumerate(components, start=1):
    print(f"\nComponent {i} ({len(component)} nodes)")
    print(sorted(component))