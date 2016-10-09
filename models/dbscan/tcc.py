# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np
import processamento

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset.csv'
df = pd.read_csv(filename, delimiter=';', names=dfHeader)

def DBSCAN2(conjunto_de_dados, eps, minPts):
    dbscan = DBSCAN(eps=eps, min_samples=minPts)
    dbscan.fit(conjunto_de_dados)
    return dbscan.labels_, dbscan.core_sample_indices_


def processarDBSCAN(subset, eps, minPts):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Centróide'])
    visualizacao.append(['core', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = processamento.extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processamento.processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado, core_points_index = DBSCAN2(listSubconjuntoTransformado, eps, minPts)

    # centroides = []

    for point_index in core_points_index:
        linhaGrupo = [str(point_index), 'core', 0]
        visualizacao.append(linhaGrupo)
        sample_indexes = np.where(resultado == resultado[point_index]) #recuperar indices das amostras do grupo do core point
        df_samples = pd.DataFrame(listSubconjuntoTransformado) #transformar em DataFrame
        df_samples = df_samples.loc[sample_indexes] #recuperar amostras do grupo do core point através dos índices

        for aspecto, column in zip(list(setCaracteristicas), df_samples):
        # for column in df_samples:
            centroide = df_samples[column].mean()
            linhaAspecto = [aspecto + ' (g' + str(point_index) + ')', str(point_index), centroide];
            visualizacao.append(linhaAspecto)


        # cluster = np.extract(resultado == resultado[point_index], resultado)

    # for cluster, centroides in zip(range(len(core_points_index)), centroides):
    #     linhaGrupo = [str(cluster + 1), 'clusters', 0]
    #     visualizacao.append(linhaGrupo)
    #
    #     for aspecto, valor in zip(list(setCaracteristicas), centroides):
    #         linhaAspecto = [aspecto + ' (g' + str(cluster + 1) + ')', str(cluster + 1), valor];
    #         visualizacao.append(linhaAspecto)

    return visualizacao

    # print resultado.tolist()

eps = 1
min_samples = 5

if __name__ == '__main__':
    print processarDBSCAN(df, eps, min_samples)
