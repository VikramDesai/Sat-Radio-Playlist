# Sat-Radio-Playlist #
==================
https://github.com/VikramDesai/Sat-Radio-Playlist/edit/master/README.md#

Most times when a track is played on the Sat radio, its hard to store the names of the track. Its totally not advised to shazam the track while driving. I realized the station tweets their tracklist, voila I can get home and run this script to get the tracks played that day. You can search and create a playlist on youtube and take these tracks on the go.


# What do I need to do?

Download the app (has a python file and a config file).

Add your twitter credentials to the settings.cfg file.

Add the youtube playlist name to the settings.cfg file

python bpmPlaylist.py

# Twitter part

Setup your Twitter developer account, get the credentials and put them in the config file.

Here's what you'll do:

    1.Sign in to dev.twitter.com with your user ID.
    2.Go to My applications > Create a new Application
    3.a name, description, website (can be anything). Leave the callback URL blank. Agree to the rules, enter the CAPTCHA and create the application.
    4.Scroll down to the bottom and create the access tokens.
    5.Copy the Consumer key, secret, Access token and secret into settings.cfg.
    6.Enter your Twitter user handle against the user_handle key.
    7.Leave since_id as is. The script will use it to track progress.

# Youtube Part

Please refer to https://developers.google.com/youtube/registering_an_application

#  A few playlists created using Sat-Radio-Playlist

https://www.youtube.com/playlist?list=PLgueaXiOUeaovDdb_osKcQxqo36b1L-mc

https://www.youtube.com/playlist?list=PLgueaXiOUeaqnpoC44WTfVEMxcpo8WaMW
