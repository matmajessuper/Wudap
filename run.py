from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Configdb

app = Flask(__name__, static_folder='static')
app.config.from_object(Configdb)
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
