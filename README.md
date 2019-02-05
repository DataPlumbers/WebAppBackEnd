## Python-Flask Backend: How To Run
[![Build Status](https://travis-ci.com/kramsey458/WebAppBackEnd.svg?branch=DAT-37)](https://travis-ci.com/kramsey458/WebAppBackEnd)

Make sure you are in the root directory, WebAppBackEnd/  

Run the following commands.  

Linux/Windows
### `pip install pipenv`
OSX
### `pip3 install pipenv`
Then run
### `pipenv install`
### `pipenv shell`
Change into the directory python-flask
run using: `gunicorn app:app`
OR `python3 app.py`

Open [http://0.0.0.0:8000/](http://0.0.0.0:8000/) to view it in the browser. 

Flask_postman_tests.json contains GET and POST requests (Postman) to test the server with  
View routes in python-flask/app.py
