import networkx as nx
import matplotlib.pyplot as plt
from graphs import P_graph,T_graph,J_graph,G1

def show_poison():
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
    plt.savefig("fig/graphe_poison_labels.png")
    plt.show()

    plt.clf()

    edge_labels = nx.get_edge_attributes(P_graph, 'weight')
    nx.draw(P_graph, pos, with_labels=True, **options)
    nx.draw_networkx_edge_labels(P_graph, pos, edge_labels=edge_labels, font_color='blue')
    plt.title("Graphe Poison")
    plt.savefig("fig/graphe_poison_poids.png")
    plt.show()



def show_graph(graph, fichier, pos=None):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    if pos is None:
        pos = nx.bfs_layout(graph, start="S0")
    
    arc_style = "arc3,rad=0.2"
    node_options = {"node_color": "lightblue", "node_size": 500}
    edge_options = {"edge_color": "gray", "width": 1.2, "arrows": True, "arrowsize": 20,"arrowstyle": "->"}

    for axis, attr, color, title in [
        (ax[0], 'label',  'red',  "Labels"),
        (ax[1], 'weight', 'blue', "Poids"),
    ]:
        axis.set_title(title)
        nx.draw_networkx_nodes(graph, pos, ax=axis, **node_options)
        nx.draw_networkx_labels(graph, pos, ax=axis, font_size=10)
        nx.draw_networkx_edges(graph, pos, ax=axis, connectionstyle=arc_style, **edge_options)
        edge_labels = nx.get_edge_attributes(graph, attr)
        nx.draw_networkx_edge_labels(
            graph, pos,
            edge_labels=edge_labels,
            ax=axis,
            font_color=color,
            connectionstyle=arc_style,
        )

    plt.tight_layout()
    plt.savefig(f"fig/{fichier}.png")
    plt.show()


import pickle

if __name__== "__main__":
    # pos_poison=  {"VO":(0,2),"vivant":(1,4),"VE":(1,2),"VV":(1,0),"VA":(2,3),"mort":(2,1)}
    # pos_test = {0:(0,3), 1:(1,5), 2:(1,1), 3:(2,6), 4:(2,4), 5:(2,2), 6:(2,0)}
    # show_graph(P_graph, "graphe_poison",pos =pos_poison)
    # show_graph(T_graph, "graphe_test", pos = pos_test)

    # show_graph(J_graph,"graphe_jardinier", pos= J_graph.positions ) 
    # show_graph(G1, None, "graphe_G1")
    G = pickle.load(open('graphs/ac_p0.pickle', 'rb'))
    print(G.edges(data=True))
    show_graph(G,"graph_AC" )
