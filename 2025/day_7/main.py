import copy
from functools import reduce
import sys

# READ DATA
fname = sys.argv[1]

with open(fname) as f:
    MANIFOLD = [list(line.rstrip()) for line in f.readlines()]
    SPLITTERS = [
        [col for col in range(len(MANIFOLD[depth])) if MANIFOLD[depth][col] == "^"]
        for depth in range(len(MANIFOLD))
    ]

# assume the beam starts on first row
TACHYON_POS = MANIFOLD[0].index("S")

# PART ONE
all_beams = [set([TACHYON_POS])]
num_split = 0
for depth in range(1, len(MANIFOLD)):
    prev_beams = all_beams[-1]
    cur_beams = set()
    for b in prev_beams:
        # no splitter = the beam carry on
        if b not in SPLITTERS[depth]:
            cur_beams.add(b)
        # splitter, beam is split
        else:
            num_split = num_split + 1
            cur_beams.add(b - 1)
            cur_beams.add(b + 1)
    all_beams.append(cur_beams)

print(f"Solution Part One: {num_split}")

# EXTRA : render beams
full_split = []
full_split.append(MANIFOLD[0])
for depth in range(1, len(MANIFOLD)):
    row = copy.copy(MANIFOLD[depth])
    for b in all_beams[depth]:
        row[b] = "|"
    full_split.append(row)

with open("part_one_output.txt", "w") as f:
    for m in full_split:
        f.write("".join(m) + "\n")

# PART TWO
# NON SCATTERING: if there is no splitter at s, the number of paths at s doesn’t change
# SCATTERING: if there are n paths incoming at splitter s,
# then there are n produced at pos s-1, n at pos s+1
# and 0 at s (no beam behind a splitter)

paths_by_column = {k: 0 for k in range(len(MANIFOLD[0]))}
paths_by_column[TACHYON_POS] = 1

for depth in range(len(MANIFOLD)):
    # SCATTERING
    for s in SPLITTERS[depth]:
        # LEFT SCATTERING
        # if there were paths already on s-1, they merge with the scattered paths
        paths_by_column[s - 1] = paths_by_column[s - 1] + paths_by_column[s]
        # RIGHT SCATTERING
        # if there were paths already on s+1, they merge with the scattered paths
        paths_by_column[s + 1] = paths_by_column[s + 1] + paths_by_column[s]
        # no more beam behind the splitter
        paths_by_column[s] = 0

num_paths = reduce(lambda S, col: S + paths_by_column[col], paths_by_column, 0)

print(f"Solution Part Two: {num_paths}")
