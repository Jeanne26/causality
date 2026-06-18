import math
import networkx as nx
import matplotlib.pyplot as plt
from graphs import P_graph,T_graph,J_graph,G1
import itertools as it
import numpy as np
import pickle
from utils import cout
from agg_operators import *
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



# https://networkx.org/documentation/stable/auto_examples/drawing/plot_multigraphs.html
def draw_labeled_multigraph(G, attr_name, ax=None):
    """
    Length of connectionstyle must be at least that of a maximum number of edges
    between pair of nodes. This number is maximum one-sided connections
    for directed graph and maximum total connections for undirected graph.
    """
    # Works with arc3 and angle3 connectionstyles
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    # connectionstyle = [f"angle3,angleA={r}" for r in it.accumulate([30] * 4)]


    pos = nx.bfs_layout(G, start=list(G.inits)[0])
    nx.draw_networkx_nodes(G, pos, ax=ax,node_size =300)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    nx.draw_networkx_edges(
        G, pos, edge_color="grey", connectionstyle=connectionstyle, ax=ax
    )

    labels = {
        tuple(edge): f"{attrs[attr_name]}"
        for *edge, attrs in G.edges(keys=True, data=True)
    }
    nx.draw_networkx_edge_labels(
        G,
        pos,
        labels,
        connectionstyle=connectionstyle,
        label_pos=0.3,
        font_color="blue",
        bbox={"alpha": 0},
        ax=ax,
    )


def visualisation(graph, attr_list, name, pos=None):
    """
    Affiche un MultiDiGraph dans une grille de subplots,
    chaque subplot affichant un attribut différent sur les arêtes.
    """
    n_attr = len(attr_list)
    ncols = 2  # toujours 2 colonnes
    nrows = math.ceil(n_attr / ncols) 
    
    fig, axes = plt.subplots(nrows, ncols, figsize=(6 * ncols, 4 * nrows))
    
    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]
    elif ncols == 1:
        axes = [[ax] for ax in axes]
    
    axes_flat = [ax for row in axes for ax in row]  # aplatisse pour itérer facilement

    for i, attr in enumerate(attr_list):
        draw_labeled_multigraph(graph, attr, axes_flat[i])
        axes_flat[i].set_title(attr)
    
    for j in range(n_attr, len(axes_flat)):
        fig.delaxes(axes_flat[j])
    
    plt.suptitle(name, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

def show_res(res_dico):
    if not res_dico:
        return
    

    policies = list(res_dico.keys())
    components = [k for k in next(iter(res_dico.values())).keys() if k != "cout"]

    x = np.arange(len(policies))
    width = 0.6

    _, ax = plt.subplots(figsize=(max(8, len(policies) * 1.2), 5))
    bottom = np.zeros(len(policies), dtype=float)

    for comp in components:
        values = np.array([float(res_dico[policy].get(comp, 0.0)) for policy in policies], dtype=float)
        bars = ax.bar(x, values, width, bottom=bottom, label=comp)
        for i, (bar, val) in enumerate(zip(bars, values)):
            if val != 0:
                y = bottom[i] + (val / 2)
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    y,
                    f"{val:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="black",
                )
        bottom += values

    totals = np.array([float(res_dico[policy].get("cout", 0.0)) for policy in policies], dtype=float)
    for i, total in enumerate(totals):
        ax.text(x[i], total, f"{total:.2f}", ha="center", va="bottom", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(policies)
    ax.set_ylabel("Coût")
    ax.set_title("Décomposition du coût par politique")
    ax.legend()
    plt.tight_layout()
    plt.show()


if __name__== "__main__":
    # pos_poison=  {"VO":(0,2),"vivant":(1,4),"VE":(1,2),"VV":(1,0),"VA":(2,3),"mort":(2,1)}
    # pos_test = {0:(0,3), 1:(1,5), 2:(1,1), 3:(2,6), 4:(2,4), 5:(2,2), 6:(2,0)}
    # show_graph(P_graph, "graphe_poison",pos =pos_poison)
    # show_graph(T_graph, "graphe_test", pos = pos_test)

    # show_graph(J_graph,"graphe_jardinier", pos= J_graph.positions ) 
    # show_graph(G1, None, "graphe_G1")
    # G = pickle.load(open('tmp/ac_p0.pickle', 'rb'))
    # print(G.edges(data=True))
    # visualisation(J_graph, ["label", "weight"], "Graphe Jardinier", pos=J_graph.positions)
    # plt.savefig("fig/graphe_jardinier.png")
    # visualisation(P_graph, ["label", "weight"], "Graphe Poison", pos={"VO":(0,2),"vivant":(1,4),"VE":(1,2),"VV":(1,0),"VA":(2,3),"mort":(2,1)})
    # plt.savefig("fig/graphe_poison.png")
    # visualisation(T_graph, ["label", "weight"], "Graphe Test", pos={0:(0,3), 1:(1,5), 2:(1,1), 3:(2,6), 4:(2,4), 5:(2,2), 6:(2,0)})
    # plt.savefig("fig/graphe_test.png")
    # visualisation(G1, ["label"], "Graphe G1")
    # plt.savefig("fig/graphe_G1.png")

    # G = pickle.load(open('graphs/ac_p0.pickle', 'rb'))
    # visualisation(G, ["label", "action", "weight"], "Graphe AC_p0")
    # plt.savefig("fig/graphe_ac_p0.png")

    # G = pickle.load(open('graphs/bw_p0.pickle', 'rb'))
    # visualisation(G, ["label", "action", "weight"], "Graphe BW_p0")
    # plt.savefig("fig/graphe_bw_p0.png")

    G = pickle.load(open("graphs/poison.pickle","rb"))
    visualisation(G, ["label", "action", "weight"], "Graphe poison_p0")
    plt.savefig("fig/graphe_poison_p0.png")