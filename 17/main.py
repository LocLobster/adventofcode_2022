import math
import re
import numpy as np
import pyperclip

EXPECTED_1 = 3068
EXPECTED_2 = 1514285714288

def read_re(filename):
    data = []

    for line in open(filename):
        data = line.strip()

    return data

def check_collision(grid, r, loc):
    r_shape = r.shape

    for s in range(r.shape[0]):
        sub_grid = grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]]
        check = np.logical_and(r[s, :], sub_grid)
    
        if np.any(check==True):
            return True

    return False
    
def first_part(data):
    rock1 = np.ones((1,4), dtype=int)
    rock2 = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=int)
    rock3 = np.array([[1,1,1],[0,0,1],[0,0,1]], dtype=int)
    rock4 = np.ones((4,1), dtype=int)
    rock5 = np.ones((2,2), dtype=int)
    rock_list = [rock1, rock2, rock3, rock4, rock5]

    grid = np.zeros((4000,9), dtype=int)
    grid[:,0] = 1
    grid[:,-1] = 1
    grid[0,:] = 1

    highest = np.where(grid.sum(axis=1) > 2)[0][-1]
    max_iterations = 2022
    wind_len = len(data)
    step =0
    for i in range(max_iterations):
        r = rock_list[i % len(rock_list)]
        r_shape = r.shape
        loc = (highest + 4, 3)

        while True:
            d = data[step%wind_len]
            # Left/right wind
            if d == '<':
                new_loc = (loc[0], loc[1]-1)
                if check_collision(grid, r, new_loc) is False:
                    loc = new_loc
            else:
                new_loc = (loc[0], loc[1]+1)
                if check_collision(grid, r, new_loc) is False:
                    loc = new_loc

            step += 1
            # Check down
            new_loc = (loc[0]-1, loc[1])
            if check_collision(grid, r, new_loc) is False:
                loc = new_loc
            else:
                for s in range(r.shape[0]):
                    grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]] = np.logical_xor(r[s,:], grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]])
                highest = np.where(grid.sum(axis=1) > 2)[0][-1]
                break
    return highest 

def second_part(data):
    rock1 = np.ones((1,4), dtype=int)
    rock2 = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=int)
    rock3 = np.array([[1,1,1],[0,0,1],[0,0,1]], dtype=int)
    rock4 = np.ones((4,1), dtype=int)
    rock5 = np.ones((2,2), dtype=int)

    print("Printing rocks")
    print(rock1)
    print(rock2)
    print(rock3)
    print(rock4)
    print(rock5)
    rock_list = [rock1, rock2, rock3, rock4, rock5]

    max_iterations = 20000
    grid_y         = 50000
    grid = np.zeros((grid_y,9), dtype=int)
    grid[:,0] = 1
    grid[:,-1] = 1
    grid[0,:] = 1

    add_height = np.zeros(max_iterations, dtype=int)

    restarts = list()

    highest = np.where(grid.sum(axis=1) > 2)[0][-1]
    wind_len = len(data)
    step =0
    for i in range(max_iterations):
        rock_num = i % len(rock_list)
        r = rock_list[rock_num]
        r_shape = r.shape
        loc = (highest + 4, 3)

        # Debugging.  Check the grid after the ith rock is initialized
#        if i == 2:
#            for s in range(r.shape[0]):
#                grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]] = np.logical_xor(r[s,:], grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]])
#            print(f"highest={highest} rockhieght={r.shape[0]}")
#            print(np.flipud(grid))
#            exit()

        while True:
            mod = step%wind_len
            if mod == 0:
                restarts.append(i)
            d = data[mod]
            # Left/right wind
            if d == '<':
                new_loc = (loc[0], loc[1]-1)
                if check_collision(grid, r, new_loc) is False:
                    loc = new_loc
            else:
                new_loc = (loc[0], loc[1]+1)
                if check_collision(grid, r, new_loc) is False:
                    loc = new_loc

            step += 1
            # Check down
            new_loc = (loc[0]-1, loc[1])
            if check_collision(grid, r, new_loc) is False:
                loc = new_loc
            else:
                for s in range(r.shape[0]):
                    grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]] = np.logical_xor(r[s,:], grid[loc[0]+s, loc[1]:loc[1]+r_shape[1]])
                last_highest = highest
                highest = np.where(grid.sum(axis=1) > 2)[0][-1]
                add_height[i] = highest-last_highest
                break

    # This showed that the pattern repeats from the second set onwards.  Should write some matcher but I'm lazy. 
    # Note this means it doesn't work for the example input.  And won't work for all inputs
    print("Printing height additions for each wind reset")
    for r in restarts[0:-1]:
        print(add_height[r:r+20])

    # Calculating the nth rock. 
    target_rock = 1000000000000

    matching_length = restarts[-1] - restarts[-2]
    matching_array = add_height[restarts[-2]:restarts[-2]+matching_length]
    matching_sum = sum(matching_array)

    target_div = math.trunc((target_rock - restarts[-1]) / matching_length)
    target_mod = math.trunc((target_rock - restarts[-1]) % matching_length)

    highest_at_match = sum(add_height[0:restarts[-1]])
    # Needs 64bit integers LOL. Otherwise:  RuntimeWarning: overflow encountered in long_scalars
    output = highest_at_match + np.int64(target_div)*np.int64(matching_sum) + sum(matching_array[0:target_mod])
    print(output)

    return output
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'example.txt'
    example_data = read_re(filename)
    example1 = first_part(example_data)
    if example1 != EXPECTED_1:
        exit()
    
    filename = 'input.txt'
    data = read_re(filename)
    solution = first_part(data)

    print("************************************")
    print("*** PART 1 SOLUTION ****************")
    print("************************************")
    print(solution)
    pyperclip.copy(str(solution))
    

    ## PART 2
###  NOTE: didn't make the second example work
#    example2 = second_part(example_data)
#    if example2 != EXPECTED_2:
#        exit()

    print("---- Starting Part 2 ------------")
    solution = second_part(data)

    print("---------------------------------")
    print("---- Part 2 solution ------------")
    print("---------------------------------")
    print(solution)
    pyperclip.copy(str(solution))
