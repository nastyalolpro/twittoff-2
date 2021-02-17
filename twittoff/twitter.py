"""Retrieve tweets and users then create embeddings and populate db"""
from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# nlp model
nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(
          id=twitter_user.id, name=username)
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode="extended"
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

        DB.session.commit()

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e
