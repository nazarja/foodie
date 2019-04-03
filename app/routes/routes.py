import json
import re
from math import ceil
from app import app, db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.forms import SignForm, EditorForm
from app.models.users import User
from app.models.recipes import Recipe


# ================================================ #
# ================================================ #


# make filters dict available to all templates
@app.context_processor
def inject_filters():
    with open('app/data/schemas/filters.json') as filters_file:
        menu_filters = json.load(filters_file)
        return dict(filters=menu_filters)


# ================================================ #
# ================================================ #


# Make recipe slug readable - remove non word chars
def slug_friendly(title):
    return re.sub(r'\W', '_', title)

app.jinja_env.filters['resub'] = slug_friendly


# ================================================ #
# ================================================ #


# index
@app.route('/')
def index():
    recipes = Recipe.get_random()
    return render_template('index.html', recipes=recipes[0], slideshow=recipes[1])


# ================================================ #
# ================================================ #


# profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


# ================================================ #
# ================================================ #


# search
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    return redirect(url_for('filters', search_term=search_term))


# ================================================ #
# ================================================ #


# filters
@app.route('/filters', methods=['GET', 'POST'])
def filters():
    
    recipe_filters = {}
    options = { 'sort': 'users.likes', 'order': -1, 'limit': 12}
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


    filtered_recipes = Recipe.get_filtered_recipes(recipe_filters, options=options, search_term=search_term)
    return render_template('filters.html', recipes=filtered_recipes, search_term=search_term, sort=options['sort'])


# ================================================ #
# ================================================ #

# categories
@app.route('/categories/<category>/<data>')
def categories(category, data):
    
    sort = request.args.get('sort') or 'users.likes'
    order = request.args.get('order') or -1
    page = request.args.get('page') or 1
    num = 12

    recipes = Recipe.get_by_category(category, data, sort, int(order), int(page), num=12)

    # pagination
    pages = ceil(recipes[2] / 12) + 1
    page = int(page)
    start = page
    end = pages

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


# ================================================ #
# ================================================ #


# recipe
@app.route('/recipe/<recipe>/<title>')
def recipe(recipe, title):
    recipe = Recipe.get_details(recipe)
    return render_template('recipe.html', recipe=recipe)


# ================================================ #
# ================================================ #


# comment
@app.route('/comments', methods=['POST'])
def comment():

    if request.method == "POST":
        comment = {
                "_id": request.form['_id'],
                "title": request.form['title'],
                "username": request.form['username'], 
                "date": request.form['date'], 
                "reply": request.form['reply']
        }
        Recipe.add_comment(request.form['_id'], comment)

    return "Comment Added"


# ================================================ #
# ================================================ #


# update user favourites
@app.route('/update_favourites', methods=['POST'])
def update_favourites():
    if request.form['value'] == 'true':
        User.add_liked_disliked(request.form['_id'], request.form['opinion'])
    else: 
        User.remove_liked_disliked(request.form['_id'], request.form['opinion'])
    return 'Favourites Updated'


# ================================================ #
# ================================================ #


# editor
@app.route('/editor/<url>')
def editor(url):
    recipe = Recipe.get_details(request.args.get('recipe'))
    if recipe:
        form = EditorForm(True, data=recipe)
    else:
        form = EditorForm(False, data=None)
    return render_template('editor.html', url=url, form=form)


# ================================================ #
# ================================================ #


# sign in / out
@app.route('/sign/<url>', methods=['GET', 'POST'])
def sign(url):

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignForm()
    if form.validate_on_submit():

        # check if user exists
        user = db.users.find_one({"username": form.username.data})

        # if the user is signing in
        if url == 'in':
            if user and User.check_password(user['password'], form.password.data):
                login_user(User(user['username']), remember=form.remember.data)
                return redirect(request.args.get("next") or url_for("profile"))
            else:
                flash("Incorrect username or password.", category='sign-error')
                return redirect(url_for('sign', url=url))
        
        # if the user is signing up
        else:
            if user:
                flash("That username is already in use.", category='sign-error')
                return redirect(url_for('sign', url=url))
            else:
                User.add_user(form.username.data, form.password.data)
                login_user(User(form.username.data), remember=form.remember.data)
                return redirect(request.args.get("next") or url_for("profile"))

    return render_template('sign.html', form=form, url=url)


# ================================================ #
# ================================================ #


# sign out
@app.route('/sign_out')
def sign_out():
    logout_user()    
    return redirect(url_for('sign', url='in'))


