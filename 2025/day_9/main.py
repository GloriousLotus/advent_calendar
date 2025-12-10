import sys

fname = sys.argv[1]

corners: list[tuple[int,int]] = list()

with open(fname,"r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        corner = [int(_) for _ in line.split(",")]
        corners.append((corner[0],corner[1]))

print(corners)