from flask.views import MethodView
from flask import json

class API_View(MethodView):
    def get(self):   
      pass 

    def post(self):
      pass
    
    def get_json_response(self, message, status, content_type):
      return json.dumps(message), status, content_type