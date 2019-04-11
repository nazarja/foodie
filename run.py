import os
from app import app

"""
    This file runs the application and imports the application from /app/__init__.py.
    During development, IP is localhost, PORT is 5000 and DEBUG is set to True.  
"""

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True)
