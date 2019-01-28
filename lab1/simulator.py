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
    def __init__(self, E_N, P_idle, P_loss):
        self.E_N = E_N
        self.P_idle = P_idle
        self.P_loss = P_loss
    
    def __repr__(self):
        return """
{{
    E_N: {},
    P_idle: {},
    P_loss: {}
}}
""".format(self.E_N, self.P_idle, self.P_loss)

def generate_events(T, L, C, rho):
    """
    Generate Events for DES
    params:
        T: Time period for simluation (s)
        L: Average package length (bits)
        C: Service rate (bps)
        rho: Traffic intensity value
    """
    lam = rho*C/L
    arrivals = [rv.exponential(1/lam)]
    while arrivals[-1] < T:
        a = arrivals[-1] + rv.exponential(1/lam)
        arrivals.append(a)
    observers = [rv.exponential(1/(lam*5))]
    while observers[-1] < T:
        o = observers[-1]+rv.exponential(1/(lam*5))
        observers.append(o)
    arrivals = [DESEvent(e_type="arrival", e_time=a) for a in arrivals[:-1]]
    observers = [DESEvent(e_type="observer", e_time=o) for o in observers[:-1]]
    events = arrivals+observers
    return sorted(events, key=lambda x: x.time)

def DES_Simulator(events, L, C, K): #M/M/1/K
    """
    Discrete Event Simulator
    Iterate through events are calculate stats
    params:
        events: Sorted list of DESEvent objects to iterate over.
        L: Average package length (bits)
        C: Output link rate (bps)
        K: Max buffer size
    """
    buffer = []
    observer_records = []
    Na, Nd, No = (0, 0, 0)
    idle_count = 0
    avg_queuesize_sum = 0
    num_packet_loss = 0
    while events or buffer:
        # Pop event that occurs first
        if buffer:
            if events:
                e = buffer.pop(0) if buffer[0].time < events[0].time else events.pop(0)
            else:
                e = buffer.pop(0)
        else:
            e = events.pop(0)
        # Conditional block to update Na and Nd
        if e.type == "arrival":
            Na += 1
            package_length = rv.exponential(L)
            service_time = package_length/C
            if len(buffer) < K:    
                if buffer:
                    next_departure = buffer[-1]
                    dept_time = next_departure.time+service_time
                else:
                    dept_time = e.time+service_time
                buffer.append(DESEvent(e_type="departure", e_time=dept_time))
            else:
                num_packet_loss += 1
        elif e.type == "departure":
            Nd += 1
        # If observer event record data and add to list
        if e.type == "observer":
            No += 1
            queue_size = len(buffer)
            idle_count += 1 if not queue_size else 0
            avg_queuesize_sum += queue_size
            P_loss=num_packet_loss/Na if Na else 0
            observer_records.append(
                ObserverRecord(E_N=avg_queuesize_sum/No, P_idle=idle_count/No, P_loss=P_loss)
            )
    return observer_records
