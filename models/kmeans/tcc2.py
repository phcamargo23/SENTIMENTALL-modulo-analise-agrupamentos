import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

X = np.array(
    [
        [0, 0],
        [1, 1],
        [1, 0],
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0],
        [1, 0],
        [1, 0],
        [0, 1],
        [1, 1],
        [1, 0],
        [1, 0],
        [1, 0],
        [0, 0],
        [0, 0],
        [1, 0],
        [0, 0],
        [1, 0],
        [0, 0],
        [1, 0],
        [0, 1],
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 0],
        [0, 1],
        [0, 0],
        [1, 0],
        [1, 1],
        [1, 1],
        [1, 0],
        [1, 1],
        [1, 1],
        [1, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [1, 1],
        [1, 0],
        [0, 0],
        [0, 0],
        [1, 1],
        [1, 0],
        [0, 1],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 1],
        [0, 1],
        [1, 0],
        [1, 1],
        [0, 1],
        [1, 0],
        [0, 0],
        [1, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0],
        [0, 1],
        [0, 0],
        [1, 0],
        [1, 0],
        [0, 1],
        [1, 1],
        [0, 0],
        [1, 0],
        [0, 0],
        [1, 0],
        [1, 0],
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 0],
        [0, 0],
        [0, 0],
        [0, 1],
        [0, 0],
        [1, 0],
        [1, 0],
        [0, 0],
        [0, 1],
        [0, 0],
        [0, 0],
        [0, 0],
        [1, 0],
        [0, 0],
        [1, 0],
        [0, 0],
        [1, 1],
        [1, 0],
        [0, 1],
        [1, 0]
    ])

kmeans = KMeans(n_clusters=2)
kmeans.fit(X)

centroids = kmeans.cluster_centers_
labels = kmeans.labels_

print(centroids)
print(round(centroids[0,0],2))
print(round(centroids[0,1],2))
print(round(centroids[1,0],2))
print(round(centroids[1,1],2))

plt.scatter(X[:, 0],X[:, 1])
plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)

plt.show()