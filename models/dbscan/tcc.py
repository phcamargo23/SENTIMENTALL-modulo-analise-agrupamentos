# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
# from sklearn.cluster import DBSCAN
from sklearn.cluster import DBSCAN as DensityBasedSpatialClustering

# from lixeira import preProcessamento2

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
filename = '../../input/dataset_5.csv'
df = pd.read_csv(filename, delimiter=';', names=dfHeader)

def DBSCAN(conjunto_de_dados, eps, minPts):
    dbscan = DensityBasedSpatialClustering(eps=eps, min_samples=minPts)
    dbscan.fit(conjunto_de_dados)

    # Number of clusters in labels, ignoring noise if present.
    # n_clusters_ = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
    n_clusters_ = set(dbscan.labels_)
    n_clusters_.discard(-1)
    # try:
    #     n_clusters_.remove(-1)
    # except KeyError:
    #     print 'Dataset não possui ruídos!'
    # print n_clusters_
    # return dbscan.labels_, dbscan.core_sample_indices_
    return dbscan.labels_, set(dbscan.labels_)

def processarDBSCAN(subset, eps, minPts):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Centróide'])
    visualizacao.append(['core', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = ['atendimento', 'comida', 'preco']
    listSubconjuntoTransformado = np.array(
        [
            [0,1,2],
            [0,1,2],
            [0,1,2],
            [7,8,9],
            [7,8,9],
            [7,8,9],
    ])
    resultado, n_clusters = DBSCAN(listSubconjuntoTransformado, eps, minPts)

    # centroides = []

    for point_index in n_clusters:
        linhaGrupo = [str(point_index), 'core', 0]
        visualizacao.append(linhaGrupo)
        sample_indexes = np.where(resultado == resultado[point_index]) #recuperar indices das amostras do grupo do core point
        df_samples = pd.DataFrame(listSubconjuntoTransformado) #transformar em DataFrame
        df_samples = df_samples.loc[sample_indexes] #recuperar amostras do grupo do core point através dos índices

        for aspecto, column in zip(list(setCaracteristicas), df_samples):
            centroide = df_samples[column].mean()
            linhaAspecto = [aspecto + ' (g' + str(point_index) + ')', str(point_index), centroide];
            visualizacao.append(linhaAspecto)

    print visualizacao

processarDBSCAN(df, 2, 2)