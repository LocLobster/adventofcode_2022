import os
import re

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    data = {}
    
    for line in lines: 
        l = line.strip()
        spl = l.split()

        print(f"{l}")
        print(f"{spl}")

        import code
        code.interact(local=locals())

    return data

def first_part(data):
    pass

def second_part(data):
    pass


if __name__ == '__main__':
    data = read_file('input.txt')
    
    exit()
    first_part(data)
    
    exit()
    second_part(data)