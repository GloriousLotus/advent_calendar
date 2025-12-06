from functools import reduce
from functions import Str_d, all_invalid_ids, is_invalid_id, slices_length, sum_ids, twins_between

import logging
main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.INFO)

fname = "input.txt"

with open(fname) as f:
    ids_range_str = f.read().split(",")

ids_range = list(map(lambda x:[_ for _ in x.split("-")],ids_range_str))
#part 1

S = 0
for C in ids_range:
    x = Str_d(C[0])
    y = Str_d(C[1])
    S = S + sum_ids(x,y)

print(S)

#part 2
invalid_ids = set()

for id_start,id_stop in ids_range:
    invalid_ids = invalid_ids.union(all_invalid_ids(id_start,id_stop))

S2 = sum(invalid_ids)

print(S2)