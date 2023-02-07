from mastodon import Mastodon
import sys
from prepare_tweet import create_tweet
from datetime import datetime, timedelta, timezone

test = "test" in sys.argv
cutoff = datetime.now(timezone(offset=timedelta())) - timedelta(days=1)

mdon = Mastodon(
    access_token="mdon.secret", api_base_url="https://mathstodon.xyz")


def replied(id):
    for d in mdon.status_context(id)["descendants"]:
        if "account" in d and "username" in d["account"] and d["account"]["username"] == "RungeBot":
            return True
    return False


for toot in mdon.notifications():
    print(toot["created_at"])
    if toot["created_at"] < cutoff:
        break
    if toot["type"] == "mention" and not replied(toot["status"]["id"]):
        user = toot["account"]["acct"]

        toot_this, data = create_tweet(
            toot["status"]["content"].replace("</p>", "").replace("<p>", ""),
            user, fname="toot_me")
        if toot_this is not None:
            if test:
                print(toot_this)
            else:
                if data is None:
                    mdon.status_post(toot_this, in_reply_to_id=toot["status"]["id"])
                else:
                    img = mdon.media_post("toot_me.png")
                    results = mdon.status_post(
                        status=toot_this, media_ids=img, in_reply_to_id=toot["status"]["id"])
            print(toot_this)
            break
