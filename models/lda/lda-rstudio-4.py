# -*- coding: utf-8 -*-
# https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import pandas as pd


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


dfHeader = ['estado', 'cidade', 'objeto', 'aspectos']
filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\input\pos_100.csv'
dfSubconjunto = pd.read_csv(filename, delimiter=';', names=dfHeader)

setCaracteristicas = extrairCaracteristicas(dfSubconjunto)
listSubconjuntoTransformado = processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)

dic = []

for l in listSubconjuntoTransformado:
    dic.append(zip(range(len(setCaracteristicas)), l))

# corpus = [(i,a) for i, a in range(len(setCaracteristicas)), listSubconjuntoTransformado]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(dic, num_topics=3)

# print ldamodel.show_topics()
# for t in ldamodel.show_topics():
#     print t

topicos = []
for i in range(3):
    distribuicao = []

    for k in ldamodel.show_topic(i, topn=len(setCaracteristicas)):
        distribuicao.append(k[1])

    topicos.append(distribuicao)

print topicos