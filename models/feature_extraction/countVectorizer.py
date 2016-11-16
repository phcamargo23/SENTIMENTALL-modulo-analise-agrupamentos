# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer

def my_tokenizer(s):
    return s.split(',')

vectorizer = CountVectorizer(binary=True, tokenizer=my_tokenizer)
corpus = [
    'localização preço'
    , 'atendimento lugar'
    , 'comida variedade'
    , 'lugar preço'
    , 'localização passeio'
    , 'atendimento lugar praia'
]
X = vectorizer.fit(corpus)
print X