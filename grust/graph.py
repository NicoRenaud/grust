import numpy as np
import networkx as nx
import community
import markov_clustering as mc 
from grust.SimilarityMeasure import Similarity
from tqdm import tqdm
import matplotlib.pyplot as plt 

class GRUST(object):

    def __init__(self):
        self.graph = nx.Graph()

    def create_graph(self,data,distance='euclidean',nmax=None):

        
        index = list(range(len(data.traces)))
        if nmax is not None:
            np.random.shuffle(index)
            index = index[:nmax]

        self.ground_truth = np.array(data.clusters)[index]

        ntrace = len(index) 
        sim = Similarity(distance,
                          log=True,
                          pad=False,
                          weight='exp')

        
        weight_vals = {'diff':[],'same':[]}

        for i1 in tqdm(range(ntrace-1)):
            x = data.traces[index[i1]][:,1]
            for i2 in range(i1+1,ntrace):
                y = data.traces[index[i2]][:,1]
                
                w = sim(x,y)

                print('----------')
                print('trace 1 : % 3d, type %d' %(index[i1], data.clusters[index[i1]]) )
                print('trace 2 : % 3d, type %d' %(index[i2], data.clusters[index[i2]]) )
                print('weight  : %f' %w)

                if data.clusters[index[i1]] ==  data.clusters[index[i2]]:
                    weight_vals['same'].append(w)

                else:
                    weight_vals['diff'].append(w)

                self.graph.add_edge(i1,i2,weight=w)

        self.ground_truth = np.array(data.clusters)[index]
        plt.hist(weight_vals['same'],color='blue',alpha=0.5,density=True)
        plt.hist(weight_vals['diff'],color='red',alpha=0.5,density=True)
        

        plt.show()

    def get_cluster(self,method='louvain'):

        if method == 'louvain':
            cluster = community.best_partition(self.graph)
            self.cluster = [v for k,v in cluster.items()]

        # detect the communities using MCL detection
        elif method == 'mcl':

            matrix = nx.to_scipy_sparse_matrix(self.graph)
            result = mc.run_mcl(matrix)           # run MCL with default parameters
            clusters = mc.get_clusters(result)    # get clusters

            num_nodes = self.graph.number_of_nodes()
            index = np.zeros(num_nodes).astype('int')
            for ic, c in enumerate(clusters):
                index[list(c)] = ic

            self.cluster = clusters            

    def plot(self):

        G = self.graph
        partition = community.best_partition(G)

        size = float(len(set(partition.values())))
        pos = nx.spring_layout(G)
        count = 0.
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))


        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.show()         

