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

decks = []
for x in lines:
    decks.append([x.split(" ")[0], int(x.split(" ")[1])])

chars = "J23456789TQKA" if args.part2 else "23456789TJQKA"


def get_value(deck):
    five = False
    four = False
    full_house = False
    three = False
    two_twos = False
    two = False

    jokers = deck.count("J")

    c = Counter(deck.replace("J", ""))
    for c in c.most_common():
        if c[1] == 5:
            five = True
        elif c[1] == 4:
            four = True
        elif c[1] == 3:
            three = True
        elif c[1] == 2:
            if two:
                two_twos = True
                two = False
            else:
                two = True

    if five:
        pass
    elif four and jokers == 1:
        four = False
        five = True

    elif three:
        if jokers == 1:
            three = False
            four = True
        elif jokers == 2:
            three = False
            five = True
    elif two_twos:
        if jokers == 1:
            two_twos = False
            three = True
            two = True
        elif jokers == 2:
            two_twos = False
            four = True
    elif two:
        if jokers == 1:
            two = False
            three = True
        elif jokers == 2:
            two = False
            four = True
        elif jokers == 3:
            two = False
            five = True
    else:
        if jokers == 1:
            two = True
        elif jokers == 2:
            three = True
        elif jokers == 3:
            four = True
        elif jokers == 4:
            five = True
        elif jokers == 5:
            five = True

    if three and two:
        full_house = True
        three = False
        two = False

    return {
        "five": five,
        "four": four,
        "full_house": full_house,
        "three": three,
        "two_twos": two_twos,
        "two": two,
    }


def cmp_chars(deck1, deck2):
    for (c1, c2) in zip(deck1, deck2):
        if chars.index(c1) > chars.index(c2):
            return 1
        elif chars.index(c1) < chars.index(c2):
            return -1
    return 0


def get_value_string(d):
    res = []
    if d.get("five"):
        res.append("five")
    if d.get("four"):
        res.append("four")
    if d.get("full_house"):
        res.append("full_house")
    if d.get("three"):
        res.append("three")
    if d.get("two_twos"):
        res.append("two_twos")
    if d.get("two"):
        res.append("two")

    return ", ".join(res)


for d in decks:
    print(d, get_value_string(get_value(d[0])))


def compare(deck1, deck2):
    d1 = get_value(deck1[0])
    d2 = get_value(deck2[0])

    if (
        (d1["five"] and d2["five"])
        or (d1["four"] and d2["four"])
        or (d1["full_house"] and d2["full_house"])
        or (d1["three"] and d2["three"])
        or (d1["two_twos"] and d2["two_twos"])
        or (d1["two"] and d2["two"])
    ):
        return cmp_chars(deck1[0], deck2[0])

    if d1["five"]:
        return 1
    if d2["five"]:
        return -1

    if d1["four"]:
        return 1
    if d2["four"]:
        return -1

    if d1["full_house"]:
        return 1
    if d2["full_house"]:
        return -1

    if d1["three"]:
        return 1
    if d2["three"]:
        return -1

    if d1["two_twos"]:
        return 1
    if d2["two_twos"]:
        return -1

    if d1["two"]:
        return 1
    if d2["two"]:
        return -1

    return cmp_chars(deck1[0], deck2[0])


def do_compare(deck1, deck2):
    res = compare(deck1, deck2)
    return res


decks = sorted(decks, key=cmp_to_key(do_compare))
print("\n".join([x[0] for x in decks]))

sum = 0
for i, deck in enumerate(decks):
    sum += (i + 1) * deck[1]

print(sum)
