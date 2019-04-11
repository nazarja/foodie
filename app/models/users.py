import json
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user
from bson.objectid import ObjectId


# user loader
@login.user_loader
def load_user(username):

    """
        Allow flask login the handle loading and remembering the user
    """

    # search for an existing user
    user = db.users.find_one({"username": username})

    if not user:
        return None

    # Call the User class with the username
    return User(user['username'], user)

# ============================================ #


# user login class
class User:

    # methods for flask login
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

    # ============================================ #

    @staticmethod
    def get_data():

        """
            When the users profile has changed, update the current users to match
        """

        user = db.users.find_one({"_id": current_user.user['_id']})
        current_user.user = user

    # ============================================ #
        
    @staticmethod
    def check_password(password_hash, password):

        """
            Returns boolean of passwords matching on login
        """

        return check_password_hash(password_hash, password)

    # ============================================ #

    @staticmethod
    def add_user(username, password):

        """
            Adds a new user to the db when signing up
        """

        with open('app/data/schemas/user.json') as users_file:
            user = json.load(users_file)
            user['username'] = username.lower()
            user['password'] = generate_password_hash(password)
            db.users.insert_one(user)

    # ============================================ #

    @staticmethod
    def add_liked_disliked(recipe_id, opinion):

        """
            Updates the users profile with the recipe_id of a liked recipe
            Updates the recipes likes
        """

        if opinion == 'like':
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$push": {"likes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.likes": 1}})
        else:
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$push": {"dislikes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.dislikes": 1}})

        # update user
        User.get_data()

    # ============================================ #

    @staticmethod
    def remove_liked_disliked(recipe_id, opinion):

        """
            Updates the users profile with the recipe_id of a disliked recipe
            Updates the recipes dislikes
        """

        if opinion == 'like':
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$pull": {"likes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.likes": -1}})
        else:
            db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$pull": {"dislikes": recipe_id}})
            db.recipes.find_one_and_update({"_id": ObjectId(recipe_id)}, {"$inc": {"users.dislikes": -1}})

        # update user
        User.get_data()

