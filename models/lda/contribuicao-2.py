# -*- coding: utf-8 -*-
# from __future__ import print_function
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


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


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

dfHeader = ['estado', 'cidade', 'objeto', 'aspectos']
filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\input\man_10.csv'
dfSubconjunto = pd.read_csv(filename, delimiter=';', names=dfHeader)

setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)


# n_samples = 2000
# n_features = 1000
# n_topics = 2
n_top_words = 20

# # Use tf (raw term count) features for LDA.
# print("Extracting tf features for LDA...")
# tf_vectorizer = CountVectorizer()
# tf = tf_vectorizer.fit_transform(data_samples)

# print dfSubconjunto.aspectos

print "Fit LDA..."
lda = LatentDirichletAllocation(n_topics=2, learning_method='online')
# lda.fit(tf)
lda.fit(listSubconjuntoTransformado)

# print setCaracteristicas

print "\nTopics in LDA model:"
# tf_feature_names = tf_vectorizer.get_feature_names()
tf_feature_names = list(setCaracteristicas)
print lda.components_
print tf_feature_names
print_top_words(lda, tf_feature_names, n_top_words)
