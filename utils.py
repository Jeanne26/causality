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


def next_state(state, action, graph):
    #renvoie le successeur de state lorsque l'action action est appliquée
    for _, succ, data in graph.out_edges(state, data=True):
        if data['label'] == action:
            return succ
    raise ValueError(f"{state}: action {action} non valide pour cet état")


def extract_sigma(pi, graph,S0):
    #extrait le chemin emprunté par une politique pi à partir d'un état initial S0 dans le graphe graph
    path = [S0]
    current_state = S0
    terminals = [node for node in graph.nodes() if is_terminal_state(node, graph)]
    while current_state not in terminals:
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


def get_edge(graph,node1,node2):
    #renvoie l'arc entre node1 et node2 dans graph, si plusieurs arcs existent on utilise l'heuristique pour choisir
    print(node1, node2)
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


#==================Policies optimales==================
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


def compute_score(path,graph, agg: lambda liste: np.mean(liste)):
    #pour un chemin donné calcul le score du chemin en utilisant les poids des arcs et une fonction d'aggreg
    scores = []
    for i in range(0, len(path)-2, 2):
        edge = get_edge(graph,path[i],path[i+2])
        print(edge)
        scores.append(edge[1])
    return agg(scores)