import math
import re

def read_re(filename):
    data = []
    for line in open(filename):
        d = re.findall(f'\w+', line)
        data.append(d)
    

    return data

#def read_numbers(filename):
#    data = []
#    for line in open(filename):
#        d = list(map(int, re.findall(f'\w+', line)))
#        data.append(d)
#    return data

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
    for d in data:
        print(d)
        pass

def second_part(data):
    pass


if __name__ == '__main__':
    filename = 'input.txt'
    data = read_re(filename)
    first_part(data)
    #second_part(data)