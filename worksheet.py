import json
import os
import pickle
import requests
import sys

from flask import Flask, Response, render_template, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return render_template('worksheet.html')

@app.route('/savefile', methods=['POST'])
def savefile():
    text = request.values.get('text')
    name = request.values.get('name')
    with open(f'data/{name}.txt', 'w') as fle:
        fle.write(text)
    data = {'response': 'success'}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":

    app.run(debug=True, port=8888)
