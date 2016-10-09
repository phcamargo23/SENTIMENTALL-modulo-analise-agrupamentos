# -*- coding: utf-8 -*-
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pandas as pd
import processamento, analise

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset_s.csv'
df = pd.read_csv(filename, delimiter=';', names=dfHeader)

n_topicos = 3

def LDA(conjunto_de_dados, n_topicos):
    lda = LatentDirichletAllocation(n_topics=n_topicos)
    lda.fit(conjunto_de_dados)

    return lda.components_

def processarLDA(subset, n_topicos):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Valor'])
    visualizacao.append(['tópicos', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = processamento.extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = processamento.processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado = LDA(listSubconjuntoTransformado, n_topicos)

    for topico, valores in zip(range(n_topicos), resultado):
        linhaGrupo = [str(topico + 1), 'tópicos', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), valores):
            linhaAspecto = [aspecto + ' (t' + str(topico + 1) + ')', str(topico + 1), valor];
            visualizacao.append(linhaAspecto)

    print visualizacao


if __name__ == '__main__':
    processarLDA(df, n_topicos)