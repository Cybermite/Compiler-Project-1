from __future__ import print_function
from sys import stdin

def separate_states(state_list):
    state_list = state_list.strip().strip('{}')
    states = []
    for state in state_list.split(','):
        states.append(state.strip())
    
    return states

if __name__ == '__main__':
    # Used to allow this to be a standalone program and not run this code if
    # it's imported from somewhere else.

    # interate over the lines from standard in.
   
    initial_state = separate_states(stdin.readline().split(':')[1])[0]
    final_states = separate_states(stdin.readline().split(':')[1])
    state_count = separate_states(stdin.readline().split(':')[1]) 
    
    # split on whitespace with no arguments to split
    tokens = stdin.readline().strip().split()
    tokens.pop(0)

    print(initial_state)
    print(final_states)
    print(state_count)
    print(tokens)
    
    states = []
    states.append({})
    line = stdin.readline().split('{')
    line.pop(0)
    
    for token in tokens:
        states[0][token] = separate_states(line[0])
        line.pop(0)
        print(states[0][token])

#    for line in stdin:
 #       print(line, end='')
