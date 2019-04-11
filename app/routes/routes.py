import json
import re
from math import ceil
from app import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.forms import SignForm
from app.models.users import User
from app.models.recipes import Recipe
from app.models.graphs import Graphs



# ============================================ #



@app.context_processor
def inject_filters():

    """
        Make recipes filters / menu dictionary available to all jinja templates
    """

    with open('app/data/schemas/filters.json') as filters_file:
        menu_filters = json.load(filters_file)

        return dict(filters=menu_filters)


# ============================================ #


def slug_friendly(title):

    """
        Make recipe slug readable - remove non word chars
    """

    title = re.sub(r'\W', '_', title)
    return title.replace('___', '_')


# make function available as a custom filter to jinja
app.jinja_env.filters['resub'] = slug_friendly


# ============================================ #


# index
@app.route('/')
def index():
    recipes = Recipe.get_random()
    return render_template('index.html', recipes=recipes[0], slideshow=recipes[1])


# ============================================ #


# profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    # get users recipes
    recipes = Recipe.get_user_recipes()

    # get graphs
    likes_chart = Graphs.likes_chart()
    kcal_chart = Graphs.kcal_chart()

    return render_template('profile.html', recipes=recipes, likes_chart=likes_chart, kcal_chart=kcal_chart)


# ============================================ #


# update user favourites
@app.route('/update_favourites', methods=['POST'])
def update_favourites():

    # form value will be a boolean indicating a liked or disliked recipe
    if request.form['value'] == 'true':
        User.add_liked_disliked(request.form['_id'], request.form['opinion'])
    else: 
        User.remove_liked_disliked(request.form['_id'], request.form['opinion'])

    return 'Favourites Updated'


# ============================================ #


# categories
@app.route('/categories/<category>/<data>')
def categories(category, data):

    # set default arguments for page and sort order
    # if an argument cannot be found it must be the first page
    sort = request.args.get('sort') or 'users.likes'
    order = request.args.get('order') or -1
    page = request.args.get('page') or 1

    # get recipes data by category
    recipes = Recipe.get_by_category(category, data, sort, int(order), int(page), num=12)

    # pagination variables
    pages = ceil(recipes[2] / 12) + 1
    page = int(page)
    start = page
    end = pages

    # pagination logic
    if pages <= 5:
        start = 1
    else:
            if page <= 3:
                start = 1
                end = 6
            elif page > 3 and page < (pages - 2):
                start = page - 2
                end = page + 3
            else:
                start = pages - 5

    # render template
    return render_template(
        'categories.html', 
        category=category, 
        data=data, 
        sort=sort, 
        num=12,
        page=int(page), 
        pages=pages, 
        recipes=recipes[0], 
        slideshow=recipes[1], 
        count=recipes[2],
        start=start,
        end=end
    )


# ============================================ #


# recipe
@app.route('/recipe/<recipe>/<title>')
def recipe(recipe, title):

    # get a single recipe by its id
    recipe = Recipe.get_details(recipe)
    return render_template('recipe.html', recipe=recipe)


# ============================================ #


# editor
@app.route('/editor/<url>')
def editor(url):

    # get recipe details if recipe is to be edited otherwise its a new recipe
    recipe = Recipe.get_details(request.args.get('recipe')) if url == 'edit' else False    
    return render_template('editor.html', url=url, recipe=recipe)


# ============================================ #


# save recipe
@app.route('/save_recipe/<recipe_id>', methods=['POST'])
def save_recipe(recipe_id):

    # save form as a dict, add edited form, redirect to recipe page
    url = Recipe.add_edit_recipe(recipe_id, request.form.to_dict())
    return redirect(url_for('recipe', recipe=url[0], title=url[1]))


# ============================================ #


# delete recipe
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):

    # delete recipe by recipe id
    Recipe.delete_recipe(recipe_id)
    return redirect(url_for('index'))


# ============================================ #


# comment
@app.route('/comments', methods=['POST'])
def comment():

    if request.method == "POST":

        # create recipe dictionary from form data
        comment = {
                "_id": request.form['_id'],
                "title": request.form['title'],
                "username": request.form['username'], 
                "date": request.form['date'], 
                "reply": request.form['reply']
        }

        # add comment to recipe comments list
        Recipe.add_comment(request.form['_id'], comment)

    return "Comment Added"


# ============================================ #


# filters
@app.route('/filters', methods=['GET', 'POST'])
def filters():

    # create default sorting options
    recipe_filters = {}
    options = {'sort': 'users.likes', 'order': -1, 'limit': 12}

    # get search term if it exists
    search_term = request.args.get('search_term')

    if request.method == 'POST':
        recipe_filters = request.form.to_dict()

        if recipe_filters['limit']:
            sort_values = recipe_filters['sort'].split(',')
            options['sort'] = sort_values[0]
            options['order'] = sort_values[1]
            options['limit'] = recipe_filters['limit']
            del recipe_filters['sort']
            del recipe_filters['limit']

    # filter recipes and return results to the same page
    filtered_recipes = Recipe.get_filtered_recipes(recipe_filters, options=options, search_term=search_term)
    return render_template('filters.html', recipes=filtered_recipes, search_term=search_term, sort=options['sort'])


# ============================================ #


# search
@app.route('/search', methods=['POST'])
def search():

    # get search term and redirect to filters page
    search_term = request.form['search_term']
    return redirect(url_for('filters', search_term=search_term))


# ============================================ #


# sign in / out
@app.route('/sign/<url>', methods=['GET', 'POST'])
def sign(url):

    # dont allow logged in users to access page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # crete form with wtf_forms
    form = SignForm()

    # if validation is ok
    if form.validate_on_submit():

        # check if user exists
        user = db.users.find_one({"username": form.username.data})

        # if the user is signing in
        if url == 'in':

            # if all credentials match ok, login the user
            if user and User.check_password(user['password'], form.password.data):
                login_user(User(user['username']), remember=form.remember.data)
                return redirect(request.args.get("next") or url_for("profile"))

            # otherwise display error
            else:
                flash("Incorrect username or password.", category='sign-error')
                return redirect(url_for('sign', url=url))
        
        # if the user is signing up
        else:

            # if the user already exists, display error
            if user:
                flash("That username is already in use.", category='sign-error')
                return redirect(url_for('sign', url=url))

            # otherwise create a new user and log them in
            else:
                User.add_user(form.username.data, form.password.data)
                login_user(User(form.username.data), remember=form.remember.data)
                return redirect(request.args.get("next") or url_for("profile"))

    return render_template('sign.html', form=form, url=url)


# ============================================ #


# sign out
@app.route('/sign_out')
def sign_out():

    # Sign out the user with flask login manager
    logout_user()
    return redirect(url_for('sign', url='in'))



