#!/usr/bin/env python3

import argparse
from pprint import pprint

parser = argparse.ArgumentParser(prog="AOC",)
parser.add_argument('filename', help="input file")
parser.add_argument('-2', '--part2', action='store_true', help="run part 2")
args = parser.parse_args()

with open(args.filename, 'r') as f:
    lines = f.readlines()

games = []
for line in lines:
    game = []
    for showing_ in line.split(':')[1].split(';'):
        showing = []
        for colors in showing_.split(','):
            amount = int(colors.strip().split(' ')[0])
            color = colors.strip().split(' ')[1]
            showing.append((amount, color))

        game.append(showing) 

    games.append(game)


if not args.part2:
    valid_amount = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    sum = 0
    for (idx, game) in enumerate(games):
        valid = True
        for showing in game:
            #print('showing', showing)
            for color in showing:
                #print(color, valid_amount[color[1]])
                if valid_amount[color[1]] < color[0]:
                    valid = False
                    break

        if valid:
            sum += idx + 1

        print("Game", idx + 1, valid)

    print("Sum", sum)

else:
    sum = 0
    for (idx, game) in enumerate(games):
        min_amounts = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }
        for showing in game:
            for color in showing:
                if min_amounts[color[1]] < color[0]:
                    min_amounts[color[1]] = color[0]

        power = min_amounts['red'] * min_amounts['green'] * min_amounts['blue']
        print("Game", idx + 1, power)
        sum += power

    print("Sum", sum)
