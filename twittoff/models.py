#! /Users/anastasialysenko/.local/share/virtualenvs/twittoff-2-prsQMhaN/bin/python
"""Database file. 
SQLAlchemy models and utility functions for Twittoff
"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy() # an instance of a database class

class User(DB.Model):
    """Twitter User Table thet will correspond to tweets - SQLAlchemy syntax
     
     Args:
        DB ([type]): [description]
    """
    id = DB.Column(DB.BigInteger, primary_key = True) # id column - primary key
    name = DB.Column(DB.String, nullable=False) # name column - string, not null

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Tweet(DB.Model):
    """Tweet text data associated with user table

    Args:
        DB ([type]): [description]
    """
    id = DB.Column(DB.BigInteger, primary_key=True) # id column - primary key
    text = DB.Column(DB.Unitcode(300)) 
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        "user.id"), nullable=False) # automatically  generated user  id, corresponds to the user id from the user table
    user = DB.relationship("user", backref=DB.backref("tweets", lazy=True)) # name of the user, <user>.tweets returns tweets from the user

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


# nick = User(id=1, name="Nick")
# nick
# <User: Nick>
