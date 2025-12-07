import sys

#CONSTANTS
vowels = ["a","e","i","o","u"]
alphabet = list('abcdefghijklmnopqrstuvwxyz')

#READING DATA

fname = sys.argv[1]
with open(fname) as f:
    data = [_.rstrip() for _ in f.readlines()]

def is_nice(x:str)->bool:
    #substring criteria
    if "ab" in x or "cd" in x or "pq" in x or "xy" in x:
        return False
    #vovel criteria
    vowel_count = 0
    for c in x:
        if c in vowels:
            vowel_count = vowel_count + 1
        if vowel_count >=3:
            break
    if vowel_count < 3:
        return False
    #repetition criteria
    for idx in range(len(x)-1):
        if x[idx]==x[idx+1]:
            return True
    return False

#PART ONE

assert is_nice("aaa") == True
assert is_nice("ugknbfddgicrmopn") == True
assert is_nice("jchzalrnumimnmhp") == False
assert is_nice("dvszwmarrgswjxmb") == False

total_nice = 0
for s in data:
    if is_nice(s):
        total_nice = total_nice + 1

print(f"Part One:{total_nice}")

#PART TWO

def is_nice2(x:str)->bool:
    #x contains a 2 substring that repeats (without overlap)
    if len(x)<4:
        return False
    rule1 = False
    for idx_1 in range(len(x)-3):
        first = x[idx_1:idx_1+2]
        for idx_2 in range(idx_1+2,len(x)):
            second = x[idx_2:idx_2+2]
            if first==second:
                rule1=True
    if rule1==False:
        return False
    #x contains a 3 substring like c1 c2 c1
    rule2 = False
    for idx in range(len(x)-2):
        first,second = x[idx],x[idx+2]
        if first==second:
            rule2 = True
    return rule2

assert is_nice2("qjhvhtzxzqqjkmpb")
assert is_nice2("xxyxx")
assert is_nice2("uurcxstgmygtbstg")==False
assert is_nice2("ieodomkazucvgmuy") == False

total_nice = 0
for s in data:
    if is_nice2(s):
        total_nice = total_nice + 1
print(f"Part Two:{total_nice}")