from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from flask_marshmallow import Marshmallow


app = Flask(__name__, static_folder='static')
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
ma = Marshmallow(app)
api = Api(app)
