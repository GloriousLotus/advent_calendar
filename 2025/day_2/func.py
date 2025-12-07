#PART ONE
def geq_pattern_2(x:str)->str:
    if len(x)%2!=0:
        return "1"+"0"*(len(x)//2)
    else:
        x_head = int(x[:len(x)//2])
        x_tail = int(x[len(x)//2:])
        if x_head<x_tail:
            x_head = x_head + 1
        return str(x_head)

def leq_pattern_2(x:str)->str:
    if len(x)%2!=0:
        return "9"*(len(x)//2)
    else:
        x_head = int(x[:len(x)//2])
        x_tail = int(x[len(x)//2:])
        if x_head>x_tail:
            x_head = x_head-1
        return str(x_head)

#PART TWO
def is_invalid_id_n(x:str,n:int)->bool:
    if n<=1 or n>len(x) or len(x)%n !=0:
        return False
    else:
        q = len(x)//n
        for _ in range(n-1):
            if x[q*_:q*_+q] != x[q*_+q:q*_+2*q]:
                return False
        return True


def slice_n(x:str,n:int)->list[str]:
    q = len(x)//n
    return [x[q*_:q*_+q] for _ in range(n)]

def geq_invalid_pattern(x:str,n:int):
    pat = "0"
    q,r = len(x)//n,len(x)%n
    if n<=1:
        return pat
    elif is_invalid_id_n(x,n):
        pat = x[0:q]
    elif r==0:
        slices = slice_n(x,n)
        pat = slices[0]
        for sl in slices[1:]:
            if int(slices[0])>int(sl):
                break
            if int(slices[0])<int(sl):
                pat = str(int(slices[0])+1)
                break
    else:
        pat = "1"+"0"*q
    return pat

def leq_invalid_pattern(x:str,n:int):
    pat = "0"
    q,r = len(x)//n,len(x)%n
    if n<=1:
        return pat
    elif is_invalid_id_n(x,n):
        pat = x[0:q]
    elif r==0:
        slices = slice_n(x,n)
        pat = slices[0]
        for sl in slices[1:]:
            if int(slices[0])<int(sl):
                break
            if int(slices[0])>int(sl):
                pat = str(int(slices[0])-1)
                break
    else:
        pat = "9"*q
    return pat