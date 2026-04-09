from graphs import P_graph, T_graph,P_policies
from utils import *

if __name__ == "__main__":

    pi2 = P_policies["pi2"]
    pi3 = P_policies["pi3"]
    pi4 = P_policies["pi4"]
    pi5 = P_policies["pi5"]

    pi_opt1 = optimal_policy_no_plan(P_graph)
    pi_opt2 = optimal_policy_plan(P_graph, agg=perplexite_agg, horizon=1)


    cout_pi2 =cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi2,choice=False,pi_opt=pi_opt1),"\n"
    cout_pi3 =cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi3,choice=False,pi_opt=pi_opt1),"\n"
    cout_pi4 =cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi4,choice=False,pi_opt=pi_opt1),"\n"
    cout_pi5 =cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi5,choice=False,pi_opt=pi_opt1),"\n"

  