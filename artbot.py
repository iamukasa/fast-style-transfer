
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
new_tweets = api.mentions_timeline(screen_name =B,count=200)

# list of specific strings we want to check for in Tweets


for s in new_tweets:

            sn = s.user.screen_name
            pic=s.media
            if pic !=0:
                output=getstyled(pic)
                m="Here is your photo turned art"
                s = api.update_with_media(output, s.id)



