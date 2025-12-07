import sys

#READING DATA

fname = sys.argv[1]

with open(fname) as f:
    radio_instructions = f.readline()

# helpers
moves = {
    "^":(0,1),
    ">":(1,0),
    "v":(0,-1),
    "<":(-1,0)
}


def houses_visited(data):
    pos = (0,0)
    grid = set([pos])
    for d in data:
        pos = (pos[0]+moves[d][0],pos[1]+moves[d][1])
        if pos not in grid:
            grid.add(pos)
    return grid

#part one
print(f"Solution part one:{len(houses_visited(radio_instructions))}")

#part two

def houses_visited2(data):
    grid_santa = [data[2*_] for _ in range(len(data)//2)]
    grid_robo_santa = [data[2*_+1] for _ in range(len(data)//2)]
    H1, H2 = houses_visited(grid_santa),houses_visited(grid_robo_santa)
    answer = H1.union(H2)
    return answer

print(f"Solution part two: {len(houses_visited2(radio_instructions))}")
