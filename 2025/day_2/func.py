#PART ONE
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

#PART TWO
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

def next_rep(x:str,n:int):
    q,r = len(x)//n,len(x)%n
    ans = ""
    if n==1:
        return x
    elif is_invalid_id_n(x,n):
        ans = x[0:q]
    elif r==0:
        slices = slice_n(x,n)
        ans = slices[0]
        for sl in slices[1:]:
            if int(slices[0])>int(sl):
                break
            if int(slices[0])<int(sl):
                ans = str(int(slices[0])+1)
                break
    else:
        ans = "1"+"0"*q
    return ans

def prev_rep(x:str,n:int):
    q,r = len(x)//n,len(x)%n
    ans = ""
    if n==1:
        return x
    elif is_invalid_id_n(x,n):
        ans = x[0:q]
    elif r==0:
        slices = slice_n(x,n)
        ans = slices[0]
        for sl in slices[1:]:
            if int(slices[0])<int(sl):
                break
            if int(slices[0])>int(sl):
                ans = str(int(slices[0])-1)
                break
    else:
        ans = "9"*q
    return ans