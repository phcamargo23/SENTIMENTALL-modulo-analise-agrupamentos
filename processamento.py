# -*- coding: utf-8 -*-
import sys
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


def mensurarContribuicao(centroides):
    contribuicao_aspecto = []

    for c in centroides:
        valores = []
        for valor in c:
            contribuicao = valor / sum(c) * 100
            valores.append(np.around(contribuicao, 4))

        contribuicao_aspecto.append(valores)

    return contribuicao_aspecto


def processarKmeans(subset, k):
    if len(subset) < k:
        # print 'Quantidade de registros inferior ao número de clusters!'
        return None

    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Contribuição (%)'])
    visualizacao.append(['clusters', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado = analise.kmeans(listSubconjuntoTransformado, k)
    contribuicao_aspectos = mensurarContribuicao(resultado)

    # Gerar visualização
    for cluster, centroides in zip(range(k), contribuicao_aspectos):
        linhaGrupo = [str(cluster + 1), 'clusters', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), centroides):
            linhaAspecto = [aspecto + ' (g' + str(cluster + 1) + ')', str(cluster + 1), valor];
            visualizacao.append(linhaAspecto)

    return visualizacao


def processarLDA(subset, n_topicos):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Contribuição (%)'])
    visualizacao.append(['tópicos', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado = analise.LDA(listSubconjuntoTransformado, n_topicos)
    contribuicao_aspectos = mensurarContribuicao(resultado)

    # Gerar visualização
    for topico, valores in zip(range(n_topicos), contribuicao_aspectos):
        linhaGrupo = [str(topico + 1), 'tópicos', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), valores):
            linhaAspecto = [aspecto + ' (t' + str(topico + 1) + ')', str(topico + 1), valor];
            visualizacao.append(linhaAspecto)

    return visualizacao


def processarDBSCAN(subset, eps, minPts):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Contribuição (%)'])
    visualizacao.append(['clusters', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado, n_clusters = analise.DBSCAN(listSubconjuntoTransformado, eps, minPts)

    # Calcular valor do centroide
    centroides = []
    for cluster in n_clusters:
        indices_amostras = np.where(resultado == resultado[cluster]) #recuperar os indices das amostras do grupo do core point
        df_subconjunto_de_dados = pd.DataFrame(listSubconjuntoTransformado, columns=setCaracteristicas) #transformar em DataFrame
        df_subconjunto_de_dados = df_subconjunto_de_dados.loc[indices_amostras] #recuperar amostras do grupo do core point através dos índices

        centroide = []
        for caracteristica in df_subconjunto_de_dados:
            media = df_subconjunto_de_dados[caracteristica].mean()
            centroide.append(media)

        centroides.append(centroide)

    # Mensurar valor da característica
    contribuicao_aspectos = mensurarContribuicao(centroides)

    # Gerar visualização
    for cluster, centroides in zip(n_clusters, contribuicao_aspectos):
        linhaGrupo = [str(cluster + 1), 'clusters', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), centroides):
            linhaAspecto = [aspecto + ' (g' + str(cluster + 1) + ')', str(cluster + 1), valor]
            visualizacao.append(linhaAspecto)

    return visualizacao if len(visualizacao) > 2 else None