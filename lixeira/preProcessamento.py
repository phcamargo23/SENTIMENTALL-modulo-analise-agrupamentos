# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
df = pd.read_csv('C:\Users\Pedro Henrique\Google Drive\CEULP-ULBRA\TCC II\Lab\dataset.csv', delimiter=';', names=dfHeader);
# listaDeAspectosDistintos = []


def extrairCaracteristicas(subconjunto):
    listaDeAspectos = set()
    # listaDeAspectos = pd.DataFrame()

    for aspectos in subconjunto.aspectos:
        for aspecto in aspectos.split(','):
            listaDeAspectos.add(aspecto)
            # listaDeAspectos[aspecto] = pd.Series();

    return listaDeAspectos

    # listaDeAspectos_str = ''
    # listaDeAspectosDistintos = []
    #
    # for aspectos in subconjunto.aspectos:
    #     listaDeAspectos_str += aspectos + ','
    #
    # listaDeAspectos = listaDeAspectos_str.split(',')
    # listaDeAspectos.pop()
    #
    # for aspecto in listaDeAspectos:
    #     if aspecto not in listaDeAspectosDistintos:
    #         listaDeAspectosDistintos.append(aspecto)
    #
    # return listaDeAspectosDistintos
    #
    # # print listaDeAspectos;
    # # print listaDeAspectosDistintos




def transformarConjuntoDeDados(caracteristicas, subconjunto):
#     valor = []
#
#     for aspecto in caracteristicas:
#         for avaliacao in subconjunto.aspectos:
#             if aspecto in avaliacao:
#                 valor.append(1)
#             else:
#                 valor.append(0)
#
#         caracteristicas[aspecto].append(valor);


    dataframe = pd.DataFrame(columns=caracteristicas)
    resultado = []

    for avaliacao in subconjunto.aspectos:
        valor = []
        for aspecto in caracteristicas:
            if aspecto in avaliacao.split(','):
                valor.append(1)
            else:
                valor.append(0)

        resultado.append(valor);

    # dataframe.loc[len(dataframe)] = np.array(resultado)
    dataframe = pd.DataFrame(data=np.array(resultado), columns=caracteristicas)
    # return np.array(resultado)
    return dataframe


def preProcessar(nivel):
    dicionario = []

    for estado in nivel.unique():
        subconjunto = df[nivel == estado]
        caracteristicas = extrairCaracteristicas(subconjunto)
        subconjuntoTransformado = transformarConjuntoDeDados(caracteristicas, subconjunto)
        dicionario.append({estado:subconjuntoTransformado});

    return dicionario


def processar():
    # TODO: ARQUIVO SEM FORMATO BOOM
    return {'estados':preProcessar(df.estado),'cidades':preProcessar(df.cidade),'tipos':preProcessar(df.tipo),'objetos':preProcessar(df.objeto)}

# if __name__ == '__main__':
#     processar()