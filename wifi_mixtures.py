
import networkx as nx
import numpy as np
import seaborn as sns
from time import time

g = nx.read_graphml('handoff_graph.graphml')

def get_weight_vector(g):
    n = len(g.edges())
    out = np.zeros(n, int)
    i = 0
    for edge in g.edges_iter(data = 'weight'):
        out[i] = edge[2]['weight']
        i += 1
    return out


t0 = time()
weights = get_weight_vector(g)
print(time() - t0)
