import sys
from func import next_head,prev_head,next_rep,prev_rep
#READING DATA
fname = sys.argv[1]

with open(fname) as f:
    ids_range_str = f.read().split(",")

ids_range = list(
    map(lambda x:[_ for _ in x.split("-")],
        ids_range_str))
#part 1

S = 0
for product_range in ids_range:
    left, right = product_range
    head_left = int(next_head(left))
    if int(str(head_left)+str(head_left))>=int(right):
        continue
    head_right = int(prev_head(right))
    for i in range(head_left,head_right+1):
        invalid_id = str(i)+str(i)
        S = S + int(invalid_id)

print(f"Part one:{S}")


#part 2
S=0
invalid_ids = set()
for product_range in ids_range:
    left,right = product_range
    for num_slices in range(2,len(right)+1):
        max_pattern = prev_rep(right,num_slices)
        min_pattern = next_rep(left,num_slices)
        if int(min_pattern)>int(max_pattern):
            continue
        print(num_slices,left,min_pattern*num_slices,max_pattern*num_slices,right)
        for pat in range(int(min_pattern),int(max_pattern)+1):
            patterned_str=str(pat)*num_slices
            invalid_ids.add(patterned_str)

L = [int(_) for _ in invalid_ids]
L.sort()
print(L)

S = sum(L)

print(f"Part two: {S}")