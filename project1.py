from __future__ import print_function
from sys import stdin

def separate_states(state_list):
    state_list = state_list.strip().strip('{}')
    states = []
    for state in state_list.split(','):
        if(state != ''):
            states.append(int(state.strip()))

    return states

def e_closure(state_list, states):
    e_closure_states = set(state_list)
    for state in state_list:
        e_closure_states = e_closure_states | set(e_closure(states[state-1]['E'], states))

    return list(e_closure_states)

if __name__ == '__main__':
    # Used to allow this to be a standalone program and not run this code if
    # it's imported from somewhere else.

    # interate over the lines from standard in.

    initial_state = separate_states(stdin.readline().split(':')[1])
    final_states = separate_states(stdin.readline().split(':')[1])
    state_count = separate_states(stdin.readline().split(':')[1])[0] 

    # split on whitespace with no arguments to split
    tokens = stdin.readline().strip().split()
    tokens.pop(0)

    print(initial_state)
    print(final_states)
    print(state_count)
    print(tokens)

    states = []

    for i in range(0, state_count):
        states.append({})
        line = stdin.readline().split('{')
        
        # get rid of the state number
        line.pop(0)
        for token in tokens:
            states[i][token] = separate_states(line[0])
            line.pop(0)
            print(states[i][token], end='')
        
        print('')
    
    # print(e_closure(initial_state, states))
