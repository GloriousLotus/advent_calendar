import sys
#READING DATA
fname = sys.argv[1]

with open(fname) as f:
    ids_range_str = f.read().split(",")

IDS_RANGE = list(
    map(lambda x:[_ for _ in x.split("-")],
        ids_range_str))

#PART ONE

def geq_pattern_2(x:str)->str:
    # for number x with two slices A B, 
    # return the next number C C such that C C >= A B
    if len(x)%2!=0:
        return "1"+"0"*(len(x)//2)
    else:
        x_head = int(x[:len(x)//2])
        x_tail = int(x[len(x)//2:])
        if x_head<x_tail:
            x_head = x_head + 1
        return str(x_head)

def leq_pattern_2(x:str)->str:
    # for number x with two slices A B, 
    # return the next number C C such that C C <= A B
    if len(x)%2!=0:
        return "9"*(len(x)//2)
    else:
        x_head = int(x[:len(x)//2])
        x_tail = int(x[len(x)//2:])
        if x_head>x_tail:
            x_head = x_head-1
        return str(x_head)

S1 = 0

for min_id, max_id in IDS_RANGE:
    min_pattern = int(geq_pattern_2(min_id))
    if int(str(min_pattern)*2)>=int(max_id):
        continue
    max_pattern = int(leq_pattern_2(max_id))
    for pat in range(min_pattern,max_pattern+1):
        i_id = str(pat)*2
        S1 = S1 + int(i_id)

print(f"Part one: {S1}")

# PART TWO

def slice_n(x:str,n:int)->list[str]:
    sl_span = len(x)//n
    return [x[sl_span*_:sl_span*_+sl_span] for _ in range(n)]

def is_invalid_id_n(x:str,n:int)->bool:
    #id is invalid iff we can slice it in a pattern that repeats
    if n<=1 or n>len(x) or len(x)%n !=0:
        return False
    else:
        slices_n = slice_n(x,n)
        return len(set(slices_n))==1 #only one slice that repeats

def next_pattern(x:str,n:int):
    # if we slice x in a_1 ... a_n, 
    # return the smallest number b such that x <= b ... b
    # e.g. x = 1328, n = 2 -> 14  (1328<=1414)
    slice_span,unsliced_span = len(x)//n,len(x)%n
    if n<=1:
        return "0"
    elif is_invalid_id_n(x,n):
        return x[0:slice_span]
    elif unsliced_span==0:
        slices = slice_n(x,n)
        pat = slices[0] #for x = a_1 ... a_n, pat = a_1
        for sl in slices[1:]:
            if int(slices[0])>int(sl): #if pat>a_k and pat=a_1=...=a_{k-1}, then pat ... pat >= x
                break
            if int(slices[0])<int(sl): #if pat < a_k we move to pat+1, since (pat+1)...(pat+1)>=x
                pat = str(int(slices[0])+1)
                break
        return pat
    else:
        return "1"+"0"*slice_span # e.g. x=132, n=2 -> next number = 1010, so pat = 10

def prev_pattern(x:str,n:int):
    # if we slice x in a_1 ... a_n, 
    # return the biggest number b such that x >= b ... b
    # e.g. x = 1328, n = 2 -> 13  (1328>=1313)
    # see next_pattern for explanations
    slice_span,unsliced_span = len(x)//n,len(x)%n
    if n<=1:
        return "0"
    elif is_invalid_id_n(x,n):
        return x[0:slice_span]
    elif unsliced_span==0:
        slices = slice_n(x,n)
        pat = slices[0]
        for sl in slices[1:]:
            if int(slices[0])<int(sl):
                break
            if int(slices[0])>int(sl):
                pat = str(int(slices[0])-1)
                break
        return pat
    else:
        return "9"*slice_span #e.g x = 13245, n = 2 -> prev number = 9999, pat = 99

invalid_ids = set()

for min_id, max_id in IDS_RANGE:
    for num_slices in range(2,len(max_id)+1):
        min_pattern = next_pattern(min_id,num_slices) #the smallest invalid pattern such that pattern*num_slices >= min_id
        max_pattern = prev_pattern(max_id,num_slices) #the largest invalid pattern such that pattern*num_slices <= max_id
        if int(min_pattern)>int(max_pattern): #no invalid ids in range
            continue
        for pat in range(int(min_pattern),int(max_pattern)+1): #we enumerate all the numbers pat ... pat in the ID range
            i_id=str(pat)*num_slices
            invalid_ids.add(i_id)

S2 = sum([int(_) for _ in invalid_ids])

print(f"Part two: {S2}")