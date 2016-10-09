# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, json
import pandas as pd
import processamento
from threading import Thread
from time import gmtime, strftime
import time

app = Flask(__name__)

directory = None

filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset0.csv'

def naoFragmentado_todasAnalises(k):
    eps = 1
    minPts = 5

    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']

    # directory = 'output\\' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) +'.pending'

    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    file_number_rows = len(open(filename).readlines())

    file_number_row_current = 0
    percentual = 0

    df = pd.read_csv(filename, delimiter=';', names=dfHeader)
    file_number_row_current += len(df)
    percentual = file_number_row_current * 100 / file_number_rows

    # json.dump({'total': file_number_rows, 'progresso': file_number_row_current, 'percentual': percentual}, open(directory+'/_progresso.json', 'w'))

    saidaEstado = {}

    for e in df.estado.unique():
        subconjuntoEstado = df[df.estado == e]
        saidaEstado[e] = {
                    'kmeans': processamento.processarKmeans(subconjuntoEstado, k),
                    'lda': processamento.processarLDA(subconjuntoEstado, k),
                    'dbscan': processamento.processarDBSCAN(subconjuntoEstado, eps, minPts),
                }

        saidaCidade = {}

        for c in subconjuntoEstado.cidade.unique():
            subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
            saidaCidade[c] = {
                    'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                    'lda': processamento.processarLDA(subconjuntoCidade, k),
                    'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
                }

            saidaObjeto = {};

            for o in subconjuntoCidade.objeto.unique():
                subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                saidaObjeto[o] = {
                    'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                    'lda': processamento.processarLDA(subconjunto_objeto, k),
                    'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                }

            saidaCidade[c].update(saidaObjeto);

        saidaEstado[e].update(saidaCidade);

    jsonData = json.dumps(saidaEstado)
    # with open(directory+'/_resultado.json', 'w') as f:
    #     json.dump(jsonData, f)

    # os.rename(directory, directory[:-8]) #remover '.pending'


def fragmentado_todasAnalises(k, chunksize=10 ** 4):
    eps = 1
    minPts = 5

    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']

    # directory = 'output\\' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) +'.pending'

    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    file_number_rows = len(open(filename).readlines())

    file_number_row_current = 0
    percentual = 0

    for df in pd.read_csv(filename, delimiter=';', names=dfHeader, chunksize=chunksize):
        file_number_row_current += len(df)
        percentual = file_number_row_current * 100 / file_number_rows

        # json.dump({'total': file_number_rows, 'progresso': file_number_row_current, 'percentual': percentual}, open(directory+'/_progresso.json', 'w'))

        saidaEstado = {}

        for e in df.estado.unique():
            subconjuntoEstado = df[df.estado == e]
            saidaEstado[e] = {
                        'kmeans': processamento.processarKmeans(subconjuntoEstado, k),
                        'lda': processamento.processarLDA(subconjuntoEstado, k),
                        'dbscan': processamento.processarDBSCAN(subconjuntoEstado, eps, minPts),
                    }

            saidaCidade = {}

            for c in subconjuntoEstado.cidade.unique():
                subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
                saidaCidade[c] = {
                        'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                        'lda': processamento.processarLDA(subconjuntoCidade, k),
                        'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
                    }

                saidaObjeto = {};

                for o in subconjuntoCidade.objeto.unique():
                    subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                    saidaObjeto[o] = {
                        'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                        'lda': processamento.processarLDA(subconjunto_objeto, k),
                        'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                    }

                saidaCidade[c].update(saidaObjeto);

            saidaEstado[e].update(saidaCidade);

    jsonData = json.dumps(saidaEstado)
    # with open(directory+'/_resultado.json', 'w') as f:
    #     json.dump(jsonData, f)

    # os.rename(directory, directory[:-8]) #remover '.pending'


def naoFragmentado_semAnalises(k):
    eps = 1
    minPts = 5

    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']

    # directory = 'output\\' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) +'.pending'

    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    file_number_rows = len(open(filename).readlines())

    file_number_row_current = 0
    percentual = 0

    df = pd.read_csv(filename, delimiter=';', names=dfHeader)
    file_number_row_current += len(df)
    percentual = file_number_row_current * 100 / file_number_rows

    # json.dump({'total': file_number_rows, 'progresso': file_number_row_current, 'percentual': percentual}, open(directory+'/_progresso.json', 'w'))

    saidaEstado = {}

    for e in df.estado.unique():
        subconjuntoEstado = df[df.estado == e]
        saidaEstado[e] = {
                    # 'kmeans': processamento.processarKmeans(subconjuntoEstado, k),
                    # 'lda': processamento.processarLDA(subconjuntoEstado, k),
                    # 'dbscan': processamento.processarDBSCAN(subconjuntoEstado, eps, minPts),
                }

        saidaCidade = {}

        for c in subconjuntoEstado.cidade.unique():
            subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
            saidaCidade[c] = {
                    # 'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                    # 'lda': processamento.processarLDA(subconjuntoCidade, k),
                    # 'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
                }

            saidaObjeto = {};

            for o in subconjuntoCidade.objeto.unique():
                subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                saidaObjeto[o] = {
                    # 'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                    # 'lda': processamento.processarLDA(subconjunto_objeto, k),
                    # 'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                }

            saidaCidade[c].update(saidaObjeto);

        saidaEstado[e].update(saidaCidade);

    jsonData = json.dumps(saidaEstado)
    # with open(directory+'/_resultado.json', 'w') as f:
    #     json.dump(jsonData, f)

    # os.rename(directory, directory[:-8]) #remover '.pending'


def fragmentado_semAnalises(k, chunksize=10 ** 4):
    eps = 1
    minPts = 5

    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']

    # directory = 'output\\' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) +'.pending'

    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    file_number_rows = len(open(filename).readlines())

    file_number_row_current = 0
    percentual = 0

    for df in pd.read_csv(filename, delimiter=';', names=dfHeader, chunksize=chunksize):
        file_number_row_current += len(df)
        percentual = file_number_row_current * 100 / file_number_rows

        # json.dump({'total': file_number_rows, 'progresso': file_number_row_current, 'percentual': percentual}, open(directory+'/_progresso.json', 'w'))

        saidaEstado = {}

        for e in df.estado.unique():
            subconjuntoEstado = df[df.estado == e]
            saidaEstado[e] = {
                        # 'kmeans': processamento.processarKmeans(subconjuntoEstado, k),
                        # 'lda': processamento.processarLDA(subconjuntoEstado, k),
                        # 'dbscan': processamento.processarDBSCAN(subconjuntoEstado, eps, minPts),
                    }

            saidaCidade = {}

            for c in subconjuntoEstado.cidade.unique():
                subconjuntoCidade = subconjuntoEstado[subconjuntoEstado.cidade == c];
                saidaCidade[c] = {
                        # 'kmeans': processamento.processarKmeans(subconjuntoCidade, k),
                        # 'lda': processamento.processarLDA(subconjuntoCidade, k),
                        # 'dbscan': processamento.processarDBSCAN(subconjuntoCidade, eps, minPts),
                    }

                saidaObjeto = {};

                for o in subconjuntoCidade.objeto.unique():
                    subconjunto_objeto = subconjuntoCidade[subconjuntoCidade.objeto == o];
                    saidaObjeto[o] = {
                        # 'kmeans': processamento.processarKmeans(subconjunto_objeto, k),
                        # 'lda': processamento.processarLDA(subconjunto_objeto, k),
                        # 'dbscan': processamento.processarDBSCAN(subconjunto_objeto, eps, minPts),
                    }

                saidaCidade[c].update(saidaObjeto);

            saidaEstado[e].update(saidaCidade);

    jsonData = json.dumps(saidaEstado)
    # with open(directory+'/_resultado.json', 'w') as f:
    #     json.dump(jsonData, f)

    # os.rename(directory, directory[:-8]) #remover '.pending'

if __name__ == '__main__':
    print('fragmentado_semAnalises 2')
    start_time = time.time()
    fragmentado_semAnalises(3, 10 ** 2)
    print("--- %s seconds ---" % (time.time() - start_time))

    print '\n'

    print('fragmentado_semAnalises 4')
    start_time = time.time()
    fragmentado_semAnalises(3, 10 ** 4)
    print("--- %s seconds ---" % (time.time() - start_time))

    print '\n'

    print('fragmentado_semAnalises 6')
    start_time = time.time()
    fragmentado_semAnalises(3, 10 ** 6)
    print("--- %s seconds ---" % (time.time() - start_time))

    print '\n'

    print('naoFragmentado_semAnalises')
    start_time = time.time()
    naoFragmentado_semAnalises(3)
    print("--- %s seconds ---" % (time.time() - start_time))


    print '\n'
    print '\n'


    print('fragmentado_todasAnalises 2')
    start_time = time.time()
    fragmentado_todasAnalises(3, 10 ** 2)
    print("--- %s seconds ---" % (time.time() - start_time))

    print '\n'

    print('fragmentado_todasAnalises 4')
    start_time = time.time()
    fragmentado_todasAnalises(3, 10 ** 4)
    print("--- %s seconds ---" % (time.time() - start_time))

    print '\n'

    print('fragmentado_todasAnalises 6')
    start_time = time.time()
    fragmentado_todasAnalises(3, 10 ** 6)
    print("--- %s seconds ---" % (time.time() - start_time))

    print '\n'

    print('naoFragmentado_todasAnalises')
    start_time = time.time()
    naoFragmentado_todasAnalises(3)
    print("--- %s seconds ---" % (time.time() - start_time))



