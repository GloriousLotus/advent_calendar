from functools import reduce
from itertools import product
import operator

#constants
str_to_ops = {"+":operator.add,"*":operator.mul}
#helpers
def column(m,idx:int):
    return [l[idx] for l in m]

def grand_total(num_list:list[list[int]],op_list):
    S = 0
    for idx in range(len(op_list)):
        S = S + reduce(op_list[idx],num_list[idx])
    return S

#part 1
#read data rows by rows
fname = "example.txt"
with open(fname) as f:
    lines = f.readlines()
    #remove all spaces
    ops = [str_to_ops[_] for _ in lines[-1].split()]
    numbers_by_lines = [list(map(int,_.split())) for _ in lines[:-1]]
    #build problem sets by transposing the numbers
    human_numbers = []
    for idx_pb in range(len(numbers_by_lines[0])):
        human_numbers.append(column(numbers_by_lines,idx_pb))

S = grand_total(human_numbers,ops)

print(f"Part One: {S}")

#part 2
#read raw colums, and build a raw_data matrix with the input content
with open(fname) as f:
    lines = f.readlines()[:-1] #last line already done with variable operators
    num_cols = len(lines[0])-1 #last column is technically \n\n\n...don’t need it
    raw_data = [[] for _ in range(num_cols)]
    for c in range(num_cols):
        for r in range(len(lines)):
            line = lines[r]
            raw_data[c].append(line[c])#adding character by character

#get our numbers
cephalopod_numbers = []
num_list = []
idx_pb = 0

#just read our numbers column by column
for col in raw_data:
    if col.count(" ")==len(col):
        #an empty column means we’re going to the next problem
        cephalopod_numbers.append(num_list)
        op = ops[idx_pb]
        idx_pb = idx_pb+1
        num_list = []
    else:#an non-empty column is a number once formatted
        n = int(reduce(operator.add,col)#concatenate all strings
                .replace(" ","")#remove empty ones
                )#now we have our number
        num_list.append(n) #add the human number to our current problem
cephalopod_numbers.append(num_list) #last_one


S = grand_total(cephalopod_numbers,ops)
print(f"Part Two: {S}")