from app import app, db, ObjectId

class Recipe:


    def get_random_recipes(category='all', data='all'):
        cursor = db.recipes.aggregate([{ "$sample": { "size": 10 } }])
        return [recipe for recipe in cursor]

    def get_recipe_details(id): 
        return db.recipes.find_one({"_id": id})