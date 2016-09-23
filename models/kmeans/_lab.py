# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
from sklearn import datasets
from pylab import *
'''
iris = datasets.load_iris()
X,y = iris.data, iris.target
k_means = KMeans(n_clusters=3, random_state=0)
#print iris
#print X
k_means.fit(X)
#print k_means

y_pred = k_means.predict(X)

#print y_pred

#scatter(X[:,0], X[:,1], c=y_pred);
#scatter(X[:,0], X[:,1], c=y_pred);
#print X
#print X[:,0]
#print y_pred
#print y
#scatter(X[:,0], X[:,1], s=200, c=y_pred);
scatter(X[:,0], X[:,1], s=200, c=y);
show()
'''

iris = datasets.load_iris()
X,y = iris.data, iris.target

print type(X)