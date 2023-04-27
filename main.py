"""
Driver program to run a mock Distributed System and simulate resource sharing.
"""

import argparse
import sys

from deadlock_detection.simulator import simulate

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_processes", default=5, help="number of processes to be used in the simualtion", type=int)
    parser.add_argument("-m", "--num_resources", default=3, help="number of resources to be used in the simulation", type=int)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    simulate(args.num_processes, args.num_resources)

if __name__ == "__main__":
    main()