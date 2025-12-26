from functools import reduce
import operator
import sys

# constants
str_to_ops = {"+": operator.add, "*": operator.mul}


# helpers
def column(m, idx: int):
    return [row[idx] for row in m]


def grand_total(num_list: list[list[int]], op_list):
    S = 0
    for op, num in zip(op_list, num_list):
        S = S + reduce(op, num)
    return S


# part 1
# read data rows by rows
fname = sys.argv[1]

with open(fname) as f:
    lines = f.readlines()
    # remove all spaces
    PROBLEM_OPERATIONS = [str_to_ops[_] for _ in lines[-1].split()]
    numbers_by_lines = [list(map(int, _.split())) for _ in lines[:-1]]
    # build problem sets by transposing the numbers
    human_numbers = [
        [row[col] for row in numbers_by_lines]
        for col in range(len(numbers_by_lines[0]))
    ]

S = grand_total(human_numbers, PROBLEM_OPERATIONS)

print(f"Part One: {S}")

# part 2
# read raw colums, and build a raw_data matrix with the input content
with open(fname) as f:
    lines = f.readlines()[:-1]  # last line already done with variable operators
    num_cols = len(lines[0]) - 1  # last column is technically \n\n\n...don’t need it
    raw_data = [[] for _ in range(num_cols)]
    for col in range(num_cols):
        for row in range(len(lines)):
            raw_data[col].append(lines[row][col])

# get our numbers
cephalopod_numbers = []
num_list = []
idx_pb = 0

# just read our numbers column by column, right to left
for col in raw_data:
    if col.count(" ") == len(col):
        # an empty column means we’re going to the next problem
        cephalopod_numbers.append(num_list)
        op = PROBLEM_OPERATIONS[idx_pb]
        idx_pb = idx_pb + 1
        num_list = []
    else:  # an non-empty column is a number once formatted
        n = int(reduce(operator.add, col).replace(" ", ""))
        num_list.append(n)  # add the human number to our current problem
cephalopod_numbers.append(num_list)  # last problem num list


S = grand_total(cephalopod_numbers, PROBLEM_OPERATIONS)
print(f"Part Two: {S}")
