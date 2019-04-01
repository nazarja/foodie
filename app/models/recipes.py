import re
from app import db
from bson.objectid import ObjectId
from flask_login import current_user


class Recipe:

    @staticmethod
    def get_random():
        cursor = [recipe for recipe in db.recipes.aggregate([{"$sample": {"size": 14}}])]
        return [cursor[10:], cursor[:10]]

    @staticmethod
    def get_details(_id):
        return db.recipes.find_one({"_id": ObjectId(_id)})

    @staticmethod
    def get_by_category(category, data, sort, order, page, num):
        count = db.recipes.count_documents({f"filters.{category}": data})
        grid = db.recipes.find({f"filters.{category}": data}).sort([(sort, order)]).skip((page-1)*num).limit(num)
        slideshow = db.recipes.aggregate([{"$match": {f"filters.{category}": data}}, {"$sample": {"size": 10}}])
        return [[recipe for recipe in grid], [recipe for recipe in slideshow], count]

    @staticmethod
    def add_comment(_id, comment):
        db.recipes.find_one_and_update({"_id": ObjectId(_id)}, {"$push": {"users.comments": comment}})
        db.users.find_one_and_update({"_id": ObjectId(current_user.user['_id'])}, {"$push": {"comments": comment}})

    @staticmethod
    def get_filtered_recipes(recipe_filters, options, search_term):

        filters = []
        sort = options['sort']
        order = int(options['order'])
        limit = int(options['limit'])

        for key, value in recipe_filters.items():
            if  value != 'all':
               filters.append({ f'filters.{key}' : value})


        # find recipes with search term
        if search_term is not None:
            search_term_kw = search_term.replace(' ', '-')
            search_term_regex = search_term.replace(' ', '.')
            if filters:
                cursor = db.recipes.find({"$or": [ {"filters.kw": {"$in": [search_term_kw]}}, {"details.title": { "$regex":  search_term_regex, "$options": "i"}} ], "$and": filters}).sort([(sort, order)]).limit(limit)
            else:
                cursor = db.recipes.find({ "$or": [ {"filters.kw": {"$in": [search_term_kw]}}, {"details.title": { "$regex":  search_term_regex, "$options": "i"}} ]}).sort([(sort, order)]).limit(limit)
        
        # only filter recipes
        elif filters:
            cursor = db.recipes.find({ "$and": filters }).sort([(sort, order)]).limit(limit)
        else:
            cursor = db.recipes.find({}).sort([(sort, order)]).limit(limit)

        # the returned filtered recipes
        return [recipe for recipe in cursor]


        
        

