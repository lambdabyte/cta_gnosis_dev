import os
import os.path
from config import DevelopmentConfig
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# instantiate the users service
app = Flask(__name__)

api = Api(app)

# set config
app.config.from_object(DevelopmentConfig)


# instantiate database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models


api.add_resource(routes.Ping, '/ping')


