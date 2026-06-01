import networkx as nx
import numpy as np
from agg_operators import *
from utils_graph import *

#===================Complétion politique et expertise====================

def complete_policy(pi, graph):
    #si une politique est definie partiellement on la complete, lorsqu'un unique arc sortant est disponible on
    #selectionne cet event, si plusieurs choix sont possibles on selectionne l'action la plus probable selon l'expert
    res_pi = pi.copy()
    for node in graph.nodes():
        if node not in res_pi:
            out_edges = list(graph.out_edges(node, data=True))
            if len(out_edges)==1:
                res_pi[node] = out_edges[0][2]['label']

            elif len(out_edges)>1:
                best_action= max(out_edges,key=lambda edge:edge[2]['weight'])
                res_pi[node]= best_action[2]['label']
    return res_pi


def complete_expertise(graph, partial_expertise, value=1):
    #complete une expertise partielle, ajout de la valeur par defaut pour les event non notés
    res = {s:{} for s in graph.nodes()}
    for state in graph.nodes():
        for _, succ, data in graph.out_edges(state, data=True):
            event_label = data["label"]
            if state in partial_expertise and event_label in partial_expertise[state]:
                res[state][event_label] = partial_expertise[state][event_label]
            else:
                res[state][event_label] = value
    return res

def add_expertise(graph, expertise):
    #ajoute une expertise au graphe en modifiant les poids des arcs
    for state in expertise.keys():
        for event_label in expertise[state].keys():
            for _, succ, data in graph.out_edges(state, data=True):
                if data['label'] == event_label:
                    data['weight'] = expertise[state][event_label]
                    break


#==================Extraction trace====================================

def extract_sigma(pi, graph,S0):
    #extrait le chemin emprunté par une politique pi à partir d'un état initial S0 dans le graphe graph
    path = [S0]
    current_state = S0
    while current_state not in graph.terminals:
        action = pi[current_state]
        path.append(action)
        next_s = next_state(current_state, action, graph)
        path.append(next_s)
        current_state = next_s
    return path

def extract_sigma_state(path):
    #extrait la séquence d'etats d'un chemin
    return path[::2]
def extract_sigma_event(path):
    #extrait la séquence d'événements d'un chemin
    return path[1::2]

def extract_sigma_state_choice(path,graph):
    #extrait la séquence d'etats d'un chemin qui possède strictement plus d'un arcs sortant
    path = extract_sigma_state(path)
    path = [s for s in path if len(graph.out_edges(s))>1]
    return path



#==================Politiques optimales==================
def optimal_policy_no_plan(graph):
    #politique optimale sans plannif choix de la meilleure action à chaque état
    policy = {}
    for s in graph.nodes():
        edges = list(graph.out_edges(s, data=True))
        if not edges:
            continue
        best_edge = max(edges, key=lambda edge: edge[2]['weight'])
        policy[s] = best_edge[2]['label']
    return policy

def optimal_policy_plan(graph,horizon, agg= perplexite_agg):
    #politique optimale avec plannification qui choisit l'evenement qui se situe sur le chemin qui maximise 
    #la fonction d'aggregation à un horizon n
    policy = {}
    for s in graph.nodes():
        if s in graph.terminals:
            policy[s] = get_edge(graph,s,s)[0]
            continue
        edges = list(graph.out_edges(s,data = True))
        if not edges:
            continue
        paths_from_s = list(find_paths(graph,s,depth_limit=horizon))
        best_path = min(paths_from_s, key=lambda path: compute_score(path, graph, agg))
        policy[s] = best_path[1]
    return policy


def optimal_policy_plan_astar(graph):
    #politique optimale avec astar qui choisit pour chaque état le premier événement du chemin qui maximise la fonction d'aggregation
    policy = {}
    augmented_graph = augment_graph(graph)
    for s in graph.nodes():
        if s in graph.terminals:
            policy[s] = get_edge(graph,s,s)[0]
            continue
        path = astar_trace(augmented_graph, s, "temp")
        policy[s] = path[1][0]
    return policy

#================================D_opt==============================================================

# def compute_score(path,graph, agg: lambda liste: np.mean(liste), choice=False):
#     #pour un chemin (etat+event) donné, calcul le score du chemin en utilisant les poids des arcs et une fonction d'aggreg
#     scores = []
#     for i in range(0, len(path)-2 ,2):
#         if choice and len(graph.out_edges(path[i]))<=1:
#             continue
#         #nb: on considère que le poids est tout le temps le dernier attribut 
#         edge= get_edge(graph,path[i],path[i+2])[-1]
#         scores.append(edge["weight"])
#     return agg(scores)


def compute_score(path,graph, agg: lambda liste: np.mean(liste), choice=False):
    #pour un chemin (etat+event) donné, calcul le score du chemin en utilisant les poids des arcs et une fonction d'aggreg
    scores = []
    for action in range(1, len(path)-1 ,2):
        scores.append(path[action]['weight'])
    return agg(scores)


def distance_pi_opt(pi,pi_opt,state_path):
    denom = len(state_path)
    assert denom>0
    num = np.sum([1 for s in state_path if pi[s]!=pi_opt[s]] )
    return num/denom





#=================================D_obs============================================================
def levenshtein_distance(path1, path2):
    #on ne prends pas en compte le dernier état car desavantage les scenarios valides qui n'ont pas le meme état terminal que la politique de référence
    s1 = path1[:-1]
    s2 = path2[:-1]
    n,m= len(s1), len(s2)
    dp = np.zeros((n+1,m+1))
    for i in range(n+1):
        for j in range(m+1):
            if i==0:
                dp[i][j] = j
            elif j==0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]: 
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) # insertion, deletion, substitution

    return dp[n][m]/max(m,n)


def levenshtein_distance_event(states1,states2,events1,events2,graph):
    n,m = len(events1), len(events2)
    dp = np.zeros((n+1, m+1))
    for i in range(n+1):
        for j in range(m+1):
            if i ==0:
                dp[i][j]=j
                
            elif j ==0:
                dp[i][j]=i
            elif events1[i-1]==events2[j-1]:
                dp[i,j]= dp[i-1][j-1]
            else:
                cout_sub = 1/len(graph.edges(states1[i]))
                dp[i,j] = min(1+ dp[i-1][j], 1+ dp[i][j-1], dp[i-1][j-1]+cout_sub)
    return dp[n][m]/max(m,n)
#=================================Cout total===========================================================
def cout(graph, S0, pi1,pi2,lambda1=1,lambda2=1, lambda3 =1, choice= False,pi_opt = None,agg = perplexite_agg,d_obs =levenshtein_distance,d_obs_event = levenshtein_distance_event):
    #pi1 politique observé pi2 la politique à evaluer relativement à pi1
    path1 = get_path(graph, pi1, S0)
    path2 = get_path(graph, pi2, S0)
    states1 = extract_sigma_state(path1)
    states2 = extract_sigma_state(path2)  

    if choice:
        states2_choice = extract_sigma_state_choice(path2, graph)
    

    d_observation = d_obs(states1,states2)
    d_observation_event = d_obs_event(states1,states2,extract_sigma_event(path1),extract_sigma_event(path2),graph)
    if pi_opt:
        if choice:
            d_optimale = distance_pi_opt(pi2, pi_opt, states2_choice)
        else:
            d_optimale = distance_pi_opt(pi2, pi_opt, states2)
    else:
        d_optimale = compute_score(path2,graph, agg,choice)
    return {"cout":lambda1*d_observation + lambda2*d_optimale+lambda3*d_observation_event,"d_obs":d_observation,"d_opt":d_optimale,"d_obs_e":d_observation_event}


#===============================Critère de sélection===========================================================

def critere_selection(graph, S0, pi1,pi2, cout_max_obs, cout_max_opt, lambda1=1, lambda2=1, agg=perplexite_agg):
    res = cout(graph, S0, pi1,pi2, lambda1=lambda1, lambda2=lambda2, agg=agg,d_obs =levenshtein_distance)
    cout_res = res["d_obs"]*lambda1 < cout_max_obs and res["d_opt"]*lambda2 < cout_max_opt
    path1 = get_path(graph, pi1, S0)
    path2 = get_path(graph, pi2, S0)
    return cout_res and path1[-1]!=path2[-2]


#===============================Analyse des politiques===========================================================

def compute_all_res(graph, S0, pi1, pi2, pi_opt,agg, lambda1=1, lambda2=1):
    res ={'L+P1' :cout(graph,S0,pi1,pi2,lambda1=lambda1,lambda2=lambda2,choice=True, agg=agg,d_obs =levenshtein_distance),
          'L+P2' :cout(graph,S0,pi1,pi2,lambda1=lambda1,lambda2=lambda2,choice=False, agg=agg,d_obs =levenshtein_distance),
          'L+D1' :cout(graph,S0,pi1,pi2,lambda1=lambda1,lambda2=lambda2,choice=True, pi_opt=pi_opt, agg=agg,d_obs =levenshtein_distance),
          'L+D2' :cout(graph,S0,pi1,pi2,lambda1=lambda1,lambda2=lambda2,choice=False, pi_opt=pi_opt, agg=agg,d_obs =levenshtein_distance)}
    return res



def analyze_policies(graph, policies_dict, policy_names,baseline_policy_name, start_state, agg_func=None, horizon=3, cout_max_obs=5, cout_max_opt=5, pi_opt=None, lambda1=1, lambda2=1):

    results = {}
    baseline_policy = policies_dict[baseline_policy_name]

    baseline_path = get_path(graph, baseline_policy, start_state)
    print(f"Baseline: {baseline_policy_name}, Path : {baseline_path}\n")
    for policy_name in policy_names:

        results[policy_name] = compute_all_res(graph, start_state, baseline_policy, 
                                                policies_dict[policy_name], pi_opt, agg_func, lambda1=lambda1, lambda2=lambda2)
    print( f"| CF    |   {agg_func.__name__}  | Distance à opt|  Levenshtein   |L +P1 | L +P2 | L +D1 | L+D2   |")
    print( "|       |   P1  |   P2  |   D1  |   D2  |       L        |      |       |       |        |")
    for policy_name in policy_names:
        if policy_name == baseline_policy_name:
            continue
        res = results[policy_name]
        print(f"|{policy_name}  |  {res['L+P1']['d_opt']:.2f} |  {res['L+P2']['d_opt']:.2f} |  {res['L+D1']['d_opt']:.2f} |"
            f"  {res['L+D2']['d_opt']:.2f} |     {res['L+P1']['d_obs']:.2f}       | {res['L+P1']['cout']:.2f} |"  
            f"  {res['L+P2']['cout']:.2f} |  {res['L+D1']['cout']:.2f} |  {res['L+D2']['cout']:.2f}  |")
    print("==========================================================================================")
    
    for config in ["L+P1", "L+P2", "L+D1", "L+D2"]:
        print(f"Configuration : {config}")
        policies = [(name, results[name][config]['cout']) for name in policy_names if name != baseline_policy_name]
        policies.sort(key=lambda x: x[1])
        for policy_name,cout in policies:
            path = get_path(graph, policies_dict[policy_name], start_state)
            path = [path[i]["label"] if isinstance(path[i],dict) else path[i] for i in range(0,len(path))]
            print(f"Policy: {policy_name}, Cost: {cout:.2f}, Path: {path}")
        print("==========================================================================================")
    
    print(f"Politiques valides pour un cout max de {cout_max_obs} (obs) et {cout_max_opt} (opt):")
    for config in ["L+P1", "L+P2", "L+D1", "L+D2"]:
        print(f"Configuration : {config}")
        valid_policies = [name for name in policy_names if name != baseline_policy_name and critere_selection(graph, start_state, baseline_policy, policies_dict[name], cout_max_obs, cout_max_opt, lambda1=lambda1, lambda2=lambda2, agg=agg_func)]
        print(f"Politiques valides: {', '.join(valid_policies)}\n")






