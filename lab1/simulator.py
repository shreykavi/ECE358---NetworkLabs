from __future__ import division
import random_variable as rv
import numpy as np

class Event:
    def __init__(self, arrival, length, service):
        self.arrival = arrival
        self.length = length
        self.service = service

    def __repr__(self):
        return "(a: {}, l: {}, s: {})".format(self.arrival, self.length, self.service)

class QueueEvent:
    def __init__(self, event_type, time):
        self.event_type = event_type
        self.time = time

def generate_events(T, L, C, rho):
    lam = rho*C/L
    arrivals = [rv.exponential(lam)]
    lengths = [rv.exponential(1/L)]
    departures = [arrivals[0] + lengths[0]/C]
    
    while arrivals[-1] < T:
        a = rv.exponential(lam)
        l = rv.exponential(1/L)
        s = l/C
        arrivals.append(a)
        lengths.append(l)
        if a < departures[-1]:
            departures.append(departures[-1]+s)
        else:
            departures.append(a+s)
    observers = [rv.exponential(lam*5)]
    while observers[-1] < T:
        observers.append(observers[-1]+rv.exponential(lam*5))

    arrivals = [dict(type="arrival", time=a) for a in arrivals]
    departures = [dict(type="departure", time=d) for d in departures]
    observers = [dict(type="observer", time=o) for o in observers]

    events = arrivals+departures+observers
    return sorted(events, key=lambda x: x["time"])


    

def DES_Simulator(events): #m/m/1
    """
    Discrete Event Simulator
    Iterate through events are calculate stats
    params:
        events: list of events
    """
    buffer_size = 0
    observer_records = []

    for e in events:
        if e["type"] == "arrival":
            # TODO logic for arrival event
            pass
        elif e["type"] == "departure":
            # TODO logic for departure event
            pass
        elif e["type"] == "observer":
            # TODO logic for observer event
            pass
        
    