# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
# import numpy

def kmeans(conjunto_de_dados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjunto_de_dados)

    centroids = kmeans.cluster_centers_
    # numpy.around(centroids, 4)
    return centroids


def LDA(conjunto_de_dados, n_topicos):
    lda = LatentDirichletAllocation(n_topics=n_topicos, max_iter=5,
                                    learning_method='online', learning_offset=50.,
                                    random_state=0)
    return lda
