import math
import re
import numpy as np
import pyperclip
import itertools

def read_re(filename):
    data = []

    for line in open(filename):
        d = line.strip()
        data.append(d)

    return data

def get_next_grid(grid, bliz, start, end):
    new_grid = np.zeros(grid.shape, dtype=int)
    new_grid[:,0].fill(8)
    new_grid[0,:].fill(8)
    new_grid[:,grid.shape[1]-1].fill(8)
    new_grid[grid.shape[0]-1,:].fill(8)

    new_grid[start] = 0
    new_grid[end] = 0

    new_bliz = []
    for b in bliz:
        y = b[0][0]
        x = b[0][1]
        dir = b[1]
        if b[1]  == '>':
            if x == grid.shape[1] - 2:
                x = 1
            else:
                x += 1
        if b[1]  == 'v':
            if y == grid.shape[0] - 2:
                y = 1
            else:
                y += 1
        if b[1]  == '<':
            if x == 1:
                x = grid.shape[1]-2
            else:
                x -= 1
        if b[1]  == '^':
            if y == 1:
                y = grid.shape[0] - 2
            else:
                y -= 1

        new_grid[(y,x)] = 1
        new_bliz.append(((y,x), dir))

    return new_grid, new_bliz

def get_safe(grid, start, end):
    (y_max, x_max) = grid.shape
    np_safe = np.where(grid[1:y_max-1, 1:x_max-1] == 0)

    safe = set()
    for i in range(len(np_safe[0])):
        y = np_safe[0][i] + 1
        x = np_safe[1][i] + 1
        safe.add((y,x))

    safe.add(start)
    safe.add(end)
    return safe

def get_locations(safe, current):
    next_current = set()
    for c in current:
        
        checklist = []
        checklist.append((c[0],   c[1]+1))
        checklist.append((c[0]+1, c[1]))
        checklist.append((c[0],   c[1]))
        checklist.append((c[0]-1, c[1]))
        checklist.append((c[0],   c[1]-1))

        for check in checklist:
            if check in safe:
                next_current.add(check)

    return next_current

def first_part(data):
    y_max  = len(data)
    x_max =  len(data[0])
    grid = np.zeros((y_max, x_max), dtype=int)
    bliz = []
    start = None
    end = None
    for y, d in enumerate(data):
        for x, val in enumerate(d):
            if y == 0 and val == '.':
                    start = (y,x)
            elif y == y_max-1 and val == '.':
                    end = (y,x)
            elif val == "#":
                grid[(y,x)] = 8
            elif val == ">":
                grid[(y,x)] = 1
                bliz.append([(y,x), '>'])
            elif val == "v":
                grid[(y,x)] = 2
                bliz.append([(y,x), 'v'])
            elif val == "<":
                grid[(y,x)] = 3
                bliz.append([(y,x), '<'])
            elif val == "^":
                grid[(y,x)] = 4
                bliz.append([(y,x), '^'])

    safe = set()
    current = set()
    current.add(start)
    for i in range(2500):
        grid, bliz = get_next_grid(grid, bliz, start, end)
        safe = get_safe(grid, start, end)
        current = get_locations(safe, current)

        if end in current:
            break

    solution = i+1
    print(f"Solution {solution}")

    return solution

def second_part(data):
    y_max  = len(data)
    x_max =  len(data[0])
    grid = np.zeros((y_max, x_max), dtype=int)
    bliz = []
    start = None
    end = None
    for y, d in enumerate(data):
        for x, val in enumerate(d):
            if y == 0 and val == '.':
                    start = (y,x)
            elif y == y_max-1 and val == '.':
                    end = (y,x)
            elif val == "#":
                grid[(y,x)] = 8
            elif val == ">":
                grid[(y,x)] = 1
                bliz.append([(y,x), '>'])
            elif val == "v":
                grid[(y,x)] = 2
                bliz.append([(y,x), 'v'])
            elif val == "<":
                grid[(y,x)] = 3
                bliz.append([(y,x), '<'])
            elif val == "^":
                grid[(y,x)] = 4
                bliz.append([(y,x), '^'])

    # Go to end
    safe = set()
    current = set()
    current.add(start)
    for i in range(2500):
        grid, bliz = get_next_grid(grid, bliz, start, end)
        safe = get_safe(grid, start, end)
        current = get_locations(safe, current)
        if end in current:
            break
    sol1 = i+1

    # End to start
    safe = set()
    current = set()
    current.add(end)
    for i in range(2500):
        grid, bliz = get_next_grid(grid, bliz, start, end)
        safe = get_safe(grid, start, end)
        current = get_locations(safe, current)
        if start in current:
            break
    sol2 = i+1

    # Back to end
    safe = set()
    current = set()
    current.add(start)
    for i in range(2500):
        grid, bliz = get_next_grid(grid, bliz, start, end)
        safe = get_safe(grid, start, end)
        current = get_locations(safe, current)
        if end in current:
            break
    sol3 = i+1

    print(sol1, sol2, sol3)
    solution = sol1 + sol2 + sol3 
    print(f"Solution {solution}")

    return solution
                
if __name__ == '__main__':
    EXPECTED_1 = 18
    EXPECTED_2 = 54

    print("###################new run###################")
    filename = 'example.txt'
    example_data = read_re(filename)
    example1 = first_part(example_data)
    if example1 != EXPECTED_1:
        exit()
    print('Part 1 Example success')
    
    filename = 'input.txt'
    data = read_re(filename)
    solution = first_part(data)

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
    print('Part 2 Example success')

    filename = 'input.txt'
    data = read_re(filename)
    solution = second_part(data)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(f"P2 Solution: {solution}")
    pyperclip.copy(str(solution))
