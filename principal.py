# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, request, json
import preProcessamento
import analise

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/')
def index():
    return make_response(open(os.path.join(DIR, 'templates/index.html')).read())

@app.route('/analisar')
def main():
    # k = int(request.args.get('k'))
    k=3
    conjuntoDeDadosDeTodosOsNiveis = preProcessamento.processar();
    resultadoDeTodosOsNiveis = analise.processar(conjuntoDeDadosDeTodosOsNiveis, k)

    # print conjuntoDeDadosDeTodosOsNiveis
    print resultadoDeTodosOsNiveis

    # return json.dumps(conjuntoDeDadosDeTodosOsNiveis)
    # return analisarConjuntoDeDados.main()

if __name__ == '__main__':
    # app.run()
    main()
