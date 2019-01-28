from __future__ import division
import random_variable as rv
import numpy as np

class DESEvent:
    """
    Class for classifying DES events
    class members:
        type: The type of event (arrival, departure, or observer).
        time: The time at which the event occurs.
    """
    def __init__(self, e_type, e_time):
        self.type = e_type
        self.time = e_time

    def __repr__(self):
        return """
{{
    DESEvent.type: {},
    DESEvent.time: {}
}}
""".format(self.type, self.time)

class ObserverRecord:
    """
    Class for recording data at observer events
    class members:
        E_N: The time-average number of packets in the buffer E[N].
        P_idle: The proportion of time the server is idle.
    """
    def __init__(self, E_N, P_idle):
        self.E_N = E_N
        self.P_idle = P_idle
    
    def __repr__(self):
        return """
{{
    E_N: {},
    P_idle: {}
}}
""".format(self.E_N, self.P_idle)

def generate_events(T, L, C, rho):
    """
    Generate Events for DES
    params:
        T: Time period for simluation
        L: Average package length in bits
        C: Service rate
        rho: Traffic intensity value
    """
    lam = rho*C/L
    arrivals = [rv.exponential(lam)]
    l = rv.exponential(1/L)
    departures = [arrivals[0] + l/C]
    while arrivals[-1] < T:
        a = rv.exponential(lam)
        l = rv.exponential(1/L)
        s = l/C
        arrivals.append(a)
        if a < departures[-1]:
            departures.append(departures[-1]+s)
        else:
            departures.append(a+s)
    observers = [rv.exponential(lam*5)]
    while observers[-1] < T:
        observers.append(observers[-1]+rv.exponential(lam*5))
    arrivals = [DESEvent(e_type="arrival", e_time=a) for a in arrivals[:-1]]
    departures = [DESEvent(e_type="departure", e_time=d) for d in departures[:-1]]
    observers = [DESEvent(e_type="observer", e_time=o) for o in observers[:-1]]
    events = arrivals+departures+observers
    return sorted(events, key=lambda x: x.time)

def DES_Simulator(events): #m/m/1
    """
    Discrete Event Simulator
    Iterate through events are calculate stats
    params:
        events: Sorted list of DESEvent objects to iterate over.
    """
    observer_records = []
    Na, Nd, No = (0, 0, 0)
    idle_count = 0
    avg_queuesize_sum = 0
    for e in events:
        # Conditional block to update Na and Nd
        if e.type == "arrival":
            Na += 1
        elif e.type == "departure":
            Nd += 1
        # If observer event record data and add to list
        if e.type == "observer":
            No += 1
            queue_size = (Na - Nd)
            idle_count += 1 if not queue_size else 0
            avg_queuesize_sum += queue_size
            observer_records.append(
                ObserverRecord(E_N=avg_queuesize_sum/No, P_idle=idle_count/No)
            )
    return observer_records
