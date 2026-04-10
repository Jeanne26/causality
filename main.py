from graphs import J_graph, P_graph, T_graph
from utils import *

if __name__ == "__main__":


    # P_pi_opt = optimal_policy_no_plan(P_graph)
    # analyze_policies(P_graph, P_graph.policies,list(P_graph.policies.keys()), "pi1", start_state="VO", agg_func=perplexite_agg, horizon=3, cout_max=5, pi_opt=P_pi_opt)
    


    # T_pi_opt = optimal_policy_plan(T_graph, horizon=2)
    # analyze_policies(T_graph, T_graph.policies, list(T_graph.policies.keys()), "pi1", start_state=0, agg_func=None, horizon=3, cout_max=5, pi_opt=T_pi_opt)
    
    
    J_pi_opt = optimal_policy_plan(J_graph, horizon=1)
    analyze_policies(J_graph, J_graph.policies, list(J_graph.policies.keys()), "pi3", start_state="S0", agg_func=None, horizon=2, cout_max=5, pi_opt=J_pi_opt)