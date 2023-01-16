import matplotlib
import matplotlib.pylab as plt
import numpy as np
from scipy.interpolate import barycentric_interpolate as interp
matplotlib.use("Agg")


class InterpolationError(BaseException):
    pass


def uniform_points(n, xlim=[-1, 1]):
    if n == 1:
        return np.array([sum(xlim) / 2])
    return np.array([xlim[0] + (xlim[1] - xlim[0]) * i / (n - 1)
                     for i in range(n)])


def chebyshev_points(n, xlim=[-1, 1]):
    return np.array([
        xlim[0] + (xlim[1] - xlim[0]) * (1 + np.cos((2 * i + 1) / (2 * n) * np.pi)) / 2
        for i in range(n)
    ])


def uniform(xs, f, n, xlim=[-1, 1], plot=None):
    points = uniform_points(n, xlim)
    return interpolate(xs, f, points, plot)


def chebyshev(xs, f, n, xlim=[-1, 1], plot=None):
    points = chebyshev_points(n, xlim)
    return interpolate(xs, f, points, plot)


def interpolate(xs, f, points, plot=None):
    if plot is not None:
        plt.plot(points, np.array([f(p) for p in points]), plot)
    return interp(points, np.array([f(p) for p in points]), xs)


def error_diff(ls1, ls2):
    return max(np.abs(ls1-ls2)) / max(np.abs(ls2))


def interpolate_and_rate(f, fname="tweet_me"):
    N = 500
    for xlim in [[-1, 1], [0, 1], [0.1, 1], [1, 2], [2, 3], [-1, -2]]:
        xs = np.array([
            xlim[0] + i / (N - 1) * (xlim[1] - xlim[0])
            for i in range(N)
        ])

        try:
            ys = np.array([f(i) for i in xs])
            for i in ys:
                if np.isnan(i):
                    raise ZeroDivisionError
            use = (None, 0)
            max2 = 0

            for n in range(10, 21):
                u = uniform(xs, f, n, xlim)
                c = chebyshev(xs, f, n, xlim)
                max_e = error_diff(u, ys) / error_diff(c, ys)
                max2 = max(error_diff(u, ys), max2)
                if np.isnan(max2) or np.isnan(max_e):
                    raise ZeroDivisionError
                if use[0] is None or max_e > use[1]:
                    use = (n, max_e)

            n = use[0]
            max_e = use[1]

            u = uniform(xs, f, n, xlim, "bo")
            c = chebyshev(xs, f, n, xlim, "ro")

            ymin = min(c)
            ymax = max(c)
            rang = ymax-ymin

            ylim = [ymin-rang/3, ymax+rang/3]

            plt.plot(xs, ys, "k--")
            plt.plot(xs, u, "b-")
            plt.plot(xs, c, "r-")

            plt.xlim(xlim)
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
        except ZeroDivisionError:
            pass
    raise InterpolationError("Could not interpolate function")
