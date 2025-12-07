import copy
from functools import reduce
import sys

#READ DATA
fname = sys.argv[1]

with open(fname) as f:
    manifold = [list(line.rstrip()) for line in f.readlines()]

#assume the beam starts on first row
tachyon_pos = [manifold[0].index("S")]

#PART ONE
all_beams = [set(tachyon_pos)]
splitters = []
num_split = 0
for depth in range(1,len(manifold)):
    prev_beams = all_beams[-1]
    next_beams = set()
    splitters=[idx for idx in range(len(manifold[depth])) if manifold[depth][idx]=="^"]
    for b in prev_beams:#beam carry on
        if b not in splitters:
            next_beams.add(b)
        else:#beam split
            num_split = num_split + 1
            next_beams.add(b-1)
            next_beams.add(b+1)
    all_beams.append(next_beams)

print(f"Part One: {num_split}")

#EXTRA : render beams
full_split = []
full_split.append(manifold[0])
for depth in range(1,len(manifold)):
    splitters = copy.copy(manifold[depth])
    for b in all_beams[depth]:
        splitters[b]="|"
    full_split.append(splitters)


with open("part_one_output.txt","w") as f:
    for m in full_split:
        f.write("".join(m)+"\n")
#PART TWO
###BRUTE FORCE, with text outputs
if len(manifold)<=25:
    all_paths:list[list[tuple]] = [[(*tachyon_pos,"D")]]
    print(all_paths)
    for row in range(1,len(manifold)):
        splitters = [idx for idx in range(len(full_split[row])) if full_split[row][idx]=="^"]
        new_paths = list()
        for idx_path in range(len(all_paths)):
            path = all_paths[idx_path]
            pos_y = path[-1][0]
            if pos_y not in splitters:#the path continue as the same if no splitters
                all_paths[idx_path] = path+[(pos_y,"D")]
            else:
                left_path, right_path = path+[(pos_y-1,"L")],path+[(pos_y+1,"R")]
                all_paths[idx_path] = left_path
                new_paths.append(right_path) #new beam to the right
        all_paths = all_paths + new_paths

    print(f"Part Two: {len(all_paths)}")
    #output all paths to a .txt
    with open("part_two_output.txt","w") as f:
        #draw all paths
        for p in all_paths:
            manifold_copy = copy.deepcopy(manifold)
            path_word = ""
            for row in range(len(manifold_copy)):
                manifold_copy[row][p[row][0]] = "|"
                path_word = path_word+p[row][1]
                f.write("".join(manifold_copy[row])+"\n")
            f.write(path_word+"\n")
            f.write("\n")

#PART 2, the smart way
#NON SCATTERING: if there is no splitter at s, the number of paths at s doesn’t change
#SCATTERING: if there are n paths incoming at splitter s, 
#then there are n produced at pos s-1, n at pos s+1
# and 0 at s (no beam behind a splitter)
else:
    paths_by_node = {k:0 for k in range(len(manifold[0]))}
    paths_by_node[tachyon_pos[0]] = 1

    for row in range(len(full_split)):
        splitters = [_ for _ in range(0,len(full_split[row])) if full_split[row][_]=="^" and _ in paths_by_node]
        for s in splitters: #SCATTERING
            #LEFT SCATTERING
            paths_by_node[s-1] = paths_by_node[s-1]+paths_by_node[s]
            #RIGHT SCATTERING
            paths_by_node[s+1] = paths_by_node[s+1]+paths_by_node[s]
            #no more beam behind the splitter
            paths_by_node[s] = 0

    num_paths = reduce(lambda S,key:S+paths_by_node[key],paths_by_node,0)
    print(f"Solution Part Two: {num_paths}")