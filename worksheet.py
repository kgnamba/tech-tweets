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

if __name__ == "__main__":

    app.run(debug=True, port=8888)
