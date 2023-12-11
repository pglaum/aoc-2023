#!/usr/bin/env python3

import argparse
import re
import math
import sys
from collections import Counter
from functools import cmp_to_key
from pprint import pprint

sys.setrecursionlimit(100000)

parser = argparse.ArgumentParser(
    prog="AOC",
)
parser.add_argument("filename", help="input file")
parser.add_argument("-2", "--part2", action="store_true", help="run part 2")
args = parser.parse_args()

with open(args.filename, "r") as f:
    content = f.read()

universe = []
for line in content.splitlines():
    uv = []
    for char in line:
        if char == "#":
            uv.append(1)
        else:
            uv.append(0)
    universe.append(uv)


def add_column(index):
    for i in range(len(universe)):
        universe[i].insert(index, 0)


def add_row(index):
    uv = []
    for _ in range(len(universe[0])):
        uv.append(0)
    universe.insert(index, uv)


rows_needed = []
for i in range(len(universe)):
    if all([x == 0 for x in universe[i]]):
        rows_needed.append(i)

cols_needed = []
for i in range(len(universe[0])):
    empty = True
    for j in range(len(universe)):
        if universe[j][i] == 1:
            empty = False
            break
    if empty:
        cols_needed.append(i)

for i, row in enumerate(rows_needed):
    add_row(row + i)

for i, col in enumerate(cols_needed):
    add_column(col + i)

galaxies = []
for x in range(len(universe)):
    for y in range(len(universe[x])):
        if universe[x][y] == 1:
            galaxies.append((x, y))

ans_1 = 0
for i, g1 in enumerate(galaxies):
    for j in range(i + 1, len(galaxies)):
        if i == j:
            continue
        g2 = galaxies[j]
        length = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        # print("galaxy", i, "to", j, length)
        ans_1 += length

print(ans_1)

# part 2

# for i, row in enumerate(rows_needed):
#    universe[row] = 2
# for i, col in enumerate(cols_needed):
#    for j in range(len(universe)):
#        universe[j][col] = 2

universe = []
for line in content.splitlines():
    uv = []
    for char in line:
        if char == "#":
            uv.append(1)
        else:
            uv.append(0)
    universe.append(uv)

for line in universe:
    print("".join(["." if x == 0 else "#" for x in line]))

galaxies = []
for x in range(len(universe)):
    for y in range(len(universe[x])):
        if universe[x][y] == 1:
            galaxies.append((x, y))

multi = 1000000
ans_part2 = 0
for i, g1 in enumerate(galaxies):
    for j in range(i + 1, len(galaxies)):
        if i == j:
            continue
        g2 = galaxies[j]
        rows = len(
            [x for x in rows_needed if x > min(g1[0], g2[0]) and x < max(g1[0], g2[0])]
        )
        cols = len(
            [x for x in cols_needed if x > min(g1[1], g2[1]) and x < max(g1[1], g2[1])]
        )
        length = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        length += (rows + cols) * (multi - 1)
        # print("galaxy", i, "to", j, length, rows, cols)
        ans_part2 += length

print(ans_part2)
