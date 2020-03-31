import os
import os.path
from config import DevelopmentConfig
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login import login_required

# instantiate the users service
app = Flask(__name__)

# initalize api
api = Api(app)

# set config
app.config.from_object(DevelopmentConfig)

login = LoginManager(app)
login.login_view = 'login'

#  instantiate database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models


api.add_resource(routes.Ping, '/ping')


