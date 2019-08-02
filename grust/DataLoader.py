import os
import glob
import h5py
from scipy.io import loadmat
from tqdm import tqdm 
import matplotlib.pyplot as plt 

class DataLoader(object):

    def __init__(self,data_path,data_type='matlab'):

        self.data_path = data_path
        self.data_type = data_type
        self.load_data()

    def load_data(self):

        if self.data_type.lower() == 'matlab':
            self.traces, self.clusters = self._load_matlab(self.data_path)
        else:
            raise ValueError('Data type %s not recognized' %self.data_type)

    @staticmethod
    def _load_matlab(data_path):

        if os.path.isfile(data_path):
            file_list = [data_path]
        elif isinstace(data_path,list):
            file_list = data_path
        elif os.path.isdir(data_path):
            file_list = glob.glob('./data/' + '**/*.mat',recursive=True)
        else:
            raise ValueError('data path not understood')

        traces = []
        clusters = []
        for f in file_list:

            data = loadmat(f)
            trace_data = data['Data']
            cluser_data = data['ClusterX_sim']

            traces += [t[0] for t in trace_data ]
            clusters += cluser_data.flatten().tolist()

        return traces,clusters

    def plot_trace(self,index):
        if not isinstance(index,list):
            index = [index]
        for i in index:
            plt.plot(self.traces[i][:,1])
        plt.show()






