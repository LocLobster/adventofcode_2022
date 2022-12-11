import math
import re
import numpy as np

def read_re(filename):
    data = []
    for line in open(filename):
        d = re.findall(f'\w+', line)
        data.append(d)
    
    return data

def valid(head, tail):
    hy = head[0]
    hx = head[1]

    ty = tail[0]
    tx = tail[1]
    
    if abs(hx - tx) <=1 and abs(hy-ty) <= 1:
        return True

    return False

def get_tail(head, tail):

    if valid(head, tail):
        return tail

    hy = head[0]
    hx = head[1]

    ty = tail[0]
    tx = tail[1]

    if hx - tx == 2  and hy - ty == 0:
        return (ty, tx+1)

    if hx - tx == -2  and hy - ty == 0:
        return (tail[0], tail[1]-1)

    if hy - ty == 2  and hx - tx == 0:
        return (tail[0]+1, tail[1])

    if hy - ty == -2  and hx - tx == 0:
        return (tail[0]-1, tail[1])

    new_tail = (tail[0] + 1, tail[1] + 1)
    if valid(head, new_tail):
        return new_tail
    new_tail = (tail[0] + 1, tail[1] - 1)
    if valid(head, new_tail):
        return new_tail
    new_tail = (tail[0] - 1, tail[1] + 1)
    if valid(head, new_tail):
        return new_tail
    new_tail = (tail[0] - 1, tail[1] - 1)
    if valid(head, new_tail):
        return new_tail

    import code
    code.interact(local=locals())
    return (0,0)

def step_head(direction, head):
    if direction == 'R':
        head = (head[0], head[1]+1)
    if direction == 'U':
        head = (head[0]+1, head[1])
    if direction == 'L':
        head = (head[0], head[1]-1)
    if direction == 'D':
        head = (head[0]-1, head[1])

    return head

def step(direction, head, tail):
    head = step_head(direction, head)
    tail = get_tail(head, tail)

    return head, tail

def first_part(data):
    grid_sz = 1000
    #grid = np.zeros((100,100))
    grid = np.zeros((grid_sz,grid_sz))

    head = (0,0)
    tail = (0,0)
    
    for d in data:
        direction = d[0]
        num_steps = d[1]
        
        for s in range(int(num_steps)):
            head, tail = step(direction, head, tail)
            grid[tail] = True


    solution = int(grid.sum())
    print(solution)


def second_part(data):
    grid_sz = 1000
    grid = np.zeros((grid_sz,grid_sz))

    knots = []
    for i in range(10):
        knots.append((0,0))

    for d in data:
        direction = d[0]
        num_steps = d[1]
        
        for s in range(int(num_steps)):
            for k in range(len(knots)-1):            
                tail = knots[k+1]

                if k == 0:
                    knots[k] = step_head(direction, knots[k])
                
                tail = get_tail(knots[k], tail)
                knots[k+1] = tail

            grid[knots[9]] = True

    #print(np.flipud(grid))
    solution = int(grid.sum())
    print(solution)


if __name__ == '__main__':
    filename = 'input.txt'
    #filename = 'example.txt'
    #filename = 'example2.txt'
    data = read_re(filename)
    #first_part(data)
    second_part(data)