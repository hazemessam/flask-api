from flask import Flask
from flask_cors import CORS
from flask_cors.decorator import cross_origin


app = Flask(__name__)
app.config.from_object('config')
# cors = CORS(app)

# @app.after_request
# def after_request(respose):
#     respose.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTION')
#     respose.headers.add('Access-Control-Allow-Origin', 'https://www.google.com')
#     return respose

# Get home page
@app.route('/')
def get_index():
    # return redirect('/api/users')
    return 'Welcome to the home page'

from application.controllers import *
