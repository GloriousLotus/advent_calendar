from functools import reduce
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

fname = "input.txt"
with open(fname,"r") as f:
    data = [_.rstrip() for _ in f.readlines()]

def max_and_idx(L):
    M,idx = int(L[0]),0
    for i in range(len(L)):
        if int(L[i])>M:
            M,idx=int(L[i]),i
    return M,idx

def joltage(bank:str,num_digits:int):
    digits_info = [{"digit":0,"pos":-1} for _ in range(num_digits)]
    start_idx = 0
    for pos in range(0,num_digits):
        end_idx = len(bank)-num_digits+pos
        logger.debug(f"start_idx: {start_idx},end_idx:{end_idx}")
        max_rating,max_pos = int(bank[start_idx]),start_idx
        for i in range(start_idx,end_idx+1):
            rating = int(bank[i])
            if rating>max_rating:
                max_rating,max_pos=rating,i
        digits_info[pos]={"digit":max_rating,"pos":max_pos}
        start_idx = max_pos+1
    logger.debug(digits_info)
    J = reduce(lambda acc,d:acc+str(d["digit"]),digits_info,"")
    s = bank
    for d in digits_info.__reversed__():
        s = f'{s[:d["pos"]-1]}+{d["digit"]}@{d["pos"]}+{s[d["pos"]+1:]}'
    return {"total_joltage":J,"bank_info":s}

S=0

for bank in data:
    logger.info(bank)
    J = joltage(bank,12)
    logger.info(J)
    S=S+int(J["total_joltage"])

print(S)