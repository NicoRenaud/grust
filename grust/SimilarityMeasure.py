import os
import numpy as np 
import scipy.spatial.distance as ssd
from fastdtw import fastdtw

def Euclidean(x,y):
	return ssd.euclidean(x,y)

def Cosine(x,y):
	return ssd.cosine(x,y)

def Minkowski(x,y,p=2):
	return ssd.minkowski(x,y,p)

def DTW(x,y):
	dist,path = fastdtw(x,y,dist=ssd.euclidean)
	return dist

def threshold(v,thr=0.5):
	if v<thr:
		return 1
	else:
		return 0

class Similarity(object):

	def __init__(self,method,log=False,pad=True,pad_val=-12,weight='pwr'):

		self.method = method
		self.weight = weight
		self.log = log
		self.pad_val = pad_val
		self.pad = pad
		self.method_dict = {'euclidean':Euclidean,
		                    'cosine':Cosine,
		                    'minkowski':Minkowski,
		                    'dtw':DTW }

	def _weight(self,dist):
		if self.weight == 'pwr':
			return 10**-dist
		elif self.weight == 'exp':
			return np.exp(-0.1*dist)
		elif self.weight == 'inv':
			return 1/dist

	def __call__(self,x,y):

		x[np.isnan(x)] = 0.
		y[np.isnan(y)] = 0.

		nx,ny  = len(x),len(y)
		nmin = min(nx,ny)
		nmax = max(nx,ny)
		min_val = -16.

		if self.pad:
			if nx < ny:
				x = np.pad(x,(0,ny-nx),'constant',constant_values=(min_val,min_val))
			if ny < nx:
				y = np.pad(y,(0,nx-ny),'constant',constant_values=(min_val,min_val))
		else:
			x = x[:nmin]
			y = y[:nmin]

		if not self.log:
			x = 10**(x)	
			y = 10**(y)

		dist = self.method_dict[self.method](x,y)
		return nmin / nmax * self._weight(dist)
