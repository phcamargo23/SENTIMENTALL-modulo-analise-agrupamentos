# -*- coding: utf-8 -*-
from __future__ import print_function
from time import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# n_samples = 2000
# n_features = 1000
n_topics = 3
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


print("Loading dataset...")
data_samples = \
    [
        'localização preço'
        , 'atendimento lugar'
        , 'lugar'
        , 'preço'
        , 'ambiente'
        , 'comida'
        , 'comida variedade'
        , 'atendimento'
        , 'passeio'
        , 'lugar preço'
        , 'localização passeio'
        , 'comida lugar praia restaurante'
        , 'atendimento comida'
        , 'opção'
        , 'local'
        , 'comida preço qualidade restaurante'
        , 'local localização restaurante'
        , 'qualidade'
        , 'qualidade variedade'
        , 'comida localização preço qualidade'
        , 'comida preço'
        , 'lugar passeio praia'
        , 'local pratos vista'
        , 'restaurante'
        , 'atendimento qualidade'
        , 'praia'
        , 'lugar opção'
        , 'local preço'
        , 'comida serviço variedade'
        , 'atendimento quartos'
        , 'preço qualidade'
        , 'preço restaurante'
        , 'funcionários'
        , 'local lugar'
        , 'localização'
        , 'ambiente comida hotel'
        , 'comida opção preço qualidade quartos'
        , 'ambiente preço'
        , 'hotel'
        , 'atendimento hotel localização'
        , 'opção variedade'
        , 'opção preço'
        , 'comida lugar'
        , 'atendimento comida localização'
        , 'atendimento local preço'
        , 'vista'
        , 'lugar restaurante'
        , 'ambiente restaurante'
        , 'atendimento funcionários'
        , 'variedade'
        , 'atendimento local'
        , 'atendimento hotel'
        , 'praia preço'
        , 'comida lugar restaurante'
        , 'atendimento local pratos'
        , 'comida localização'
        , 'ambiente comida'
        , 'ambiente local'
        , 'atendimento localização qualidade'
        , 'preço variedade'
        , 'comida hotel'
        , 'localização opção'
        , 'comida restaurante'
        , 'hotel localização'
        , 'pratos'
        , 'ambiente lugar preço'
        , 'comida funcionários hotel'
        , 'atendimento restaurante'
        , 'lugar variedade'
        , 'atendimento preço'
        , 'hotel preço'
        , 'hotel local'
        , 'hotel quartos'
        , 'localização lugar restaurante'
        , 'localização variedade'
        , 'passeio praia preço'
        , 'localização restaurante'
        , 'serviço'
        , 'comida praia'
        , 'local variedade'
        , 'opção preço variedade'
        , 'ambiente lugar'
        , 'passeio preço'
        , 'localização opção preço restaurante'
        , 'lugar passeio'
        , 'local passeio'
        , 'atendimento opção'
        , 'comida restaurante serviço'
        , 'atendimento local localização preço'
        , 'funcionários localização'
        , 'hotel quartos variedade'
        , 'opção preço qualidade'
        , 'local localização'
        , 'hotel lugar'
        , 'local opção'
        , 'lugar opção restaurante'
        , 'opção passeio'
        , 'lugar praia'
        , 'local praia'
        , 'ambiente local praia vista']

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer()
tf = tf_vectorizer.fit_transform(data_samples)

print("Fit LDA...")
lda = LatentDirichletAllocation(n_topics=3, learning_method='online')
lda.fit(tf)

print("\nTopics in LDA model:")
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, n_top_words)
