from app import app, db, ObjectId
from app.models.users import User
from flask_login import current_user

class Recipe:


    def get_random_recipes():
        grid = db.recipes.aggregate([{ "$sample": { "size": 4 }}])
        slideshow = db.recipes.aggregate([{ "$sample": { "size": 10 }}])
        return ([recipe for recipe in grid], [recipe for recipe in slideshow])


    def get_recipe_details(id): 
        return db.recipes.find_one({"_id": ObjectId(id)})


    def get_recipes_by_category(category, data, sort, order, page, num):
        count = db.recipes.count_documents({f"recipe_filters.{category}": data })
        grid = db.recipes.find({ f"recipe_filters.{category}": data }).sort([(sort, order)]).skip((page-1)*num).limit(num)
        slideshow = db.recipes.aggregate([{ "$match": { f"recipe_filters.{category}": data }},{ "$sample": { "size": 10 }}])
        return ([recipe for recipe in grid], [recipe for recipe in slideshow], count)

    def add_comment(id, comment):
        db.recipes.find_one_and_update({"_id": ObjectId(id)}, { "$push": { "users.comments": comment }})
        db.users.find_one_and_update({"_id": ObjectId(current_user.user['_id'])}, { "$push": { "comments": comment }})


        
        

