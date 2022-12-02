import os
import re

def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    data = []
    
    for line in lines: 
        l = line.strip()
        spl = l.split()

        opp = ""
        you = ""

        if spl[0] == 'A':
            opp = "rock"
        elif spl[0] == 'B':
            opp = "paper"
        elif spl[0] == 'C':
            opp = "scissors"
            
        if spl[1] == 'X':
            you = "rock"
        elif spl[1] == 'Y':
            you = "paper"
        elif spl[1] == 'Z':
            you = "scissors"
            
        data.append((opp, you))

    return data

def read_file2(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    data = []
    
    for line in lines: 
        l = line.strip()
        spl = l.split()

        opp = ""
        you = ""

        if spl[0] == 'A':
            opp = "rock"
        elif spl[0] == 'B':
            opp = "paper"
        elif spl[0] == 'C':
            opp = "scissors"
            
        if spl[1] == 'X':
            you = "lose"
        elif spl[1] == 'Y':
            you = "draw"
        elif spl[1] == 'Z':
            you = "win"
            
        data.append((opp, you))

    return data

def first_part(data):
    score = 0
    
    for play in data:
        if play[1] == 'rock':
            score += 1
            if play[0] == 'scissors':
                score += 6
            elif play[0] == 'rock':
                score += 3

        elif play[1] == 'paper':
            score += 2
            if play[0] == 'rock':
                score += 6
            elif play[0] == 'paper':
                score += 3

        elif play[1] == 'scissors':
            score += 3
            if play[0] == 'paper':
                score += 6
            elif play[0] == 'scissors':
                score += 3
        
    print(score)
    
def get_score(type):
    if type == 'rock':
        return 1
    if type == 'paper':
        return 2
    if type == 'scissors':
        return 3
    

def second_part(data):
    
    score = 0
    
    for play in data:
        if play[1] == 'lose':
            score += 0
            if play[0] == 'rock':
                score += get_score('scissors')
            if play[0] == 'paper':
                score += get_score('rock')
            if play[0] == 'scissors':
                score += get_score('paper')

        elif play[1] == 'draw':
            score += 3
            score += get_score(play[0])

        elif play[1] == 'win':
            score += 6
            if play[0] == 'rock':
                score += get_score('paper')
            if play[0] == 'paper':
                score += get_score('scissors')
            if play[0] == 'scissors':
                score += get_score('rock')
        
    print(score)


if __name__ == '__main__':
    data = read_file('input.txt')
    first_part(data)

    data = read_file2('input.txt')
    second_part(data)