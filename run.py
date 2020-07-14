from flask import Flask
from flask_restplus import Api
from flask_marshmallow import Marshmallow


app = Flask(__name__, static_folder='static')
ma = Marshmallow(app)
api = Api(app)
