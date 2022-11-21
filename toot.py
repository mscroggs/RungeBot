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
        function = get_function(toot["status"]["content"])
        done.append(toot["status"]["id"])
        user = toot["account"]["acct"]
        if function is not None:
            try:
                f = fp.parse(function)
                data, rating, n = ip.interpolate_and_rate(f, fname="toot_me")
            except TypeError:
                toot_this = f"@{user} I couldn't parse your function. Sorry."
                mdon.status_post(toot_this, in_reply_to_id=toot["status"]["id"])
                print(toot_this)
                break
            except:
                toot_this = f"@{user} Something went wrong. @mscroggs: Can you fix me please."
                mdon.status_post(toot_this, in_reply_to_id=toot["status"]["id"])
                print(toot_this)
                break

            img = mdon.media_post("toot_me.png")

            toot_this = (
                f"@{user} Here's f(x)={function} interpolated using "
                f"{n} equally spaced points (blue) and {n} Chebyshev points (red). "
                f"For your function, Runge's phenomenon is {rating}."
            )
            print(toot_this)

            results = mdon.status_post(
                status=toot_this, media_ids=img, in_reply_to_id=toot["status"]["id"])
            break

with open("mdone.json", "w") as f:
    json.dump(done, f)

