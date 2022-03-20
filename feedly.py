import requests
from database import *
from helpers import *
from datetime import datetime
import json

headers = {
    'Authorization': 'OAuth ' + ACCESS_TOKEN_FEEDLY
}
api_call_get_all = "https://cloud.feedly.com/v3/streams/contents?streamId=user/{user_id}/category/global.all&unreadOnly=false".format(user_id = USER_ID) 
api_call_get_data_articles = "https://cloud.feedly.com/v3/streams/contents?streamId=user/{user_id}/category/{category}".format(user_id = USER_ID, category = DATA_ARTICLES_CATEGORY)

def get_articles(url, headers):
    """
    This function retrieves articles from Feedly app and writes them to a local json file. The purpose is to make available the data from the API anytime 
    without needing to query it again.
    
    Response JSON relevant fields:
        items->canonicalUrl
        items->title
        items->content 
        items->visual->url
        items->engagement
    """
    print()
    logging.info('Running get_articles to obtain new articles from the internet')
    res = requests.get(url, headers = headers)

    if res.status_code == requests.codes.ok:
        api_data = json.dumps(res.json())
        records = [(api_data,str(datetime.now()),"Feedly API")]
        upsert("raw_data",records)
        logging.info('Get articles function upserted into raw_data sucessfully')

    else:
        logging.error("Get articles function api call failed, response code: {r_code}".format(r_code = res.status_code))
        send_mail("Feedly API call failed: ", str(res.status_code))

#get_articles(api_call_get_data_articles, headers)