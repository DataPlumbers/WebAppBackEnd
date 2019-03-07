''' flask app with mongo '''
import json
import datetime
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from flask_cors import CORS
import os, sys

UPLOAD_FOLDER = 'uploads'


class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, bytes):
            return o.decode('utf-8')
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def init_config_details():
    lib_path = os.path.abspath(os.path.join('python-flask'))
    sys.path.append(lib_path)
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    os.environ.update({'ROOT_PATH': ROOT_PATH})
    # Port variable to run the server on.
    PORT = os.environ.get('PORT')
    sys.path.remove(lib_path)


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    CORS(app)
    # add mongo url to flask config, so that flask_pymongo can use it to make connection
    app.config['MONGO_DBNAME'] = 'test'
    # app.config['MONGO_URI'] = 'mongodb://%s:%s@ds161764.mlab.com:61764/dataplumers' % (os.environ.get('db_user'), os.environ.get('db_password'))
    app.config['MONGO_URI'] = 'mongodb://admin:c4pston3@ds161764.mlab.com:61764/dataplumers'
    app.config['JWT_SECRET_KEY'] = 'key.txt'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=365)
    # use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
    app.json_encoder = JSONEncoder
    return app


# stick into create_app
# create the flask object
app = create_app()
mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
