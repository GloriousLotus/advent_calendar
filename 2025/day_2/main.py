import sys
from func import geq_pattern_2,leq_pattern_2,geq_invalid_pattern,leq_invalid_pattern
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
    min_id, max_id = product_range
    min_pattern = int(geq_pattern_2(min_id))
    if int(str(min_pattern)*2)>=int(max_id):
        continue
    max_pattern = int(leq_pattern_2(max_id))
    for i in range(min_pattern,max_pattern+1):
        i_id = str(i)*2
        S = S + int(i_id)

print(f"Part one: {S}")


#part 2
invalid_ids = set() #we use a set to eliminate duplicates, e.g. 1111 = 11+11 and 1111 = 1+1+1+1

for product_range in ids_range:
    min_id,max_id = product_range
    for num_slices in range(2,len(max_id)+1):
        min_pattern = geq_invalid_pattern(min_id,num_slices) #the smallest invalid pattern such that pattern*num_slices >= min_id
        max_pattern = leq_invalid_pattern(max_id,num_slices) #the largest invalid pattern such that pattern*num_slices <= max_id
        if int(min_pattern)>int(max_pattern): #no invalid ids in range
            continue
        for pat in range(int(min_pattern),int(max_pattern)+1):
            i_id=str(pat)*num_slices
            invalid_ids.add(i_id)

S = sum([int(_) for _ in invalid_ids])

print(f"Part two: {S}")