# -*- coding: utf-8 -*-
import os
from flask import Flask, make_response, jsonify
import kmeans

DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/')
def index():
    return make_response(open(os.path.join(DIR, 'templates/index.html')).read())

@app.route('/kmeans')
def main():
    return kmeans.main()

if __name__ == '__main__':
    app.run()
