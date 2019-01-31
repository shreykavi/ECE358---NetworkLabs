# ECE 358 Lab 1

This is the codebase for the Discrete Event Simulator (DES)

The code implements a M/M/1/K queue. To run the program, cd into this directory and enter:

```
python main.py $K0 $K1 $K2 ... $Kn
```

Where Ki is the ith element in the sequence of K values to simulate with. If no K values are given, K=infinity and a M/M/1 queue is simulated.