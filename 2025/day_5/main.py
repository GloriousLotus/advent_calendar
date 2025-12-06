from functools import reduce

#reading data
ingredients = list()
messy_inventory = []
fname = "example.txt"
with open(fname,"r") as f:
    for line in f.readlines():
        if line.strip().isdigit():
            ingredients.append(int(line.strip()))
        if line.count("-") > 0:
            messy_inventory.append([int(_) for _ in line.split("-")])

ingredients.sort() #probably optimize part 1 ?
messy_inventory.sort() #sort with lex order (useful for part 1 and 2)

#PART 1 : fresh ingredients
amount_fresh = 0
for ig in ingredients:
    for R in messy_inventory:
        if R[0]<=ig and ig<=R[1]:
            amount_fresh = amount_fresh+1
            break

print(f"Part One:{amount_fresh}")

#PART 2 : optimize inventory to have only disjoint ranges
#remember, inventory is sorted
cur_R = messy_inventory[0]
optimized_inventory = list()
for next_R in messy_inventory:
    if next_R[0]>cur_R[1]:#disjoint
        optimized_inventory.append(cur_R)
        cur_R = next_R
    else:#overlap
        if (next_R[0]==cur_R[0]) or (next_R[0]>cur_R[0] and next_R[1]>=cur_R[0]):#prev_R included in R
            cur_R = [cur_R[0],max(cur_R[1],next_R[1])] # we merge by extending the range to the max
optimized_inventory.append(cur_R) #at the end of the loop, prev_R contains the last maximal disjoint interval

#compute inventory size
inventory_size = reduce(lambda acc,R:acc+R[1]-R[0]+1,optimized_inventory,0)
print(f"Part Two:{inventory_size}")