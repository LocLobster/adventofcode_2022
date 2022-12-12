import math
import re
import numpy as np
import pyperclip

EXPECTED_1 = 31
EXPECTED_2 = 29

def read_re(filename):
    data = []

    lines = []
    y = 0 
    
    start = (0, 0)
    for line in open(filename):
        lines.append(line)
        d = []
        x = 0
        for l in line:

            if l == 'S':
                d.append(0)
                start=(y, x)
            elif l == 'E':
                d.append(ord('z') - ord('a'))
                end=(y, x)
            elif l == '\n':
                break
            else:
                d.append(ord(l) - ord('a'))
            x += 1
        data.append(d)

        y += 1

    return data, start, end

def check_valid(loc, check, data):
    max_y = len(data)
    max_x = len(data[0])

    y = check[0]
    x = check[1]

    if y >= max_y:
        return False
    if x >= max_x:
        return False
    if x < 0:
        return False
    if y < 0:
        return False

    if data[check] - data[loc] > 1:
        return False

    return True

def first_part(input_data, start, end):
    iterations = 500

    max_y = len(input_data)
    max_x = len(input_data[0])

    data = np.array(input_data)
    dist = iterations * np.ones((max_y, max_x), dtype=int)
    dist[start] = 0

    prev_locations = [start]
    for _ in range(iterations):
        locs = []
        for loc in prev_locations:
            #up
            check = (loc[0]-1, loc[1])
            result = check_valid(loc, check, data)
            if result:
                my_distance = dist[loc] + 1
                if my_distance < dist[check]:
                    dist[check] = my_distance
                    locs.append(check)
            
            #down
            check = (loc[0]+1, loc[1])

            result = check_valid(loc, check, data)
            if result:
                my_distance = dist[loc] + 1
                if my_distance < dist[check]:
                    dist[check] = my_distance
                    locs.append(check)
            #left
            check = (loc[0], loc[1]-1)

            result = check_valid(loc, check, data)
            if result:
                my_distance = dist[loc] + 1
                if my_distance < dist[check]:
                    dist[check] = my_distance
                    locs.append(check)

            #right
            check = (loc[0], loc[1]+1)

            result = check_valid(loc, check, data)
            if result:
                my_distance = dist[loc] + 1
                if my_distance < dist[check]:
                    dist[check] = my_distance
                    locs.append(check)
        
        prev_locations = locs
        if len(locs) == 0:
            break

    return dist[end]

def second_part(input_data, end):
    data = np.array(input_data)
    starts = np.where(data==0)
    
    min_distance = 9999999999
    for y, x in zip(starts[0], starts[1]):
        start = (y, x)
        distance = first_part(input_data, start, end)
        if distance < min_distance:
            min_distance = distance

    return min_distance
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'example.txt'
    example_data, start, example_end = read_re(filename)
    example1 = first_part(example_data, start, example_end)

    if example1 != EXPECTED_1:
        exit()
    
    filename = 'input.txt'
    data, start, end = read_re(filename)
    solution = first_part(data, start, end)

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(solution)
    pyperclip.copy(str(solution))
    
    example2 = second_part(example_data, example_end)
    if example2 != EXPECTED_2:
        exit()

    solution = second_part(data, end)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(solution)
    pyperclip.copy(str(solution))