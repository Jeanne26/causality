from graph_poison import P_graph, policies, terminals
from utils import *

if __name__ == "__main__":
    paths = list(nx.all_simple_paths(P_graph, source="VO", target="vivant", cutoff=3))
    res = find_paths(P_graph,terminals,"VO", depth_limit=1 )
    for r in res:
        print(r)
    # for p in paths:
    #     score = compute_score(p, P_graph, np.sum)
    #     print(p,score)