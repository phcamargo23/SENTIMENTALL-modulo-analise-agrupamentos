# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, json
import pandas as pd
import processamento
from sklearn.cluster import KMeans

app = Flask(__name__)
DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return make_response(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')).read())


@app.route('/analisar')
def main():
    k = int(request.args.get('k'))
    # k = 3

    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
    df = pd.read_csv('C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset.csv', delimiter=';', names=dfHeader);

    saidaEstado = {}

    for e in df.estado.unique():
        subconjuntoEstado = df[df.estado == e]
        saidaEstado[e] = {'kmeans':processamento.processarKmeans(subconjuntoEstado, k)}

        saidaCidade = {}

        for c in subconjuntoEstado.cidade.unique():
            subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
            saidaCidade[c] = {'kmeans': processamento.processarKmeans(subconjuntoCidade, k)}

            saidaObjeto = {};

            for o in subconjuntoCidade.objeto.unique():
                subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                saidaObjeto[o] = {
                        'kmeans': processamento.processarKmeans(subconjunto_objeto, k)
                        # 'dbscan': processamento.processarDBSCAN(subconjunto_objeto, 0, 0),
                        # 'lda': processamento.processarLDA(subconjunto_objeto, k)
                };

            saidaCidade[c].update(saidaObjeto);

        saidaEstado[e].update(saidaCidade);

    # print json.dumps(saidaEstado)
    return json.dumps(saidaEstado)

if __name__ == '__main__':
    app.run()
    # main()