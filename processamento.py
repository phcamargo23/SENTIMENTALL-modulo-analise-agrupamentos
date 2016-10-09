# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import analise

def extrairCaracteristicas(subconjunto):
    listaDeAspectos = set()

    for aspectos in subconjunto.aspectos:
        for aspecto in aspectos.split(','):
            listaDeAspectos.add(aspecto)

    return listaDeAspectos

def processarPonderacaoBinaria(caracteristicas, subconjunto):
    resultado = []

    for avaliacao in subconjunto.aspectos:
        valor = []
        for aspecto in caracteristicas:
            if aspecto in avaliacao.split(','):
                valor.append(1)
            else:
                valor.append(0)

        resultado.append(valor);

    return resultado


def processarKmeans(subset, k):
    if len(subset) < k:
        # print 'Quantidade de registros inferior ao número de clusters!'
        return None

    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Centróide'])
    visualizacao.append(['clusters', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado = analise.kmeans(listSubconjuntoTransformado, k)

    for cluster, centroides in zip(range(k), resultado):
        linhaGrupo = [str(cluster + 1), 'clusters', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), centroides):
            linhaAspecto = [aspecto + ' (g' + str(cluster + 1) + ')', str(cluster + 1), valor];
            visualizacao.append(linhaAspecto)

    return visualizacao


def processarLDA(subset, n_topicos):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Valor'])
    visualizacao.append(['tópicos', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado = analise.LDA(listSubconjuntoTransformado, n_topicos)

    for topico, valores in zip(range(n_topicos), resultado):
        linhaGrupo = [str(topico + 1), 'tópicos', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), valores):
            linhaAspecto = [aspecto + ' (t' + str(topico + 1) + ')', str(topico + 1), valor];
            visualizacao.append(linhaAspecto)

    return visualizacao


def processarDBSCAN(subset, eps, minPts):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Centróide'])
    visualizacao.append(['core', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado, core_points_index = analise.DBSCAN(listSubconjuntoTransformado, eps, minPts)

    # centroides = []

    for point_index in core_points_index:
        linhaGrupo = [str(point_index), 'core', 0]
        visualizacao.append(linhaGrupo)
        sample_indexes = np.where(resultado == resultado[point_index]) #recuperar indices das amostras do grupo do core point
        df_samples = pd.DataFrame(listSubconjuntoTransformado) #transformar em DataFrame
        df_samples = df_samples.loc[sample_indexes] #recuperar amostras do grupo do core point através dos índices

        for aspecto, column in zip(list(setCaracteristicas), df_samples):
            centroide = df_samples[column].mean()
            linhaAspecto = [aspecto + ' (g' + str(point_index) + ')', str(point_index), centroide];
            visualizacao.append(linhaAspecto)

    return visualizacao