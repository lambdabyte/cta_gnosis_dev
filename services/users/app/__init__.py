import os
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# instantiate the users service
app = Flask(__name__)

api = Api(app)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object('app.config.DevelopmentConfig')

# instantiate database
db = SQLAlchemy(app)


from app import routes, models

api.add_resource(routes.Ping, '/ping')


