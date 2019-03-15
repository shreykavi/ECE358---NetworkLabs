from __future__ import division
import sys
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
    """
    Function for simulating a CSMA/CD network.
    parameters:
        persistent (bool): If true, simulate a persistent CMSA/CD. Else simulate non-persistent
        N (int): The number of nodes to use for simulation.
        A (int): The packet arrival rate for all nodes.
        R (int): The transmission speed of the network.
        L (int): The fixed length of a packet.
        D (int): The distance between adjacent nodes in the network.
        S (int): The propagation speed of the channel
    returns:
        Dictionary with keys:
            successful: The number of successfully transmitted packets in the simulation.
            total: The total number of attempts to transmit packets in the simulation.
    """
    def exponential_backoff(i):
        """
        Function for calculating wait time in exponential backoff
        parameters:
            i: seed for generating a random number r between 0 and (2^i)-1
        returns:
            int: r*512/R where R is the transmission speed
        """
        r = randint(0, (2**i)-1)
        return r*(512/R)

    def update_queue(q, t):
        """
        Function to update packet arrival times in a queue.
        parameters: 
            q (list): Queue of packet arrival times
            t (float): Time to update any packets that arrive before.
        """
        i = 0
        q_length = len(q)
        while i < q_length and q[i] < t:
            q[i] = t
            i += 1

    def get_collision_time(node1, node2, t1, t2):
        """
        Function for calculating the time for when packets from two nodes will collide.
        Assumptions are that the nodes' packets will collide, and t1 < t2
        parameters:
            node1 (int): Index of one of the nodes
            node2 (int): Index of the other node
            t1 (float): Time of node1's packet arrival
            t1 (float): Time of node2's packet arrival
        returns:
            (float): t2 + calculated collision time
        """
        distance = abs(node1-node2)*D
        collision_time = (distance - (t2-t1)*S)/2/S
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
    collision_counts = {i: 0 for i in range(N)}
    busy_counts = {i: 0 for i in range(N)}
    # Simulate
    while queues:
        first_node = min(queues, key=lambda x: queues[x][0])
        first_arrival = queues[first_node][0]
        t_prop = D / S
        propagation_times = {i: t_prop*abs(i-first_node) + first_arrival for i in queues if i != first_node}
        next_packets = {i: queues[i][0] for i in queues if i != first_node}
        collisions = [i for i in next_packets if next_packets[i] <= propagation_times[i]]
        if collisions:
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
                    if new_time < T:
                        update_queue(queues[n], new_time)
                if not queues[n]:
                    del queues[n]
        # Condition block for successful transmission
        else:
            busy_packets = [i for i in next_packets if propagation_times[i] < next_packets[i] < propagation_times[i] + transmission_time]
            for i in busy_packets:
                if persistent:
                    busy_counts[i] += 1
                    if busy_counts[i] >= Kmax:
                        busy_counts[i] = 0
                        queues[i].pop(0)
                        if not queues[i]:
                            del queues[i]
                        continue                        
                t_wait = propagation_times[i] + transmission_time if persistent else exponential_backoff(busy_counts[i])
                new_time = t_wait
                if new_time < T:
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
    """
    Main function to call when script is run
    returns:
        None if console argument of persistence is not specified
        results (list): A list of results that contains the information returned from calling CSMACD_simulation for the range of parameters
        specified in the lab manual.
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <persistent>")
        print("    persistent: 1 for CSMA/CD persistent simulation. 0 for non-persistent.")
        return None
    persistent = bool(int(sys.argv[1]))
    if persistent:
        title = "CSMA/CD Persistent Throughput"
        print("Simulating Persistent CSMA/CD")
    else:
        title = "CSMA/CD Non-Persistent Throughput"
        print("Simulating Non-Persistent CSMA/CD")
    for A in [7, 10, 20]:
        results = []
        for N in range(20, 120, 20):    
            parameters = dict(
                persistent = persistent,
                T = 1000,
                N = N,
                A = A,
                R = 1000000,
                L = 1500,
                D = 10,
                S =  200000000,
                Kmax = 10
            )
            res = CSMACD_simulation(**parameters)
            results.append(res["successful"]*parameters['L']/1000000/parameters['T'])
            print("Finished simulation for A={}, N={}".format(parameters['A'], parameters['N']))

if __name__ == "__main__":
    main()