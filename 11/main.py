import math
import re
import numpy as np
import pyperclip

def read_re(filename):
    data = []

    lines = []
    for line in open(filename):
        lines.append(line)
    
    data = []
    num_monkeys = int((len(lines)+1) / 7)
    for i in range(num_monkeys):
        monkey = {}
        monkey_id = re.findall(f'\d+', lines[7*i+0])
        items = list(map(int, re.findall(f'\d+',     lines[7*i+1])))
        operation = re.findall(f'\S+', lines[7*i+2])
        test = re.findall(f'\S+',      lines[7*i+3])
        true_id = re.findall(f'\S+',   lines[7*i+4])
        false_id = re.findall(f'\S+',  lines[7*i+5])


        monkey['id']  = monkey_id
        monkey['items']  = items
        monkey['op']  = operation
        monkey['test']  = int(test[-1])
        monkey['true_id']  = int(true_id[-1])
        monkey['false_id']  = int(false_id[-1])
        data.append(monkey)

    print(data)

    return data

def perform_operation(worry, op):
    
    if op[-1] == 'old':
        val = worry
    else:
        val = int(op[-1])

    m  =  op[-2]
    
    new_worry = 0
    if m == '*':
        new_worry = worry * val
    if m == '+':
        new_worry = worry + val

    return new_worry

def first_part(data):
    solution = 100
    rounds = 20

    count = [0] * len(data)

    for _ in range(rounds):
        for i, monkey in enumerate(data):
            for item in monkey['items']:
                count[i] += 1
                new_worry = perform_operation(item, monkey['op'])
                new_worry = math.trunc(new_worry/3)
                
                #print(new_worry)
                
                if new_worry % monkey['test'] == 0:
                    data[monkey['true_id']]['items'].append(new_worry)
                else:
                    data[monkey['false_id']]['items'].append(new_worry)
            
            monkey['items'] = []
    
    solution = count[-1] * count[-2]
    print(solution)
    pyperclip.copy(solution)

def second_part(data):
    solution = 100
    rounds = 10000

    count = [0] * len(data)

    factor = 1
    for monkey in data:
        factor *= monkey['test']

    for r in range(rounds):
        if r % 200 == 0:
            print(f"calculating Round {r}")

        for i, monkey in enumerate(data):
            for item in monkey['items']:
                count[i] += 1
                new_worry = perform_operation(item, monkey['op'])
                
                new_worry = new_worry % factor
                
                if new_worry % monkey['test'] == 0:
                    data[monkey['true_id']]['items'].append(new_worry)
                else:
                    data[monkey['false_id']]['items'].append(new_worry)
            
            monkey['items'] = []
    
    count.sort()
    solution = count[-1] * count[-2]
    print(solution)
    pyperclip.copy(solution)
                
if __name__ == '__main__':
    print("###################new run###################")
    filename = 'input.txt'
    #filename = 'example.txt'
    data = read_re(filename)
    #first_part(data)
    second_part(data)