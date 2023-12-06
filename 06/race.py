#!/usr/bin/env python3

import argparse
import re
import math

parser = argparse.ArgumentParser(
    prog="AOC",
)
parser.add_argument("filename", help="input file")
parser.add_argument("-2", "--part2", action="store_true", help="run part 2")
args = parser.parse_args()

with open(args.filename, "r") as f:
    lines = f.readlines()

if args.part2:
    lines[0] = lines[0].replace(" ", "")
    lines[1] = lines[1].replace(" ", "")

times = re.findall(r"\d+", lines[0].split(":")[1])
distances = re.findall(r"\d+", lines[1].split(":")[1])


if args.part2:
    # y = x * (n - x)
    # y = nx - x^2
    # 0 = x^2 - nx + y
    # p = -n
    # q = y
    # x = (-p +- sqrt(p^2 - 4q)) / 2
    x1 = -(int(times[0]) / 2) + ((int(times[0]) / 2) ** 2 - int(distances[0])) ** 0.5
    x2 = -(int(times[0]) / 2) - ((int(times[0]) / 2) ** 2 - int(distances[0])) ** 0.5
    print("x", x1, x2)
    print(abs(x2) - abs(x1))
    exit(0)

results = []
for i in range(len(times)):
    wins = 0
    for charge in range(int(times[i])):
        speed = charge
        distance = speed * (int(times[i]) - charge)
        # print(f"Charge: {charge}, Speed: {speed}, Distance: {distance}")
        # results.append(distance)
        if distance > int(distances[i]):
            wins += 1

    results.append(wins)

print(results)
sum = 1
for r in results:
    sum *= r

print(sum)
