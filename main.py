from graphs import J_graph, P_graph, T_graph,G1
from utils import *

import pickle
from visualisation import show_res

def load_graphs():
    J_graph = pickle.load(open('graphs/J_graph.pickle', 'rb'))
    P_graph = pickle.load(open('graphs/P_graph.pickle', 'rb'))
    T_graph = pickle.load(open('graphs/T_graph.pickle', 'rb'))
    G1 = pickle.load(open('graphs/G1.pickle', 'rb'))
    AC = pickle.load(open('graphs/ac_p0.pickle', 'rb'))
    BW = pickle.load(open('graphs/bw_p0.pickle', 'rb'))
    return J_graph, P_graph, T_graph, G1, AC, BW

if __name__ == "__main__":

    lambda1 = 1
    lambda2 = 1
    horizon = 5
    agg = gamma_late
    coût_max_obs = 5
    coût_max_opt = 5

    J_graph, P_graph, T_graph, G1, AC, BW = load_graphs()
    
    
    print("===============================AC=====================================\n")
    AC.policies ={}
    for i in range(0,6):
        with open(f'policies/ac_p0/ac_p0_plan_policy_{i}.pickle', 'rb') as f:
            AC.policies[f'pi{i}'] = pickle.load(f)
            AC.policies[f'pi{i}'] = complete_policy(AC.policies[f'pi{i}'], AC)
    # analyze_policies(AC,AC.policies, list(AC.policies.keys()),"pi0","S0",agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=None, lambda1=lambda1, lambda2=lambda2)
    res_dico = {}
    for p in AC.policies:
        res_dico[p] = cout(AC,"S0",AC.policies["pi0"],AC.policies[p], agg = gamma_late)
    del res_dico["pi0"]
    show_res(res_dico)

    for p in AC.policies:
        print(p)
        print(extract_sigma_state(get_path(AC,AC.policies[p],"S0")))


    # print("===============================BW=====================================\n")
    # BW.policies ={}
    # for i in range(0,2):
    #     with open(f'policies/bw_p0/bw_p0_plan_policy_{i}.pickle', 'rb') as f:
    #         BW.policies[f'pi{i}'] = pickle.load(f)
    #         BW.policies[f'pi{i}'] = complete_policy(BW.policies[f'pi{i}'], BW)
    # analyze_policies(BW,BW.policies, list(BW.policies.keys()),"pi0","S0",agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=None, lambda1=lambda1, lambda2=lambda2)    

    

    # print(f"Parametres : lambda1={lambda1}, lambda2={lambda2}, horizon={horizon}, agg={agg.__name__}, coût_max_obs={coût_max_obs}, coût_max_opt={coût_max_opt}\n")
    # print("===============================Poison=====================================\n")

    # P_pi_opt = optimal_policy_no_plan(P_graph)

    # analyze_policies(P_graph, P_graph.policies,list(P_graph.policies.keys()), "pi1", start_state="VO", agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=P_pi_opt, lambda1=lambda1, lambda2=lambda2)
    
    # print("===============================Test=====================================\n")
    # T_pi_opt = optimal_policy_plan(T_graph, horizon=2)
    # analyze_policies(T_graph, T_graph.policies, list(T_graph.policies.keys()), "pi1", start_state=0, agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=T_pi_opt, lambda1=lambda1, lambda2=lambda2)
    

    # print("===============================Jardinier=====================================\n")
    # J_pi_opt = optimal_policy_plan(J_graph, horizon=1)
    # analyze_policies(J_graph, J_graph.policies, list(J_graph.policies.keys()), "pi3", start_state="S0", agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=J_pi_opt, lambda1=lambda1, lambda2=lambda2)

    # print("===============================G1=====================================\n")
    # G1_opt = optimal_policy_no_plan(G1)
    # analyze_policies(G1, G1.policies, list(G1.policies.keys()),"pi1", start_state = 0,agg_func=agg, horizon=horizon, cout_max_obs=coût_max_obs, cout_max_opt=coût_max_opt, pi_opt=G1_opt, lambda1=lambda1, lambda2=lambda2)
    
