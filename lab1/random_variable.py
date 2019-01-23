import numpy as np

def uniform(a, b, size=None):
    return np.random.uniform(low=a, high=b, size=size) 

def exponential(lam, size=None):
    lam = float(lam)
    e = np.random.exponential(scale=1/lam, size=size)
    # while e > limit:
    #     e = np.random.exponential(scale=1/lam, size=size)
    return e

def poisson(lam, limit, size=None):
    lam = float(lam)
    e = np.random.poisson(lam=lam, size=size)
    # while e > limit:
    #     e = np.random.poisson(lam=lam, size=size)
    return e