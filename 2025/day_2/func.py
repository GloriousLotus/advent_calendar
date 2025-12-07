import copy
from functools import reduce


def next_head(x:str)->str:
    if len(x)%2!=0:
        return "1"+"0"*(len(x)//2)
    else:        
        x_head = int(x[:len(x)//2])
        x_tail = int(x[len(x)//2:])
        if x_head<x_tail:
            x_head = x_head + 1
        return str(x_head)

def prev_head(x:str)->str:
    if len(x)%2!=0:
        return "9"*(len(x)//2)
    else:
        x_head = int(x[:len(x)//2])
        x_tail = int(x[len(x)//2:])
        if x_head>x_tail:
            x_head = x_head-1
        return str(x_head)

def is_invalid_id_n(x:str,n:int)->bool:
    if n==1 or len(x)%n !=0:
        return False
    else:
        q = len(x)//n
        for _ in range(n-1):
            if x[q*_:q*_+q] != x[q*_+q:q*_+2*q]:
                return False
        return True


def slice_n(x:str,n:int)->list[str]:
    q= len(x)//n
    return [x[q*_:q*_+q] for _ in range(n)]

def next_n(x:str,n:int)->list[str]:
    q,r = len(x)//n,len(x)%n
    if n==1:
        if x == "9"*q:
            return ["1" for _ in range(q+1)]
        else:
            max_d = max([int(_) for _ in x])
            return [str(max_d) for _ in x]
    elif r==0:
        slices = slice_n(x,n)
        sl = int(slices[0])
        if sl<=max([int(_) for _ in slices[1:]]):
            sl = sl+1
        return [str(sl) for _ in range(n)]
    else:
        return [("1"+"0"*q) for _ in range(n)]