import math
import re
import numpy as np
import pyperclip
import itertools

def read_re(filename):
    data = []
    last = False
    pw = None
    for line in open(filename):
        line = line.removesuffix('\n')
        if line == "":
            last = True
            continue

        if last:
            pw = line
        else:
            data.append(line)

    return data

def rule_north(elf, grid):
#If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    y = elf[0]
    x = elf[1]

    if grid[y-1][x] == 0 and grid[y-1][x+1] == 0 and grid[y-1][x-1] == 0:
        return (y-1, x), True
    else: 
        return None, False

def rule_south(elf, grid):
#If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    y = elf[0]
    x = elf[1]

    if grid[y+1][x] == 0 and grid[y+1][x+1] == 0 and grid[y+1][x-1]==0:
        return (y+1, x), True
    else: 
        return None, False

def rule_west(elf, grid):
#If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    y = elf[0]
    x = elf[1]

    if grid[y][x-1] == 0 and grid[y-1][x-1] == 0 and grid[y+1][x-1]==0:
        return (y, x-1), True
    else: 
        return None, False

def rule_east(elf, grid):
#If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
    y = elf[0]
    x = elf[1]

    if grid[y][x+1] == 0 and grid[y-1][x+1] == 0 and grid[y+1][x+1]==0:
        return (y, x+1), True
    else: 
        return None, False

def check_neighbor(elf, grid):
    y = elf[0]
    x = elf[1]

    count = np.sum(grid[y-1:y+2, x-1:x+2])
    if count == 0:
        print('SOMETHING WENT WRONG')
    if count == 1:
        return True
    return False

def work(elf, grid, start_rule):
    if check_neighbor(elf, grid) is True:
        return None
    
    for r in range(4): 
        rule = (start_rule + r) % 4

        success = False
        if rule == 0:
            #print("try north")
            proposal, success = rule_north(elf, grid)
        elif rule == 1:
            proposal, success = rule_south(elf, grid)
        elif rule == 2:
            proposal, success = rule_west(elf, grid)
        elif rule == 3:
            proposal, success = rule_east(elf, grid)

        if success:
            return proposal
            
    #print("NO PROPOSAL")

EXPECTED_1 = 110
def first_part(data):
    for d in data:
        print(d)

    grid = np.zeros((len(data), len(data[0])), dtype=int)
    large_grid = np.zeros((grid.shape[0] * 2, grid.shape[1]*2), dtype=int)
    sub_y = math.trunc(grid.shape[0] / 2)
    sub_x = math.trunc(grid.shape[1] / 2)

    elves = []
    for y, d in enumerate(data):
        for x, value in enumerate(d):
            if value == '#':
                #grid[y][x] = 1
                elf = (sub_y+y,sub_x+x)
                large_grid[elf] = 1
                elves.append(elf)
                
    print(large_grid)
    print(elves)

    iterations = 10
    for i in range(iterations):
        proposals = []
        for elf in elves:
            prop = work(elf, large_grid, i)
            proposals.append(prop)

        count_moved = 0
        new_elves = []
        for elf, prop in zip(elves, proposals):
            if prop is None: # no elves around
                new_elves.append(elf)
            elif proposals.count(prop) > 1:
                new_elves.append(elf)
                continue
            else:
                count_moved += 1
                new_elves.append(prop)

        large_grid = np.zeros(large_grid.shape, dtype=int)
        for elf in new_elves:
            large_grid[elf] = 1
        elves = new_elves

        if count_moved == 0:
            break

        print(f"iteration  {i}") 
        print(large_grid)

    print(large_grid)
    sum_x = np.trim_zeros(np.sum(large_grid, axis=0))
    sum_y = np.trim_zeros(np.sum(large_grid, axis=1))

    print(sum_y)
    print(sum_x)

    solution = len(sum_x)*len(sum_y) - np.sum(large_grid)

    print(f"solution {solution}")
    return solution

EXPECTED_2 = 5031
def second_part(data):
    for d in data:
        print(d)

    grid = np.zeros((len(data), len(data[0])), dtype=int)
    large_grid = np.zeros((grid.shape[0] * 4, grid.shape[1]*4), dtype=int)
    sub_y = math.trunc(grid.shape[0] )
    sub_x = math.trunc(grid.shape[1] )

    elves = []
    for y, d in enumerate(data):
        for x, value in enumerate(d):
            if value == '#':
                #grid[y][x] = 1
                elf = (sub_y+y,sub_x+x)
                large_grid[elf] = 1
                elves.append(elf)
                
    print(large_grid)
    print(elves)

    iterations = 10000
    for i in range(iterations):
        proposals = []
        for elf in elves:
            prop = work(elf, large_grid, i)
            proposals.append(prop)

        count_moved = 0
        new_elves = []
        for elf, prop in zip(elves, proposals):
            if prop is None: # no elves around
                new_elves.append(elf)
            elif proposals.count(prop) > 1:
                new_elves.append(elf)
                continue
            else:
                count_moved += 1
                new_elves.append(prop)

        large_grid = np.zeros(large_grid.shape, dtype=int)
        for elf in new_elves:
            large_grid[elf] = 1
        elves = new_elves

        if count_moved == 0:
            break

        print(f"iteration  {i}   moved={count_moved}") 
        #print(large_grid)

    solution = i+1
#
#    print(large_grid)
#    sum_x = np.trim_zeros(np.sum(large_grid, axis=0))
#    sum_y = np.trim_zeros(np.sum(large_grid, axis=1))
#
#    print(sum_y)
#    print(sum_x)
#
#    solution = len(sum_x)*len(sum_y) - np.sum(large_grid)
#
    print(f"solution {solution}")
    return solution
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'example.txt'
    example_data= read_re(filename)
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
    
    #debug_get_next_coord()
    #exit()
    
    ## PART 2
    print("---- Part 2 Start  ---------------")
#    filename = 'example.txt'
#    example_data, example, pw = read_re(filename, pw)
#    example2 = second_part(example_data)
#    if example2 != EXPECTED_2:
#        exit()
#    else:
#        print("Part 2 example success")

    filename = 'input.txt'
    data = read_re(filename)
    solution = int(second_part(data ))

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(f"P2 Solution: {solution}")
    pyperclip.copy(str(solution))
    # guessed  51251.  Too low
    # guessed 114020.  Too high
    # guessed 148147.  Too high
    # Solution 55267
