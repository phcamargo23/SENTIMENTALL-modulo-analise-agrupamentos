# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, json
import pandas as pd
import processamento
import time
from threading import Thread

def myfunc(i):
    dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
    filename = 'C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset3.csv'
    file_n = len(open(filename).readlines())
    file_n_total = 0
    total = 0
    k = 3
    chunksize = 10 ** 3
    for df in pd.read_csv(filename, delimiter=';', names=dfHeader, chunksize=chunksize):
        file_n_total += len(df)
        total = file_n_total * 100 / file_n

        jsonData = json.dumps({'progresso': total})
        with open('_progesso.json', 'w') as f:
            json.dump(jsonData, f)

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

    # print json.dumps(saidaEstado)
    # return json.dumps(saidaEstado)
    jsonData = json.dumps(saidaEstado)
    with open('_resultado.json', 'w') as f:
        json.dump(jsonData, f)

if __name__ == '__main__':
    t = Thread(target=myfunc, args=(8,))
    t.start()
    print 'teste'