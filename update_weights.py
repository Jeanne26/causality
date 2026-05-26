import networkx as nx
import pickle 
G = pickle.load(open('graphs/bw_p0.pickle', 'rb'))

print(G.edges(data= True))