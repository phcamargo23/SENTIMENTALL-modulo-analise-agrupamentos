# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()

counts = [[3, 0, 1],
          [2, 0, 0],
          [3, 0, 0],
          [4, 0, 0],
          [3, 2, 0],
          [3, 0, 2]]

tfidf = transformer.fit_transform(counts)
print tfidf