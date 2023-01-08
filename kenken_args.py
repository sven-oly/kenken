# Define and handle arguments for running and debugging the kenken solver.
#
import argparse


class ArgParse:
    def __init__(self):
        # Run just one step
        parser = argparse.ArgumentParser('Process kenken solver arguments')
        parser.add_argument('--onestep', default=False)
        parser.add_argument('--userinput', default=False)
        parser.add_argument('--showsteps', default=False)
        self.args = parser.parse_args()