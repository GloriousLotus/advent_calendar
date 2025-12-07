from enum import Enum
from functools import reduce
import sys

#constants
class Action(Enum):
    OFF=0
    ON=1
    TOGGLE=2



#read data
fname = sys.argv[1]

instructions = []
with open(fname) as f:
    for line in f.readlines():
        corners = [list(map(int,_2.split(","))) for _2 in [_1.rstrip() for _1 in line.split(" ") if "," in _1]]
        action = Action.ON if "turn on" in line else Action.OFF if "turn off" in line else Action.TOGGLE
        instructions.append((action,corners))

#ACT ONE
grid = dict()

def act_one(light:bool,a:Action)->bool:
    match a:
        case Action.OFF:
            return False
        case Action.ON:
            return True
        case Action.TOGGLE:
            return not light

for i in instructions:
    a=i[0]
    x_min,y_min,x_max,y_max = i[1][0][0],i[1][0][1],i[1][1][0],i[1][1][1]
    for x in range(x_min,x_max+1):
        for y in range(y_min,y_max+1):
            old_light = grid[x,y] if (x,y) in grid else False
            new_light = act_one(old_light,a)
            grid[x,y] = new_light

lights_turned_on = reduce(lambda S,l:S+int(l),grid.values(),0)

print(f"Part One: {lights_turned_on}")

#PART TWO

grid = {}

def act_two(light:int,a:Action):
    match a:
        case Action.OFF:
            return max(light-1,0)
        case Action.ON:
            return light+1
        case Action.TOGGLE:
            return light+2

for i in instructions:
    a=i[0]
    x_min,y_min,x_max,y_max = i[1][0][0],i[1][0][1],i[1][1][0],i[1][1][1]
    for x in range(x_min,x_max+1):
        for y in range(y_min,y_max+1):
            old_light = grid[x,y] if (x,y) in grid else 0
            new_light = act_two(old_light,a)
            grid[x,y] = new_light

lights_turned_on = reduce(lambda S,l:S+l,grid.values(),0)

print(f"Part Two: {lights_turned_on}")