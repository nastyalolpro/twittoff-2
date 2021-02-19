"""Retrieve tweets and users then create embeddings and populate db"""
import os
from dotenv import load_dotenv
import tweepy
import spacy
from .models import DB, Tweet, User

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# nlp model
nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        # grabs user from the twitter db
        twitter_user = TWITTER.get_user(username)
        # adds user to our db, if its not yet there or updates it
        db_user = (User.query.get(twitter_user.id)) or User(
          id=twitter_user.id, name=username)
        DB.session.add(db_user)

        # grabs 200 tweets from the user
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode="extended"
        )

        # if user has tweets, adds newest tweet to the newest tweet column
        # in user table
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # vectorizes every user's tweet
            # and stores numerical representations in the tweet table
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    # if the format of the username is wrong or the user doesnt exists
    # raise an error
    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    # commits changes after try has completed
    else:
        DB.session.commit()


def update_all_users():
    """Update all Tweets for all users in the User table."""
    for user in User.query.all():
        add_or_update_user(user.name)
