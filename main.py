from graphs import J_graph, P_graph, T_graph,G1
from utils import *

if __name__ == "__main__":

    lambda1 = 1
    lambda2 = 1
    horizon = 5
    agg = geometrique_agg
    coût_max_obs = 5
    coût_max_opt = 5




    

    print(f"Parametres : lambda1={lambda1}, lambda2={lambda2}, horizon={horizon}, agg={agg.__name__}, coût_max_obs={coût_max_obs}, coût_max_opt={coût_max_opt}\n")
    print("===============================Poison=====================================\n")

    P_pi_opt = optimal_policy_no_plan(P_graph)

    analyze_policies(P_graph, P_graph.policies,list(P_graph.policies.keys()), "pi1", start_state="VO", agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=P_pi_opt, lambda1=lambda1, lambda2=lambda2)
    
    # print("===============================Test=====================================\n")
    # T_pi_opt = optimal_policy_plan(T_graph, horizon=2)
    # analyze_policies(T_graph, T_graph.policies, list(T_graph.policies.keys()), "pi1", start_state=0, agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=T_pi_opt, lambda1=lambda1, lambda2=lambda2)
    
    # print("===============================Jardinier=====================================\n")
    # J_pi_opt = optimal_policy_plan(J_graph, horizon=1)
    # analyze_policies(J_graph, J_graph.policies, list(J_graph.policies.keys()), "pi3", start_state="S0", agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=J_pi_opt, lambda1=lambda1, lambda2=lambda2)

    # print("===============================G1=====================================\n")
    # G1_opt = optimal_policy_no_plan(G1)
    # analyze_policies(G1, G1.policies, list(G1.policies.keys()),"pi1", start_state = 0,agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=G1_opt, lambda1=lambda1, lambda2=lambda2)
    
