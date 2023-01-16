RungeBot
========
RungeBot is a [Twitter](https://twitter.com/RungeBot) and [Mathstodon](https://mathstodon.xyz/@RungeBot) bot that tweets polynomial interpolations of functions using
equidistant points and Chebyshev points to show Runge's phenomenon.

There's an explanation of what RungeBot does at [mscroggs.co.uk/blog/57](https://mscroggs.co.uk/blog/57).

Tweeting
--------
To get RungeBot to interpolate a function for you, tweet `@RungeBot f(x)=[your function here]` or toot `@RungeBot@mathstodon.xyz f(x)=[your function here]`.
It will reply with a picture and it will tell you how bad Runge's phenomenon is for your function.

Dependencies
------------
RungeBot uses [my fork of the Equation package](https://github.com/mscroggs/Equation).
