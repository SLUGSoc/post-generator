import tweepy
import os


def init_tweepy():
    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    return tweepy.API(auth)


def update_status(api, content):
    try:
        api.update_status(content)
    except tweepy.error.TweepError as e:
        if e.api_code == 187:
            print('Duplicate tweet.')
        else:
            raise e
