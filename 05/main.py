import math
import re

def read_re(filename):
    data = {}
    first = True
    box = 1
    
    move = []

    for line in open(filename):
        if first:
            d = re.findall(f'\w+', line)
            if d == []:
                first = False
                continue
            data[box] = d
            box += 1
        else:
            numbers = list(map(int, re.findall(f'\d+', line)))
            if numbers == []:
                continue
            move.append(numbers)
    
        if box == 10:
            first = False

    
    return data, move

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

def first_part(data, move):
    
    for m in move:
        a = m[0]
        b = m[1]
        c = m[2]
        
        for i in range(a):
            
            if len(data[b]) ==  0:
                continue

            crate = data[b].pop(0)
            data[c].insert(0, crate)
            
            
    print("FIRST")
    for d in data:
        print(data[d])
            
def second_part(data, move):
    
    for m in move:
        a = m[0]
        b = m[1]
        c = m[2]
        
        try: 
            if a > len(data[b]):
                a = len(data[b])
        except:
            import code
            code.interact(local=locals())

        x = data[b][:a]
        data[b] = data[b][a:]
        if data[b] is None:
            data[b] = []

        data[c] = x +data[c]
            
    print("SECOND")
    for d in data:
        print(data[d])

if __name__ == '__main__':
    filename = 'day05.txt'
    data, move = read_re(filename)
    first_part(data, move)
    second_part(data, move)
