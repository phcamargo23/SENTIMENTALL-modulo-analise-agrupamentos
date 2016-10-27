# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import DBSCAN as DensityBasedSpatialClustering
# import numpy

def kmeans(conjunto_de_dados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjunto_de_dados)

    # numpy.around(kmeans.cluster_centers_, 4)
    return kmeans.cluster_centers_


def LDA(conjunto_de_dados, n_topicos):
    lda = LatentDirichletAllocation(n_topics=n_topicos)
    lda.fit(conjunto_de_dados)

    return lda.components_


def DBSCAN(conjunto_de_dados, eps, minPts):
    dbscan = DensityBasedSpatialClustering(eps=eps, min_samples=minPts, algorithm='ball_tree')
    dbscan.fit(conjunto_de_dados)

    return dbscan.labels_, dbscan.core_sample_indices_