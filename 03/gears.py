#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(prog="AOC",)
parser.add_argument('filename', help="input file")
parser.add_argument('-2', '--part2', action='store_true', help="run part 2")
args = parser.parse_args()

with open(args.filename, 'r') as f:
    lines = f.readlines()

def is_symbol_adjacent(line, i):
    matrices = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1],
              [1, -1], [1, 0], [1, 1]]

    for matrix in matrices:
        x = line + matrix[0]
        y = i + matrix[1]
        if x < 0 or y < 0 or x >= len(lines) or y >= len(lines[x])-1:
            continue

        if lines[x][y] != '.' and not lines[x][y].isdigit():
            #print(x, y, lines[x][y], True, len(lines), len(lines[x]))
            if args.part2:
                return True, lines[x][y], [x, y]

            return True

    if args.part2:
        return False, '', []
    return False

cur_number = 0
cur_is_part = False
cur_is_gear = False
sum = 0
gears = {}
for (x, line) in enumerate(lines):
    for (y, char) in enumerate(line):
        if y == len(line)-1 or not char.isdigit():
            if cur_is_part:
                sum += cur_number
            if cur_is_gear:
                idx = f'{cur_is_gear[0]}-{cur_is_gear[1]}'
                if idx not in gears:
                    gears[idx] = []
                gears[idx].append(cur_number)
            cur_number = 0
            cur_is_part = False
            cur_is_gear = False
            continue

        if char.isdigit():
            if cur_number == 0:
                cur_is_part = False
            cur_number = cur_number * 10 + int(char)
            if args.part2:
                res = is_symbol_adjacent(x, y)
                if res[0]:
                    cur_is_part = True

                if res[1] == '*':
                    cur_is_gear = res[2]
            else:
                if is_symbol_adjacent(x, y):
                    cur_is_part = True


gear_sum = 0
for gear in gears:
    g = gears[gear]
    if len(g) == 2:
        gear_sum += g[0] * g[1]

print('Part 1 sum:', sum)
print('Part 2 gear sum:', gear_sum)
