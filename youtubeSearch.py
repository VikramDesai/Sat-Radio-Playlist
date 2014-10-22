from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import ConfigParser
import codecs
import os
import sys

import httplib2
import sqlite3
from bpmPlaylist import sqlite_file

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

sqlite_file = 'my_first_db.sqlite'  # name of the sqlite database file
table_name = 'my_table_1'  # name of the table to be queried

config = ConfigParser.RawConfigParser()
CONFIG_FILE = 'settings.cfg'

config.read(CONFIG_FILE)

DEVELOPER_KEY = config.get('youtube', 'developer_key')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"

CLIENT_SECRETS_FILE = "client_secrets.json"
# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://cloud.google.com/console

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))


vidId = []

def write_to_config_file(config):
    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)

def add_video_to_playlist(videoID, playlistID):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    
    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)
        
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))
    add_video_request = youtube.playlistItems().insert(
      part="snippet",
      body={
            'snippet': {
              'playlistId': playlistID,
              'resourceId': {
                      'kind': 'youtube#video',
                      'videoId': videoID
                }
            # 'position': 0
            }
    }
     ).execute()
    
def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    
    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)
        
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))

    
def youtube_playlist(playlistName):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()
    
    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)
        
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))
    playlists_insert_response = youtube.playlists().insert(part="snippet,status",body=dict(snippet=dict(title=playlistName,
                                                            description="BPM Playlist"),
                                                            status=dict(privacyStatus="public"))).execute()
    
    if playlists_insert_response["id"]:
        config.set('youtube', 'playlist_id', playlists_insert_response["id"])
        write_to_config_file(config)
                                                                                                


    
  
def youtube_search(line):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=line,
    part="id,snippet",
    maxResults=1
  ).execute()

  videos = []
  

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
      videoId = search_result["id"]["videoId"] + "\n"
      vidId.append(videoId)
      
      
      
      
      
def gen_playlist():
    
    config.set('youtube', 'playlist_id',"")
    write_to_config_file(config)   
  
    try:
        youtube = get_authenticated_service()
        playlist_name = config.get('youtube', 'playlist_name')
        youtube_playlist(playlist_name)
        print "Playlist Created"
        playlist_id = config.get('youtube', 'playlist_id')
        playlist_id = playlist_id.rstrip()      
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)    
               
    conn = sqlite3.connect(sqlite_file)
    
    cursor = conn.execute("SELECT my_2nd_column from my_table_1")
    for row in cursor:
        print row[0]
        try:
            youtube_search(row[0])
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    conn.close()
    
    youtube = get_authenticated_service()
    for line in vidId:
        line = line.rstrip()
        # line = line.rsplit('.',1)[1]
        # line = line.rstrip()
        print line
        try:
            add_video_to_playlist(line, playlist_id)
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content) 
      
        
    
 



if __name__ == "__main__":
    main()
