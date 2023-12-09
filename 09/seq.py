#!/usr/bin/env python3

import argparse
import re
import math
from collections import Counter
from functools import cmp_to_key

parser = argparse.ArgumentParser(
    prog="AOC",
)
parser.add_argument("filename", help="input file")
parser.add_argument("-2", "--part2", action="store_true", help="run part 2")
args = parser.parse_args()

with open(args.filename, "r") as f:
    lines = f.readlines()

lns = []
for line in lines:
    lns.append([int(x) for x in line.strip().split(" ")])


def get_abl(line):
    abl = []
    for i in range(len(line) - 1):
        abl.append(line[i + 1] - line[i])

    return abl


res = 0
for line in lns:
    abls = [line]
    done = False
    while not done:
        abl = get_abl(abls[-1])
        abls.append(abl)
        if all(x == 0 for x in abl):
            done = True

    for i in range(len(abls) - 1):
        a = abls[len(abls) - i - 2]
        prev = abls[len(abls) - i - 1]
        a.insert(0, a[0] - prev[0])

    print(abls)
    print()
    res += abls[0][0]

print(res)
