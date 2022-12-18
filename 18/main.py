import math
import re
import numpy as np
import pyperclip
import itertools

def read_re(filename):
    data = []

    for line in open(filename):
        d = list(map(int, re.findall(f'-?\d+', line)))
        data.append(d)

    return data

def first_part(data):
    length = len(data)
    
    sides = 6*np.ones(length, dtype=int)
    
    for i in range(length-1):
        print(f"Calculating  {i}")
        for j in range(i+1, length):
            if abs(data[i][0]-data[j][0]) + abs(data[i][1]-data[j][1]) + abs(data[i][2]-data[j][2]) == 1:
                sides[i] -= 1
                sides[j] -= 1

    solution = sum(sides)
    print(solution)
    
    return solution

def second_part(data):
    
    np_data = np.array(data)
    shape_min = np.min(np_data, axis=0)
    boundary_min = np.min(np_data, axis=0) - [2,2,2]
    boundary_max = np.max(np_data, axis=0) + [2,2,2]
    
    data_set = set()
    for d in data:
        data_set.add((d[0], d[1], d[2]))
    
    collisions = 0
    start  = (shape_min[0]-1, shape_min[1]-1, shape_min[2]-1)
    next_to_check = [start]
    checked = set()
    num_check = 0

    while True:
        if num_check % 1000 == 0:
            print(f"Num checked = {num_check}")
        if len(next_to_check) == 0:
            break

        loc = next_to_check.pop()
        if loc in checked:
            continue
        checked.add(loc)
        
        up    = (loc[0], loc[1], loc[2]+1)
        down  = (loc[0], loc[1], loc[2]-1)
        left  = (loc[0], loc[1]+1, loc[2])
        right = (loc[0], loc[1]-1, loc[2])
        front = (loc[0]+1, loc[1], loc[2])
        back  = (loc[0]-1, loc[1], loc[2])

        checklist = [up, down, left, right, front, back]
        for c in checklist:
            if c in data_set:
                collisions += 1
            elif c in checked:
                continue
            elif np.any(np.less_equal(c, boundary_min)) or np.any(np.greater_equal(c, boundary_max)):
                continue
            else:
                next_to_check.append(c)
        
        num_check += 1
        if len(next_to_check) == 0:
            break

    print(f"collision {collisions}")
    return collisions
                
if __name__ == '__main__':
    EXPECTED_1 = 64
    EXPECTED_2 = 58

    print("###################new run###################")
    filename = 'example.txt'
    example_data = read_re(filename)
    example1 = first_part_alt(example_data)
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
    print("---- Part 2 Start  ---------------")
    filename = 'example.txt'
    example_data = read_re(filename)
    example2 = second_part(example_data)
    if example2 != EXPECTED_2:
        exit()

    filename = 'input.txt'
    data = read_re(filename)
    solution = second_part(data)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(solution)
    pyperclip.copy(str(solution))
