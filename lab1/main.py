from __future__ import division
import simulator
import sys
import matplotlib.pyplot as plt
import numpy as np
import time

def main(args):
    T, L, C = (
        100,
        2000,
        1
    )
    E_N = []
    P_idle = []
    rhos = np.arange(0.25, 0.35, 0.1)
    for i, rho in enumerate(rhos):
        t0 = time.time()
        event_queue = simulator.generate_events(T, 1/L, C, rho)
        observer_records = simulator.DES_Simulator(event_queue)
        E_N.append(observer_records[-1].E_N)
        P_idle.append(observer_records[-1].P_idle)
        t1 = time.time()
        print("Finished Test {}: rho={}, elapsed time: {}s".format(i, rho, t1-t0))
    plt.plot(rhos, E_N)
    plt.show()

if __name__ == "__main__":
    main(sys.argv)
