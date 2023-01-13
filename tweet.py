from twitter import Twitter, OAuth
import json
import config
from prepare_tweet import create_tweet

with open("done.json") as f:
    done = json.load(f)

twitter = Twitter(auth=OAuth(config.access_key, config.access_secret,
                             config.consumer_key, config.consumer_secret))

query = twitter.statuses.mentions_timeline()


for tweet in query[::-1]:
    if tweet["id"] not in done:
        done.append(tweet["id"])
        user = tweet["user"]["screen_name"]

        tweet_this, data = create_tweet(tweet["text"], user)

        if tweet_this is not None:
            if data is None:
                results = twitter.statuses.update(
                    status=tweet_this, in_reply_to_status_id=tweet["id"])
            else:
                results = twitter.statuses.update_with_media(
                    status=tweet_this, media=data, in_reply_to_status_id=tweet["id"])
            print(tweet_this)

            break

with open("done.json", "w") as f:
    json.dump(done, f)
