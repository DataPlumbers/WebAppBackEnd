import os, sys

lib_path = os.path.abspath(os.path.join('python-flask'))
sys.path.append(lib_path)
from modules.app.config import app

if __name__ == "__main__":
    app.run()
