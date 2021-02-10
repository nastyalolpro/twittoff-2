"""Main app/routing file for Twittoff
"""

from flask import Flask, render_template
from models import DB, User

def create_app():
    """Creating and configuring an instance 
    of the Flask application
    """
    app = Flask(__name__) # name of the current python module

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/') # adds a specific url to an associated function
    def root():
        users = User.query.all()
        # return f"Hello, {__name__}"
        return render_template("base.html", title="home", users=users)

    return app
