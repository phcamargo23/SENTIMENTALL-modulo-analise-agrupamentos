# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, jsonify, json, request
import numpy as np
from sklearn.cluster import KMeans

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)


def main():
    Z = ['atendimento', 'comida', 'bar'];

    X = [
        [1, 2, 2],
        [1, 6, 3],
        [5, 8, 4],
        [5, 8, 5],
        [8, 8, 6],
        [9, 9, 7]
    ]

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    Y = []
    for i in centroids:
        Y.append(zip(Z, i))

    return json.dumps(Y)

if __name__ == '__main__':
    main()