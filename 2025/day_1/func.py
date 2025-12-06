dial_range = 100
#HELPERS
def rot_dial(dial:int,mov:int)->int:
    '''
    Rotate dial position by mov
    dial positions are an int between 0 and 99
    '''
    S = (dial+mov)%dial_range
    if S<0:
        S = S+dial_range
    return S

def point_at_zero(cur_pos:int,mov:int)->int:
    '''
    Count the number of times the dial point at zero
    during the move of cur_pos by mov
    cur_pos excluded
    '''
    q = abs(mov)//100
    if cur_pos == 0:
        return q
    if mov<0:
        if cur_pos <= abs(mov)%100:
            q = q+1
    elif mov>0:
        if cur_pos + mov%100 >= 100:
            q=q+1
    return q
