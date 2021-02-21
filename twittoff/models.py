#! /Users/anastasialysenko/.local/share/virtualenvs/twittoff-2-prsQMhaN/bin/python
"""Database file. 
SQLAlchemy models and utility functions for Twittoff
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from .twitter import add_or_update_user

DB = SQLAlchemy()  # an instance of a database class
migrate = Migrate()


class User(DB.Model):
    """Twitter User Table that will correspond to tweets - SQLAlchemy syntax
     
     Args:
        DB ([type]): [description]
    """
    # __tablename__ = 'user'

    id = DB.Column(DB.BigInteger, primary_key=True)  # id column - primary key
    name = DB.Column(DB.String, nullable=False)  # name column - string, not null
    newest_tweet_id = DB.Column(DB.BigInteger)  # keeps track of recent user tweet

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Tweet(DB.Model):
    """Tweet text data associated with user table

    Args:
        DB ([type]): [description]
    """
    # __tablename__ = 'tweet'

    id = DB.Column(DB.BigInteger, primary_key=True)  # id column - primary key
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)  # pickle type stores numpy array
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False)  # automatically  generated user  id, corresponds to the user id from the user table
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))  # name of the user, <user>.tweets returns
    # tweets from the user

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)

# def insert_example_user():
#     """We will get an error if we run this twice without dropping and creating"""
#     user1 = add_or_update_user("elonmusk")



