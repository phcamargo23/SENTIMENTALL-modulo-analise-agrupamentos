# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, json
import pandas as pd
import processamento
from threading import Thread

app = Flask(__name__)


def myfunc(k):
    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
    filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset3.csv'
    file_number_rows = len(open(filename).readlines())

    # k = 3

    file_number_row_current = 0
    percentual = 0

    for df in pd.read_csv(filename, delimiter=';', names=dfHeader, chunksize=10 ** 3):
        file_number_row_current += len(df)
        percentual = file_number_row_current * 100 / file_number_rows

        json.dump({'total': file_number_rows, 'progresso': file_number_row_current, 'percentual': percentual}, open('output/_progresso.json', 'w'))

        saidaEstado = {}

        for e in df.estado.unique():
            subconjuntoEstado = df[df.estado == e]
            saidaEstado[e] = {'kmeans': processamento.processarKmeans(subconjuntoEstado, k)}

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

    jsonData = json.dumps(saidaEstado)
    with open('output/_resultado.json', 'w') as f:
        json.dump(jsonData, f)


@app.route('/')
def index():
    return make_response(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')).read())


@app.route('/progresso')
def progresso():
    with open('output/_progresso.json', 'r') as f:
        data = json.load(f)

    return json.dumps(data)


@app.route('/analisar')
def main():
    k = int(request.args.get('k'))
    t = Thread(target=myfunc, args=[k])
    t.start()
    return ''


if __name__ == '__main__':
    app.run()
    # main()
