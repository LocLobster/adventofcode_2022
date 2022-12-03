import os
import re
import math

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    data = []
    for line in lines: 
        l = line.strip()
        spl = l.split()
        data.append(l)

    return data

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def get_value(c):
    x = ord(c[0])
    a = ord('a')
    z = ord('z')
    A = ord('A')
    Z = ord('Z')
    if x >= a and x <= z:
        return x - a + 1

    return x - A + 27

def first_part(data):
    acc = 0
    for d in data:
        length = len(d)

        w1 = d[0:math.trunc(length/2)]
        w2 = d[math.trunc(length/2):]
        
        x = intersection(w1, w2)

        val = get_value(x)
        acc += val
    print(acc)

def second_part(data):
    length = len(data)
    smaller = math.trunc(length /3)
    acc = 0
    for l in range(smaller):
        a = data[3*l + 0]
        b = data[3*l + 1]
        c = data[3*l + 2]
        
        x = intersection(a, b)
        y = intersection(x, c)
        
        val = get_value(y)

        acc  += val
    print(acc)

if __name__ == '__main__':
    data = read_file('day03.txt')
    
    first_part(data)
    
    second_part(data)