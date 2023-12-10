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


S_REPLACE = ""


def get_neighbors(x, y):
    global S_REPLACE
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

    if dir == "S":
        print(directions.items())
        print(valid)
        for (k, v) in directions.items():
            if all((z[0] - x, z[1] - y) in v for z in valid):
                print("found S", k)
                S_REPLACE = k
                break

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


final_loop = []
for k in network:
    if k not in visited:
        current = find_loop(k[0], k[1], [(k[0], k[1])])
        if S_POS in current:
            # print("found S", current)
            print("loop len", len(current))
            print("result", int(len(current) - 1) / 2)
            final_loop = current
            break

        visited.extend(current)
        current = []

outside = []
visited = []
enclosed = []


def is_outside(x, y):
    if (
        x == 0
        or y == 0
        or x >= len(matrix) - 1
        or y >= len(matrix[0]) - 2
        or (x, y) in outside
        or (x, y) in visited
    ):
        return True

    # dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    exdirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    # outs = []
    for (i, d) in enumerate(exdirs):
        nx = x + d[0]
        ny = y + d[1]
        if (nx, ny) in enclosed:
            continue

        if (
            nx == 0
            or ny == 0
            or nx >= len(matrix) - 1
            or ny >= len(matrix[0]) - 2
            or (nx, ny) in outside
        ):
            return True

        if matrix[nx][ny] == ".":
            enclosed.append((nx, ny))

            out = is_outside(nx, ny)
            if out:
                return True

    # print(path, blocked)

    return False


matrix = []
for i in range(len(lines) * 3):
    ml = []
    for j in range(len(lines[0]) * 3):
        ml.append(".")
    matrix.append(ml)

cube = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
directions = {
    "|": ".x..x..x.",
    "-": "...xxx...",
    "L": ".x..xx...",
    "J": ".x.xx....",
    "7": "...xx..x.",
    "F": "....xx.x.",
    ".": ".........",
}

for i in range(len(lines)):
    for j in range(len(lines[0]) - 1):
        for (idx, (x, y)) in enumerate(cube):
            if (i, j) not in final_loop:
                continue
            char = lines[i][j]
            if char == "S":
                char = S_REPLACE
            print(i, j, char)
            matrix[i * 3 + x][j * 3 + y] = directions[char][idx]

for m in matrix:
    print("".join(m))
    # print(m.join())


def find_cubes(enclosed):
    sum = 0
    for i in range(len(lines) - 1):
        for j in range(len(lines[0]) - 1):
            if (i * 3 + 1, j * 3 + 1) in enclosed:
                sum += 1

    return sum


for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j] == "." and (i, j) not in visited:
            enclosed = []
            out = is_outside(i, j)
            if out:
                # print("outside", visited)
                outside.extend(enclosed)
                visited.extend(enclosed)
            else:
                print("encl", enclosed)
                visited.extend(enclosed)
                print("inside", find_cubes(enclosed))
