# -*- coding: utf-8 -*-
import os
from flask import Flask, send_file, request, json
import pandas as pd
import processamento
from threading import Thread
from time import gmtime, strftime
import time
import json
import utils
import sys

app = Flask(__name__)

saida_dir = 'output/' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) + '.pending'

def analisar(entrada, k, n, eps, minPts):
    dfHeader = ['estado', 'cidade', 'objeto', 'aspectos']
    input_dir = 'input/' + entrada

    def preparar():
        if not os.path.exists(saida_dir):
            os.makedirs(saida_dir)

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
                    'id': saida_dir[7:-8],
                    'progresso': progresso,
                    'total': total,
                    'percentual': 0
                }
            }

            json_string = json.dumps(obj)  # transforma em string
            open(saida_dir + '/_progresso.json', 'w').write(json_string)
        else:
            json_string = open(saida_dir + '/_progresso.json').read()  # carrega arquivo json
            obj = json.loads(json_string)  # transforma em object

            obj['analise']['progresso'] = progresso
            obj['analise']['percentual'] = float(progresso) / float(obj['analise']['total']) * 100

            json_string = json.dumps(obj)  # transforma em string
            open(saida_dir + '/_progresso.json', 'w').write(json_string)

    def salvar(estado, obj):
        utils.obj2JsonFile(obj, saida_dir + '/' + estado + '.json')

    def finalizar():
        nova_saida_dir = saida_dir[:-8]
        os.rename(saida_dir, nova_saida_dir)  # remover '.pending'

        utils.mergeFilesAndSave(nova_saida_dir, 'json', nova_saida_dir + '/_resultado.json')  # mesclando arquivos

        obj = utils.loadJsonFromFile(nova_saida_dir + '/_progresso.json')
        obj['analise']['tempo'] = time.time() - start_time
        utils.obj2JsonFile(obj, nova_saida_dir + '/_progresso.json')

        print("--- %s s ---" % (time.time() - start_time))

    df = pd.read_csv(input_dir, delimiter=';', names=dfHeader)
    preparar()
    progresso = 0

    for e in df.estado.unique():
        # print e + ';null;null;'
        sys.stdout.write(e + ';null;null;')
        saidaEstado = {}
        subconjuntoEstado = df[df.estado == e]
        saidaEstado[e] = {
            'kmeans': processamento.processarKmeans(subconjuntoEstado, k),
            'lda': processamento.processarLDA(subconjuntoEstado, n),
            'dbscan': processamento.processarDBSCAN(subconjuntoEstado, eps, minPts),
        }

        # print '|'
        saidaCidade = {}

        for c in subconjuntoEstado.cidade.unique():
            # print e + ';' + c + ';null;'
            sys.stdout.write(e + ';' + c + ';null;')
            subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c]
            saidaCidade[c] = {
                'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                'lda': processamento.processarLDA(subconjuntoCidade, n),
                'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
            }

            # print '|'
            # print ''

            saidaObjeto = {};

            for o in subconjuntoCidade.objeto.unique():
                # print e + ';' + c + ';' + o + ';'
                sys.stdout.write(e + ';' + c + ';' + o + ';')
                subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o]
                saidaObjeto[o] = {
                    'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                    'lda': processamento.processarLDA(subconjunto_objeto, n),
                    'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                }
                # print '|'
                # print ''

            saidaCidade[c].update(saidaObjeto)
            # print '|'

        saidaEstado[e].update(saidaCidade)
        # print '|'
        # print ''

        progresso += 1
        atualizarProgresso(progresso)
        salvar(e, saidaEstado)

    finalizar()


# @app.route('/consultar-progresso')
def consultarProgresso(directory):
    # directory = str(request.args.get('directory'))
    # with open('output/' + directory + '/_resultado.json', 'r') as f:
    #     data = json.load(f)
    #
    # return json.dumps(data)
    with open('output/' + directory + '/_progresso.json', 'r') as f:
        data = json.load(f)

    # return json.dumps(data)
    return data


@app.route('/resumo')
def consultarResumo():
    retorno = {}

    for dir in os.listdir('output'):
        if dir[-7:] == 'pending':
            retorno[dir] = consultarProgresso(dir)

    return json.dumps(retorno)


@app.route('/resultados')
def consultarResultados():
    # retorno = dict.fromkeys(os.listdir('output'))
    retorno = {}

    for dir in os.listdir('output'):
        if dir[-7:] != 'pending':
            retorno[dir] = consultarProgresso(dir)

    return json.dumps(retorno)


@app.route('/resultado')
def consultarResultado():
    directory = str(request.args.get('directory'))
    with open('output/' + directory + '/_resultado.json', 'r') as f:
        data = json.load(f)

    return json.dumps(data)


@app.route('/iniciar')
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


@app.route('/')
def index():
    return send_file("templates/index.html")


if __name__ == '__main__':
    print "--- iniciando... ---"
    start_time = time.time()

    if not os.path.exists('input'):
        os.makedirs('input')

    if not os.path.exists('output'):
        os.makedirs('output')

    # app.run()
    analisar('pos_100.csv', 2, 2, 2, 2)
