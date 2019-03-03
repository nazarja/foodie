from flask import Flask
from config.config import Config
from flask_login import LoginManager
from pymongo import MongoClient


# initialize app
app = Flask(__name__)
app.config.from_object(Config)

# login manager
login = LoginManager(app)
login.login_view = '/sign/in'

# configure mongodb
client = MongoClient('localhost', 27017)
db = client.foodie


from app.views import routes, errors