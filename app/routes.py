from app import app
from flask import render_template


@app.context_processor
def inject_filters():
    with open('app/data/schemas/filters.json') as filters_file:
        filters = json.load(filters_file)
        return dict(filters=filters)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign/<url>', methods=['GET', 'POST'])
def sign(url):
    return render_template('index.html')
