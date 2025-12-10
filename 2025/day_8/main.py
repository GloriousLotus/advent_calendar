import copy
from functools import reduce
import sys
from typing import TypeAlias

Junction:TypeAlias = tuple[int,int,int]

#helpers
def dist_3D(lhs:Junction,rhs:Junction)->int:
    return (lhs[0]-rhs[0])**2+(lhs[1]-rhs[1])**2+(lhs[2]-rhs[2])**2

def find_keys(d:dict,lookup):
    return [_ for _,v in d.items() if v==lookup]

def read_data(fname:str)->list[Junction]:
    junctions = list()
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            line.rstrip()
            j = [int(_) for _ in line.split(",")]
            junctions.append((j[0],j[1],j[2]))
    return junctions

class JunctionGrid:
    size:int
    distances:dict[int,list[tuple[int,int]]]

    def __init__(self,junctions:list[Junction]):
        self.size = len(junctions)
        self.distances = dict()
        self.connections = {_:_ for _ in range(self.size)}
        for idx_1 in range(self.size):
            j1 = junctions[idx_1]
            for idx_2 in range(idx_1+1,self.size):
                j2 = junctions[idx_2]
                d = dist_3D(j1,j2)
                if d in self.distances:
                    self.distances[d].append((idx_1,idx_2))
                else:
                    self.distances[d] = [(idx_1,idx_2)]


    def closest_n_pairs(self,n:int):
        D = list(self.distances.keys())
        D.sort()
        pairs = list()
        loop=0
        for d in D:
            for p in self.distances[d]:
                pairs.append(p)
                loop=loop+1
                if loop==n:
                    return pairs
        return pairs


# READING data
fname = sys.argv[1]
num_connections = int(sys.argv[2])

junctions = read_data(fname)
grid = JunctionGrid(junctions)

#PART 1
connections: dict[int,int] = dict()
P = grid.closest_n_pairs(num_connections)

for lhs,rhs in P:
    if lhs not in connections:
        connections[lhs] = lhs
    if rhs not in connections:
        connections[rhs] = rhs
    lhs_circuit,rhs_circuit = connections[lhs],connections[rhs]
    to_connect = {junction:id_circuit for junction,id_circuit in connections.items() if id_circuit in [lhs_circuit,rhs_circuit]}
    id_circuit = min(to_connect.values())
    for id_junction in to_connect:
        connections[id_junction]=id_circuit

id_circuits = set(connections.values())
size_circuits:list[int] = list()
for id_c in id_circuits:
    circuit = find_keys(connections,id_c)
    size_circuits.append(len(circuit))

#circuits
size_circuits.sort(reverse=True)
print(f"circuits by size:{size_circuits[0:3]}")
triple_max = reduce(lambda P,x:P*x,size_circuits[0:3])
print(f"Solution Part One:{triple_max}")

#PART TWO

P = grid.closest_n_pairs(len(grid.distances.values()))
history = []

for lhs,rhs in P:
    if lhs not in connections:
        connections[lhs] = lhs
    if rhs not in connections:
        connections[rhs] = rhs
    lhs_circuit,rhs_circuit = connections[lhs],connections[rhs]
    to_connect = {junction:id_circuit for junction,id_circuit in connections.items() if id_circuit in [lhs_circuit,rhs_circuit]}
    id_circuit = min(to_connect.values())
    for id_junction in to_connect:
        connections[id_junction]=id_circuit
    if lhs_circuit != rhs_circuit:
        history.append([lhs,rhs])
    if len(connections.values())==1:
        break

last_connection = junctions[history[-1][0]],junctions[history[-1][1]]

print(f"Solution Part Two:{last_connection[0][0]*last_connection[1][0]}")
