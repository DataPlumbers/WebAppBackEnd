""" index file for REST APIs using Flask """
import os, sys
lib_path = os.path.abspath(os.path.join('python-flask'))
sys.path.append(lib_path)
import modules.schemas.user as validate
from flask import jsonify, request, make_response, send_from_directory
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from modules.app.app import app, mongo, flask_bcrypt, jwt

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
# Port variable to run the server on.
PORT = os.environ.get('PORT')

sys.path.remove(lib_path)


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
        if(user_exists):
            return jsonify({'ok': 'False', 'message': 'Email already exists!'}), 401
        else:
            mongo.db.users.insert_one(user)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data['message'])}), 400


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


if __name__ == '__main__':
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'  # Debug mode if development env
    port = int(os.environ.get('PORT', 33507))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port)  # Run the app