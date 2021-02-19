"""Main app/routing file for Twittoff"""
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users

load_dotenv()

def create_app():
    """Creating and configuring an instance 
    of the Flask application
    """
    app = Flask(__name__)  # name of the current python module

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')  # adds a specific url to an associated function
    def root():
        # DB.drop_all()
        # DB.create_all()
        # avoiding error since we are dropping all values - no duplicate users
        # insert_example_user()
        # return f"Hello, {__name__}"
        return render_template("base.html", title='Home', users=User.query.all())

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted(
            [request.values['user1'], request.values['user2']])

        if user0 == user1:
            message = "Can not compare users to themselves!"

        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = '{} is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction[0] == user1 else user0,
                user0 if prediction[0] == user1 else user1
            )

        return render_template('prediction_form.html', title="Prediction", message=message)

    @app.route('/user', methods=["POST"])  # http://127.0.0.1:5000/user
    # http://127.0.0.1:5000/user/<name>
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = "User {} was successfully added!".format(name)

            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/update')
    def update():
        update_all_users()
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/reset')
    def reset():
        # first we create the database
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", users=User.query.all(),
                               title='All Tweets updated!')

    return app
