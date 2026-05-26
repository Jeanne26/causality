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
argparser.add_argument('--plan_folder', type= str, default= "pddl_exemples/ac_p0_plan", help="folder de plans ")
argparser.add_argument('--output_folder', type=str, default="policies/ac_p0/", help='dossier de sortie pour les politiques')

args = argparser.parse_args()
GRAPH_FILE = args.graph_file
PLAN_FOLDER = args.plan_folder
POLICIES_FOLDER = args.output_folder                                                            
OUTPUT_NAME = PLAN_FOLDER.split("/")[-1]

def get_label(state_label, action, G):
    #verifie si l'action est autorisée et renvoie son label associé
    for u,v,dico in G.out_edges(state_label, data=True):
        if dico['action'].lower() == action.lower():
            return dico['label']
    return None

#recupere tous les plan du folder
def get_plans(folder):
    import os
    plans = []
    for filename in os.listdir(folder):
        if filename.endswith(".plan"):
            with open(os.path.join(folder, filename), 'r') as f:
                plan_text = f.read()
                regex=r'^\d+\.\d+:\s*(\([^)]+\))'
                plan_clean = re.findall(regex, plan_text, re.MULTILINE)
                plans.append(plan_clean)
    return plans

if __name__ == "__main__":
    G = pickle.load(open(GRAPH_FILE, 'rb'))
    print("Graphe chargé depuis le fichier :", GRAPH_FILE)
    plans = get_plans(PLAN_FOLDER)
    print(f"{len(plans)} plans extraits du dossier {PLAN_FOLDER}")
    for i, plan in enumerate(plans):
        print(f"\nPlan {i+1} : {plan}")
        dic_label = {dico['action']: dico['label'] for (_,_,dico) in G.edges(data=True)}
        
        pi = {}
        state = list(G.inits)[0]
        for action in plan:
            label = get_label(state, action, G)
            if label:
                next_state = [v for u,v,dico in G.out_edges(state, data=True) if dico['label'] == label and u == state][0]
                pi[state] = label
                state = next_state
            else:
                print(f"action {action} non autorisée depuis l'état {state}, ({G.nodes[state]['predicates']})")
                break
        assert next_state in G.terminals, f"pas d'etat terminal atteint: {next_state} ({G.nodes[next_state]['predicates']})"
        pi[next_state] = "Goal"

        pi = complete_policy(pi, G)
        with open(POLICIES_FOLDER + OUTPUT_NAME + f"_policy_{i}.pickle", 'wb') as f:
            pickle.dump(pi, f)
        print("politique saved dans le fichier :", POLICIES_FOLDER + OUTPUT_NAME + f"_policy_{i}.pickle")









