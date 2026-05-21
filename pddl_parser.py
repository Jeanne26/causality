from pddl import parse_domain, parse_problem
from pddl.logic.base import And, Not, Or
from itertools import product
import networkx as nx
import pickle
import argparse
from utils import complete_expertise, add_expertise
#nb: domain : name, requirements, predicates, actions
#nb: problem : name, domain, objects, init, goal
#nb: action : name, parameters, precondition, effect
#nb: predicate : name, parameters

#nb: les états sont des frozenset qui contiennent les predicats qui sont vrais (si absent alors faux)
#nb: les actions sont pas des ensemble de fluents c'est juste un seul fluent (pas de combinaison d'action)

argparser = argparse.ArgumentParser()
argparser.add_argument('--pddl_folder', type=str, default="pddl_exemples/", help='dossier contenant les fichiers pddl')
argparser.add_argument('--domain_file', type=str, default="bw_domain.pddl", help='nom fichier domaine')
argparser.add_argument('--problem_file', type=str, default="bw_p0.pddl", help='nom probleme fichier')
argparser.add_argument("--output_folder", type=str, default="graphs/", help="dossier de sortie pour les graphes")
args = argparser.parse_args()
PDDL_FOLDER = args.pddl_folder
DOMAIN_FILE = args.domain_file
PROBLEM_FILE = args.problem_file
EXEMPLE_NAME = PROBLEM_FILE.split(".pddl")[0]




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
            name = f"({action.name} {' '.join(str(o) for o in args)})"
            instanciated_actions.append((name, precond, effect))
    return instanciated_actions



def build_graph(actions, init_state):
    i=0
    state = init_state
    G = nx.DiGraph()
    G.add_node("S0",predicates = state)
    queue = ["S0"]
    visited = set()
    while queue:
        current_node = queue.pop(0)
        if current_node in visited:
            continue
        visited.add(current_node)
        
        for action_name, precond, effect in actions:
            if statisfied(precond, G.nodes[current_node]["predicates"]):
                new_state = apply_effects(effect, G.nodes[current_node]["predicates"])

                #check si le noeud existe pas deja
                existe  = next((n for n in G.nodes if G.nodes[n]["predicates"]==new_state),None)
                if existe is None:
                    i+=1
                    new_node = f"S{i}"
                    G.add_node(new_node, predicates= new_state)
                else:
                    new_node = existe

                G.add_edge(current_node, new_node, label = f'A{len(G.edges)}', action= action_name)
                if new_state not in visited:
                    queue.append(new_node)

    #ajoute label nodes, etat terminaux (ajout d'une arrete goal) et init
    i= 0
    G.terminals = set()
    G.inits = {"S0"}

    for node in G.nodes:
        if statisfied(problem.goal, G.nodes[node]["predicates"]):
            G.terminals.add(node)
            G.add_edge(node, node, label = 'Goal')

        i+=1
 

    return G







if __name__ == "__main__":
    problem = parse_problem(PDDL_FOLDER + PROBLEM_FILE)
    domain  = parse_domain(PDDL_FOLDER + DOMAIN_FILE)

    objects = list(problem.objects) 

    actions = instanciate_action(domain.actions,objects)
    init_state = frozenset(str(p) for p in problem.init)
    G = build_graph(actions, init_state)
    print(f"Nombre de noeuds : {len(G.nodes)}")
    print(f"Nombre d'arêtes : {len(G.edges)}")
    print(f"Nombre d'états terminaux : {len(G.terminals)}")

    #ajout des attributs poids
    expertise =complete_expertise(G,{})
    add_expertise(G, expertise)
    
    pickle.dump(G, open(f'{args.output_folder}{EXEMPLE_NAME}.pickle', 'wb'))
    print(f'Graphe sauvegardé dans {args.output_folder}{EXEMPLE_NAME}.pickle')