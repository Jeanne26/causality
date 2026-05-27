import networkx as nx
import pickle
import argparse

#recupere des politiques à partir d'un graphe en générant tous les chemins simples entre les etats initiaux et les etats terminaux
#les politiques sont incompletes
#attention non adapté pour graphe de taille importante complexite en O(n!)
argparser = argparse.ArgumentParser()
argparser.add_argument('--graph_file', type=str, default= "graphs/P_graph.pickle", help="fichier du graphe" )
argparser.add_argument('--output_file', type=str, default="policies/P_graph_policies.pickle", help='fichier de sortie pour les politiques')
args = argparser.parse_args()

G2 = pickle.load(open(args.graph_file, 'rb'))
G2.policies = dict()
i=0

paths = []
for source in G2.inits:
    for target in G2.terminals:
        paths+= list(nx.all_simple_edge_paths(G2,source =source, target=target ))
for path in paths:

    p_name = f"pi{i}"
    G2.policies[p_name] = dict()
    for state, next_state,key in path:
        G2.policies[p_name][state]= G2.edges[state,next_state, key]["label"]
    G2.policies[p_name][next_state] = G2.edges[next_state,next_state,0]["label"]

    i+=1

pickle.dump(G2.policies, open(args.output_file, 'wb'))