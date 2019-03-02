import json
from app import app
from flask import render_template
from app.models.forms import SignForm


#================================================#


# make filters dict availible to all templates
@app.context_processor
def inject_filters():
    with open('app/data/schemas/filters.json') as filters_file:
        filters = json.load(filters_file)
        return dict(filters=filters)


#================================================#


# index
@app.route('/')
def index():
    return render_template('index.html')


#================================================#


# sign in / out
@app.route('/sign/<url>', methods=['GET', 'POST'])
def sign(url):

    form = SignForm()
    if form.validate_on_submit():
            pass

    return render_template('sign.html', form=form, url=url)


#================================================#


# sign out
@app.route('/signout')
def signout():
    return render_template('sign.html', url='in')
