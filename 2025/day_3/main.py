from functools import reduce
import sys

# READING DATA
fname = sys.argv[1]
with open(fname, "r") as f:
    data = [_.rstrip() for _ in f.readlines()]


# HELPERS
def joltage(bank: str, num_digits: int):
    digits_info = [{"digit": 0, "pos": -1} for _ in range(num_digits)]
    start_idx = 0
    for pos in range(0, num_digits):
        end_idx = len(bank) - num_digits + pos
        max_rating, max_pos = int(bank[start_idx]), start_idx
        for i in range(start_idx, end_idx + 1):
            rating = int(bank[i])
            if rating > max_rating:
                max_rating, max_pos = rating, i
        digits_info[pos] = {"digit": max_rating, "pos": max_pos}
        start_idx = max_pos + 1
    J = reduce(lambda acc, d: acc + str(d["digit"]), digits_info, "")
    s = bank
    for d in digits_info.__reversed__():
        s = f'{s[:d["pos"]-1]}+{d["digit"]}@{d["pos"]}+{s[d["pos"]+1:]}'
    return {"total_joltage": J, "bank_info": s}


# PART ONE

S1 = 0

for bank in data:
    J = joltage(bank, 2)
    S1 = S1 + int(J["total_joltage"])

print(f"Solution Part Two: {S1}")

# PART TWO

S2 = 0

for bank in data:
    J = joltage(bank, 12)
    S2 = S2 + int(J["total_joltage"])

print(f"Solution Part Two: {S2}")
