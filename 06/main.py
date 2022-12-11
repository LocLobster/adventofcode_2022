import math
import re
import numpy as np

def read_re(filename):
    data = []
    for line in open(filename):
        d = re.findall(f'\w+', line)
        data.append(d)
    return data

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

def solution(data, num_unique):
    for d in data:
        for i in range(len(d[0])-num_unique):
            packet = set(d[0][i:i+num_unique])
            
            if len(packet) == num_unique:
                print(i+num_unique)
                return


if __name__ == '__main__':
    filename = 'input.txt'
    data = read_re(filename)
    solution(data, 4)
    
    # second part
    solution(data, 14)