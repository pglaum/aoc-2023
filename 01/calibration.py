#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(prog="AOC",)
parser.add_argument('filename', help="input file")
parser.add_argument('-2', '--part2', action='store_true', help="run part 2")
args = parser.parse_args()

with open(args.filename, 'r') as f:
    lines = f.readlines()

digits = [
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
]

sum = 0
for line in lines:
    nums = []
    for idx, char in enumerate(line):
        if args.part2:
            for d in digits:
                if line[idx:].startswith(d):
                    nums.append(digits.index(d) + 1)
                    break

        if char.isnumeric():
            nums.append(int(char))

    print(nums[0], nums[-1])
    sum += nums[0] * 10 + nums[-1]

print('The sum is:', sum)
