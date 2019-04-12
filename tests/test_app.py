import os
import re
import unittest
from app import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_login import current_user

"""
    Resources: 
        https://rallion.bitbucket.io/explorations/flask_tutorial/api/flask.Response.html
        https://docs.python.org/3/library/unittest.html
"""

#================================#

# config
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY_SK'
app.config["WTF_CSRF_ENABLED"] = False
app.config['TESTING'] = True


#================================#


# configure mongo
client = MongoClient('localhost', 27017)

# database / collections
db = client.foodie
recipes = db.recipes
users = db.users
filters = db.filters


# ================================ #


class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        
        """ 
            Assign client
        """
        
        self.client = app.test_client()

    # ============== #

    def test_routes(self):

        """ 
            Test a couple of routes to make sure ok and redirect function correctly
        """
        
        # ok
        response = self.client.get('/')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'Create & Store your own Delicious Food and Drink Recipes!' in data

        # filters
        response = self.client.get('/filters')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'Filter All Recipes' in data
        
        # categories
        response = self.client.get('/categories/cuisine/chinese')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'Featured Chinese Recipes' in data

        # recipe
        response = self.client.get('/recipe/5caf8126cf37084fba86ac86/All_American_T_bone')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'All-American T-Bone' in data 

        # pagination
        response = self.client.get('/categories/cuisine/greek?page=2&sort=users.likes')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'All Greek Recipes' in data 
   
        # sign in
        response = self.client.get('/sign/in')
        assert response.status_code == 200
        
        # sign up
        response = self.client.get('/sign/up')
        assert response.status_code == 200

        # redirect - sign out
        response = self.client.get('/sign_out')
        assert response.status_code == 302

        # redirect
        response = self.client.get('/profile')
        assert response.status_code == 302

        # 404
        response = self.client.get('/unknown')
        assert response.status_code == 404

    # ============== #

    def test_filters(self): 

        """
            test post filters page with pre-selected options sent as dictionary
        """

        response = self.client.post('/filters', data=dict(sort='users.likes,-1', limit='12', cuisine='american', course='dinner', planning='all', mood='all', diet='all', skill='all'), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'Buffalo Chicken' in data

    # ============== #

    def test_search(self): 

        """
            test search page with search term sent as dictionary
        """

        response = self.client.post('/search', data=dict(search_term='chicken'), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'Spicy Moroccan Rice' in data

    # ============== #

    def test_search_and_filter(self): 

        """
            test searching and filtering together with pre-selected options sent as dictionary and search_term passed as query to url
        """

        response = self.client.post('/filters?search_term=chicken', data=dict(sort='users.likes,-1', limit='12', cuisine='indian', course='dinner', planning='all', mood='all', diet='all', skill='all'), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'Creamy Masala Chicken' in data

    # ============== #

    def test_failed_login(self):

        """
            test incorrect username entered
        """

        response = self.client.post('/sign/in', data=dict(username='sean', password='wrong_password', remember=False), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'Incorrect username or password.' in data

    # ============== #

    def test_failed_sign_up(self):

        """
            test existing username entered, test short username entered
        """

        response = self.client.post('/sign/up', data=dict(username='sean', password='wrong_password', remember=False), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'That username is already in use' in data

        response = self.client.post('/sign/up', data=dict(username='s', password='wrong_password', remember=False), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'username must be longer than 4 characters' in data

    # ============== #

    def test_successful_login(self):

        """
            test correct username/password entered, will redirect to profile page
        """

        response = self.client.post('/sign/in', data=dict(username='sean', password='password', remember=False), follow_redirects=True)
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert 'Welcome, Sean' in data
        sign_out = self.client.get('/sign/out')
       

    # ============== #

    def test_successful_sign_up(self):

      """
          test non-existing username/password entered, will redirect to profile page,
          check mongodb for new user
      """

        response = self.client.post('/sign/up', data=dict(username='paul',password='password',remember=False), follow_redirects=True)
        data = response.data.decode('utf-8')
        found_user = db.users.find_one({'username': 'paul'})
        assert found_user is not None
        delete_user = db.users.delete_one({'username': 'paul'})


    # ============== #

    def tearDown(self):
        sign_out = self.client.get('/sign/out')

# ================================ #

class TestAppDataBase(unittest.TestCase):

    def setUp(self):
        """
            Assign test client and log in
        """
        
        self.client = app.test_client()
        self.client.post('/sign/in', data=dict(username='sean',password='password',remember=False))
    
    # ============== #


    def  test_add_a_comment(self):
        
        """
            Test adding a comment to a recipe
        """

        response = self.client.post('/comments', data=dict(_id='5caf8126cf37084fba86ac75', title='Buffalo_chicken', username='sean', date='4/12/2019, 4:58:38 PM', reply='This is a comment'))
        clist = db.recipes.find_one({'_id':ObjectId('5caf8126cf37084fba86ac75')})
        comments = [c for c in clist['users']['comments']]
        is_there = False
        for item in comments:
            if '5caf8126cf37084fba86ac75' == item['_id']:
                is_there = True

        assert is_there is True
        

    # ============== #

    def  test_like_a_recipe(self):
        
        """
            Test adding a like to a recipe, recipe integer will increase
        """
        
        recipe = db.recipes.find_one({'_id':ObjectId('5caf8126cf37084fba86ac75')})
        likes_before = recipe['users']['likes']
        response = self.client.post('/update_favourites', data=dict(_id='5caf8126cf37084fba86ac75', opinion='like', value='true'))
        recipe = db.recipes.find_one({'_id':ObjectId('5caf8126cf37084fba86ac75')})
        likes_after = recipe['users']['likes']
        assert likes_after - likes_before == 1

    # ============== #

    def  test_dislike_a_recipe(self):

        """
             Test adding a dislike to a recipe, recipe integer will increase
        """

        recipe = db.recipes.find_one({'_id':ObjectId('5caf8126cf37084fba86ac75')})
        likes_before = recipe['users']['dislikes']
        response = self.client.post('/update_favourites', data=dict(_id='5caf8126cf37084fba86ac75', opinion='dislike', value='true'))
        recipe = db.recipes.find_one({'_id':ObjectId('5caf8126cf37084fba86ac75')})
        likes_after = recipe['users']['dislikes']
        assert likes_before + 1 == likes_after
        
    # ============== #

    def  test_edit_a_recipe(self):
        
        """
            Test editing a recipe and check it has been updated in the db
        """
        
        response = self.client.post('/save_recipe/5cb0c999cf37083a8226f1ae', data={'author': 'David', 'title': 'title', 'description': 'description', 'image-url': 'http://tinyurl.com/y43mkb4h', 'cuisine': 'american', 'course': '', 'planning': '', 'mood': '', 'diet': '', 'skill': '', 'serves': 'Serves: 20', 'cook-time': 'Cook: 20', 'prep-time': 'Prep: 20', 'instruction-1': 'instruction 1', 'instruction-2': 'instruction 2', 'ingredient-1': 'ingredients1', 'ingredient-2': 'ingredients2', 'ingredient-3': '', 'ingredient-4': '', 'keywords': 'keyword1, keyword2', 'nutrition-1': '0', 'nutrition-2': '0', 'nutrition-3': '0', 'nutrition-4': '0', 'nutrition-5': '0', 'nutrition-6': '0'})
        data = response.data.decode('utf-8')

        # get id from retured url
        _id = re.findall('\w{24}', data)[0]
        is_created = db.recipes.find_one({'_id': ObjectId(_id)})
        assert is_created['details']['author'] == 'David'

    # ============== #

    def  test_create_a_recipe(self):
        
        """
            Test creating a recipe and check it exists in db after creation
        """
       
        response = self.client.post('/save_recipe/new', data={'author': 'Sean', 'title': 'title', 'description': 'description', 'image-url': 'http://tinyurl.com/y43mkb4h', 'cuisine': 'american', 'course': '', 'planning': '', 'mood': '', 'diet': '', 'skill': '', 'serves': 'Serves: 20', 'cook-time': 'Cook: 20', 'prep-time': 'Prep: 20', 'instruction-1': 'instruction 1', 'instruction-2': 'instruction 2', 'ingredient-1': 'ingredients1', 'ingredient-2': 'ingredients2', 'ingredient-3': '', 'ingredient-4': '', 'keywords': 'keyword1, keyword2', 'nutrition-1': '0', 'nutrition-2': '0', 'nutrition-3': '0', 'nutrition-4': '0', 'nutrition-5': '0', 'nutrition-6': '0'})
        data = response.data.decode('utf-8')

        # get id from retured url
        _id = re.findall('\w{24}', data)[0]
        is_created = db.recipes.find_one({'_id': ObjectId(_id)})
        assert is_created is not None

    # ============== #

    def  test_delete_a_recipe(self):
        
        """
            Test delete a recipe from the db, it should not exist after deletion
        
        """

        response = self.client.get('/delete_recipe/5caf8126cf37084fba86ac75')
        recipe = db.recipes.find_one({'_id': ObjectId('5caf8126cf37084fba86ac75')})
        assert recipe is None

    ============== #

    def tearDown(self):
        sign_out = self.client.get('/sign/out')
# ================================ #


# run tests
if __name__ == '__main__':
    unittest.main()