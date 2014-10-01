from __future__ import print_function
from sys import stdin
import pprint


def separate_states(state_list):
    state_list = state_list.strip().strip('{}')
    states = []
    for state in state_list.split(','):
        if(state != ''):
            states.append(state.strip())

    return states


def e_closure(state_list, states):
    e_closure_states = set(state_list)
    for state in state_list:
        my_set = set(e_closure(states[state]['E'], states))
        e_closure_states = e_closure_states | my_set

    return list(e_closure_states)


def move(state_list, states, symbol):
    set_states = set()
    for state in state_list:
        # print(states[state][symbol])
        my_set = set(states[state][symbol])
        set_states = set_states | my_set

    return list(set_states)


def find_index(state_list, d_states):
    for i in range(0, len(d_states)):
        if set(d_states[i]) == set(state_list):
            return i

    return len(d_states)


def convert_to_dfa(io, states, tokens):
    d_states = []
    dfa_states = {}
    d_states.append(e_closure(io, states))
    marked_index = 0
    while marked_index < len(d_states):
        print('')
        state_list = d_states[marked_index]
        marked_index += 1
        print("Mark " + str(marked_index))
        dfa_states[marked_index] = {}
        for token in tokens:
            if token != 'E':
                dfa_states[marked_index][token] = []
                states_on_token = move(state_list, states, token)
                if len(states_on_token) > 0:
                    print(state_list, end='')
                    print(" --" + token + "--> ", end='')
                    print(states_on_token)
                    print("E-closure", end='')
                    print(states_on_token, end='')
                    print(" = ", end='')
                    u = e_closure(states_on_token, states)
                    print(u, end='')
                    print(" = ", end='')

                    index_of_state = find_index(u, d_states)
                    if index_of_state == len(d_states):
                        # if it is a new state not on d_states
                        d_states.append(u)

                    print(index_of_state+1)
                    dfa_states[marked_index][token] = index_of_state+1

            # print(u)
    # print(d_states)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(dfa_states)


if __name__ == '__main__':
    # Used to allow this to be a standalone program and not run this code if
    # it's imported from somewhere else.

    # interate over the lines from standard in.

    initial_state = separate_states(stdin.readline().split(':')[1])
    final_states = separate_states(stdin.readline().split(':')[1])
    state_count = int(separate_states(stdin.readline().split(':')[1])[0])

    # split on whitespace with no arguments to split
    tokens = stdin.readline().strip().split()
    tokens.pop(0)

    print(initial_state)
    print(final_states)
    print(state_count)
    print(tokens)

    states = {}
    for i in range(0, state_count):
        line = stdin.readline().split('{')
        state_name = line.pop(0).strip()
        states[state_name] = {}

        for token in tokens:
            states[state_name][token] = separate_states(line[0])
            line.pop(0)
            print(states[state_name][token], end='')

        print('')

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(states)
    convert_to_dfa(initial_state, states, tokens)
    # print(e_closure(e_closure(initial_state, states), states))
