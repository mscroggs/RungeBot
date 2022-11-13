import matplotlib
import matplotlib.pylab as plt
import numpy as np
from scipy.interpolate import barycentric_interpolate as interp
matplotlib.use("Agg")


def uniform_points(n):
    return np.array([-1+2*i/(n-1) for i in range(n)])


def chebyshev_points(n):
    return np.array([np.cos((2*i+1)/(2*n)*np.pi) for i in range(n)])


def uniform(xs, f, n, plot=None):
    points = uniform_points(n)
    return interpolate(xs, f, points, plot)


def chebyshev(xs, f, n, plot=None):
    points = chebyshev_points(n)
    return interpolate(xs, f, points, plot)


def interpolate(xs, f, points, plot=None):
    if plot is not None:
        plt.plot(points, f(points), plot)
    return interp(points, f(points), xs)


def error_diff(ls1, ls2):
    return max(np.abs(ls1-ls2)) / max(np.abs(ls2))


def interpolate_and_rate(f, fname="tweet_me"):
    N = 500
    xs = np.array([i/N for i in range(-N, N+1)])

    ys = f(xs)

    use = (None, 0)
    max2 = 0

    for n in range(10, 21):
        u = uniform(xs, f, n)
        c = chebyshev(xs, f, n)
        max_e = error_diff(u, ys) / error_diff(c, ys)
        max2 = max(error_diff(u, ys), max2)
        if use[0] is None or max_e > use[1]:
            use = (n, max_e)

    n = use[0]
    max_e = use[1]

    u = uniform(xs, f, n, "bo")
    c = chebyshev(xs, f, n, "ro")

    ymin = min(c)
    ymax = max(c)
    rang = ymax-ymin

    ylim = [ymin-rang/3, ymax+rang/3]

    plt.plot(xs, ys, "k--")
    plt.plot(xs, u, "b-")
    plt.plot(xs, c, "r-")

    plt.xlim([-1, 1])
    plt.ylim(ylim)
    plt.savefig(f"{fname}.png")

    if max_e < 1 or max2 < 0.1:
        rating = "not a problem"
    elif max_e < 1.2:
        rating = "hardly a problem"
    elif max_e < 1.5:
        rating = "not too bad"
    elif max_e < 2:
        rating = "ok"
    elif max_e < 3:
        rating = "quite bad"
    elif max_e < 4:
        rating = "bad"
    elif max_e < 8:
        rating = "very bad"
    elif max_e < 15:
        rating = "terrible"
    else:
        rating = "unbelievably bad"

    with open(f"{fname}.png", 'rb') as f:
        data = f.read()
    return data, rating, n
