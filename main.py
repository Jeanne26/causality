from graphs import P_graph, T_graph,P_policies
from utils import *

if __name__ == "__main__":

    pi2 = P_policies["pi2"]
    pi3 = P_policies["pi3"]
    pi4 = P_policies["pi4"]
    pi5 = P_policies["pi5"]
    print(cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi2,choice=True),"\n")
    print(cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi3,choice=True),"\n")
    print(cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi4,choice=True),"\n")
    print(cout(P_graph,levenshtein_distance,"VO", P_policies["pi1"], pi5,choice=True),"\n")

