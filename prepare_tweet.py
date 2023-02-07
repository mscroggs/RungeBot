import function_parser as fp
import interpolator as ip


def get_function(tweet):
    tweet = "".join(tweet.split())
    if "f(x)=" in tweet:
        return tweet.split("f(x)=")[1]
    else:
        return "NO FUNCTION"


def create_tweet(function_string, user, fname="tweet_me"):
    function = get_function(function_string)
    if function == "NO FUNCTION":
        return None, None

    # Commonly used functions that are unsupported
    if "!" in function:
        return (f".@{user} Sorry, I don't yet understand \"!\", "
                "you can use \"factorial(...)\" instead."), None
    if "//" in function:
        return f".@{user} Sorry, I don't yet understand \"//\".", None

    try:
        f = fp.parse(function)
        data, rating, n = ip.interpolate_and_rate(f, fname=fname)
    except TypeError:
        return f".@{user} I couldn't understand your function. Sorry.", None
    except ip.InterpolationError:
        return (f".@{user} I had trouble evaluating your function. "
                "Is it undefined for some values? "
                "@mscroggs: I might need fixing."), None
    except BaseException:
        return f".@{user} Something went wrong. @mscroggs: Can you fix me please.", None

    return (
        f".@{user} Here's f(x)={function} interpolated using "
        f"{n} equally spaced points (blue) and {n} Chebyshev points (red). "
        f"For your function, Runge's phenomenon is {rating}."
    ), data
