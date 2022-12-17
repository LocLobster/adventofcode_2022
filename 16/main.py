import math
import re
import numpy as np
import pyperclip
import itertools
import random

EXPECTED_1 = 1651
EXPECTED_2 = 29

def read_re(filename):
    data = {}
    pressure = {}
    for line in open(filename):
        d = re.findall(f'-?\d+', line)
        l = line.strip().split(' ')
        print(l)

        lead = []
        length = len(l)
        for i in range(length-9):
            lead.append(l[9+i][0:2])

        data[l[1]] =  lead
        pressure[l[1]] = int(d[0])
    return data, pressure

def get_distance(data, start):

    nodes = {}
    distance = 0

    current_leads = data[start]
    while len(current_leads) > 0:
        next_leads = []
        distance += 1
        for cl in current_leads:
            if cl in nodes:
                continue
            else:
                nodes[cl] = distance
                next_leads += data[cl]

        current_leads = next_leads

    print(nodes)
    return(nodes)

    
def get_grid(data):
    grid = np.zeros((len(data), len(data)), dtype=int)

def get_permutations(iterable, distance_map, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])

    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]

                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

def get_perms(sorted_map, location='AA', nodes=[], level=0):
    print('get_perms')
    print(sorted_map[location])

    d = sorted_map[location]
    d = dict((k, v) for k, v in d.items() if v <= 5)

    if level < 3:
        for k, v in d.items():
            k = get_perms(sorted_map, location=k, nodes=nodes+[k], level=level+1)
    else:
        return d
    

def first_part(data, pressure):
    positive = []
    sorted_pressure = {k: v for k, v in sorted(pressure.items(), reverse=True, key=lambda item: item[1])}

    for p in sorted_pressure:
        print(pressure[p])
        if pressure[p] > 0:
            positive.append(p)

    distance_map = {}
    for d in data:
        result = get_distance(data, d)
        distance_map[d] = result

    random.shuffle(positive)

    max_pressure = 0
    time_limit = 30
    # 259,440,000 permutations 
    permuations = itertools.permutations(positive, 8)
    num_perms = 0
    
    ## Best perm so far
    # ('ZZ', 'AO', 'IF', 'EB', 'UH', 'BH', 'KZ', 'RW', 'WG', 'IS', 'NH') 1601
    # ('ZZ', 'AO', 'IF', 'EB', 'UH', 'BH', 'NH', 'IS', 'WG', 'RW', 'KZ') 1601
    # ('SI', 'ZZ', 'AO', 'IF', 'EB', 'UH', 'BH', 'WG', 'IP', 'MT')  1614
    # ('ZZ', 'AO', 'IF', 'EB', 'UH', 'ZQ', 'BH', 'WG', 'IP', 'KZ') 1630
    # ('SI', 'ZZ', 'AO', 'IF', 'EB', 'UH', 'ZQ', 'BH', 'KZ')  1614
    # ('SI', 'ZZ', 'AO', 'IF', 'EB', 'UH', 'ZQ', 'BH', 'KZ')  1638 correct answer. KZ isn't required

    #trying different locations first
    best_perm = []
    best_perm_last = None
    total_pressure = 0

    for perm in permuations:
        num_perms += 1
        if num_perms % 20000 == 0:
            print(f"{num_perms} {max_pressure} {best_perm} {best_perm_last}")

        # Reversed permuation since perms vary the last values more.  But adjusting hte first values produce better variability 
        total_pressure, _, node = run_permuation(perm[::-1], distance_map, pressure)

        if total_pressure > max_pressure:
            max_pressure = total_pressure
            best_perm = perm[::-1]
            best_perm_last = node

    solution = max_pressure
    print(solution)
    print('best perm')
    print(best_perm)
    return solution

def run_permuation(perm, distance_map, pressure, start_location='AA', time_limit=30):

    total_pressure = 0 
    my_pressure = 0 
    my_timer = 0 
    my_location = start_location

    for node in perm:
        movement_time = distance_map[my_location][node]
        my_timer += movement_time
        if my_timer < time_limit:
            my_timer += 1
            total_pressure += (movement_time+1) * my_pressure
            my_pressure += pressure[node]
        else:
            total_pressure += (time_limit - (my_timer - movement_time)) * my_pressure
            break
        
        #print(f"location={my_location} pressure={total_pressure} timer={my_timer}")
        my_location = node

    time_left = time_limit - my_timer
    if my_timer < time_limit:
        total_pressure += (time_limit - my_timer) * my_pressure

    return total_pressure, time_left, node

def second_part(data, pressure, plan):
    positive = []
    for p in pressure:
        print(pressure[p])
        if pressure[p] > 0:
            positive.append(p)

    distance_map = {}
    for d in data:
        result = get_distance(data, d)
        distance_map[d] = result

    remaining = list( set(positive) - set(plan))
    print(f"remaining {remaining}")
    
    plan_set = set(positive)

    total_max_pressure = 0
    combos = itertools.combinations(plan, math.trunc((len(plan_set))/2))
    my_best = None
    elephant_best = None
    for combo in combos:
        my_set = set(combo)
        elephant_set = plan_set - my_set

        elephant = tuple(elephant_set)

        my_max_pressure = 0
        for my_perm in itertools.permutations(combo):
            my_pressure, my_time_left, _ = run_permuation(my_perm, distance_map, pressure, time_limit=26)
            if my_pressure > my_max_pressure:
                my_max_pressure = my_pressure
                my_best_perm = my_perm
                my_best_time_left = my_time_left

        elephant_max_pressure = 0
        for elephant_perm in itertools.permutations(elephant):
            elephant_pressure, elephant_time_left, _ = run_permuation(elephant_perm, distance_map, pressure, time_limit=26)
            if elephant_pressure > elephant_max_pressure:
                elephant_max_pressure = elephant_pressure
                elephant_best_perm = elephant_perm
                elephant_best_time_left = my_time_left

        both_pressures = my_max_pressure + elephant_max_pressure
        if both_pressures > total_max_pressure:
            total_max_pressure = both_pressures
            my_best = my_best_perm
            elephant_best = elephant_best_perm
            my_remaining_time = my_best_time_left
            elephant_remaining_time = elephant_best_time_left
    
        print(total_max_pressure)
        print(my_best)
        print(elephant_best)
        print(my_remaining_time)
        print(elephant_remaining_time)
        
    pass
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'example.txt'
    example_data, example_pressures = read_re(filename)
    example1 = first_part(example_data, example_pressures)
    if example1 != EXPECTED_1:
        exit()
    
    filename = 'input.txt'
    data, pressures = read_re(filename)
    solution = first_part(data, pressures)

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(solution)
    pyperclip.copy(str(solution))
    
    ## PART 2
    example_plan = ('BB', 'CC', 'DD', 'EE', 'HH', 'JJ')
    example2 = second_part(example_data, example_pressures, example_plan)
    if example2 != EXPECTED_2:
        exit()

    plan = ('SI', 'ZZ', 'AO', 'IF', 'EB', 'UH', 'ZQ', 'BH', 'KZ')
    solution = second_part(data, pressures, plan)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(solution)
    pyperclip.copy(str(solution))


    # Guessed 1673. Too low
    # Guessed 1878. Too low
    # Guessed 2392. Too low
    # 2400 correct answer