from graph_poison import P_graph, policies
from utils import *

if __name__ == "__main__":
    paths = list(nx.all_simple_paths(P_graph, source="VO", target="mort", cutoff=5))
    print(paths)
    print(paths[0], compute_score(paths[0], P_graph, np.mean))