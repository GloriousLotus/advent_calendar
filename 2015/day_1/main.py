import sys

#READING DATA

fname = sys.argv[1]
with open(fname) as f:
    data = f.readline()

#part one
target_floor = data.count("(")-data.count(")")

print(f"Solution Part 1: {target_floor}")

#part two
floor = 0
solution = 0
for idx in range(len(data)):
    floor = floor + (1 if data[idx]=="(" else -1)
    if floor<0:
        solution = idx+1
        break

print(f"Solution Part 2: {solution}")