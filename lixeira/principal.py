# -*- coding: utf-8 -*-
import os

from flask import Flask, make_response

import analise
from lixeira import preProcessamento

app = Flask(__name__)

# tudo = {'estados':{'TO':pd.DataFrame()}}
# tudo = {'estados':{'SP':pd.DataFrame()}}

# dfTodosNiveis = pd.DataFrame()
# dfTodosNiveis['estados'] = pd.Series();
# dfTodosNiveis['estados']['cidades'];

@app.route('/')
def index():
    return make_response(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/index.html')).read())

@app.route('/analisar')
def main():
    # k = int(request.args.get('k'))
    k=2
    conjuntoDeDadosDeTodosOsNiveis = preProcessamento.processar();
    resultadoDeTodosOsNiveis = analise.processar(conjuntoDeDadosDeTodosOsNiveis, k)

    x=0
    # print conjuntoDeDadosDeTodosOsNiveis
    print resultadoDeTodosOsNiveis

    # return json.dumps(conjuntoDeDadosDeTodosOsNiveis)
    # return analisarConjuntoDeDados.main()

if __name__ == '__main__':
    # app.run()
    main()
