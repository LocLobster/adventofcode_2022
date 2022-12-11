import math
import re
import numpy as np

def read_re(filename):
    data = []

    for line in open(filename):
        d = re.findall(f'\S+', line)
        data.append(d)
    
    return data

def first_part(data):
    cycle = []
    cycle.append(0)
    reg = 1
    
    for d in data:
        if d[0] == 'addx':
            cycle.append(reg)
            cycle.append(reg)
            reg += int(d[1])
        else:
            cycle.append(reg)


    xlist = [20, 60, 100, 140, 180, 220]

    solution =0
    for x in xlist:
        print(f"{x}  {cycle[x]} {cycle[x]*x}")
        solution += cycle[x]*x


    a = 20*cycle[20] 
    b = 60*cycle[20] 
    c = 100*cycle[20] 
    d = 140*cycle[20] 
    e = 20*cycle[20] 
    
    print(cycle)
    print(solution)

    return cycle


def second_part(data):
    cycle = []
    reg = 1

    for d in data:
        if d[0] == 'addx':
            cycle.append(reg)
            cycle.append(reg)
            reg += int(d[1])
        else:
            cycle.append(reg)

    grid = np.zeros(6*40, dtype=int)
    for i in range(6*40):
        c = cycle[i]
        if abs(c-(i%40)) <=1:
            grid[i] = 8

    out = grid.reshape((6,-1))

    for row in out:
        line = ""
        for r in row:
            if r==8:
                line += "#"
            else:
                line += " "
        print(line)

                
if __name__ == '__main__':
    filename = 'input.txt'
    #filename = 'example.txt'
    data = read_re(filename)
    #first_part(data)
    second_part(data)