from app import app
from flask_restx import Resource
from flask import render_template

@app.route('/index')
def index():
    return render_template('index.html')

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }