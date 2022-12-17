import math
import re
import numpy as np
import pyperclip

EXPECTED_1 = 26
EXPECTED_2 = 56000011

def read_re(filename):
    data = []

    for line in open(filename):
        d = re.findall(r'x=\S+, y=\S?\d+', line)
        out_list = []
        for dd in d:
            ddd = dd.split(', ')
            out = (int(ddd[0][2:]), int(ddd[1][2:]))
            out_list.append(out)
        data.append(out_list)

    return data

def distance(a, b):
    return abs(b[1] - a[1])  + abs(b[0] - a[0])

def first_part(data, y):
    dists = []
    max_dist = 0
    min_x = 999999999999
    max_x = -99999999900
    for d in data:
        dist = distance (d[0], d[1])
        dists.append(dist)
        if dist > max_dist:
            max_dist = dist
        if d[0][0] < min_x:
            min_x = d[0][0]
        if d[0][1] > max_x:
            max_x = d[0][1]

    acc = 0 
    for x in range(min_x-max_dist, max_x+max_dist):
        for d, dist in zip(data, dists):
            my_dist = distance(d[0], (x,y))
            if my_dist <= dist:
                acc += 1
                break
    
    # remove beacons
    beacons = []
    for d in data:
        if d[1][1] == y:
            beacons.append(d[1])

    for b in set(beacons):
        for d, dist in zip(data, dists):
            my_dist = distance(d[0], b)
            if my_dist <= dist:
                acc -= 1
                break

    solution = acc
    print(solution)
    return solution

def get_points(point, distance):
    x = point[0]
    y = point[1]

    for d in range(distance):
        xx = x - d
        yy = y - (distance - d)
        yield (xx, yy)

    for d in range(distance):
        yy = y - d
        xx = x - (distance - d)
        yield (xx, yy)


def second_part(data, search_area):
    dists = []
    for d in data:
        dist = distance (d[0], d[1])
        dists.append(dist)

    for d, dist in zip(data, dists):
        for p in get_points(d[0], dist+1):
            if p[0] < search_area and p[1] < search_area and p[0]>=0 and p[1]>=0:
                found = True
                for nested_d, nested_dist in zip(data, dists):
                    my_dist = distance(nested_d[0], p)
                    if my_dist <= nested_dist:
                        found = False
                        break
                    
                if found:
                    print(f"x={p[0]} y={p[1]}")
                    solution = p[0]*4000000+p[1]
                    print(solution)
                    return solution
                
if __name__ == '__main__':
    print("###################new run###################")
    print('example')
    filename = 'example.txt'
    example_data = read_re(filename)
    example1 = first_part(example_data, y=10)
    if example1 != EXPECTED_1:
        exit()
    
    filename = 'input.txt'
    data = read_re(filename)
    solution = first_part(data, y=2000000)

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(solution)
    print("************************************")
    pyperclip.copy(str(solution))
    
    ## PART 2
    example2 = second_part(example_data, search_area=20)
    if example2 != EXPECTED_2:
        exit()

    solution = second_part(data, search_area=4000000)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(solution)
    print("---------------------------------")
    pyperclip.copy(str(solution))
