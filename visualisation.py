import networkx as nx
import matplotlib.pyplot as plt
from graph_poison import P_graph


pos = {"VO":(0,2),"vivant":(1,4),"VE":(1,2),"VV":(1,0),"VA":(2,3),"mort":(2,1)}
edge_labels = nx.get_edge_attributes(P_graph, 'label')
options = {
    "node_color": 'lightblue',
    "node_size": 2000,
    "font_size": 10,
    "edge_color": 'gray',
    "width": 1.5,
}
nx.draw(P_graph, pos, with_labels=True, **options)
nx.draw_networkx_edge_labels(P_graph, pos, edge_labels=edge_labels, font_color='red')

plt.title("Graphe Poison")
plt.savefig("fig/graphe_poison.png")
plt.show()