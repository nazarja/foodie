from flask import Flask
from flask_login import LoginManager
from config.config import Config
from pymongo import MongoClient


# initialize app
app = Flask(__name__)
app.config.from_object(Config)

# login manager
login = LoginManager(app)
login.login_view = '/sign/in'

# configure mongodb, during development ('localhost', 27017) was used
client = MongoClient('localhost', 27017)
db = client.foodie

# import routes
from app.routes import routes, errors