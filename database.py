from helpers import *
import sqlite3

DATABASE = './data/da.db'

def create_tables():
    """
    This function make sure that "article" and "raw_data" tables exists in da.db, and if don't, it creates them.
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS article 
        (
            id text primary key,
            title text, 
            url text not null, 
            img_url text, 
            article_date text, 
            source text, 
            engagement integer, 
            published integer default 0 
        )''')
    logging.info('article table created')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS raw_data 
        (
         raw_data text, 
         extraction_date text, 
         source text
         )''')
    logging.info('raw_data table created')

    # Save (commit) the changes
    con.commit()

    # Close the connection
    con.close()


def upsert(table, records):
    """
    This function upserts automatically on the selected table the values provided
    
    Input: 
        table: can be "article" or "raw_data"
        records: a list of tuples with the column values for each column corresponding with the table being inserted
    Output: the number of rows inserted to the table

    For table article, records (id text primary key, title text, url text, img_url text, article_date text, source text, engagement integer, published integer)
    For table raw_data, records raw_data (raw_data text, extraction_date text, source text)
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    if table == 'article':
        cur.executemany('INSERT INTO article VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (id) DO NOTHING;', records)
        upserted_rows = cur.rowcount
        logging.info(f'{upserted_rows} inserted records to article table')
    
    elif table == 'raw_data':
        cur.executemany('INSERT INTO raw_data VALUES(?,?,?);',records)
        upserted_rows = cur.rowcount
        logging.info(f'{upserted_rows} inserted records to raw_data table')
    
    con.commit()
    con.close()

    return upserted_rows


def update_db_published(id):
    """
    Input: id primary key of the article being published
    Action: published column of the corresponding record set to 1 meaning "this article has been published"
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    
    cur.execute(f'''UPDATE article SET published = 1 WHERE id = "{id}"''')
    logging.info(f'{id} article set to published')
    
    con.commit()
    con.close()

def retrieve_raw_data(source):
    """
    This function returns the selected source fresher data from the raw_data table
    Input: Source to be queried. Current possible values are: 'Feedly API'
    Output: The first row ordered by descending date as a list of one tuple, this tuple has the column values of raw_data table as elements
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    
    data = cur.execute(f"""SELECT * FROM raw_data WHERE source = '{source}' ORDER BY extraction_date DESC LIMIT 1""").fetchall()
    logging.info('Most recent api raw data retrieved from raw_data table')
    
    con.commit()
    con.close()

    return data

def retrieve_np_articles():
    """
    Input: None
    Output: A list of tuples being all the non-published articles, in descending order by the engagement columns
    """
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    
    data = cur.execute(f"""SELECT * FROM article WHERE published = 0 ORDER BY engagement DESC""").fetchall()
    logging.info('Non-published articles ordered by descending engagement retrieved from raw_data table')
    
    con.commit()
    con.close()

    return data