# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
import pandas as pd

def kmeans(conjuntoDeDados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjuntoDeDados)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    return centroids

def processar(conjuntoDeDados, k):
    # for estado in conjuntoDeDados['estados']:
    #     resultado = kmeans(estado.values()[0].values, k)
    #     df = pd.DataFrame(data=resultado, columns=estado.values()[0].columns)
    #
    #     for chave, valor in estado.iteritems():
    #         valor = resultado
    #
    # return conjuntoDeDados

    for chaveNivel, valorNivel in conjuntoDeDados.iteritems():
        for chave, valor in conjuntoDeDados[chaveNivel].iteritems():
            conjuntoDeDados[chaveNivel] = None

    return conjuntoDeDados
#     print conjuntoDeDados
#
# if __name__ == '__main__':
#     processar()