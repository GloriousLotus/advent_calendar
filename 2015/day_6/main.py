import sys

fname = sys.argv[1]
instructions = []

with open(fname) as f:
    for line in f.readlines():
        corners = [list(map(int,_2.split(","))) for _2 in [_1.rstrip() for _1 in line.split(" ") if "," in _1]]
        action = "turn on" if "turn on" in line else "turn off" if "turn off" in line else "toggle"
        entry = {"action":action,"corners":corners}
        instructions.append(entry)
