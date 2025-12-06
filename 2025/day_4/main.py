from functools import reduce
from typing import TypeVar
T = TypeVar("T")

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

nearby = [[_1,_2] for _1 in range(-1,2) for _2 in range(-1,2) if _1 != 0 or _2 !=0]
fewer_than = 4

fname = "input.txt"

data:list[list[bool]] = list()

with open(fname,"r") as f:
    for line in f.readlines():
        line_data = [True if _=="@" else False for _ in line.rstrip()]
        data.append(line_data)

def within_bounds(graph_2D:list[list[T]],x:int,y:int):
    height, width = len(graph_2D),len(graph_2D[0])
    return y>=0 and y < height and x>=0 and x < width

def adjacent_positions(graph_2D:list[list[T]],x:int,y:int):
    adj_pos = []
    if within_bounds(graph_2D,x,y) == False:
        return adj_pos
    for u,v in nearby:
        if within_bounds(graph_2D,x+u,y+v):
            value = graph_2D[y+v][x+u]
            adj_pos.append([y+v,x+u,value])
    return adj_pos

def forklift_work(warehouse:list[list[bool]]):  
    result = []
    for y in range(len(warehouse)):
        for x in range(len(warehouse[0])):
            if warehouse[y][x] == True:
                neighbors = adjacent_positions(warehouse,x,y)
                if [point[2] for point in neighbors].count(True) < fewer_than:
                    result.append([x,y])
    return result

def forklife_workload_optimal(warehouse:list[list[bool]]):
    num_rolls_removed = 0
    X = warehouse
    work = forklift_work(X)
    while len(work)>0:
        num_rolls_removed = num_rolls_removed + len(work)
        for point in work:
            X[point[1]][point[0]] = False
        work = forklift_work(X)
    return num_rolls_removed

print(forklife_workload_optimal(data))
