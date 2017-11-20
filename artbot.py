from io import BytesIO
from PIL import Image
from PIL import ImageFile

from evaluate import ffwd
import tweepy
import wget
import requests
import tweepy
from tweepy.streaming import StreamListener
from credentials import *
import random



ckpoints=["checkpoint/pretrained-networks/dora-marr-network",
       "checkpoint/pretrained-networks/rain-princess-network",
       "checkpoint/pretrained-networks/starry-night-network"]

def getstyled(data_in):
    paths_out="styled"
    checkpoint_dir=random.choice(ckpoints)
    ffwd(data_in, paths_out, checkpoint_dir, device_t='/cpu:0', batch_size=1)
    return paths_out

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



B="@shtaki_ke"

def tweet_image(url,sn,s):

    filename = 'output/temp.png'
    # send a get request
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        # read data from downloaded bytes and returns a PIL.Image.Image object
        i = Image.open(BytesIO(request.content))
        # Saves the image under the given filename
        i.save(filename)
        output = getstyled("output")
        m = "Here is your photo turned art"
        s = api.update_with_media(output,m, s.id)

	


class MyStreamListener(StreamListener):
    def on_status(self, s):
        sn = s.user.screen_name
        if 'media' in s.entities:
            for image in s.entities['media']:
                x=image['media_url']
                file=tweet_image(x,sn,s)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return  true


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@shtaki_ke'])
