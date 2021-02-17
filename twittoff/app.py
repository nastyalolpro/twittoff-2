"""Main app/routing file for Twittoff
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User, insert_example_user


def create_app():
    """Creating and configuring an instance 
    of the Flask application
    """
    app = Flask(__name__)  # name of the current python module

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/', methods=['GET'])  # adds a specific url to an associated function
    def root():
        # avoiding error since we are dropping all values - no duplicate users
        insert_example_user()
        # return f"Hello, {__name__}"
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        insert_example_user()
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/reset')
    def reset():
        # first we create the database
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Home")

    @app.route('/compare', methods=['POST'])
    def compare():
        user1 = request.values['user1']
        user2 = request.values['user2']

    return app
