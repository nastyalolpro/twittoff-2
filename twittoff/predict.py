"""Prediction of users based on the twitter embeddings"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, tweet_text):
    """"Predicts user based on the hypothetical tweet text

    return: 0 or 1 label, where 0 is user0_name, 1 - user1_name
    """
    # find usernames in the database
    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    # find their tweets
    embeddings = []
    labels = []
    for tweet in user0.tweets:
        embeddings.append(tweet.vect)
        labels.append(user0.name)
    for tweet in user1.tweets:
        embeddings.append(tweet.vect)
        labels.append(user1.name)

    # make a vector out of tweet_text
    tweet_text_vect = vectorize_tweet(tweet_text)

    # train model
    # TODO: let user choose a model to train
    classifier = LogisticRegression()
    classifier.fit(embeddings, labels)

    return classifier.predict([tweet_text_vect])

