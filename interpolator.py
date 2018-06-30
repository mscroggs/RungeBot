import matplotlib
matplotlib.use("Agg")
import matplotlib.pylab as plt
import numpy as np
from scipy.interpolate import barycentric_interpolate as interp
from random import choice
from os.path import isfile

def uniform_points(n):
    return np.array([-1+2*i/(n-1) for i in range(n)])

def chebyshev_points(n):
    return np.array([np.cos((2*i+1)/(2*n)*np.pi) for i in range(n)])

def uniform(xs,f,n,plot=None):
    points = uniform_points(n)
    return interpolate(xs,f,points,plot)

def chebyshev(xs,f,n,plot=None):
    points = chebyshev_points(n)
    return interpolate(xs,f,points,plot)

def interpolate(xs,f,points,plot=None):
    if plot is not None:
        plt.plot(points,f(points),plot)
    return interp(points,f(points),xs)

def interpolate_and_rate(f):
    N = 500
    xs = np.array([i/N for i in range(-N,N+1)])

    ys = f(xs)
    ymin = min(ys)
    ymax = max(ys)
    rang = ymax-ymin

    ylim = [ymin-rang/3,ymax+rang/3]

    use = (None,0)

    for n in range(10,21):
        u = uniform(xs,f,n)
        max_e = max(np.abs(u-ys))
        if max_e > use[1]:
            use = (n,max_e)

    n = use[0]

    plt.plot(xs,ys,"k--")
    u = uniform(xs,f,n,"bo")
    plt.plot(xs,u,"b-")
    c = chebyshev(xs,f,n,"ro")
    plt.plot(xs,c,"r-")

    plt.xlim([-1,1])
    plt.ylim(ylim)
    plt.savefig("tweet_me.png")
    plt.show()
    plt.clf()

    max_e = use[1]/max(np.abs(c-ys))

    if max_e < 1:
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
        rating = "insanely bad"

    with open("tweet_me.png", 'rb') as f:
        data = f.read()

    return data, rating, n
