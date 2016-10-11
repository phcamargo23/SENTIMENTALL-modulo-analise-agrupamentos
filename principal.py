# -*- coding: utf-8 -*-
import os
from flask import Flask, send_file, request, json
import pandas as pd
import processamento
from threading import Thread
from time import gmtime, strftime

app = Flask(__name__)

directory = None


def analisar(entrada, k, n, eps, minPts):
    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
    if not os.path.exists('input'):
        os.makedirs('input')

    filename = '/input/' + entrada

    directory = 'output\\' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) + '.pending'

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_number_rows = len(open(filename).readlines())

    file_number_row_current = 0
    percentual = 0

    for df in pd.read_csv(filename, delimiter=';', names=dfHeader, chunksize=10 ** 3):
        file_number_row_current += len(df)
        percentual = file_number_row_current * 100 / file_number_rows

        json.dump({'total': file_number_rows, 'progresso': file_number_row_current, 'percentual': percentual}, open(directory + '/_progresso.json', 'w'))

        saidaEstado = {}

        for e in df.estado.unique():
            subconjuntoEstado = df[df.estado == e]
            saidaEstado[e] = {
                'kmeans': processamento.processarKmeans(subconjuntoEstado, k),
                'lda': processamento.processarLDA(subconjuntoEstado, n),
                'dbscan': processamento.processarDBSCAN(subconjuntoEstado, eps, minPts),
            }

            saidaCidade = {}

            for c in subconjuntoEstado.cidade.unique():
                subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
                saidaCidade[c] = {
                    'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                    'lda': processamento.processarLDA(subconjuntoCidade, n),
                    'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
                }

                saidaObjeto = {};

                for o in subconjuntoCidade.objeto.unique():
                    subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                    saidaObjeto[o] = {
                        'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                        'lda': processamento.processarLDA(subconjunto_objeto, n),
                        'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                    }

                saidaCidade[c].update(saidaObjeto);

            saidaEstado[e].update(saidaCidade);

    jsonData = json.dumps(saidaEstado)
    with open(directory + '/_resultado.json', 'w') as f:
        json.dump(jsonData, f)

    os.rename(directory, directory[:-8])  # remover '.pending'


@app.route('/')
def index():
    # return make_response(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')).read())
    return send_file("templates/index.html")


@app.route('/resumo')
def consultarResumo():
    retorno = {'entradas': {},
               'saidas':
                   {'pendentes': {}, 'concluidos': {}, 'erro': {}}
               }

    # for i in os.listdir('input'):
    #     retorno['entradas'].append(i)

    retorno['entradas'] = os.listdir('input')

    for o in os.listdir('output'):
        if o[-7:] == 'pending':
            retorno['saidas']['pendentes'][o] = consultarProgresso(o)
        else:
            retorno['saidas']['concluidos'][o] = consultarProgresso(o)

    return json.dumps(retorno)


@app.route('/consultar-analises')
def consultarAnalises():
    # for dir in os.listdir('output'):
    #     if dir[-7:] == 'pending':
    #         print dir
    #
    return json.dumps(os.listdir('output'))


@app.route('/consultar-progresso')
def consultarProgresso(directory):
    # directory = str(request.args.get('directory'))
    with open('output/' + directory + '/_progresso.json', 'r') as f:
        data = json.load(f)

    # return json.dumps(data)
    return data


@app.route('/consultar-resultado')
def consultarResultado():
    directory = str(request.args.get('directory'))
    with open('output/' + directory + '/_resultado.json', 'r') as f:
        data = json.load(f)

    return data


@app.route('/iniciar-analise')
def main():
    entrada = request.args.get('entrada')
    k = int(request.args.get('k'))
    n = int(request.args.get('n'))
    eps = float(request.args.get('eps'))
    minPts = float(request.args.get('minPts'))

    t = Thread(target=analisar, args=[entrada, k, n, eps, minPts])
    t.start()
    return 'Análise iniciada!'


@app.route('/entradas')
def consultarEntradas():
    return json.dumps(os.listdir('input'))


if __name__ == '__main__':
    app.run()
