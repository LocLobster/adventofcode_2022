import math
import re
import numpy as np
import pyperclip

EXPECTED_1 = 24
EXPECTED_2 = 93

def read_re(filename):
    data = []

    for line in open(filename):
        reg = re.findall(f'\S+,\S+', line)

        d = []
        for r in reg:
            rr = list(map(int, r.split(',')))
            d.append((rr[1], rr[0]))
        data.append(d)

    return data

def shift(input):
    global min_x
    global min_y
    return (input[0]-min_y, input[1]-min_x)

def check(spot, grid):
    s = grid.shape

    if spot[0] < 0  or spot[0] >= s[0] or spot[1] < 0 or spot[1] >= s[1]:
        return False
    return True

def find_next(spot, grid):
    new_spot = spot

    down_spot = (spot[0]+1, spot[1])
    dl_spot = (spot[0]+1, spot[1]-1)
    dr_spot = (spot[0]+1, spot[1]+1)
    if check(down_spot, grid) is False:
        return False

    # empty. go down
    if grid[down_spot] == 0:
        new_spot = find_next(down_spot, grid)
    else:
        # go down left
        if check(dl_spot, grid) is False:
            return False
        if grid[dl_spot] == 0:
            new_spot = find_next(dl_spot, grid)
        else:
            # go down right
            if check(dr_spot, grid) is False:
                return False
            if grid[dr_spot] == 0:
                new_spot = find_next(dr_spot, grid)

    return new_spot

def first_part(data):
    global min_x
    global min_y

    allx =[]
    ally =[0]
    for d in data:
        print(d)
        for point in d:
            ally.append(point[0])
            allx.append(point[1])
    
    min_x = min(allx)
    max_x = max(allx) + 1
    min_y = min(ally)
    max_y = max(ally) +1

    grid = np.zeros((max_y-min_y, max_x-min_x), dtype=int)

    start = shift( (0,500) )
    for d in data:
        for i in range(len(d)-1):
            p1 = shift(d[i])
            p2 = shift(d[i+1])
            
            ydiff = abs(p1[0] - p2[0])
            xdiff = abs(p1[1] - p2[1])
            if ydiff == 0:
                xx = min(p1[1], p2[1])
                for i in range(xdiff+1):
                    grid[(p1[0], xx+i)] = 1
            if xdiff == 0:
                yy = min(p1[0], p2[0])
                for i in range(ydiff+1):
                    grid[(yy+i, p1[1])] = 1

    print(grid)

    acc = 0 
    # Start sand
    for _ in range(50000):
        spot = find_next(start, grid)

        if spot is False:
            break
        acc  += 1
        grid[spot] = 8

        if spot == start:
            break

    print(grid)
    return acc

def second_part(data):
    allx =[]
    ally =[0]
    for d in data:
        print(d)
        for point in d:
            ally.append(point[0])
            allx.append(point[1])
    
    min_x = min(allx)
    max_x = max(allx) + 1
    max_y = max(ally)

    data.append([(max_y+2, min_x-500), (max_y+2, max_x+500)])
    sol = first_part(data)
    return sol
                
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
