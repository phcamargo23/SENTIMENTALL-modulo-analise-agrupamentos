# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

s = 50

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

plt.close('all')

plt.subplot(321)
#plt.axis('off')
plt.scatter(X[:,0], X[:,1], s=s, cmap='bone');

plt.subplot(322)
plt.scatter(X[:,0], X[:,1], s=s);
plt.scatter(X[0, 0], X[0, 1], s=s, c=1, cmap='ocean');
plt.scatter(X[1,0], X[2,1], s=s, c=1, cmap='ocean');

plt.subplot(323)
plt.scatter(X[:,0], X[:,1], s=s, c=labels);

plt.show()