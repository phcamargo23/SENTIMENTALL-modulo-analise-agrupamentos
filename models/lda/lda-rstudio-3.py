# -*- coding: utf-8 -*-
#https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
#en_stop = get_stop_words('en')
en_stop = stopwords.words('portuguese')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# compile sample documents into a list
doc_set = \
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

#doc_set = [w.decode() for w in doc_set]

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:

    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw.decode('utf-8'))

    # remove stop words from tokens
    #stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
#print dictionary

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]
#print corpus

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
print(ldamodel.print_topics(num_topics=3, num_words=4))