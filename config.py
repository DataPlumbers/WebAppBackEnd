from os import environ

bind = '0.0.0.0:' + environ.get('PORT', '8000')