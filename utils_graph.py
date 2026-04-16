

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