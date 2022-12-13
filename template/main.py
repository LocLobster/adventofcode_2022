import math
import re
import numpy as np
import pyperclip

EXPECTED_1 = 31
EXPECTED_2 = 29

def read_re(filename):
    data = []

    for line in open(filename):
        d = list(map(int, re.findall(f'\S+', line)))
        data.append(d)

    return data

def first_part(data):
    for d in data:
        print(d)

    solution = 0

    return solution

def second_part(data):
    pass
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'example.txt'
    example_data = read_re(filename)
    example1 = first_part(example_data)
    if example1 != EXPECTED_1:
        exit()
    
    filename = 'input.txt'
    data = read_re(filename)
    solution = first_part(data)

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(solution)
    pyperclip.copy(str(solution))
    
    ## PART 2
    example2 = second_part(example_data)
    if example2 != EXPECTED_2:
        exit()

    solution = second_part(data)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(solution)
    pyperclip.copy(str(solution))
