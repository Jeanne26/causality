#construire une politique à partirl d'un plan obtenu par solver pddl


#donner problem domain et
#recup graph à partir de fichier et extraire politique à partir de fichier

import argparse
import re
from utils import complete_policy
import pickle



argparser = argparse.ArgumentParser()
# argparser.add_argument('--pddl_folder', type=str, default="pddl_exemples/", help='dossier contenant les fichiers pddl')
# argparser.add_argument('--domain_file', type=str, default="bw_domain.pddl", help='nom fichier domaine')
# argparser.add_argument('--problem_file', type=str, default="bw_p0.pddl", help='nom probleme fichier')
# argparser.add_argument("--output_folder", type=str, default="graphs/", help="dossier de sortie pour les graphes")
# args = argparser.parse_args()
# PDDL_FOLDER = args.pddl_folder
# DOMAIN_FILE = args.domain_file
# PROBLEM_FILE = args.problem_file
# EXEMPLE_NAME = PROBLEM_FILE.split(".pddl")[0]
# PLAN_FILE = PROBLEM_FILE.split(".pddl")[0]+".plan"

argparser.add_argument('--graph_file', type=str, default= "graphs/ac_p0.pickle", help="fichier du graphe" )
argparser.add_argument('--plan_file', type= str, default= "pddl_exemples/ac_p0.plan", help="fichier de plan ")

args = argparser.parse_args()
GRAPH_FILE = args.graph_file
PLAN_FILE = args.plan_file
POLICIES_FOLDER = "policies/"
OUTPUT_NAME = PLAN_FILE.split(".plan")[0].split("/")[-1]

def get_label(state_label, action, G):
    #verifie si l'action est autorisée et renvoie son label associé
    for u,v,dico in G.out_edges(state_label, data=True):
        if dico['action'].lower() == action.lower():
            return dico['label']
    return None

if __name__ == "__main__":
    G = pickle.load(open(GRAPH_FILE, 'rb'))
    print("Graphe chargé depuis le fichier :", GRAPH_FILE)

    regex=r'^\d+\.\d+:\s*(\([^)]+\))'
    plan_text = open(PLAN_FILE, 'r').read()
    plan_clean = re.findall(regex, plan_text, re.MULTILINE)
    print("Plan extrait du fichier :", PLAN_FILE)
    print("Plan :", plan_clean)


    dic_label = {dico['action']: dico['label'] for (_,_,dico) in G.edges(data=True)}
    
    pi = {}
    state = list(G.inits)[0]
    for action in plan_clean:
        label = get_label(state, action, G)
        if label:
            next_state = [v for u,v,dico in G.out_edges(state, data=True) if dico['label'] == label and u == state][0]
            pi[state] = label
            state = next_state
        else:
            print(f"action {action} non autorisée depuis l'état {state}, ({G.nodes[state]['predicates']})")
            break
    assert next_state in G.terminals, f"le plan ne mène pas à un état terminal, dernier état atteint : {next_state} ({G.nodes[next_state]['predicates']})"
    pi[next_state] = "Goal"

    # pi = complete_policy(pi, G)
    with open(POLICIES_FOLDER + OUTPUT_NAME + "_policy.pickle", 'wb') as f:
        pickle.dump(pi, f)
    print("politique saved dans le fichier :", POLICIES_FOLDER + OUTPUT_NAME + "_policy.pickle")







