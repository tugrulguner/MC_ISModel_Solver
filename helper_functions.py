'''
This file contains the helper functions used in main.py
of Monte Carlo Method for Ising Spin Model

Author: Tugrul Guner
Date: 02 Dec 2021

'''

import logging
import numpy as np

logging.basicConfig(
    filename='ising_model_running.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def input_reader(input_file):
    '''
    This is a helper function that imported to main.py to read and check the
    input_file provided by the user in the terminal.

    Inputs:
      input_file: path of the input file

    Outputs:
      number_of_spin: number of spin provided by user
      nodes: nodes that are given where u = v
      edges: edges that are defined where u != v
      weight_nodes: weights provided by user for nodes, hi value
      weight_edges: weights provided by user for edges, Jij value
      test_name: test name provided by user, which is used while
      saving the results as output in the format of output_test_name.txt

      Author: Tugrul Guner
      Date: 02 Dec 2021
    '''

    nodes = []
    edges = []
    weight_nodes = []
    weight_edges = []

    with open(input_file) as file:
        p_command = False  # This is to track if user provided a line starting with p

        for line in file:

            if line[0] == 'c':
                logging.info('Comment line found and skipped')
                continue

            if line[0] == 'p':  # Take care of the parameters in the line starting with p
                logging.info('p line found: SUCCESS')
                p_command = True  # We read p, set it to True

                try:
                  test_name = line.split()[1]
                  number_of_spin = int(line.split()[2])
                  number_of_weights = int(line.split()[3])
                except IndexError as err:
                  logging.error('Check your p line: should have test_name, num of spin and num of weights')
                  raise err

                try:  # Check if Number of Spin and Number of Weights are read
                    number_of_spin
                    number_of_weights
                    logging.info(
                        'Number of Spin and Number of Weights are well read: SUCCESS')
                except NameError as err:
                    logging.error(
                        'Number of Spins or Number of Weights were not read: ERROR')
                continue

            try:
                assert p_command  # Check if p_command remained False
            except AssertionError as err:
                logging.error(
                    'You should add a line starting with -p test_name number_of_spin number_of_weights-')
                raise err

            u_v_weight = line.split()  # From now on, we start to read weights

            # Read u, v and weight values and append them to corresponding
            # lists
            if u_v_weight[0] != u_v_weight[1]:
                edges.append([int(u_v_weight[0]), int(u_v_weight[1])])
                weight_edges.append(int(u_v_weight[2]))
            else:
                nodes.append(int(u_v_weight[0]))
                weight_nodes.append(int(u_v_weight[2]))

            # Check if provided nodes are more than provided number of spins
            try:
                assert len(nodes) <= number_of_spin
            except AssertionError as err:
                logging.error(
                    'There are more nodes than number of spins: ERROR')
                raise err

            # Check total provided weights match with the number of weights
            try:
                assert (
                    len(weight_nodes) +
                    len(weight_edges)) <= number_of_weights
            except AssertionError as err:
                logging.error(
                    'Number of weights and weight inputs parameters dont match: ERROR')
                raise err

    return number_of_spin, nodes, edges, weight_nodes, weight_edges, test_name


def mc_iteration(number_of_spin, nodes, edges, weights_nodes, weights_edges):
    '''
    This helper function imported to main.py performs 1000 iteration over randomly generated
    spins, which these generated spin state distribution -spin_distr-, is used to calculate
    total energy by applying Energy Function: E(S) = E(hi*si) + E(Jij*si*sj), provided in the
    Test. Here, hi and Jij parameters are used as input parameters and multiplied with randomly
    generated spin states at each iteration. Resulting total_energy of each iteration and
    corresponding spin states saved to total_energy_list and spin_state_list, which np.argmin()
    was applied them to reveal the minimum energy and its corresponding spin states.

    Input:
      number_of_spin: Number of spin
      nodes: Nodes where u=v
      edges: Edges where u!=v
      weight_nodes: weights of nodes
      weights_edges: weights of edges

    Output:
      min_energy: Ground state energy as the minimum total energy over entire iteration
      spin_state: Spin states resulting in minimum total energy

    Author: Tugrul Guner
    Date: 02 Dec 2021
    '''

    total_energy_list = []
    spin_state_list = []

    for iteration in range((2**number_of_spin)*100):
        spin_distr = [(-1)**(np.random.randint(1, 3))  # randomly generated spin states
                      for number in range(number_of_spin)]
        energy_nodes = [spin_distr[el] * weights_nodes[el]  # hi*si over spin states
                        for el in range(len(nodes))]
        energy_edges = [spin_distr[edges[el][0]] *  # Jij*si*sj over spin states
                        spin_distr[edges[el][1]] *
                        weights_edges[el] for el in range(len(edges))]

        # total energy as their sum
        total_energy = np.sum(energy_nodes + energy_edges)

        total_energy_list.append(total_energy)
        spin_state_list.append(spin_distr)

    try:  # Check if there are values saved in lists or not
        assert len(total_energy_list) > 0
        assert len(spin_state_list) > 0
        logging.info('Total energies and Spin states were calculated: SUCCESS')
    except AssertionError as err:
        logging.error(
            'Either Total Energies or Spin states were not calculated: ERROR')
        raise err

    min_energy = total_energy_list[np.argmin(
        total_energy_list)]  # find the minimum energy
    # get the corresponding spin states
    spin_state = spin_state_list[np.argmin(total_energy_list)]

    return min_energy, spin_state


def state_converter(spin_state_list):
    '''
    This helper function convertes spin states: +1 and -1, to '+' and '-'
    and adds them based on the given spin state list

    Author: Tugrul Guner
    Date: 02 Dec 2021
    '''
    conv_state = ''
    for spin in spin_state_list:

        try:  # Check if there are spin values different than +1 and -1
            assert spin != 1 or spin != -1
        except AssertionError as err:
            logging.error(
                'There are different spin values than +1 and -1 : Convertion ERROR')
            raise err

        if spin == 1:
            conv_state += '+'
        else:
            conv_state += '-'

    return conv_state
