import re, json
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
                cursor = db.recipes.find(
                    {"$or": [ {"filters.kw": {"$in": [search_term_kw]}}, {"details.title": { "$regex":  search_term_regex, "$options": "ig"}} ], "$and": filters}
                    ).sort([(sort, order)]).limit(limit)
            else:
                cursor = db.recipes.find(
                    { "$or": [ {"filters.kw": {"$in": [search_term_kw]}}, {"details.title": { "$regex":  search_term_regex, "$options": "ig"}} ]}
                    ).sort([(sort, order)]).limit(limit)
                
        
        # only filter recipes
        elif filters:
            cursor = db.recipes.find({ "$and": filters }).sort([(sort, order)]).limit(limit)
        else:
            cursor = db.recipes.find({}).sort([(sort, order)]).limit(limit)

        # the returned filtered recipes
        return [recipe for recipe in cursor]


    @staticmethod
    def add_edit_recipe(recipe_id, data):

        if recipe_id != 'new':
            recipe = db.recipes.find_one({"_id": ObjectId(recipe_id)})
        else:    
            with open('app/data/schemas/recipe.json') as recipe_file:
                recipe = json.load(recipe_file)

        temp = []
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
        recipe['nutrition'] = [["kcal", ""],["fat", ""],["saturates", ""],["carbs", ""],["sugars", ""],["fibre", ""]]
        del recipe['filters']['kw'][len(recipe['filters']['kw']) - 1]
        
        if recipe_id == 'new':
            recipe['image'] = [data['image-url']]
            recipe['filters']['ingred'] = [data['cuisine']]
        else:
             recipe['image'][0] = data['image-url']

        for key, value in data.items():
           
            if re.match("instruction", key) and value is not '':
                recipe['methods'].append(value)

            if re.match("ingredient", key) and value is not '':
                recipe['ingredients'].append(value)

            if re.match("nutrition", key):
                temp.append(value)

        for index, value in enumerate(temp):
            recipe['nutrition'][index][1] = value

        if recipe_id == 'new':
            db.recipes.insert_one(recipe);
        else:
            db.recipes.replace_one({"_id": ObjectId(recipe_id)}, recipe, upsert=True)

        # Add recipe to users recipes
        Recipe.add_user_recipe(recipe)
        # Redirect to edited / created recipe page
        return (recipe['_id'], recipe['details']['title'])


    @staticmethod
    def delete_recipe(recipe_id):
        db.recipes.delete_one({"_id": ObjectId(recipe_id)})
        db.users.update({}, {"$pull": {"recipes": ObjectId(recipe_id), "comments": {"_id": recipe_id}}})


    @staticmethod
    def add_user_recipe(recipe):
        db.users.find_one_and_update({"_id": current_user.user['_id']}, {"$addToSet": {"recipes": recipe['_id']}})


    @staticmethod
    def get_user_recipes():
        user_recipes = []
        for recipe_id in current_user.user['recipes']:
            user_recipes.append({"_id": recipe_id})

        return [recipe for recipe in db.recipes.find({"$or": user_recipes})] if user_recipes else []
        
        
        
        

        
                

        

        
        

