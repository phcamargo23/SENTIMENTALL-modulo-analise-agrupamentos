# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

X = np.array([
    [7, 5],
    [5, 7],
    [7, 7],
    [3, 3],
    [4, 6],
    [1, 4],
    [0, 0],
    [2, 2],
    [8, 7],
    [6, 8],
    [5, 5],
    [3, 7]
])

kmeans = KMeans(n_clusters=2)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_
#http://matplotlib.org/examples/color/colormaps_reference.html
plt.scatter(X[:,0], X[:,1], s=200);
#plt.scatter(X[11,0], X[8,1], s=200, c=1, cmap='RdYlBu');
#plt.scatter(X[3,0], X[6,1], s=200, c=1, cmap='RdYlBu');
#plt.scatter(X[:,0], X[:,1], s=200, c=labels);
plt.show()