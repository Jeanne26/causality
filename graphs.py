from utils import complete_expertise, add_expertise
import networkx as nx
import pickle

from utils import complete_policy, terminals

#========================POISON===============================================

P_graph = nx.MultiDiGraph()
P_graph.add_edge("VO", "vivant", label="boire", weight=1)
P_graph.add_edge("VO", "VE", label="emp", weight=0.1)
P_graph.add_edge("VO", "VV", label="vider", weight=0.5)
P_graph.add_edge("VE", "VV", label="vider", weight=0.5)
P_graph.add_edge("VE", "mort", label="boire", weight=0.1)
P_graph.add_edge("VE", "VA", label="antidote", weight=1)
P_graph.add_edge("VA", "vivant", label="boire", weight=1)
P_graph.add_edge("VV", "mort", label="$\\varnothing$", weight=0.5)
P_graph.add_edge("vivant", "vivant", label="$\\varnothing$", weight=1)
P_graph.add_edge("mort", "mort", label="$\\varnothing$", weight=1)


P_graph.terminals = terminals(P_graph)
P_graph.inits = {"VO"}

pi1 = {'VO': 'emp', 'VE': 'boire'}
pi2 = {'VO': 'boire'}   
pi3 = {'VO': 'vider', 'VV': '$\\varnothing$'}
pi4 = {'VO': 'emp', 'VE': 'vider', 'VV': '$\\varnothing$'}
pi5 = {'VO': 'emp', 'VE': 'antidote', 'VA': 'boire'}
P_graph.policies = {"pi1": complete_policy(pi1, P_graph), "pi2": complete_policy(pi2, P_graph), "pi3": complete_policy(pi3, P_graph), "pi4": complete_policy(pi4, P_graph), "pi5": complete_policy(pi5, P_graph)}
    



#=======================TEST==================================================
T_graph = nx.MultiDiGraph()

T_graph.add_edge(0,1,label="a",weight=0.7)
T_graph.add_edge(0,2,label="b",weight=0.4)

T_graph.add_edge(1,3,label="a",weight=0.2)
T_graph.add_edge(1,4,label="b",weight=0.2)



T_graph.add_edge(2,5,label="a",weight=0.9)
T_graph.add_edge(2,6,label="b",weight=0.9)


T_graph.add_edge(3,3, label="$\\varnothing$", weight=1)
T_graph.add_edge(4,4, label="$\\varnothing$", weight=1)
T_graph.add_edge(5,5, label="$\\varnothing$", weight=1)
T_graph.add_edge(6,6, label="$\\varnothing$", weight=1)
T_graph.terminals = terminals(T_graph)
T_graph.inits = {0}
pi1 = {0: "a", 1: "a"}
pi2 = {0: "b", 2: "a"}
pi3 = {0: "a", 1: "b"}
pi4 = {0: "b", 2: "b"}
T_graph.policies = {"pi1": complete_policy(pi1, T_graph), "pi2": complete_policy(pi2, T_graph), "pi3": complete_policy(pi3, T_graph), "pi4": complete_policy(pi4, T_graph)}



#========================Jardinier===============================================
J_graph= nx.MultiDiGraph()
J_graph.add_edge("S0","S1",label="SW",weight=0.1)
J_graph.add_edge("S0","S1",label="JW",weight=0.9)
J_graph.add_edge("S0","S2",label="$\\varnothing$",weight=0.5)

J_graph.add_edge("S1","S1",label="$\\varnothing$",weight=1)
J_graph.add_edge("S2","S2",label="$\\varnothing$",weight=1)
J_graph.terminals = terminals(J_graph)
J_graph.inits = {"S0"}
J_graph.positions = {"S0": (0, 0), "S1": (1, 2), "S2": (2, -1)}

pi1 = {"S0": "JW"}
pi2 = {"S0": "SW"}
pi3 = {"S0": "$\\varnothing$"}
J_policies = {"pi1": complete_policy(pi1, J_graph), "pi2": complete_policy(pi2, J_graph), "pi3": complete_policy(pi3, J_graph)}
J_graph.policies = J_policies



#====================================================
G1= nx.MultiDiGraph()
G1.add_edge(0,1,label="a")
G1.add_edge(1,2,label="b")
G1.add_edge(2,3,label="c")
G1.add_edge(3,4,label="d")
G1.add_edge(4,5,label="e")

G1.add_edge(0,2,label="f")
G1.add_edge(3,5,label="g")

G1.add_edge(5,5,label="$\\varnothing$")

partial_expertise= {0:{"f":0.5},3:{"g":0.5}}
expertise = complete_expertise(G1,partial_expertise)
add_expertise(G1, expertise)

pi1 = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "$\\varnothing$"}
pi2 = {0:"f",3:"d"}
pi3 = {0:"a",3:"g"}
G1.positions = {0: (0, 0), 1: (2,1), 2: (4,2), 3: (6,3), 4: (8,4), 5: (10,5)}
G1.terminals = terminals(G1)
G1.policies = {"pi1": complete_policy(pi1, G1), "pi2": complete_policy(pi2, G1), "pi3": complete_policy(pi3, G1)}
G1.inits = {0}

if __name__=="__main__":
    pickle.dump(P_graph, open('graphs/P_graph.pickle', 'wb'))
    nx.write_gexf(P_graph, 'graphs/P_graph.gexf')
    pickle.dump(T_graph, open('graphs/T_graph.pickle', 'wb'))
    nx.write_gexf(T_graph, 'graphs/T_graph.gexf')
    pickle.dump(J_graph, open('graphs/J_graph.pickle', 'wb'))
    nx.write_gexf(J_graph, 'graphs/J_graph.gexf')
    pickle.dump(G1, open('graphs/G1.pickle', 'wb'))
    nx.write_gexf(G1, 'graphs/G1.gexf')

