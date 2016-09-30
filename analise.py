# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans

def kmeans(conjuntoDeDados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjuntoDeDados)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    return centroids

def processar(conjuntoDeDados, k):
    for estado in conjuntoDeDados['estados']:
        print kmeans(list(estado.values()[0].values), k)

if __name__ == '__main__':
    processar()