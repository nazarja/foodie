from app import app
from flask import render_template


# handle 404 error - page not found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html', error=error), 404


# handle 500 error - internal server error
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html', error=error), 500


