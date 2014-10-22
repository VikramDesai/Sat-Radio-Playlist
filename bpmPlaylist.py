'''
Created on Mar 24, 2014

@author: Vikram
'''
import ConfigParser
import twitter
from twitter import TwitterError
import urllib2
import time
import sqlite3
import youtubeSearch

MAX_TWEETS = 3200
TWEETS_PER_QUERY = 200


sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name1 = 'my_table_1'  # name of the table to be created
table_name2 = 'my_table_2'  # name of the table to be created
new_field = 'my_1st_column' # name of the column
field_type = 'INTEGER'  # column data type

config = ConfigParser.RawConfigParser()
CONFIG_FILE = 'settings.cfg'

def write_to_config_file(config):
    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)
        
def get_twitter_api(config):
    
    api = twitter.Api(
        consumer_key = config.get('twitter', 'consumer_key'),
        consumer_secret = config.get('twitter', 'consumer_secret'),
        access_token_key = config.get('twitter', 'access_token_key'),
        access_token_secret = config.get('twitter', 'access_token_secret'))
    return api
   
    
def read_tweets(api, user, since_id):
    """ reads user's tweets
    """
    # fetch next 200 tweets starting the tracker id, updated in each iteration
    max_id = None
    
    print "Reading Tweets"

    # list of 'Status' objects to be populated
    statuses = []

    while True:
        new_statuses = []
        try:
            new_statuses = api.GetUserTimeline(screen_name=user,
                count=TWEETS_PER_QUERY, include_rts=False, max_id=max_id)
                
          
        except (TwitterError, urllib2.HTTPError) as e:
            print e
        
            
        if len(new_statuses) > 0:
            statuses.extend(new_statuses)
            max_id = new_statuses[-1].id - 1
            
        else:
            break
        
    print "Fetched", len(statuses), "tweets."
    return statuses

    

def main():
    """ read config file
        read tweets
    """
    last_successful_status_id = None
    config.read(CONFIG_FILE)
    
    twitter_api = get_twitter_api(config)
    twitter_handle = config.get('twitter', 'user_handle')
    for i in range(1):
        since_id = config.getint('twitter', 'since_id')
        statuses = read_tweets(twitter_api, twitter_handle, since_id )
        myDict = { }

        for status in statuses:
                last_successful_status_id = status.id
                myStr = status.text
                
                print myStr
                index = myStr.find("playing on #BPM")
                parsedStr = myStr[ : index]
                index = parsedStr.find("-")
                myDict[parsedStr[: index]] = parsedStr[ index + 1 : ]
                
        if last_successful_status_id:
            config.set('twitter', 'since_id', last_successful_status_id)
            write_to_config_file(config)
            
        conn = None
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        
        c.execute("DROP TABLE IF EXISTS my_table_1")
        c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name1, nf=new_field, ft=field_type))
        
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name1, cn='my_2nd_column', ct='TEXT'))
        
        id = 0        
        for key in myDict: 
            myKey = key.encode('ascii', 'ignore')
            myVal = myDict[key].encode('ascii', 'ignore')
            index = myKey.find("/")
            id = id+1
            if index:
                myKey = myKey.replace("/", "   ")
            index = myKey.find("&amp;")
            if index:
                myKey = myKey.replace("&amp;", "&")
            myStr = myKey + ", " + myVal + '\n'
            print myStr
            try:
                c.execute("INSERT INTO my_table_1 VALUES (?, ?);",(id, myStr))
            except sqlite3.IntegrityError:
                print('ERROR: ID already exists in PRIMARY KEY column {}'.format('my_1st_column'))    
         
        conn.commit()
        conn.close()  
        time.sleep(10)
        i = i+1
        
        youtubeSearch.gen_playlist()



if __name__ == '__main__':
    main()
