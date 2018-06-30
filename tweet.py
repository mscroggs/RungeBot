from twitter import *
from random import choice
from datetime import datetime
import json

import config
import function_parser as fp
import interpolator as ip

with open("done.json") as f:
    done = json.load(f)

twitter = Twitter(auth=OAuth(config.access_key, config.access_secret,
                             config.consumer_key, config.consumer_secret))

query = twitter.statuses.mentions_timeline()

def get_function(tweet):
    tweet = "".join(tweet.split())
    if "f(x)=" in tweet:
        return tweet.split("f(x)=")[1]
    else:
        return "ERROR"

for tweet in query[::-1]:
    if tweet["id"] not in done:
        function = get_function(tweet["text"])
        done.append(tweet["id"])
        user = tweet["user"]["screen_name"]
        try:
            f = fp.parse(function)
            data, rating, n = ip.interpolate_and_rate(f)
        except TypeError:
            tweet_this = ".@"+user+" I couldn't understand your function. Sorry."
            results = twitter.statuses.update(status=tweet_this, in_reply_to_status_id=tweet["id"])
            break

        tweet_this = ".@"+user+" Here's your function interpolated using "
        tweet_this+= str(n)+" equally spaced points (blue) and "
        tweet_this+= str(n)+" Chebyshev points (red). "
        tweet_this+= "For your function, Runge's phenomenon is "+rating+"."

        results = twitter.statuses.update_with_media(status=tweet_this, media=data, in_reply_to_status_id=tweet["id"])
        break

with open("done.json","w") as f:
    json.dump(done,f)

