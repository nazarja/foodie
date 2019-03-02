import json
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash


# User Loader
@login.user_loader
def load_user(username):
    user = db.users.find_one({"username": username})
    if not user:
        return None
    return User(user['username'], user)


# User Login Class
class User():

    def __init__(self, username, user=None):
        self.username = username
        self.user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
        
    def get_user_data(self):
        user = db.users.find_one({"username": self.username })
        self.user = user
        
    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def add_user(username, password):
        with open('app/data/schemas/user.json') as users_file:
            user = json.load(users_file)
            user['username'] = username.lower()
            user['password'] = generate_password_hash(password)
            db.users.insert_one(user)