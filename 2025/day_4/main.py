import sys
from typing import TypeVar

T = TypeVar("T")

NEARBY = [[_1, _2] for _1 in range(-1, 2) for _2 in range(-1, 2) if _1 != 0 or _2 != 0]
FEWER_THAN = 4

# DATA

fname = sys.argv[1]
warehouse: list[list[bool]] = list()

with open(fname, "r") as f:
    for line in f.readlines():
        line_data = [True if _ == "@" else False for _ in line.rstrip()]
        warehouse.append(line_data)

# HELPERS


def within_bounds(graph_2D: list[list[T]], col: int, row: int):
    height, width = len(graph_2D), len(graph_2D[0])
    return row >= 0 and row < height and col >= 0 and col < width


def adjacent_positions(graph_2D: list[list[T]], col: int, row: int):
    adj_pos = []
    if within_bounds(graph_2D, col, row) == False:
        return adj_pos
    for x, y in NEARBY:
        if within_bounds(graph_2D, col + x, row + y):
            value = graph_2D[row + y][col + x]
            adj_pos.append([row + y, col + x, value])
    return adj_pos


# PART ONE


def forklift_work(data: list[list[bool]]):
    rolls_to_move = []
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == True:
                neighbors = adjacent_positions(data, col, row)
                if [point[2] for point in neighbors].count(True) < FEWER_THAN:
                    # if less than 4 rolls of paper around, we can access the roll
                    rolls_to_move.append([col, row])  # and move it
    return rolls_to_move


S1 = len(forklift_work(warehouse))
print(f"Solution Part One: {S1}")

# PART TWO
num_rolls_removed = 0
# we remove rolls till there’s no more work (accessible rolls) left
work = forklift_work(warehouse)
while len(work) > 0:
    num_rolls_removed = num_rolls_removed + len(work)
    for point in work:
        warehouse[point[1]][point[0]] = False
    work = forklift_work(warehouse)


S2 = num_rolls_removed
print(f"Solution Part Two: {S2}")
