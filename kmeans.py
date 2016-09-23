# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, jsonify, request
import numpy as np
from sklearn.cluster import KMeans

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

def main():
    X = np.array([[1, 2],
                  [5, 8],
                  [1.5, 1.8],
                  [8, 8],
                  [1, 0.6],
                  [9, 11]])

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    # print X
    # print(labels)
    # print(centroids)
    return jsonify(centroids.tolist())
    # return 'teste'