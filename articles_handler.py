import json
from database import *
import hashlib
from urllib.parse import urlparse

def feedly_processer():
    """
    This function reads the raw json file from the Feedly API get call and retrieves the following data for each article:
    title, url, content, image_url and engagement.
    The data is upserted in the articles table.
    """
    logging.info('Running feedly_processer')
    new_articles_list = []

    # One [0] to access the tuple inside the list returned by retrieve_raw_data function, 
    # and another to retrieve the first element of the tuple, which is the json file
    raw_data = retrieve_raw_data('Feedly API')[0]
    raw_json = raw_data[0]
    raw_articles_json = json.loads(raw_json)

    # Get values from json
    for item in raw_articles_json['items']:

        # Title
        title = str(item['title'])

        # URL
        try:
            url = str(item['canonicalUrl'])
        except:
            try:
                url = str(item['originId'])
            except:
                try:
                    url = str(item['alternate']['href'])
                except:
                    url = None

        # Image URL
        try: 
            img_url = str(item['visual']['url'])
        except:
            img_url = None

        # Engagement value
        try: 
            engagement = item['engagement'] 
        except:
            engagement = 0

        # Published 
        published = 0

        # Get the id
        id_pre_hash = ''.join(filter(None, (title, url)))
        id = hashlib.md5(id_pre_hash.encode("utf8")).hexdigest()
        
        # Article date, it is actually the date when the raw_data was retrieved (i.e. when the API was called)
        article_date = raw_data[1]
        
        # Source
        if url:
            source = urlparse(url).netloc
        else:
            source = None

        # Build the tuple with the values
        article_tuple = (id, title, url, img_url, article_date, source, engagement, published)

        new_articles_list.append(article_tuple)
    
    # Upsert articles to database
    upsert("article",new_articles_list)


def article_choicer():
    """
    Input: None
    Output: A tuple with the top article retrieved from retrieve_np_articles function, which filter the non-published and orders them by
    engagement.
    """
    best_article = retrieve_np_articles()[0]
    best_article_id = best_article[0]
    best_article_title = best_article[1]
    logging.info(f'Best article selected: {best_article_id}, {best_article_title}')
    
    return best_article