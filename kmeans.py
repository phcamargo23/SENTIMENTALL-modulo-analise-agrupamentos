# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, jsonify, json, request
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import OrderedDict

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

inputHeader = ['aspectos', 'estado', 'cidade']
input = pd.read_csv('C:\Users\Pedro Henrique\Downloads\\b.csv', delimiter=';', names=inputHeader );
listaDeAspectosDistintos = []
dataset = []

def criarListaDeApectos():
    listaDeAspectos_str = ''

    for aspectos in input.aspectos:
        listaDeAspectos_str += aspectos + ','

    listaDeAspectos = listaDeAspectos_str.split(',')

    for aspecto in listaDeAspectos:
        if aspecto not in listaDeAspectosDistintos:
            listaDeAspectosDistintos.append(aspecto)

    listaDeAspectosDistintos.pop()

    # print listaDeAspectos;
    # print listaDeAspectosDistintos

def prepararDataset():
    for aspectosDaAvaliacao in input.aspectos:
        row = []
        for aspecto in listaDeAspectosDistintos:
            if aspecto in aspectosDaAvaliacao.split(','):
                row.append(1)
            else:
                row.append(0)

        dataset.append(row)

def main():
    criarListaDeApectos()
    prepararDataset()

    # print listaDeAspectosDistintos
    # print dataset

    # listaDeAspectosDistintos = ['atendimento', 'comida', 'bar'];
    # dataset = [
    #     [1, 2, 2],
    #     [1, 60, 3],
    #     [5, 8, 4],
    #     [5, 8, 5],
    #     [8, 8, 6],
    #     [9, 9, 0]
    # ]

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(dataset)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    Y = []
    for i in centroids:
        Y.append(zip(listaDeAspectosDistintos, i))

    return json.dumps(Y)

if __name__ == '__main__':
    main()