# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xUbQZT2AGxMmVdmRS_9e_NnD5dlJu6EV

# Implementation de K-Means
"""

from google.colab import drive
drive.mount('/content/drive')

import cv2
import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib import style

"""## Chargement des descripteurs"""

files = os.listdir("/content/drive/My Drive/eh_descriptors_1/")
L = []
imgs = []
for i in range(1,2):
   edh0 = open ("/content/drive/My Drive/eh_descriptors_1/"+ "eh"+str(i)+".txt","r")
   print("/content/drive/My Drive/eh_descriptors_1/"+ "eh"+str(i)+".txt")
   for j in edh0:
     img = j[:-2].split(' ')
     L=[]
     for k in img:
          L.append(float(k))
       
     imgs.append(L)

"""## Calcul de la distance entre deux descripteurs"""

data=imgs

def ehddist(ehd1,ehd2):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for i in range(80):
      sum1 += abs(float(ehd1[i])-float(ehd2[i]))
    for i in range(79,85):
      sum2 += abs(float(ehd1[i])-float(ehd2[i]))
    for i in range(84,150):
      sum3 += abs(float(ehd1[i])-float(ehd2[i]))
      
    distance = sum1 +5*sum2 + sum3
    return(distance)

"""## Algorithme de Kmeans et méthodes associées"""

style.use('ggplot')

class K_Means:
	def __init__(self, k =3, tolerance = 0.001, max_iterations = 900):
		self.k = k
		self.tolerance = tolerance
		self.max_iterations = max_iterations

	def fit(self, data):

		self.centroids = {}

		#initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
		for i in range(self.k):
			self.centroids[i] = data[i]

		#begin iterations
		for i in range(self.max_iterations):
			self.classes = {}
			for i in range(self.k):
				self.classes[i] = []

			#find the distance between the point and cluster; choose the nearest centroid
			for features in data:
				distances = [ehddist(features ,self.centroids[centroid]) for centroid in self.centroids]
				classification = distances.index(min(distances))
				self.classes[classification].append(features)

			previous = dict(self.centroids)
      
			#average the cluster datapoints to re-calculate the centroids
			for classification in self.classes:
				self.centroids[classification] = np.average(self.classes[classification], axis = 0)

			isOptimal = True

			for centroid in self.centroids:

				original_centroid = previous[centroid]
				curr = self.centroids[centroid]

			if np.sum((curr - original_centroid)/original_centroid * 100.0) > self.tolerance:
				isOptimal = False


			if (i == self.max_iterations-1) or (isOptimal):
				print(isOptimal)
				distance=[]
				for classs in self.classes:
					for sample in self.classes[classs]:
						distance.append(ehddist(sample,self.centroids[classs]))
				self.inertia=np.sum(np.square(distance))
		
		  #break out of the main loop if the results are optimal, ie. the centroids don't change their positions much(more than our tolerance)
			if isOptimal:
				break

	def pred(self, data):
		classification =[]
		for features in data:
			distances = [ehddist(features ,self.centroids[centroid]) for centroid in self.centroids]
			classification.append(distances.index(min(distances)))
		return classification

"""## Elbow et choix du nombre de clusters"""

wcss =[]
liste=[80,150,200]
for i in liste:
    kmeans=K_Means(i)
    kmeans.fit(imgs)
    wcss.append(kmeans.inertia)
    print(wcss,"####",i)
plt.plot(liste, sse)
plt.title("The elbow methode")
plt.xlabel("number of clusters")
plt.ylabel("SSE")
plt.show()