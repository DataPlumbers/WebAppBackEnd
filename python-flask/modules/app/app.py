''' flask app with mongo '''
import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from flask_cors import CORS

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


# create the flask object
app = Flask(__name__)
CORS(app)

# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://%s:%s@ds161764.mlab.com:61764/dataplumers' % (os.environ.get('db_user'), os.environ.get('db_password'))
app.config['JWT_SECRET_KEY'] = 'key.txt'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=365)

mongo = PyMongo(app)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder
