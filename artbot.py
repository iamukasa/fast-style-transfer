
from evaluate import ffwd
import tweepy

import tweepy
from tweepy.streaming import StreamListener
from credentials import *

def getstyled(data_in):
    paths_out="generated/img1.jpg"
    checkpoint_dir="checkpoints"
    ffwd(data_in, paths_out, checkpoint_dir, device_t='/gpu:0', batch_size=4)
    return paths_out

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



B="@shtaki_ke"

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, s):
        sn = s.user.screen_name
        pic = s.media

        if 'media' in s.entities:
            for image in s.entities['media']:
                output = getstyled(image['media_url'])
                m = "Here is your photo turned art"
                s = api.update_with_media(output,m, s.id)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener())
myStream.filter(track=[B])