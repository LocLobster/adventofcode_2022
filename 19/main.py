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
                
# ore, clay, obsid, geode
def run(time_passed, materials, robots, next_robot, d, time_limit=24):
    make_clay = False
    make_ore = False
    make_obsid = False
    make_geode = False

    while(time_passed<time_limit):
        time_passed += 1

        if next_robot == 'R':  # ore
            if materials[0] >= d[1]:
                materials[0] -= d[1]
                make_ore = True
        elif next_robot == 'C': # clay
            if materials[0] >= d[2]:
                materials[0] -= d[2]
                make_clay = True
        elif next_robot == 'O':  # obsidian
            if materials[0] >= d[3] and materials[1] >= d[4]:
                materials[0] -= d[3]
                materials[1] -= d[4]
                make_obsid = True
        elif next_robot == 'G': # geode
            if materials[0] >= d[5] and materials[2] >= d[6]:
                materials[0] -= d[5]
                materials[2] -= d[6]
                make_geode = True

        materials += robots

        if make_ore == True:
            robots[0] += 1
            break
        if make_clay == True:
            robots[1] += 1
            break
        if make_obsid == True:
            robots[2] += 1
            break
        if make_geode == True:
            robots[3] += 1
            break
        
    if time_passed >= time_limit:
        return materials[3]

    # Some optimization
    next_list = []
    # Don't create more ore robots if we get more ore every turn than the cost of the most expensive robot
    if robots[0] < max(d[2], d[3], d[5]):
        next_list += ['R']
    if robots[1] < (d[4])/2+1:
        next_list += ['C']

    # Time to make clay robot:

    # Only consider making obsidian robot if there is a clay robot
    if(robots[1] > 0):  
        ttm_clay_robot  = (d[3] - materials[0])/robots[0]
        ttm_obsid_robot = max( [math.trunc((d[3]-materials[0])/robots[0]), math.trunc((d[4]-materials[1])/robots[1]) ])
    
        leftover_ore =  robots[0] * ttm_clay_robot - d[3]
        ttm_clay_and_obsid = max( [math.trunc((d[3]-leftover_ore)/robots[0]), math.trunc((d[4]-materials[1])/(robots[1]+1)) ])
        ttm_clay_and_obsid += ttm_clay_robot

        if ttm_obsid_robot <= ttm_clay_and_obsid:
            next_list += ['O']

    # Only consider making obsidian robot if there is an obsidian robot
    if(robots[2] > 0):
        ttm_obsid_robot = max( [math.trunc((d[3]-materials[0])/robots[0]), math.trunc((d[4]-materials[1])/robots[1]) ])
        ttm_geode_robot = max( [math.trunc((d[5]-materials[0])/robots[0]), math.trunc((d[6]-materials[2])/robots[2]) ])
    
        leftover_ore =  robots[0] * ttm_clay_robot - d[3]
        ttm_obsid_and_geode = max( [math.trunc((d[5]-leftover_ore)/robots[0]), math.trunc((d[6]-materials[2])/(robots[2]+1)) ])
        ttm_obsid_and_geode += ttm_obsid_robot

        if ttm_geode_robot <= ttm_obsid_and_geode:
            next_list += ['G']
        #next_list += ['G']

    # If you already have a few geode robots.  Don't make any more clay or ore robots. Too late now to be ramping.
    if (robots[3]>3):
        next_list = ['O', 'G']

    my_max = 0
    for next in next_list:
        result = run(time_passed, np.copy(materials), np.copy(robots), next, d, time_limit)
        if result > my_max:
            my_max = result

    return my_max
    
def first_part(data):

    geode_list = []
    for d in data:
        result_c = run(0, np.array([0,0,0,0]), np.array([1,0,0,0]),'C', d)
        result_r = run(0, np.array([0,0,0,0]), np.array([1,0,0,0]),'R', d)

        geode_list.append(max(result_c, result_r) * d[0])
        print(f"Quality: {geode_list}")
        
    print(geode_list)
    solution = sum(geode_list)
    print(f"solution {solution}")
    
    return solution

def second_part(data):
    geode_list = []
    max_blueprints = 3
    num_blueprints = 0
    for d in data:
        num_blueprints += 1
        if num_blueprints > max_blueprints:
            break
        print(d)
        result_c = run(0, np.array([0,0,0,0]), np.array([1,0,0,0]),'C', d, time_limit=32)
        result_r = run(0, np.array([0,0,0,0]), np.array([1,0,0,0]),'R', d, time_limit=32)
        
        print(max(result_c, result_r))
        geode_list.append(max(result_c, result_r))
        print(f"GEODES {geode_list}")
        
    print(geode_list)
    
    solution = np.prod(geode_list)
    print(f"solution {solution}")
    return solution
                
if __name__ == '__main__':
    EXPECTED_1 = 33
    EXPECTED_2 = 58

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
    print(f"solution: {solution}")
    pyperclip.copy(str(solution))
    # Guessed 67
    # Guessed 71
    # Solution 1144
    
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
