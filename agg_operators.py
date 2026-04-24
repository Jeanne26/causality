import numpy as np

def perplexite_agg(liste_score):
    assert len(liste_score)>0
    N= len(liste_score)
    return np.exp(-(1/N)* np.sum(np.log(liste_score)))



def gamma_agg(liste_score,gamma=0.7):
    #aggregation qui prend en compte la position de l'événement dans le chemin, les événements plus proches du début du chemin sont plus importants que ceux proches de la fin
    #on normalise le score pour qu'il soit compris entre 0 et 1 
    assert len(liste_score)>0
    score_mulplied =[]
    N = len(liste_score)
    for i in range(0,len(liste_score)):
        score_mulplied.append((gamma**i) * liste_score[i])
    if gamma == 1:
        return (N - np.sum(score_mulplied))/N
    sum_gamma = (1- gamma**(N))/(1 -gamma)
    return (sum_gamma - np.sum(score_mulplied))/sum_gamma

def gamma_agg_late(liste_score,gamma=0.7):
    #aggregation qui prend en compte la position de l'événement dans le chemin, les événements plus proches du début du chemin sont plus importants que ceux proches de la fin
    #on normalise le score pour qu'il soit compris entre 0 et 1 
    assert len(liste_score)>0
    score_mulplied =[]
    N = len(liste_score)
    for i in range(0,len(liste_score)):
        score_mulplied.append((gamma**(N-1-i)) * liste_score[i])
    if gamma == 1:
        return (N - np.sum(score_mulplied))/N
    sum_gamma = (1- gamma**(N))/(1 -gamma)
    return (sum_gamma - np.sum(score_mulplied))/sum_gamma


def geometrique_agg(liste_score):
    #moyenne geometrique
    assert len(liste_score)>0
    N = len(liste_score)
    prod = np.prod(liste_score)
    return (1- prod**(1/N))




def seuil_agg(liste_score, seuil=0.4):
    assert len(liste_score)>0
    return 0 if all(score >= seuil for score in liste_score) else 1


def mean_agg(liste_score):
    assert len(liste_score)>0
    return 1- np.mean(liste_score)
