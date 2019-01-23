import numpy as np
import math

def uniform(a, b, size=None):
    return np.random.uniform(low=a, high=b, size=size) 

def exponential(lam, size=1):
    lam = float(lam)

    collection = []

    for x in range(0, size):
        x = uniform(0,1)
        x = - (1/lam) * math.log(1-x)
        collection.append(x)

    if (len(collection) == 1):
        return collection[0]
        
    return collection

    # e = np.random.exponential(scale=1/lam, size=size)
    # return e

def poisson(lam, limit, size=None):
    lam = float(lam)
    e = np.random.poisson(lam=lam, size=size)
    return e