import matplotlib.pyplot as plt
from grust.DataLoader import DataLoader 
from grust.graph import GRUST 

file_path = '../../data/Simulation001/Data.mat'
data = DataLoader(file_path)

grust = GRUST()
grust.create_graph(data,distance='euclidean',nmax=250)
grust.get_cluster(method='louvain')
grust.plot()