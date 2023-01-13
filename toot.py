from mastodon import Mastodon
import json

import function_parser as fp
import interpolator as ip

with open("mdone.json") as f:
    done = json.load(f)

mdon = Mastodon(
    access_token="mdon.secret", api_base_url="https://mathstodon.xyz")


def get_function(toot):
    toot = "".join(toot.split())
    if "f(x)=" in toot:
        return toot.split("f(x)=")[1].split("</p>")[0]
    else:
        return None


for toot in mdon.notifications():
    if toot["type"] == "mention" and toot["status"]["id"] not in done:
        done.append(toot["status"]["id"])
        user = toot["account"]["acct"]

        tweet_this, data = create_tweet(toot["status"]["content"], user, fname="toot_me")
        if tweet_this is not None:
            if data is None:
                mdon.status_post(toot_this, in_reply_to_id=toot["status"]["id"])
            else:
                img = mdon.media_post("toot_me.png")
                results = mdon.status_post(
                    status=toot_this, media_ids=img, in_reply_to_id=toot["status"]["id"])
            print(toot_this)
            break

with open("mdone.json", "w") as f:
    json.dump(done, f)
