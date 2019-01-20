from os import environ

bind = environ.get('HOST', 'https://capstone-plumbers-api.herokuapp.com') + ':' + environ.get('PORT', '8000')