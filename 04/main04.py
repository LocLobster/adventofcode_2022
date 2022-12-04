import math
import re

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    data = []
    
    for line in lines: 
        l = line.strip()
        spl = l.split(',')

        spl0 = spl[0].split('-')
        spl1 = spl[1].split('-')

        data.append((spl0[0], spl0[1], spl1[0], spl1[1]))
        
    return data

def first_part(data):
    acc = 0
    for d in data:
        first =  list(range(int(d[0]), int(d[1])+1))
        second = list(range(int(d[2]), int(d[3])+1))
        
        x = set(first)
        y = list(x.intersection(second))
        y.sort()

        if y == first or y == second:
            acc += 1

    print(acc)

def second_part(data):
    acc = 0
    for d in data:
        first =  list(range(int(d[0]), int(d[1])+1))
        second = list(range(int(d[2]), int(d[3])+1))
        
        x = set(first)
        y = list(x.intersection(second))
        
        if len(y) > 0:
            acc += 1

    print(acc)


if __name__ == '__main__':
    data = read_file('day04.txt')
    first_part(data)
    
    second_part(data)