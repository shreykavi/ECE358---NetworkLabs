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
        1000000
    )
    K = 10
    E_N = []
    P_idle = []
    rhos = np.arange(1.5, 1.6, 0.1)
    for i, rho in enumerate(rhos):
        t0 = time.time()
        event_queue = simulator.generate_events(T, L, C, rho)
        observer_records = simulator.DES_Simulator(event_queue, L, C, K)
        print(observer_records[-1])
    #     E_N.append(observer_records[-1].E_N)
    #     P_idle.append(observer_records[-1].P_idle)
    #     t1 = time.time()
    #     print("Finished Test {}: rho={}, elapsed time: {}s".format(i, rho, t1-t0))
    # plt.plot(rhos, P_idle)
    # plt.xlabel("rho")
    # plt.ylabel("P_idle")
    # plt.title("Question 3.2: P_idle vs rho")
    # plt.show()

if __name__ == "__main__":
    main(sys.argv)
