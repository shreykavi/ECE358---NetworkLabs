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

def generate_events(experiment_time, L):
    arrivals = rv.exponential(75, 1000)
    lengths = rv.exponential(1/float(L), 1000)
    services = rv.exponential(75, 1000)
    departures = np.array([]*1000)
    departures[0] = arrivals[0] + services[0]
    for i in range(1)

    

def DES_Simulator(): #m/m/1
    buffer_size = 0
    event_table = generate_events(experiment_time=1000, L=2000)
    queue = []
    for e in event_table:
        a_event = QueueEvent("arrival", e.arrival)
        dept_time = e.arrival + e.service
        if len(queue) > 0:
            dept_time 
        d_event = QueueEvent()
    



    #TODO: server process