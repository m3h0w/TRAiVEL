# Import flask and template operators
from flask import Flask
from flask import jsonify, request

app = Flask(__name__, static_url_path='/static')
