import networkx as nx

from utils import complete_policy, terminals

#========================POISON===============================================

P_graph = nx.DiGraph()
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

pi1 = {'VO': 'emp', 'VE': 'boire'}
pi2 = {'VO': 'boire'}   
pi3 = {'VO': 'vider', 'VV': '$\\varnothing$'}
pi4 = {'VO': 'emp', 'VE': 'vider', 'VV': '$\\varnothing$'}
pi5 = {'VO': 'emp', 'VE': 'antidote', 'VA': 'boire'}
policies = {"pi1": complete_policy(pi1, P_graph), "pi2": complete_policy(pi2, P_graph), "pi3": complete_policy(pi3, P_graph), "pi4": complete_policy(pi4, P_graph), "pi5": complete_policy(pi5, P_graph)}
    



#=======================TEST==================================================
T_graph = nx.DiGraph()

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