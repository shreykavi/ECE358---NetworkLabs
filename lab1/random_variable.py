import numpy as np

def uniform(a, b, size=None):
    return np.random.uniform(low=a, high=b, size) 

def exponential(lam, limit, size=None):
    e = np.random.exponential(scale=1/lam)
    while e > limit:
        e = np.random.exponential(scale=1/lam)
    return e

def poisson(lam, limit, size=None):
    e = np.random.poisson(scale=lam)
    while e > limit:
        e = np.random.poisson(scale=lam)
    return e
