import json
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user
from bson.objectid import ObjectId


# user loader
@login.user_loader
def load_user(username):
    user = db.users.find_one({"username": username})
    if not user:
        return None
    return User(user['username'], user)


# user login class
class User:

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
        
    def get_data():
        user = db.users.find_one({"_id": current_user.user['_id']})
        current_user.user = user
        
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

    @staticmethod
    def add_liked_disliked(recipe_id, opinion):
        if opinion == 'like':
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$push": {"likes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.likes": 1}})
        else:
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$push": {"dislikes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.dislikes": 1}})
        
        User.get_data()

    @staticmethod
    def remove_liked_disliked(recipe_id, opinion):
        if opinion == 'like':
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$pull": {"likes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.likes": -1}})
        else:
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$pull": {"dislikes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.dislikes": -1}})
        
        User.get_data()
