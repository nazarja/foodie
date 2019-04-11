import re
import json
from app import db
from bson.objectid import ObjectId
from flask_login import current_user


class Recipe:

    @staticmethod
    def get_random():

        """
            Gets random recipes from the entire recipe collection for index page
        """

        cursor = [recipe for recipe in db.recipes.aggregate([{"$sample": {"size": 14}}])]

        #  Return values are 10 for the slideshow and 4 for the you may also like section
        return [cursor[10:], cursor[:10]]

    # ============================================ #

    @staticmethod
    def get_details(_id):

        """
            Finds a recipe by id and return the whole document
        """

        return db.recipes.find_one({"_id": ObjectId(_id)})

    # ============================================ #

    @staticmethod
    def get_by_category(category, data, sort, order, page, num):

        """
            Receives category details and pagination information,
            Queries the db for document count, random recipes and all category specific recipes.
        """

        count = db.recipes.count_documents({f"filters.{category}": data})
        grid = db.recipes.find({f"filters.{category}": data}).sort([(sort, order)]).skip((page - 1) * num).limit(num)
        slideshow = db.recipes.aggregate([{"$match": {f"filters.{category}": data}}, {"$sample": {"size": 10}}])

        return [[recipe for recipe in grid], [recipe for recipe in slideshow], count]

    # ============================================ #

    @staticmethod
    def add_comment(_id, comment):

        """
            Adds / Pushes a logged in users comments to both the specific recipe and the users profile arrays
        """

        db.recipes.find_one_and_update({"_id": ObjectId(_id)}, {"$push": {"users.comments": comment}})
        db.users.find_one_and_update({"_id": ObjectId(current_user.user['_id'])}, {"$push": {"comments": comment}})

    # ============================================ #

    @staticmethod
    def get_filtered_recipes(recipe_filters, options, search_term):

        """
            Serves as both search and filter recipes function. Receives a dictionary of options to be used
            as filters, sorting order, number of results to be sent back and a search term if provided.
        """

        filters = []
        sort = options['sort']
        order = int(options['order'])
        limit = int(options['limit'])

        # only create a filter category for options without the value 'all'
        for key, value in recipe_filters.items():
            if value != 'all':
                filters.append({f'filters.{key}': value})

        # find recipes with search term
        if search_term is not None:

            # alter search term for regex and keyword searches
            search_term_kw = search_term.replace(' ', '-')
            search_term_regex = search_term.replace(' ', '.')

            # if filters are passed down, add the filters to the query
            # check both keywords and recipe title
            if filters:
                cursor = db.recipes.find(
                    {"$or": [{"filters.kw": {"$in": [search_term_kw]}},
                             {"details.title": {"$regex": search_term_regex, "$options": "ig"}}], "$and": filters}
                ).sort([(sort, order)]).limit(limit)
            else:
                cursor = db.recipes.find(
                    {"$or": [{"filters.kw": {"$in": [search_term_kw]}},
                             {"details.title": {"$regex": search_term_regex, "$options": "ig"}}]}
                ).sort([(sort, order)]).limit(limit)

        # only filter recipes
        elif filters:
            cursor = db.recipes.find({"$and": filters}).sort([(sort, order)]).limit(limit)
        else:
            cursor = db.recipes.find({}).sort([(sort, order)]).limit(limit)

        # return the filtered recipes
        return [recipe for recipe in cursor]

    # ============================================ #

    @staticmethod
    def add_edit_recipe(recipe_id, data):

        """
            Creates or replaces a recipe in the database
        """

        # if the recipe is being edited, find it in the db
        if recipe_id != 'new':
            recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})

        # if its a new recipe, open and load the schema
        else:
            with open('app/data/schemas/recipe.json') as recipe_file:
                recipe = json.load(recipe_file)

        temp = []

        # assign form data to recipe dictionary
        recipe['details']['author'] = data['author']
        recipe['details']['title'] = data['title']
        recipe['details']['description'] = data['description']
        recipe['filters']['cuisine'] = data['cuisine']
        recipe['filters']['course'] = data['course']
        recipe['filters']['planning'] = data['planning']
        recipe['filters']['mood'] = data['mood']
        recipe['filters']['diet'] = data['diet']
        recipe['filters']['skill'] = data['skill']
        recipe['details']['serves'] = data['serves']
        recipe['details']['cook_time'] = data['cook-time']
        recipe['details']['prep_time'] = data['prep-time']
        recipe['filters']['kw'] = [x.strip() for x in data['keywords'].split(',')]
        recipe['methods'] = []
        recipe['instructions'] = []
        recipe['ingredients'] = []
        recipe['nutrition'] = [["kcal", ""], ["fat", ""], ["saturates", ""], ["carbs", ""], ["sugars", ""], ["fibre", ""]]
        del recipe['filters']['kw'][len(recipe['filters']['kw']) - 1]

        if recipe_id == 'new':
            recipe['image'] = [data['image-url']]
            recipe['filters']['ingred'] = [data['cuisine']]
        else:
            recipe['image'][0] = data['image-url']

        # to account for additional inputs being created for
        # instructions and ingredients - match the input name
        # make sure it is n0t empty and append the value
        for key, value in data.items():

            if re.match("instruction", key) and value is not '':
                recipe['methods'].append(value)

            if re.match("ingredient", key) and value is not '':
                recipe['ingredients'].append(value)

            if re.match("nutrition", key):
                temp.append(value)

        # assign nutrition values from temp list to recipe
        for index, value in enumerate(temp):
            recipe['nutrition'][index][1] = value

        # if its a new recipe, insert it
        if recipe_id == 'new':
            db.recipes.insert_one(recipe)

        # otherwise replace the current recipe
        else:
            db.recipes.replace_one({"_id": ObjectId(recipe_id)}, recipe, upsert=True)

        # Add recipe to users list of edited recipes
        Recipe.add_user_recipe(recipe)

        # Redirect to edited / created recipe page
        return [recipe['_id'], recipe['details']['title']]

    # ============================================ #

    @staticmethod
    def delete_recipe(recipe_id):

        """
            Deletes recipe from db, pulls recipe id from user arrays (comments, recipes) if any
        """

        db.recipes.delete_one({"_id": ObjectId(recipe_id)})
        db.users.update({}, {"$pull": {"recipes": ObjectId(recipe_id), "comments": {"_id": recipe_id}}})

    # ============================================ #

    @staticmethod
    def add_user_recipe(recipe):

        """
            Adds recipe to users edited recipe list, used add to set to prevent duplicates
        """

        db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$addToSet": {"recipes": recipe['_id']}})

    # ============================================ #

    @staticmethod
    def get_user_recipes():

        """
            Gets users edited recipes if any
        """

        user_recipes = []

        # put all item into a list of dictionaries for searching with $or
        for recipe_id in current_user.user['recipes']:
            user_recipes.append({"_id": recipe_id})

        # only search the db if there are recipes otherwise return an empty list
        return [recipe for recipe in db.recipes.find({"$or": user_recipes})] if user_recipes else []
