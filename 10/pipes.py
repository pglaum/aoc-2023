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
    lines = f.readlines()

S_POS = []
for (i, line) in enumerate(lines):
    for (j, c) in enumerate(line):
        if c == "S":
            S_POS = (i, j)

directions = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    "S": [(1, 0), (-1, 0), (0, 1), (0, -1)],
}


def is_valid_from(x, y, nx, ny):
    if lines[nx][ny] == "S":
        return True
    if lines[nx][ny] not in directions:
        return False

    dir = directions[lines[nx][ny]]
    # print("is valid from", lines[nx][ny], dir)
    for d in dir:
        if nx + d[0] == x and ny + d[1] == y:
            return True
    return False


def get_neighbors(x, y):
    dir = lines[x][y]

    if dir not in directions:
        return []

    valid = []
    for d in directions[dir]:
        nx = x + d[0]
        ny = y + d[1]
        if nx >= 0 and nx < len(lines) and ny >= 0 and ny < len(lines[0]):
            if is_valid_from(x, y, nx, ny):
                valid.append((nx, ny))
                # print("connection", nx, ny)
            else:
                # print("not valid", nx, ny)
                pass
        else:
            # print("out of bounds", nx, ny)
            pass

    return valid


network = {}
for i in range(len(lines)):
    for j in range(len(lines[0])):
        joint = get_neighbors(i, j)
        if len(joint) > 2:
            print("joint", joint)
        if len(joint) > 1:
            network[(i, j)] = joint
        # print("loop done")

# pprint(network)

visited = []


def find_loop(x, y, path):
    if (x, y) in visited:
        return path

    j = []
    if (x, y) not in network:
        return path

    for n in network[(x, y)]:
        if n not in path:
            j.append(n)

    for n in j:
        path.append((n[0], n[1]))
        find_loop(n[0], n[1], path)

    # if len(j) == 0:
    #    print("loop or dead end", path)

    return path


for k in network:
    if k not in visited:
        current = find_loop(k[0], k[1], [(k[0], k[1])])
        if S_POS in current:
            # print("found S", current)
            print("loop len", len(current))
            print("result", int(len(current) - 1) / 2)
            break

        visited.extend(current)
        current = []
