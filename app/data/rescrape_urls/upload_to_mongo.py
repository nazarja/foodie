from pymongo import MongoClient
from config.config import Config
import json

""" 
    This file takes the recipe database and transfers it to a mongodb collection.
    In addition a first user will be inserted to the user collection and filter
    keywords will be extracted from the database and stored in a filters collection
    for easy and quick queries and to be used to create menus and options.
"""

#  configure mongodb, during development ('localhost', 27017) was used
client = MongoClient(Config.MONGO_URI)

# database / collections
db = client.foodie
recipes = db.recipes

# ============================================ #


def add_recipes():

    """
        Add recipes to recipe collection
    """

    with open('json/newDB.json') as db_file:
        data = json.load(db_file)
        recipes.insert_many(data['recipes'])



# ============================================ #

add_recipes()
