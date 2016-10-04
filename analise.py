# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans

def kmeans(conjuntoDeDados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjuntoDeDados)

    centroids = kmeans.cluster_centers_
    return centroids