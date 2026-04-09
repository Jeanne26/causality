from graphs import P_graph, T_graph,P_policies
from utils import *

if __name__ == "__main__":

    pi2 = P_policies["pi2"]
    pi3 = P_policies["pi3"]
    pi4 = P_policies["pi4"]
    pi5 = P_policies["pi5"]

    pi_opt1 = optimal_policy_no_plan(P_graph)
    pi_opt2 = optimal_policy_plan(P_graph, agg=perplexite_agg, horizon=3)


    res_pi2 =compute_all_res(P_graph,"VO", P_policies["pi1"], pi2, pi_opt1)
    res_pi3 =compute_all_res(P_graph,"VO", P_policies["pi1"], pi3, pi_opt1)
    res_pi4 =compute_all_res(P_graph,"VO", P_policies["pi1"], pi4, pi_opt1)
    res_pi5 =compute_all_res(P_graph,"VO", P_policies["pi1"], pi5, pi_opt1)

    
    #P1: d_opt = perplexité sur les transitions avec choix
    #P2: d_opt = perplexité sur tous les transitions
    #D1: d_opt = distance à la politique optimale uniquement sur les états du path avec choix
    #D2: d_opt = distance à la politique optimale sur tous les états du path
    #L:  d_obs: distance de levenshtein

    print("==========================================================================================")
    print( "| CF    |   Perplexité  | Distance à opt|  Levenshtein   |L +P1 | L +P2 | L +D1 | L+D2   |")
    print( "|       |   P1  |   P2  |   D1  |   D2  |       L        |      |       |       |        |")
    print(f"|chi 2  |  {res_pi2['L+P1']['d_opt']:.2f} |  {res_pi2['L+P2']['d_opt']:.2f} |  {res_pi2['L+D1']['d_opt']:.2f} |  {res_pi2['L+D2']['d_opt']:.2f} |     {res_pi2['L+P1']['d_obs']:.2f}       | {res_pi2['L+P1']['cout']:.2f} |  {res_pi2['L+P2']['cout']:.2f} |  {res_pi2['L+D1']['cout']:.2f} |  {res_pi2['L+D2']['cout']:.2f}  |")
    print(f"|chi 3  |  {res_pi3['L+P1']['d_opt']:.2f} |  {res_pi3['L+P2']['d_opt']:.2f} |  {res_pi3['L+D1']['d_opt']:.2f} |  {res_pi3['L+D2']['d_opt']:.2f} |     {res_pi3['L+P1']['d_obs']:.2f}       | {res_pi3['L+P1']['cout']:.2f} |  {res_pi3['L+P2']['cout']:.2f} |  {res_pi3['L+D1']['cout']:.2f} |  {res_pi3['L+D2']['cout']:.2f}  |")
    print(f"|chi 4  |  {res_pi4['L+P1']['d_opt']:.2f} |  {res_pi4['L+P2']['d_opt']:.2f} |  {res_pi4['L+D1']['d_opt']:.2f} |  {res_pi4['L+D2']['d_opt']:.2f} |     {res_pi4['L+P1']['d_obs']:.2f}       | {res_pi4['L+P1']['cout']:.2f} |  {res_pi4['L+P2']['cout']:.2f} |  {res_pi4['L+D1']['cout']:.2f} |  {res_pi4['L+D2']['cout']:.2f}  |")
    print(f"|chi 5  |  {res_pi5['L+P1']['d_opt']:.2f} |  {res_pi5['L+P2']['d_opt']:.2f} |  {res_pi5['L+D1']['d_opt']:.2f} |  {res_pi5['L+D2']['d_opt']:.2f} |     {res_pi5['L+P1']['d_obs']:.2f}       | {res_pi5['L+P1']['cout']:.2f} |  {res_pi5['L+P2']['cout']:.2f} |  {res_pi5['L+D1']['cout']:.2f} |  {res_pi5['L+D2']['cout']:.2f}  |")
    print("==========================================================================================")  
