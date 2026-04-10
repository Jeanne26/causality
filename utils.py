import networkx as nx
import numpy as np


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


def is_terminal_state(state, graph):
    #les états terminaux sont ceux qui ont pour unique successeur eux memes
    out_edges = list(graph.out_edges(state))
    return len(out_edges)==1 and out_edges[0][1]==state

def terminals(graph):
    #retoyurne l'ensemble des états terminaux du graphe
    return [node for node in graph.nodes() if is_terminal_state(node, graph)]

def next_state(state, action, graph):
    #renvoie le successeur de state lorsque l'action action est appliquée
    for _, succ, data in graph.out_edges(state, data=True):
        if data['label'] == action:
            return succ
    raise ValueError(f"{state}: action {action} non valide pour cet état")

def get_path(graph, pi,S0):
    current_node = S0
    path = [current_node]
    while current_node not in graph.terminals:
        action = pi[current_node]
        path.append(action)
        current_node = next_state(current_node, action, graph)
        path.append(current_node)
    return path



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

def get_edge(graph,node1,node2):
    #renvoie l'arc entre node1 et node2 dans graph, si plusieurs arcs existent on utilise l'heuristique pour choisir
    edge = list(graph.get_edge_data(node1, node2).values())
    if not edge:
        raise ValueError(f"pas d'arc entre {node1} et {node2}")
    return edge


def astar_trace(graph,start,end):
    path = nx.astar_path(graph, start, end, weight='weight')
    res = []
    for i in range(len(path)-1):
        edge = get_edge(graph,path[i],path[i+1])
        res.append(path[i])
        res.append(edge)
    res.append(path[-1])
    return res


def find_paths(graph, start, path=None, seen=None, depth_limit=2):
    #explore le graph en partant de node et retourne tous les chemins de longueur distance depuis cette source
    #ou qui ont atteint un état terminal
    if path is None:
        path = [start]
    if seen is None:
        seen = {start}
    
    # limite profondeur
    if len(path)-1 >= depth_limit * 2:
        yield path
        return
    
    # etat terminal atteint
    if start in graph.terminals:
        yield path
        return
    
    # descendant direct
    desc = nx.descendants_at_distance(graph, start, 1)
    for n in desc:
        if n in seen: 
            yield path
        else:
            edge = get_edge(graph, start, n)
            new_path = path + [edge[0], n]
            yield from find_paths(graph, n, new_path, seen.union([n]), depth_limit)

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


def compute_score(state_path,graph, agg: lambda liste: np.mean(liste), choice=False):
    #pour un chemin (etat+event) donné, calcul le score du chemin en utilisant les poids des arcs et une fonction d'aggreg
    scores = []
    for i in range(0, len(state_path)-2 ,2):
        if choice and len(graph.out_edges(state_path[i]))<=1:
            continue
        edge_weight= get_edge(graph,state_path[i],state_path[i+2])[1]
        scores.append(edge_weight)
    return agg(scores)

def perplexite_agg(liste_score):
    assert len(liste_score)>0
    N= len(liste_score)
    return np.exp(-(1/N)* np.sum(np.log(liste_score)))

def gamma_agg(liste_score,gamma=.9):
    #aggregation qui prend en compte la position de l'événement dans le chemin, les événements plus proches du début du chemin sont plus importants que ceux proches de la fin
    #on normalise le score pour qu'il soit compris entre 0 et 1 
    assert len(liste_score)>0
    N = len(liste_score)
    for i in range(0,len(liste_score)):
        liste_score[i] = (gamma**i) *liste_score[i]
    if gamma == 1:
        return (N - np.sum(liste_score))/N
    sum_gamma = (1- gamma**(N))/(1 -gamma)
    return (sum_gamma - np.sum(liste_score))/sum_gamma



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



#=================================D_OPT============================================================



def distance_pi_opt(pi,pi_opt,state_path):
    denom = len(state_path)
    assert denom>0
    num = np.sum([1 for s in state_path if pi[s]!=pi_opt[s]] )
    return num/denom



#=================================D_Obs============================================================
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
    mini = abs(m-n)
    maxi = max(m,n)
    return dp[n][m]-mini/max(m,n)


def cout(graph,d_obs, S0, pi1,pi2,lambda1=1,lambda2=1, choice= False,pi_opt = None,agg = perplexite_agg):
    #pi1 politique observé pi2 la politique à evaluer relativement à pi1
    path1 = get_path(graph, pi1, S0)
    path2 = get_path(graph, pi2, S0)
    states1 = extract_sigma_state(path1)
    states2 = extract_sigma_state(path2)  

    if choice:
        # states1_choice = extract_sigma_state_choice(path1, graph)
        states2_choice = extract_sigma_state_choice(path2, graph)
    

    d_observation = d_obs(states1,states2)

    if pi_opt:
        if choice:
            d_optimale = distance_pi_opt(pi2, pi_opt, states2_choice)
        else:
            d_optimale = distance_pi_opt(pi2, pi_opt, states2)
    else:
        d_optimale = compute_score(path2,graph, agg,choice)
    return {"cout":lambda1*d_observation + lambda2*d_optimale,"d_obs":d_observation,"d_opt":d_optimale}

def critere_selection(graph, S0, pi1,pi2, cout_max, lambda1=1, lambda2=1, agg=perplexite_agg):
    res = cout(graph,levenshtein_distance, S0, pi1,pi2, lambda1=lambda1, lambda2=lambda2, agg=agg)
    path1 = get_path(graph, pi1, S0)
    path2 = get_path(graph, pi2, S0)
    return res['cout']<= cout_max and path1[-1]!=path2[-1]

def compute_all_res(graph, S0, pi1, pi2, pi_opt,agg, lambda1=1, lambda2=1):
    res ={'L+P1' :cout(graph,levenshtein_distance,S0, pi1, pi2,lambda1=lambda1, lambda2=lambda2, choice=True, agg=agg),
          'L+P2' :cout(graph,levenshtein_distance,S0, pi1, pi2,lambda1=lambda1, lambda2=lambda2, choice=False, agg=agg),
          'L+D1' :cout(graph,levenshtein_distance,S0, pi1, pi2,lambda1=lambda1, lambda2=lambda2, choice=True, pi_opt=pi_opt, agg=agg),
          'L+D2' :cout(graph,levenshtein_distance,S0, pi1, pi2,lambda1=lambda1, lambda2=lambda2, choice=False, pi_opt=pi_opt, agg=agg)}
    return res



def analyze_policies(graph, policies_dict, policy_names,baseline_policy_name, start_state, agg_func=None, horizon=3, cout_max=5, pi_opt=None, lambda1=1, lambda2=1):

    results = {}
    baseline_policy = policies_dict[baseline_policy_name]

    baseline_path = get_path(graph, baseline_policy, start_state)
    print(f"Baseline: {baseline_policy_name}, Path : {baseline_path}\n")
    for policy_name in policy_names:

        results[policy_name] = compute_all_res(graph, start_state, baseline_policy, 
                                                policies_dict[policy_name], pi_opt, agg_func, lambda1=lambda1, lambda2=lambda2)
    print( "| CF    |   Perplexité  | Distance à opt|  Levenshtein   |L +P1 | L +P2 | L +D1 | L+D2   |")
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
            print(f"Policy: {policy_name}, Cost: {cout:.2f}, Path: {path}")
        print("==========================================================================================")
    
    print(f"Politiques valides pour un cout max de {cout_max}:")
    for config in ["L+P1", "L+P2", "L+D1", "L+D2"]:
        print(f"Configuration : {config}")
        valid_policies = [name for name in policy_names if name != baseline_policy_name and critere_selection(graph, start_state, baseline_policy, policies_dict[name], cout_max, lambda1=lambda1, lambda2=lambda2, agg=agg_func)]
        print(f"Politiques valides: {', '.join(valid_policies)}\n")



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


