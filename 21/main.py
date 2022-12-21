import math
import re
import numpy as np
import pyperclip
import itertools

def read_re(filename):
    data = {}
    for line in open(filename):
        d = line.strip().split(':')
        d[1] = d[1].strip()
        data[d[0]] = d[1]

    return data

def get_value(data, monkey):
    if data[monkey].isnumeric():
        return int(data[monkey])

    d = data[monkey].split(" ")
    a = get_value(data, d[0])
    b = get_value(data, d[2])
    op = d[1]

    if op == "+":
        return a+b
    if op == "-":
        return a-b
    if op == "/":
        return a/b
    if op == "*":
        return a*b


EXPECTED_1 = 152
def first_part(data):
    solution = get_value(data, 'root')
    return solution

EXPECTED_2 = 301
def second_part(data):
    
    d = data['root'].split(' ')
    m1 = d[0]
    m2 = d[2]
    
   # data['humn'] = "0"
   # v1 = get_value(data, m1)
    v2 = get_value(data, m2)
    
    # This assumes the correct i is positive
    pos = None
    neg = None
    i = 1
    while True:
        data['humn'] = str(i)
        v1 = get_value(data, m1)
        diff = v1 - v2
        #print(f"value={i} difference={v1-v2}")

        if diff == 0:
            solution = i
            #print(f"solution {i}")
            break
        if diff > 0:
            pos = i
        if diff < 0:
            neg = i

        if pos is None or neg is None:
            i = i*2
        else:
            i = math.trunc((pos+neg)/2)

    return solution
                
if __name__ == '__main__':

    print("###################new run###################")
    filename = 'example.txt'
    example_data = read_re(filename)
    example1 = first_part(example_data)
    if example1 != EXPECTED_1:
        exit()
    else:
        print("Part 1 example success")
    
    filename = 'input.txt'
    data = read_re(filename)
    solution = int(first_part(data))

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(f"P1 Solution: {solution}")
    pyperclip.copy(str(solution))
    
    ## PART 2
    print("---- Part 2 Start  ---------------")
    filename = 'example.txt'
    example_data = read_re(filename)
    example2 = second_part(example_data)
    if example2 != EXPECTED_2:
        exit()
    else:
        print("Part 2 example success")

    filename = 'input.txt'
    data = read_re(filename)
    solution = int(second_part(data))

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(f"P2 Solution: {solution}")
    pyperclip.copy(str(solution))
