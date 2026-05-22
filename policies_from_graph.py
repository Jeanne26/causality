import networkx as nx
import pickle



G2 = pickle.load(open('graphs/J_graph.pickle', 'rb'))

paths = list(nx.all_simple_edge_paths(G2, source="S0", target="S1"))
for path in paths:
    print(" -> ".join(f"{u} -[{G2.edges[u, v, key]['label']}]-> {v}" for u, v, key in path))