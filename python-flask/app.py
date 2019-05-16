import os, logging
import modules.schemas.user as validate
from flask import jsonify, request, make_response, send_from_directory
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from modules.Configuration.config import app, mongo, flask_bcrypt, jwt, init_config_details
from modules.utils.allowed_filenames import allowed_file
from modules.utils.init_classifier import classify_data
from modules.utils.validate_csv import validate_csv_file
from werkzeug.utils import secure_filename
from bson import json_util


@app.errorhandler(404)
def not_found(error):
    """ error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    """ static files serve """
    return make_response(jsonify({'message': 'Hello World'}), 200)


@app.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join('static', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)


@app.route('/users', methods=['GET'])
@jwt_required
def user():
    ''' route read user '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query, {"_id": 0})
        return jsonify({'ok': True, 'data': data}), 200


@app.route('/users/signup', methods=['POST'])
def register():
    ''' register user endpoint '''
    data = validate.validate_user(request.get_json())
    if data['ok']:
        user = data['data']
        user['password'] = flask_bcrypt.generate_password_hash(
            user['password'])
        user_exists = mongo.db.users.find_one({'email': user['email']}) != None
        if (user_exists):
            return jsonify({'ok': 'False', 'message': 'Email already exists!'}), 401
        else:
            mongo.db.users.insert_one(user)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Error: password must be at least 5 characters'}), 401


@app.route('/users/auth', methods=['POST'])
def auth_user():
    ''' auth endpoint '''
    data = validate.validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']}, {"_id": 0})
        if user and flask_bcrypt.check_password_hash(user['password'], data['password']):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user['token'] = access_token
            user['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify({'ok': False, 'message': 'invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401


@app.route('/category/get', methods=['GET'])
def get_category():
    if request.method == 'GET':
        try:
            data = (request.values.get('category_name'))
            result = mongo.db.categories.find_one({'Category': data})
            category = result.get('Category')
            properties = result.get('Properties')[0].split(",")
            return jsonify({'ok': True, 'categories': ([
                {'label': category, 'value': properties}])})
        except:
            return jsonify({'ok': True, 'categories': ([
               {'label': 'Review', 'value': ['author', 'comment', 'date']},
               {'label': 'Employee', 'value': ['fullname', 'occupation', 'address', 'id']}
            ])})



@app.route('/category/remove', methods=['POST'])
def remove_category():
    data = request.get_json()
    category = data['category_name']
    result = mongo.db.categories.remove(({'Category': category}))
    if result.deleted_count == 0:
        return jsonify({'ok': False, 'message': 'Category not found'}), 401
    else:
        return jsonify({'ok': True}), 200


@app.route('/upload', methods=['POST'])
def classify_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        category = (request.values.get('category'))
        properties = (request.values.get('properties'))
        MongoObject = ({'Category': category, 'Properties': properties})
        if not mongo.db.categories.find_one(MongoObject):
            mongo.db.categories.insert_one(MongoObject)
        filenames = []
        for file in files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(file_path)
        # data = (json_util.dumps(category))
        results_json = (classify_data(category, properties, filenames))
        print(results_json)
        return jsonify({'ok': True, 'results': results_json}), 200
        # return jsonify({'ok': True}), 200
    else:
        return jsonify({'ok': False}), 404


if __name__ == '__main__':
    init_config_details()
    app.config['DEBUG'] = True  # Debug mode if development env
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host=host, port=port)  # Run the Configuration
