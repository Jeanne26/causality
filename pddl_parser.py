from pddl import parse_domain, parse_problem
import pddl
from pddl.logic.base import And, Not, Or
from itertools import product
import networkx as nx
import matplotlib.pyplot as plt

#nb: domain : name, requirements, predicates, actions
#nb: problem : name, domain, objects, init, goal
#nb: action : name, parameters, precondition, effect
#nb: predicate : name, parameters

#nb: les états sont des frozenset qui contiennent les predicats qui sont vrais (si absent alors faux)
#nb: les actions sont pas des ensemble de fluents c'est juste un seul fluent (pas de combinaison d'action)


problem = parse_problem("pddl_exemples/bw_p0.pddl")
domain  = parse_domain("pddl_exemples/bw_domain.pddl")

objects = list(problem.objects) 



def statisfied(preconditions,state):
    #check si les preconditions sont satisfaites dans l'état donné, geree and or et not
    if isinstance(preconditions, And):
        return all(statisfied(p,state) for p in preconditions.operands)
    if isinstance(preconditions, Not):
        return not statisfied(preconditions.argument,state)
    if isinstance(preconditions, Or):
        return any(statisfied(p,state) for p in preconditions.operands)
    return str(preconditions) in state


def apply_effects(effects,state):
    #applique des effets à un état donné gère and et not
    new_state = set(state)
    for eff in effects.operands:
        if isinstance(eff, Not):
            new_state.discard(str(eff.argument))
        else:
            new_state.add(str(eff))
    return frozenset(new_state)

def instanciate_action(actions,objets):
    #instancie toutes les actions possibles avec les objets
    instanciated_actions = []
    for action in actions:
        params= list(action.parameters)
        for args  in product(objets,repeat=len(params)):
            subst = {p:o for p,o in zip(params, args)}
            precond = action.precondition.instantiate(subst)
            effect = action.effect.instantiate(subst)
            name = f"{action.name}({', '.join(str(o) for o in args)})"
            instanciated_actions.append((name, precond, effect))
    return instanciated_actions

actions = instanciate_action(domain.actions,objects)
init_state = frozenset(str(p) for p in problem.init)
def build_graph(actions, init_state):
    state = init_state
    G = nx.DiGraph()
    G.add_node(state)
    queue = [state]
    visited = set()
    while queue:
        current_state = queue.pop(0)
        if current_state in visited:
            continue
        visited.add(current_state)
        for action_name, precond, effect in actions:
            if statisfied(precond, current_state):
                new_state = apply_effects(effect, current_state)
                G.add_edge(current_state, new_state, label = f'A{len(G.edges)}', action= action_name)
                if new_state not in visited:
                    queue.append(new_state)

    #ajoute label nodes
    i= 0
    for node in G.nodes:
        G.nodes[node]['label'] = f'S{i}'
        i+=1
    return G

G = build_graph(actions, init_state)

def show_graph(graph):
    plt.figure(figsize=(8, 6))

    edge_labels = nx.get_edge_attributes(graph, 'label')
    options = {
        "node_color": 'lightblue',
        "node_size": 2000,
        "font_size": 10,
        "edge_color": 'gray',
        "width": 1.5,
    }

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, **options)
    # nx.draw_networkx_edge_labels(G, pos, font_color='red')
    plt.show()


show_graph(G)