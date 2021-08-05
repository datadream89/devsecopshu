"""
This script runs the FlaskWebProject2 application using a development server.
"""

from flask_cors import CORS
from datamanagement import create_app
from waitress import serve

app = create_app()
cors = CORS(app)

if __name__ == '__main__':
  serve(app, host="0.0.0.0",port=5002)
