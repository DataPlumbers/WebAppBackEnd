from os import environ

bind = environ.get('HOST', '0.0.0.0') + ':' + environ.get('PORT', '8000')