# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans

def kmeans(conjuntoDeDados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjuntoDeDados)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    Y = []
    for i in centroids:
        Y.append(zip(listaDeAspectosDistintos, i))

    return json.dumps(Y)

def analisarEstado():
    for estado in df.estado.unique():
        if df[df.estado == estado]:
            print ''
    # for index, row in df.iterrows():
    #     print row['c1'], row['c2'

def analisarCidade():
    print #

def analisarTipo():
    print #

def analisarObjeto():
    print #


def processar(conjuntoDeDados, k):
    return analisar()
    # analisarEstado()

if __name__ == '__main__':
    processar()