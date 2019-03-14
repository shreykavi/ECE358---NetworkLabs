from __future__ import division
import numpy as np
import math
from random import randint
import matplotlib.pyplot as plt

def exponential(beta, size=1):
    """
    Return random number based on exponential probability distribution
    parameters:
        beta: The expected value of the distribution function (inverse of the rate)
        size: number of values to output. Default value is 1.
    """
    collection = []
    for x in range(0, size):
        x = np.random.uniform(low=0, high=1)
        x = - beta * math.log(1-x)
        collection.append(x)
    if (len(collection) == 1):
        return collection[0]
    return collection

def CSMACD_simulation(persistent, N, A, R, L, D, S, Kmax, T):
    def exponential_backoff(i):
        r = randint(0, (2**i)-1)
        return r*(512/R)

    def update_queue(q, t):
        i = 0
        q_length = i < len(q)
        while q[i] < t and i < q_length:
            q[i] = t
            i += 1

    def get_collision_time(node1, node2, t1, t2):
        distance = abs(node1-node2)*D
        collision_time = (distance - (t1-t2)*S)/2/S
        return t2 + collision_time
    
    transmit_counter = 0
    successful_transmit_counter = 0
    transmission_time = L / R
    # Generate arrival queues for N nodes
    queues = {}
    for i in range(N):
        queues[i] = [exponential(1/A)]
        while queues[i][-1] < T:
            queues[i].append(queues[i][-1] + exponential(1/A))
    # print([len(queues[i]) for i in queues])
    collision_counts = {i: 0 for i in range(N)}
    # Simulate
    while queues:
        first_node = min(queues, key=lambda x: queues[x][0])
        first_arrival = queues[first_node][0]
        t_prop = D / S
        propagation_times = {i: t_prop*abs(i-first_node) + first_arrival for i in queues if i != first_node}
        next_packets = {i: queues[i][0] for i in queues if i != first_node}
        collisions = [i for i in next_packets if next_packets[i] <= propagation_times[i]]
        if collisions:
            # print("COLLISION DETECTED")
            collision_times = [get_collision_time(first_node, i, first_arrival, next_packets[i]) for i in collisions]
            first_collision = min(collision_times)

            colliding_nodes = [i for i in next_packets if next_packets[i] < first_collision] + [first_node]
            for n in colliding_nodes:
                transmit_counter += 1
                collision_counts[n] += 1
                if collision_counts[n] >= Kmax:
                    collision_counts[n] = 0
                    queues[n].pop(0)
                else:
                    t_wait = exponential_backoff(collision_counts[n])
                    new_time = first_collision + t_wait
                    update_queue(queues[n], new_time)
                if not queues[n]:
                    del queues[n]
        # Condition block for busy
        else:
            # print("SUCCESSFUL TRANSMISSION")
            busy_packets = [i for i in next_packets if propagation_times[i] < next_packets < propagation_times[i] + transmission_time]
            for i in busy_packets:
                t_wait = propagation_times[i] + transmission_time if persistent else 0 # make exponential backoff for non persistent
                new_time = first_arrival + t_wait
                update_queue(queues[i], new_time)
            successful_transmit_counter += 1
            collision_counts[first_node] = 0
            queues[first_node].pop(0)
            transmit_counter += 1
            if not queues[first_node]:
                del queues[first_node]
    return {
        "total": transmit_counter,
        "successful": successful_transmit_counter
    }

def main():
    # Parameters for simulation
    efficiency = []
    for N in range(20, 120, 20):    
        parameters = dict(
            persistent = True,
            T = 1000,
            N = N,
            A = 5,
            R = 1000000,
            L = 1500,
            D = 10,
            S =  200000000,
            Kmax = 10
        )
        res = CSMACD_simulation(**parameters)
        efficiency.append(res["successful"]/res["total"])
        print("Finished test for A={}, N={}".format(parameters['A'], parameters['N']))
    plt.plot(range(20, 120, 20), efficiency, label="A=5")
    plt.show()

if __name__ == "__main__":
    main()