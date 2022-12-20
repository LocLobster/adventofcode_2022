import math
import copy
import re
import numpy as np
import pyperclip
import itertools

def read_re(filename):
    data = []

    for line in open(filename):
        d = list(map(int, re.findall(f'-?\d+', line)))[0]
        data.append(d)

    return data

def first_part(data):
    work_data = copy.deepcopy(data)
    locator = list(range(len(data)))
   
    length = len(data)
    for i in range(length):
        index = 0
        index = locator.index(i)

        value = work_data[index]
        if value == 0:
            continue
        new_loc = value + index
            
        if new_loc > length:
            new_loc = new_loc%(length-1)
        
        if new_loc < 0:
            new_loc = (new_loc%(length-1) - (length-1))

        if value < 0 and new_loc == 0:
            new_loc = length-1

        work_data.pop(index)
        work_data.insert(new_loc, value)
        x = locator.pop(index)
        locator.insert(new_loc, x)

    zero_loc = work_data.index(0)
    solution = 0 
    nums = [1000, 2000, 3000]
    for num in nums:
        print(f"  {num}  {work_data[(zero_loc+num)%length]}")
        solution += work_data[(zero_loc+num)%length]

    print(solution)
    return solution

def second_part(data, key):
    work_data = [key * d for d in data]
    locator = list(range(len(data)))
   
    length = len(data)
    print(f"length = {length}")
    for _ in range(10):
        for i in range(length):
            index = 0
            index = locator.index(i)

            value = work_data[index]
            if value == 0:
                continue
            new_loc = value + index

            if new_loc > length:
                new_loc = new_loc%(length-1)

            if new_loc < 0:
                new_loc = (new_loc%(length-1) - (length-1))

            if value < 0 and new_loc == 0:
                new_loc = length-1

            work_data.pop(index)
            work_data.insert(new_loc, value)
            x = locator.pop(index)
            locator.insert(new_loc, x)

    zero_loc = work_data.index(0)
    solution = 0 
    nums = [1000, 2000, 3000]
    for num in nums:
        print(f"  {num}  got:{work_data[(zero_loc+num)%length]}")
        solution += work_data[(zero_loc+num)%length]

    print(solution)
    return solution
                
if __name__ == '__main__':
    EXPECTED_1 = 3
    EXPECTED_2 = 1623178306

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
    print(f"Solution {solution}")
    pyperclip.copy(str(solution))
    # guessed 8192. too low
    # guessed 11651. too low
    # guessed 11836. too low
    # guessed 15289. too low
    # Solution 19070
    
    ## PART 2
    print("---- Part 2 Start  ---------------")
    filename = 'example.txt'
    example_data = read_re(filename)
    example2 = second_part(example_data, key=811589153)
    if example2 != EXPECTED_2:
        exit()

    filename = 'input.txt'
    data = read_re(filename)
    solution = second_part(data, key=811589153)
    # solution = 14773357352059

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(f"Solution {solution}")
    pyperclip.copy(str(solution))
