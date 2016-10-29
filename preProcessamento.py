# -*- coding: utf-8 -*-
import sys

def extrairCaracteristicas(subconjunto):
    listaDeAspectos = set()

    for aspectos in subconjunto.aspectos:
        for aspecto in aspectos.split(','):
            listaDeAspectos.add(aspecto)

    return listaDeAspectos

def processarPonderacaoBinaria(caracteristicas, subconjunto):
    resultado = []

    # i = 0
    for avaliacao in subconjunto.aspectos:
        valor = []
        for aspecto in caracteristicas:
            if aspecto in avaliacao.split(','):
                valor.append(1)
            else:
                valor.append(0)
        # try:
            resultado.append(valor)
        # except:
        #     print 'erro'

        # i = i + 1
        # print str(i) + '-' + str(sys.getsizeof(resultado))

    return resultado