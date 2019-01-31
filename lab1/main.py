from __future__ import division
import simulator
import sys

def main(k_values):
    """
    Main program for lab 1.
    Runs simulation for different values of L, C, rho, and K
    Repeats simulation for incrementing T values until error is <= 5%
    parameters:
        k_values: List of values of K to simulate with. If empty list, simulate K=infinity (M/M/1)
    """
    L = 2000
    C = 1000000
    rho_list = [i*0.1 for i in range(5, 16)]
    K_lst = [int(i) for i in k_values] if k_values else [float('inf')]
    E_N = 0
    P_idle = 0
    P_loss = 0
    T = 10
    T_step = 10
    unstable = True
    for K in K_lst:
        for rho in rho_list:
            while True:
                event_queue = simulator.generate_events(T, L, C, rho)
                res = simulator.DES_Simulator(event_queue, L, C, K)[-1]
                error_E_N = abs(E_N - res.E_N)/res.E_N if res.E_N else float('inf')
                error_P_idle = abs(P_idle - res.P_idle)/res.P_idle if res.P_idle else float('inf')
                if 0 <= error_E_N <= 0.05 and 0 <= error_P_idle <= 0.05:
                    break
                else:
                    T += T_step
                    E_N = res.E_N
                    P_idle = res.P_idle
                    P_loss = res.P_loss
            print("Finished stable simulation with parameters: {}.".format(dict(T=T, L=L, C=C, rho=rho, K=K)))

if __name__ == "__main__":
    main(sys.argv[1:])
