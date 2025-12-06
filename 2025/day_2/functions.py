from functools import total_ordering,reduce
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@total_ordering
class Str_d:
    head:str
    tail:str
    def __init__(self,s:str):
        self.head = s[:len(s)//2]
        self.tail = s[len(s)//2:]

    def __str__(self):
        return self.head+self.tail
    
    def to_int(self):
        return int(str(self))

    def __eq__(self,other):
        return str(self)==str(other)
    
    def __lt__(self,other):
        return int(str(self)) < int(str(other))
    
    @staticmethod
    def pow(k)->str:
        return "1"+"0"*(k-1)

    def is_twin(self)->bool:
        return self.head == self.tail

    def next_twin(self)->"Str_d":
        if len(self.head) < len(self.tail):
            h = Str_d.pow(len(self.head)+1)
        elif self.head>self.tail:
            h = self.head
        else:
            h = str(int(self.head)+1)    
        return Str_d(h+h)

def twins_between(x:"Str_d",y:"Str_d"):
    L = []
    if x<=y:
        if x.is_twin():
            L.append(str(x))
        while(x.next_twin()<=y):
            x = x.next_twin()
            L.append(str(x))
    return L

def sum_ids(x:"Str_d",y:"Str_d"):
    S = 0
    if x<=y:
        S = 0
        if x.is_twin():
            S = S+ x.to_int()
        while(x.next_twin()<=y):
            x = x.next_twin()
            S = S+x.to_int()
    return S

def slices_length(santa_id):
    max_slice_length = (len(santa_id)+1)//2
    return [slice for slice in range(1,max_slice_length+1)                    
            if len(santa_id)%slice == 0 #id can be sliced equally
            ]

def is_invalid_id_for_slice_len(santa_id:str,slice_len:int):
    if len(santa_id)%slice_len != 0:
        return False
    first_slice = santa_id[:slice_len]
    for i in range(slice_len,len(santa_id),slice_len):
        new_slice = santa_id[i:i+slice_len]
        if first_slice != new_slice: #no pattern
            return False
    # all slices are equal to first slices -> true
    return True

def is_invalid_id(santa_id:str):
    #an id is invalid if there is a slice that repeats
    for s_l in slices_length(santa_id):
        if is_invalid_id_for_slice_len(santa_id,s_l):
            return True
    return False

def all_invalid_ids(id_start:str,id_stop:str)->set[int]:
    result = set() #we use a set in cases of duplicate range intersection
    int_start = int(id_start)
    int_stop = int(id_stop)
    if int_start>int_stop:#range is empty
        return result
    for n in range(int_start,int_stop+1):
        if n<10:#pattern needs to repeat TWICE at least
            continue
        str_n = str(n)
        if is_invalid_id(str_n) is True:
            result.add(n)
    return result