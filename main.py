from graph_poison import P_graph, policies
from utils import *

if __name__ == "__main__":
    print('Politique no plan\n', optimal_policy_no_plan(P_graph))
    print("Politique plan\n", optimal_policy_plan(P_graph, horizon=3))

