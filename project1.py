"""
AUTHOR: Zane Ralston
CLASS: EECS 665, Compiler Construction
DUE DATE: October 3, 2014
SUMMARY: Will take in input of the nfa and convert to dfa by doing the
        algorithm learned in class.
"""

from __future__ import print_function
from sys import stdin


def separate_states(state_list):
    """
    Summary: Will return a list of states that is inclosed within the '{}'
    state_list: The state list that is of the format '{number, number, ...}'
    Return: Returns a list of the seprate states
    """
    state_list = state_list.strip().strip('{}')
    states = []
    for state in state_list.split(','):
        if(state != ''):
            states.append(state.strip())

    return states


def e_closure(state_list, states, visited):
    """
    Summary: Will do the null closure from each state within state_list
    state_list: list of states that is apart of one bigger state in the diagram
    states: The entire nfa transition dictionary
    Return: Returns a list of states that can be reachable from this state_list
            on 'E' transition
    """
    e_closure_states = set(state_list)
    for state in state_list:
        # check to see if E exist
        if 'E' in states[state]:
            if state in visited:
                continue
            else:
                visited.append(state)
                my_set = set(e_closure(states[state]['E'], states, visited))
                e_closure_states = e_closure_states | my_set

    return list(e_closure_states)


def move(state_list, states, symbol):
    """
    Summary: Will do the move function from this list of states on the symbol.
    state_list: current list of states
    states: THe entire nfa transition dictionary
    Return: Returns a list of states that are reachable from this state_list on
            the symbol passed in.
    """
    set_states = set()
    for state in state_list:
        # print(states[state][symbol])
        my_set = set(states[state][symbol])
        set_states = set_states | my_set

    return list(set_states)


def find_index(state_list, d_states):
    """
    Summary: Will search through the list of d_states to see if the current
            state is already in d_states
    state_list: current list of states
    d_states: The new states currently after eliminating 'E' transitions
    Return: Returns the index of the this state within d_states. If the state
            wasn't in d_states, it will return the length of d_states.
    """
    for i in range(0, len(d_states)):
        if set(d_states[i]) == set(state_list):
            return i

    return len(d_states)


def print_state(state_list):
    """
    Summary: Will print out the current state between brackets ({values})
    state_list: current list of states to print out
    Return: none
    """

    # sort the states within this list
    temp_list = []
    for i in range(0, len(state_list)):
        temp_list.append(int(state_list[i]))

    temp_list.sort()
    state_list = temp_list

    print('{', end='')
    for i in range(0, len(state_list)):
        print('%s' % (state_list[i]), end='')
        if i != len(state_list)-1:
            # if it's not the last state in this list
            print(',', end='')

    print('}', end='')


def is_final_state(state_list, final_states):
    """
    Summary: Checks to see if this state is suppose to be a final state
    state_list: The state, which can have multiple states apart of it.
    final_states: The list of final states before the dfa conversion.
    Return: Returns true if it's suppose to be a final state, false otherwise.
    """
    for state in state_list:
        for final_state in final_states:
            if state == final_state:
                return True

    return False


def print_dfa(states, tokens, final_states, initial_state):
    """
    Summary: Prints out the dfa
    states: Dictionary of my states and transitions
    tokens: symbols that is apart of the language
    final_states: list of final states
    initial_state: list of initial state
    Return: none
    """
    print('Initial State: ', end='')
    print_state(initial_state)
    print('')
    print('Final States: ', end='')
    print_state(final_states)
    print('')
    print('State\t', end='')

    for token in tokens:
        if token != 'E':
            print('%s\t' % (token), end='')

    print('')
    for state in states:
        print('%d\t' % (state), end='')
        for token in tokens:
            if token != 'E':
                print_state(states[state][token])
                print('\t', end='')

        print('')


def convert_to_dfa(io, states, tokens, final_states):
    """
    Summary: Will convert the nfa to a dfa
    io: list of the initial state
    states: Dictionary of my states and transitions on symbols
    tokens: List of symbols that moves can happen on.
    final_states: List of final states
    Return: none
    """
    d_states = []
    dfa_final_states = []
    dfa_initial_state = []
    dfa_states = {}
    d_states.append(e_closure(io, states, []))
    marked_index = 0
    print('E-closure(I0) = ', end='')
    print_state(d_states[0])
    print(' = %d' % (marked_index+1))
    dfa_initial_state.append(marked_index+1)
    while marked_index < len(d_states):
        print('')
        state_list = d_states[marked_index]
        marked_index += 1
        print('Mark %d' % (marked_index))
        dfa_states[marked_index] = {}
        for token in tokens:
            if token != 'E':
                dfa_states[marked_index][token] = []
                states_on_token = move(state_list, states, token)
                if len(states_on_token) > 0:
                    print_state(state_list)
                    print(' --' + token + '--> ', end='')
                    print_state(states_on_token)
                    print('')
                    print('E-closure', end='')
                    print_state(states_on_token)
                    print(' = ', end='')
                    u = e_closure(states_on_token, states, [])

                    print_state(u)
                    print(' = ', end='')

                    index_of_state = find_index(u, d_states)
                    if index_of_state == len(d_states):
                        # if it is a new state not on d_states
                        d_states.append(u)
                        if is_final_state(u, final_states):
                            dfa_final_states.append(index_of_state+1)

                    print(index_of_state+1)
                    dfa_states[marked_index][token].append(index_of_state+1)

    print('')
    print_dfa(dfa_states, tokens, dfa_final_states, dfa_initial_state)


if __name__ == '__main__':
    # Used to allow this to be a standalone program and not run this code if
    # it's imported from somewhere else.

    initial_state = separate_states(stdin.readline().split(':')[1])
    final_states = separate_states(stdin.readline().split(':')[1])
    state_count = int(separate_states(stdin.readline().split(':')[1])[0])

    # split on whitespace with no arguments to split
    tokens = stdin.readline().strip().split()
    tokens.pop(0)

    states = {}
    for i in range(0, state_count):
        line = stdin.readline().split('{')
        state_name = line.pop(0).strip()
        states[state_name] = {}

        for token in tokens:
            states[state_name][token] = separate_states(line[0])
            line.pop(0)

    convert_to_dfa(initial_state, states, tokens, final_states)
