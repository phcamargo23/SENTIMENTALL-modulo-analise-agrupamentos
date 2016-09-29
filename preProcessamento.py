# -*- coding: utf-8 -*-
import os
import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
df = pd.read_csv('C:\Users\Pedro Henrique\Downloads\dataset.csv', delimiter=';', names=dfHeader);
# listaDeAspectosDistintos = []


def extrairCaracteristicas(subconjunto):
    # aspectos = []
    # aspectos.append(dataset_estado.aspectos.str.split(','))
    # print aspectos

    listaDeAspectos_str = ''
    listaDeAspectosDistintos = []

    for aspectos in subconjunto.aspectos:
        listaDeAspectos_str += aspectos + ','

    listaDeAspectos = listaDeAspectos_str.split(',')
    listaDeAspectos.pop()

    for aspecto in listaDeAspectos:
        if aspecto not in listaDeAspectosDistintos:
            listaDeAspectosDistintos.append(aspecto)

    return listaDeAspectosDistintos

    # print listaDeAspectos;
    # print listaDeAspectosDistintos




def transformarConjuntoDeDados(caracteristicas, subconjunto):
    valores = []

    for aspectosDaAvaliacao in subconjunto.aspectos:
        registro = []
        for aspecto in caracteristicas:
            if aspecto in aspectosDaAvaliacao.split(','):
                registro.append(1)
            else:
                registro.append(0)

        valores.append(registro)

    return valores


def fragmentarConjuntoDeDados():
    # TODO: ARQUIVO SEM FORMATO BOOM
    conjuntoDeDadosDeTodosOsNiveis = []

    # POR ESTADO
    conjuntosDeDados = []

    for estado in df.estado.unique():
        subconjunto = df[df.estado == estado]
        caracteristicas = extrairCaracteristicas(subconjunto)
        subconjuntoTransformado = transformarConjuntoDeDados(caracteristicas, subconjunto)
        conjuntosDeDados.append(subconjuntoTransformado);

    conjuntoDeDadosDeTodosOsNiveis.append(conjuntosDeDados);

    # POR CIDADE
    conjuntosDeDados = []

    for cidade in df.cidade.unique():
        subconjunto = df[df.cidade == cidade]
        caracteristicas = extrairCaracteristicas(subconjunto)
        subconjuntoTransformado = transformarConjuntoDeDados(caracteristicas, subconjunto)
        conjuntosDeDados.append(subconjuntoTransformado);

    conjuntoDeDadosDeTodosOsNiveis.append(conjuntosDeDados);

    return conjuntoDeDadosDeTodosOsNiveis

def processar():
    return fragmentarConjuntoDeDados()