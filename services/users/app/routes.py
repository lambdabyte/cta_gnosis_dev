from app import app
from flask_restx import Resource

@app.route('/hello')
def index():
    return "Hello, Worlds!"

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }