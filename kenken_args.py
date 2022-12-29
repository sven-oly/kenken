# Define and handle arguments for running and debugging the kenken solver.
#
import argparse


class ArgParse:
    def __init__(self):
        # Run just one step
        self.single_step = False
        # Accept user inputs
        self.accept_user_input = False

        parser = argparse.ArgumentParser('Process kenken solver arguments')
        parser.add_argument('--onestep', default=False)
        parser.add_argument('--userinput', default=False)
        parser.add_argument('--showsteps', default=False)
        self.parser = parser
