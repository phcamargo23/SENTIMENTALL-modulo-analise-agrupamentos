# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, jsonify, json, request
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import OrderedDict

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

inputHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
df = pd.read_csv('C:\Users\Pedro Henrique\Downloads\dataset.csv', delimiter=';', names=inputHeader);
listaDeAspectosDistintos = []
dataset = []

def criarListaDeApectos():
    listaDeAspectos_str = ''

    for aspectos in df.aspectos:
        listaDeAspectos_str += aspectos + ','

    listaDeAspectos = listaDeAspectos_str.split(',')

    for aspecto in listaDeAspectos:
        if aspecto not in listaDeAspectosDistintos:
            listaDeAspectosDistintos.append(aspecto)

    listaDeAspectosDistintos.pop()

    # print listaDeAspectos;
    # print listaDeAspectosDistintos

def prepararDataset():
    for aspectosDaAvaliacao in df.aspectos:
        row = []
        for aspecto in listaDeAspectosDistintos:
            if aspecto in aspectosDaAvaliacao.split(','):
                row.append(1)
            else:
                row.append(0)

        dataset.append(row)

def analisar():
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(dataset)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    Y = []
    for i in centroids:
        Y.append(zip(listaDeAspectosDistintos, i))

    return json.dumps(Y)

def analisarEstado():
    for estado in df.estado.unique():
        if df[df.estado == estado]:
            print ''
    # for index, row in df.iterrows():
    #     print row['c1'], row['c2'

def analisarCidade():
    print #

def analisarTipo():
    print #

def analisarObjeto():
    print #


def main():
    # criarListaDeApectos()
    # prepararDataset()
    analisarEstado()

if __name__ == '__main__':
    main()