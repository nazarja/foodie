from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign/<url>', methods=['GET', 'POST'])
def sign(url):
    return render_template('index.html')
