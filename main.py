from feedly import *
from articles_handler import *
from tweet import *
from database import *
from helpers import *
import schedule
import time

def main():

    logging.info('Running main.py')

    # Create tables if not exists
    create_tables()
    logging.info('Tables created')

    # Get the articles from api
    schedule.every().day.at("07:00").do(get_articles,api_call_get_data_articles, headers)
    schedule.every().day.at("17:00").do(get_articles,api_call_get_data_articles, headers)
    
    # Read the json file and return a processed list of articles
    schedule.every().day.at("07:15").do(feedly_processer)
    schedule.every().day.at("17:15").do(feedly_processer)
    
    # Select an article from the list and publish the article in Twitter
    schedule.every().day.at("08:37").do(tweet)
    schedule.every().day.at("18:07").do(tweet)
    logging.info('Jobs scheduled')

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()