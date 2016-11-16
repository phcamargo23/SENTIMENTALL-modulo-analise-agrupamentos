# -*- coding: utf-8 -*-
import os
from flask import Flask, send_file, request, json
import pandas as pd
import processamento
from threading import Thread
from time import gmtime, strftime
import time
import json
import glob

app = Flask(__name__)


def analisar(entrada, k, n, eps, minPts):
    dfHeader = ['estado', 'cidade', 'objeto', 'aspectos']
    input_dir = 'input/' + entrada
    output_dir = 'output/' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) + '.pending'

    def preparar():
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        atualizarProgresso(0, True)

    def atualizarProgresso(progresso, primeiraIteracao=False):
        if primeiraIteracao:
            qtd_linhas = len(open(input_dir).readlines())
            # qtd_linhas = df.size
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
                    'id':output_dir[7:-8],
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
            obj['analise']['percentual'] = float(progresso) / float(obj['analise']['total']) * 100

            json_string = json.dumps(obj)  # transforma em string
            open(output_dir + '/_progresso.json', 'w').write(json_string)


    def salvar(estado, obj):
        # jsonData = json.dumps(obj)

        # with open(output_dir + '/'+estado+'.json', 'w') as f:
        #     json.dump(jsonData, f)
        json_string = json.dumps(obj)
        open(output_dir + '/'+estado+'.json', 'w').write(json_string)


    def finalizar():
        new_output_dir = output_dir[:-8]
        os.rename(output_dir, new_output_dir)  # remover '.pending'

        read_files = glob.glob(new_output_dir + "/*.json")
        read_files.pop()  # removendo o arquivo '_progresso.json'
        output_list = {}

        for f in read_files:
            with open(f, "rb") as infile:
                output_list.update(json.load(infile))

        json_string = json.dumps(output_list)  # transforma em string
        open(new_output_dir + '/_resultado.json', 'w').write(json_string)

        json_string = open(new_output_dir + '/_progresso.json').read()  # carrega arquivo json
        obj = json.loads(json_string)  # transforma em object

        obj['analise']['tempo'] = time.time() - start_time

        json_string = json.dumps(obj)  # transforma em string
        open(new_output_dir + '/_progresso.json', 'w').write(json_string)

        print("--- %s s ---" % (time.time() - start_time))

    df = pd.read_csv(input_dir, delimiter=';', names=dfHeader)
    preparar()
    progresso = 0

    for e in df.estado.unique():
        saidaEstado = {}
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
                print e+'-'+c+'-'+o
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
    analisar('dataset_100.csv', 2, 3, 2, 2)
