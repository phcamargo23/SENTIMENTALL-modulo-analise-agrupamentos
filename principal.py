# -*- coding: utf-8 -*-
import os
from flask import Flask, send_file, request, json
import pandas as pd
import processamento
from threading import Thread
from time import gmtime, strftime
import time

app = Flask(__name__)


def analisar(entrada, k, n, eps, minPts):
    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
    input_dir = 'input/' + entrada
    output_dir = 'output/' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) + '.pending'

    def preparar():
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        atualizarProgresso(0, True)

    def atualizarProgresso(progresso, primeiraIteracao=False):
        if primeiraIteracao:
            qtd_linhas = len(open(input_dir).readlines())
            total = df.estado.unique().size

            obj = {
                'parametros': {
                    'k': k,
                    'n': n,
                    'eps': eps,
                    'minPts': minPts
                },
                'dataset': {
                    'entrada': entrada,
                    'qtd_linhas': qtd_linhas
                },
                'analise': {
                    'progresso': progresso,
                    'total': total,
                    'percentual': 0
                }
            }

            json_string = json.dumps(obj)  # transforma em string
            open(output_dir + '/_progresso.json', 'w').write(json_string)
        else:
            json_string = open(output_dir + '/_progresso.json').read()  # carrega arquivo json
            obj = json.loads(json_string)  # transforma em object

            obj['analise']['progresso'] = progresso
            obj['analise']['percentual'] = obj['analise']['total'] / progresso * 100

            json_string = json.dumps(obj)  # transforma em string
            open(output_dir + '/_progresso.json', 'w').write(json_string)

    def finalizar(obj):
        jsonData = json.dumps(obj)

        with open(output_dir + '/_resultado.json', 'w') as f:
            json.dump(jsonData, f)

        os.rename(output_dir, output_dir[:-8])  # remover '.pending'

        json_string = open(output_dir[:-8] + '/_progresso.json').read()  # carrega arquivo json
        obj = json.loads(json_string)  # transforma em object

        obj['analise']['tempo'] = time.time() - start_time

        json_string = json.dumps(obj)  # transforma em string
        open(output_dir[:-8] + '/_progresso.json', 'w').write(json_string)

        print("--- %s s ---" % (time.time() - start_time))

    df = pd.read_csv(input_dir, delimiter=';', names=dfHeader)
    preparar()
    progresso = 0
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
            subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c]
            saidaCidade[c] = {
                'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                'lda': processamento.processarLDA(subconjuntoCidade, n),
                'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
            }

            saidaObjeto = {};

            for o in subconjuntoCidade.objeto.unique():
                subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o]
                saidaObjeto[o] = {
                    'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                    'lda': processamento.processarLDA(subconjunto_objeto, n),
                    'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                }

            saidaCidade[c].update(saidaObjeto)

        saidaEstado[e].update(saidaCidade)

        progresso += 1
        atualizarProgresso(progresso)

    finalizar(saidaEstado)


@app.route('/')
def index():
    return send_file("templates/index.html")


@app.route('/resumo')
def consultarResumo():
    retorno = {}

    for o in os.listdir('output'):
        retorno[o] = consultarProgresso(o)

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
    entrada = str(request.args.get('entrada'))
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
    print "--- iniciando... ---"
    start_time = time.time()

    if not os.path.exists('input'):
        os.makedirs('input')

    if not os.path.exists('output'):
        os.makedirs('output')

    app.run()
    # analisar('dataset_100.csv', 2, 3, 2, 2)
