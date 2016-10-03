# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, json
import pandas as pd
import preProcessamento
from sklearn.cluster import KMeans

app = Flask(__name__)
DIR = os.path.dirname(os.path.abspath(__file__))

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
df = pd.read_csv('C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset.csv', delimiter=';', names=dfHeader);

k = 2

@app.route('/')
def index():
    return make_response(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')).read())

@app.route('/teste2')
def kmeans(conjuntoDeDados, k):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(conjuntoDeDados)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    return centroids

@app.route('/teste')
def criarDataset(caracteristicas, subconjunto):
    # dataframe = pd.DataFrame(columns=caracteristicas)
    resultado = []

    for avaliacao in subconjunto.aspectos:
        valor = []
        for aspecto in caracteristicas:
            if aspecto in avaliacao.split(','):
                valor.append(1)
            else:
                valor.append(0)

        resultado.append(valor);

    # dataframe.loc[len(dataframe)] = np.array(resultado)
    # dataframe = pd.DataFrame(data=np.array(resultado), columns=caracteristicas)
    # return np.array(resultado)
    # return dataframe
    return resultado

def processar(subset, objetoDoNivel):
    if len(subset) < k:
        # print 'Quantidade de registros inferior ao número de clusters!'
        return None

    visualizacao = []
    visualizacao.append(['no', 'pai', 'valor'])
    visualizacao.append(['nivel', None, 0])

    # if nivel == 'estado':
    #     dfSubconjunto = df[df.estado == objetoDoNivel]
    # elif nivel == 'cidade':
    #     dfSubconjunto = df[df.cidade == objetoDoNivel]
    # elif nivel == 'objeto':
    #     dfSubconjunto = df[df.objeto == objetoDoNivel]

    # dfSubconjunto = df[subset == objetoDoNivel]
    dfSubconjunto = subset
    setCaracteristicas = preProcessamento.extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = criarDataset(setCaracteristicas, dfSubconjunto)
    analise = kmeans(listSubconjuntoTransformado, k)

    for cluster, centroides in zip(range(k), analise):
        linhaGrupo = [str(cluster + 1), 'nivel', 0]
        visualizacao.append(linhaGrupo)

        for aspecto, valor in zip(list(setCaracteristicas), centroides):
            linhaAspecto = [aspecto + ' (g' + str(cluster + 1) + ')', str(cluster + 1), valor];
            visualizacao.append(linhaAspecto)

    return visualizacao

@app.route('/analisar')
def main():

    saidaEstado = {}

    for e in df.estado.unique():
        subconjuntoEstado = df[df.estado == e]
        saidaEstado[e] = {'resultado':processar(subconjuntoEstado, e)}

        saidaCidade = {}

        for c in subconjuntoEstado.cidade.unique():
            subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
            saidaCidade[c] = {'resultado': processar(subconjuntoCidade, c)}

            saidaObjeto = {};

            for o in subconjuntoCidade.objeto.unique():
                subconjuntoObjeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                saidaObjeto[o] = {'resultado': processar(subconjuntoObjeto, o)};

            saidaCidade[c].update(saidaObjeto);

        saidaEstado[e].update(saidaCidade);



    # saida['estados'] = saidaEstado
    print json.dumps(saidaEstado)



    #     linhaAgrupamento = []
    #     linhaAgrupamento.append(estado)
    #     linhaAgrupamento.append('estado')
    #     linhaAgrupamento.append(0)
    #
    #     dfSubconjunto = df[df.estado == estado]
    #     setCaracteristicas = preProcessamento.extrairCaracteristicas(dfSubconjunto)
    #     subconjuntoTransformado = criarDataset(setCaracteristicas, dfSubconjunto)
    #     analise = kmeans(subconjuntoTransformado, k)
    #
    #     linhaAspecto = []
    #     for cluster, centroides in zip(range(k), analise):
    #         for aspecto, valor in zip(list(setCaracteristicas), centroides):
    #             linhaAspecto = [aspecto+'(g'+str(cluster+1)+')', 'nivel', valor];
    #
    #         visualizacao.append(linhaAspecto)
    #
    return json.dumps(saidaEstado)

if __name__ == '__main__':
    app.run()
    # main()