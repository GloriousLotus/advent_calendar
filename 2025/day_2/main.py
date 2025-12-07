import sys
from func import next_head,prev_head
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
    print(product_range)
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
invalid_ids = set()