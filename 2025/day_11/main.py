import copy
import sys
from typing import Iterable, NamedTuple
from functools import cache

fname = sys.argv[1]

class Node(NamedTuple):
    label:str
    children:set[str]

out = Node(label="out",children=set())
DEVICES:dict[str,Node] = dict()
DEVICES["out"] = out
#read data

with open(fname,"r") as f:
    lines = f.readlines()
    for line in lines:
        name,stuff = line.rstrip().split(": ")
        data = stuff.split(" ")
        device = Node(label=name,children=set())
        for d in data:
            device.children.add(d)
        DEVICES[name] = device

def paths_from_to(nodes:dict[str,Node],start:str,goal:str)->set[str]:
    paths:set[str] = set()
    visited_nodes:set[str] = set()
    #we store our paths as the sequence of nodes’ label visited, 
    # so you -> aaa -> bbb wil be you aaa bbb (just like in input.txt)
    journeys:list[str] = [f"{start} {_}" for _ in nodes[start].children] 
    N = len(journeys)
    while(N>0):
        new_journeys = list()
        for j in journeys:
            dest = j[-3:] #our destination is the last node in j
            visited_nodes.add(dest)
            device = nodes[dest]
            if goal in device.children: #destination reached
                paths.add(f"{j} {goal}")
            else:
                for child in device.children:
                    if child not in visited_nodes: #no need to revisit devices
                        n_j = f"{j} {child}"
                        new_journeys.append(n_j) #we add every children as new destinations
        journeys = copy.copy(new_journeys)
        N = len(new_journeys)
    return paths

def num_paths(nodes:dict[str,Node],start_label:str,end_label:str):
    if start_label == end_label:
        return 1
    @cache
    def _recursive(start_label,end_label)->int:
        if start_label == end_label: #we’ve arrived, one path
            return 1
        children = nodes[start_label].children
        return sum([_recursive(c,end_label) for c in children]) #number of paths = sum of numbers of paths from children to end
    return _recursive(start_label,end_label)

        
#PART 1

start = "you"
P = paths_from_to(DEVICES,"you","out")
print(f"Solution Part One:{len(P)}")

#PART 2

SERVER_RACK = "svr"
DAC = "dac"
FFT = "fft"

DAC_TO_FFT = paths_from_to(DEVICES,DAC,FFT)
print(f"No paths from DAC to FFT:{len(DAC_TO_FFT)==0}")
print(f"All our paths therefore will be like {SERVER_RACK}->{FFT}->{DAC}->out")

N_PATHS_DAC_OUT = num_paths(DEVICES,DAC,"out")
assert N_PATHS_DAC_OUT == len(paths_from_to(DEVICES,DAC,"out"))

N_PATHS_FFT_DAC= num_paths(DEVICES,FFT,DAC)

N_PATHS_SERVER_FFT = num_paths(DEVICES,SERVER_RACK,FFT)

print(f"Solution Part Two: {N_PATHS_DAC_OUT*N_PATHS_FFT_DAC*N_PATHS_SERVER_FFT}")