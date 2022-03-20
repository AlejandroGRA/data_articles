import tweepy
from database import *
from helpers import *
from articles_handler import article_choicer

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def tweet():
    """
    This function takes an article tuple and publish it on Twitter.
    Please refer to related documentation: https://docs.tweepy.org/en/latest/api.html?highlight=update#API.update_status

    Input: An article with its values in a tuple as saved in the database
    Output: True if the tweet has been published, False and Exception object if not
    """

    best_article = article_choicer()

    # Create API object
    api = tweepy.API(auth) # auth works because is global in this file

    # Retrieve values
    id = best_article[0]
    title = best_article[1]
    url = best_article[2]

    # Create a tweet
    try:
        logging.info(f"Trying to tweet article {id}, {title}")
        api.update_status(status = title + "\n\n" + url + "\n\n #dataengineering #datascience #data #programming #tech")
        update_db_published(id)
        return True
        
    except Exception as e: 
        logging.error(e)
        send_mail("Tweet posting failed",str(e))
        return False, e