import math
import re
import numpy as np
import pyperclip
import itertools

RIGHT = 0
DOWN =  1
LEFT =  2
UP =    3

def read_re(filename):
    data = []
    last = False
    pw = None
    for line in open(filename):
        line = line.removesuffix('\n')
        if line == "":
            last = True
            continue

        if last:
            pw = line
        else:
            data.append(line)

    return data, pw

def move_in_array(arr, dir, index, step):
    for _ in range(step):
        next = None
        for i in range(1, len(arr)):
            next = (index+i*dir)%len(arr)
            val = arr[next]
            if val == 0:
                continue
            break
        val = arr[next]
        if val == 1:
            index = next 
        elif val == 2:
            break
    return index

def next_loc(grid, facing, x, y, step):
    row = grid[y,:]
    col = grid[:,x]

    if facing == 0:  # right
        x = move_in_array(row, 1, x, step)
    elif facing == 1:  # down
        y = move_in_array(col, 1, y, step)
    elif facing == 2:  # left
        x = move_in_array(row, -1, x, step)
    elif facing == 3:  # up
        y = move_in_array(col, -1, y, step)

    return x, y


EXPECTED_1 = 6032
def first_part(data, pw):
    max_length = 0
    for d in data:
        print(d)
        if len(d) > max_length:
            max_length = len(d)
    print(pw)

    grid = np.zeros((len(data), max_length), dtype='int')
    for y_index, d in enumerate(data):
        for x_index, x in enumerate(d):
            if x =='.':
                grid[y_index, x_index] = '1'
            elif x =='#':
                grid[y_index, x_index] = '2'
    print(grid)

    instruct = re.findall(r'(\d+)([RL])?', pw)
    print(instruct)

    facing = 0  # 0 right, 1 down, 2 left, 3 up
    x = data[0].index('.')
    y = 0
    print(f'initial {x}')

    for i in instruct:
        step = int(i[0])
        turn = i[1]

        x, y = next_loc(grid, facing, x, y, step)
        print(f"After Instruction {i},  x={x} y={y} step={step}")

        if turn == 'R':
            facing += 1
        elif turn == 'L':
            facing -= 1
        facing = facing % 4
            
    solution = 1000*(y+1) + 4*(x+1) + facing
    print(f"solution {solution}")
    return solution

def facing_string(facing):
    if facing == 0:
        return 'right'
    if facing == 1:
        return 'down'
    if facing == 2:
        return 'left'
    if facing == 3:
        return 'up'

def debug_get_next_coord():
    block = 50

    y = 3*block 

    x = block -1 
    facing = RIGHT
    new_x, new_y, new_facing  = get_next_coord(x,y,facing)

    print(f"orig {x}, {y}, {facing_string(facing)}")
    print(f"new  {new_x}, {new_y}, {facing_string(new_facing)}")

def get_next_coord(x, y, facing):
    block = 50
    if x >= 0 and x < block:
        # 4 going up
        if y == 2*block and facing == UP:
            new_facing = RIGHT
            new_x = block
            new_y = block+x
            return new_x, new_y, new_facing
        # 6 going down
        if y == 4*block-1 and facing == DOWN:
            new_facing = DOWN
            new_y = 0
            new_x = x+2*block
            return new_x, new_y, new_facing
    elif x >= block and x < 2*block:
        # 1 going up
        if y == 0 and facing == UP:
            new_facing = RIGHT
            new_x = 0
            new_y = x+(2*block)
            return new_x, new_y, new_facing
        # 5 going down
        if y == 3*block-1 and facing == DOWN:
            new_facing = LEFT
            new_x = block - 1 
            new_y = x+(2*block)
            return new_x, new_y, new_facing
    elif x >= 2*block and x < 3*block:
        # 2 going up
        if y == 0 and facing == UP:
            new_facing = UP
            new_y = 4*block-1
            new_x = x - 2*block
            return new_x, new_y, new_facing
        # 2 going down
        if y == block-1 and facing == DOWN:
            new_facing = LEFT
            new_y = x - block
            new_x = 2*block-1
            return new_x, new_y, new_facing
    if y >= 0 and y < block:
        # 1 going left
        if x == block and facing == LEFT:
            new_facing = RIGHT
            new_y = (block-1) - y  + 2*block
            new_x = 0
            return new_x, new_y, new_facing
        # 2 going right
        if x == 3*block-1 and facing == RIGHT:
            new_facing = LEFT
            new_y = (block-1) - y  + 2*block
            new_x = 2*block -1 
            return new_x, new_y, new_facing
    elif y >= block and y < 2*block:
        # 3 going left
        if x == block and facing == LEFT:
            new_facing = DOWN 
            new_x = y - block
            new_y = 2*block
            return new_x, new_y, new_facing
        # 3 going right
        if x == 2*block-1 and facing == RIGHT:
            new_facing = UP
            new_x = y + block
            new_y = block-1
            return new_x, new_y, new_facing
    elif y >= 2*block and y < 3*block:
        # 4 going left
        if x == 0 and facing == LEFT:
            new_facing = RIGHT
            new_y = (block-1) - (y - 2*block)
            new_x = block
            return new_x, new_y, new_facing
        # 5 going right
        if x == 2*block-1  and facing == RIGHT:
            new_facing = LEFT
            new_y = (block-1) - (y - 2*block)
            new_x = 3*block - 1
            return new_x, new_y, new_facing
    elif y >= 3*block and y < 4*block:
        # 6 going left
        if x == 0 and facing == LEFT:
            new_facing = DOWN
            new_y = 0 
            new_x = y-2*block
            return new_x, new_y, new_facing
        # 6 going right
        if x == block-1 and facing == RIGHT:
            new_facing = UP
            new_y = 3*block - 1
            new_x = y - 2 * block 
            return new_x, new_y, new_facing

def next_loc_cube(grid, facing, x, y):
    wall = False
    new_x = x
    new_y = y
    new_facing = facing

    if facing == 0:  # right
        new_x += 1
    elif facing == 1:  # down
        new_y += 1
    elif facing == 2:  # left
        new_x -= 1
    elif facing == 3:  # up
        new_y -= 1

    # Gets a modified x and y if it is going off a cube face
    if new_x < 0 or new_y < 0 or new_y >= len(grid) or new_x >= len(grid[0]):
        new_x, new_y, new_facing = get_next_coord(x, y, facing)
    elif grid[new_y][new_x] == 0:
        new_x, new_y, new_facing = get_next_coord(x, y, facing)

    if grid[new_y][new_x] == 1:
        x = new_x 
        y = new_y 
        facing = new_facing
    elif grid[new_y][new_x] == 2:
        wall = True
    elif grid[new_y][new_x] == 0:
        print("something went wrong in grid")
        import code
        code.interact(local=locals())

    return x, y, facing, wall

EXPECTED_2 = 5031
def second_part(data, pw):
    max_length = 0
    for d in data:
        if len(d) > max_length:
            max_length = len(d)
    grid = np.zeros((len(data), max_length), dtype='int')

    for y_index, d in enumerate(data):
        for x_index, x in enumerate(d):
            if x =='.':
                grid[y_index, x_index] = '1'
            elif x =='#':
                grid[y_index, x_index] = '2'

    instruct = re.findall(r'(\d+)([RL])?', pw)

    mini_y = int(len(data)/50)
    mini_x = int(max_length/50)
    mini_grid = np.zeros((mini_y, mini_x), dtype='int')
    label = 1
    for y in range(mini_y):
        for x in range(mini_x):
            print(grid[50*y][50*x])
            if grid[50*y][50*x] > 0:
                mini_grid[y][x] = label
                label += 1
    print(mini_grid)

    facing = 0  # 0 right, 1 down, 2 left, 3 up
    x = data[0].index('.')
    y = 0
    print(f'initial {x}')

    for i in instruct:
        step = int(i[0])
        turn = i[1]

        for _ in range(step):
            x, y, facing, wall = next_loc_cube(grid, facing, x, y)
            if wall is True:
                break

        print(f"After Instruction {i},  x={x} y={y} step={step}")

        if turn == 'R':
            facing += 1
        elif turn == 'L':
            facing -= 1
        facing = facing % 4
            
    solution = 1000*(y+1) + 4*(x+1) + facing
    print(f"solution {solution}")
    return solution
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'example.txt'
    example_data, example_pw = read_re(filename)
    example1 = first_part(example_data, example_pw)
    if example1 != EXPECTED_1:
        exit()
    else:
        print("Part 1 example success")
    
    filename = 'input.txt'
    data, pw = read_re(filename)
    solution = int(first_part(data, pw))

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(f"P1 Solution: {solution}")
    pyperclip.copy(str(solution))
    
    #debug_get_next_coord()
    #exit()
    
    ## PART 2
    print("---- Part 2 Start  ---------------")
#    filename = 'example.txt'
#    example_data, example, pw = read_re(filename, pw)
#    example2 = second_part(example_data)
#    if example2 != EXPECTED_2:
#        exit()
#    else:
#        print("Part 2 example success")

    filename = 'input.txt'
    data, pw = read_re(filename)
    solution = int(second_part(data, pw))

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(f"P2 Solution: {solution}")
    pyperclip.copy(str(solution))
    # guessed  51251.  Too low
    # guessed 114020.  Too high
    # guessed 148147.  Too high
    # Solution 55267
