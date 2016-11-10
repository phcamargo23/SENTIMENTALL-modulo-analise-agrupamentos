# -*- coding: utf-8 -*-
from sklearn.datasets import load_iris
from sklearn.cluster import DBSCAN

iris = load_iris()
dbscan = DBSCAN(random_state=111)

dbscan = DBSCAN(random_state=111)