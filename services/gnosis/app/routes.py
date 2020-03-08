from app import app
from flask_restx import Resource
# test
@app.route('/hello')
def index():
    return "Hello, Worsldss!"

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }