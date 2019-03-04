from random import sample
from app import app, db, ObjectId

class Recipe:


    def get_random_recipes():
        cursor = db.recipes.aggregate([{ "$sample": { "size": 10 } }])
        return [recipe for recipe in cursor]


    def get_recipe_details(id): 
        return db.recipes.find_one({"_id": ObjectId(id)})


    def get_recipes_by_category(category, data):
        cursor = db.recipes.find({ f"recipe_filters.{category}": data})
        recipes = [recipe for recipe in cursor]
        slideshow = sample(recipes, len(recipes)) if len(recipes) <= 10 else sample(recipes, 10) 
        return (recipes, slideshow)

