import flask
import requests
import simplejson
from flask import request
from flask import Flask, Response
from flask import jsonify
from flask import make_response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/hello', methods=['GET'])
def health():
    data = {'message': 'hello world'}
    return data



app.run(host='0.0.0.0', port=8080)
