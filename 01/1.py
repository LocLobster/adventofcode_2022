#!/bin/python3

import os

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    elf_num = 1
    data = {}
    acc = 0

    for l in lines: 
        num = l.strip()
        if num == "":
            data[elf_num] = acc
            acc = 0
            elf_num += 1
        else:
            acc += int(num)

    return data

def get_highest(data):
    high_cal = 0 
    high_elf = 0
    
    for i, cal in data.items():
        if cal > high_cal:
            high_cal = cal
            high_elf = i
    
    return high_elf, high_cal

data = read_file('input.txt')

total = 0
for i in range(0,3):
    elf, cal = get_highest(data)

    print(elf)
    print(cal)

    total += cal

    data.pop(elf)

print(total)
