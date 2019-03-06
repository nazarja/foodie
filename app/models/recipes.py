from random import sample
from app import app, db, ObjectId
from app.models.users import User
from flask_login import current_user

class Recipe:


    def get_random_recipes():
        cursor = db.recipes.aggregate([{ "$sample": { "size": 10 }}])
        return [recipe for recipe in cursor]


    def get_recipe_details(id): 
        return db.recipes.find_one({"_id": ObjectId(id)})


    def get_recipes_by_category(category, data, sort, order):
        cursor = db.recipes.find({ f"recipe_filters.{category}": data }).sort([(sort, order)]).limit(12)
        slideshow = db.recipes.aggregate([{ "$match": { f"recipe_filters.{category}": data }},{ "$sample": { "size": 10 }}])
        return ([recipe for recipe in cursor], [recipe for recipe in slideshow])

    def add_comment(id, comment):
        db.recipes.find_one_and_update({"_id": ObjectId(id)}, { "$push": { "users.comments": comment }})
        db.users.find_one_and_update({"_id": ObjectId(current_user.user['_id'])}, { "$push": { "comments": comment }})


        
        

