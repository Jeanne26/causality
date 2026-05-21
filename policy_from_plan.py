#construire une politique à partirl d'un plan obtenu par solver pddl


#donner problem domain et
#recup graph à partir de fichier et extraire politique à partir de fichier

import argparse
import re
from pddl import parse_domain, parse_problem
from pddl_parser import instanciate_action, build_graph
from utils import complete_expertise, add_expertise
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

argparser.add_argument('--graph_folder', type=str, default= "graphs/", help="dossier des graphes" )
argparser.add_argument('--plan_folder', type= str, default= "pddl_exemples/", help= "dossier des plans")
argparser.add_argument('--exemple_name', type= str, default= "bw_p0", help="nom de l'exemple (nom partage par le fichier de plan et de graphe)")

args = argparser.parse_args()
GRAPH_FILE = args.graph_folder + args.exemple_name +".pickle"
PLAN_FILE = args.plan_folder + args.exemple_name+ ".plan"

if __name__ == "__main__":
    G = pickle.load(open(GRAPH_FILE, 'rb'))
    print("Graphe chargé depuis le fichier :", GRAPH_FILE)

    regex=r'^\d+\.\d+:\s*(\([^)]+\))'
    plan_text = open(PLAN_FILE, 'r').read()
    plan_clean = re.findall(regex, plan_text, re.MULTILINE)
    print("Plan extrait du fichier :", PLAN_FILE)
    print("Plan :", plan_clean)




