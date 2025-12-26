from functools import reduce
import sys
from typing import NamedTuple


class IntervalID(NamedTuple):
    low: int
    high: int

    def has(self, x):
        return self.low <= x <= self.high

    def is_disjoint(self, other: "IntervalID") -> bool:
        return other.low > self.high or self.low > other.high

    def width(self):
        return self.high - self.low + 1


# READING DATA

fname = sys.argv[1]
FRESH_INVENTORY: list[IntervalID] = []
INGREDIENTS: list[int] = list()

with open(fname, "r") as f:
    for line in f.readlines():
        if line.strip().isdigit():
            INGREDIENTS.append(int(line.strip()))
        if line.count("-") > 0:
            r = [int(_) for _ in line.split("-")]
            FRESH_INVENTORY.append(IntervalID(low=r[0], high=r[1]))

INGREDIENTS.sort()  # probably optimize part 1 ?
# sort with lex order (useful for part 1 and 2)
FRESH_INVENTORY.sort(key=lambda l: l.low)

# PART 1 : fresh ingredients
amount_fresh = 0
for ing in INGREDIENTS:
    for range_inv in FRESH_INVENTORY:
        if range_inv.has(ing):
            amount_fresh = amount_fresh + 1
            break

print(f"Part One:{amount_fresh}")

# PART 2 : optimize inventory to have only disjoint ranges
# remember, inventory is already sorted by lex order
prev = FRESH_INVENTORY[0]
disjointed_inventory: list[IntervalID] = list()
for cur in FRESH_INVENTORY:
    if cur.is_disjoint(prev):  # if disjoint, just add it to the list and go next
        disjointed_inventory.append(prev)
        prev = cur
    else:
        # since prev <= cur for lex order must overlap like
        # [prev.low----[cur.low-----cur.high]---prev.high],
        # or [prev.low----[cur.low-----prev.high]---cur.high],
        # we merge them -> [prev.low ---- max(prev.high,cur.high)]
        prev = IntervalID(low=prev.low, high=max(prev.high, cur.high))
# at the end of the loop, prev contains the last maximal disjoint interval that we haven’t yet used
disjointed_inventory.append(prev)

# compute inventory size
inventory_size = reduce(lambda acc, R: acc + R.width(), disjointed_inventory, 0)
print(f"Part Two:{inventory_size}")
