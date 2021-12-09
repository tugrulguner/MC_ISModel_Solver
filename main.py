'''
Monte Carlo Approach for Determining the Ground State
and Spin States of an Ising Spin Model with given
number of spins and number of weights using nodes and
edges (Treating system like a graph with nodes and edges)

Author: Tugrul Guner
Date: 02 Dec 2021

Must be used as "python path_to_input_file"

'''

import argparse
import logging
import os
from helper_functions import *

logging.basicConfig(
    filename='ising_model_running.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def is_mc_gstate(args):
    '''
    This is the main function that calls helper functions: input_reader, mc_iteration and state_converter
    that takes input file as input argument from terminal and saves the results: minimum energy and spin states
    to a output file: output_test_name.txt

    Input:
      args: path of the input file provided by user in the terminal

    Output:
      output file: saves the minimum energy and converted spin states to
      output_test_name.txt where test_name is given by the user in input file

    Author: Tugrul Guner
    Date: 02 Dec 2021
    '''
    nofspin, nodes, edges, weights_nodes, weights_edges, test_name = input_reader(
        args.input_file)
    min_energy, spin_states = mc_iteration(
        nofspin, nodes, edges, weights_nodes, weights_edges)
    conv_state = state_converter(spin_states)

    with open(f'output_{test_name}.txt', "w") as output_file:
        output_file.write(f'{min_energy}\n')
        output_file.write(f'{conv_state}')

    try:  # Checking file if it is successfully saved
        assert os.path.isfile(f'output_{test_name}.txt')
        assert os.path.getsize(f'output_{test_name}.txt') != 0
        logging.info(f'Results are saved to output_{test_name}.txt: SUCCESS')
    except AssertionError as err:
        logging.error(
            'File could not be saved. Check file paths and results: ERROR')
        raise err


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Calculates Ground State Energy of the system provided by input file')
    parser.add_argument(
        'input_file',
        type=str,
        help='Please provide the input file path')
    args = parser.parse_args()
    is_mc_gstate(args)
