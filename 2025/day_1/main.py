from itertools import accumulate
#CONSTANTS
start_pos = 50
dial_range = 100

#READING DATA
fname = "input.txt"

with open(fname) as f:
    lines = [_.rstrip() for _ in f]

safe_moves = []
for safe_move in lines:
    move_n = int(safe_move[1:])
    sign = 1 if safe_move[0]=="R" else -1
    safe_moves.append(sign*move_n)

#HELPERS
def mod_fn(x,y):
    S = (x+y)%dial_range
    if S<0:
        S = S+dial_range
    return S

def point_at_zero(cur_pos,mov):
    q = abs(mov)//100
    if cur_pos == 0:
        return q
    if mov<0:
        if cur_pos <= abs(mov)%100:
            q = q+1
    if mov>0:
        if cur_pos + mov%100 >= 100:
            q=q+1
    return q

#part one
real_moves = [start_pos]+safe_moves
santa_one = list(accumulate(real_moves,mod_fn))[1:] #we count AFTER the rotation so we exclude step 1
pwd_one = santa_one.count(0)
print(f"Part One Password : {pwd_one}")

#part two
santa_two = [start_pos]
pwd_two = [0]

for move_n in safe_moves:
    cur_pos = santa_two[-1]
    cur_pwd = pwd_two[-1]
    new_pwd = cur_pwd + point_at_zero(cur_pos,move_n)
    pwd_two.append(new_pwd)
    new_pos = mod_fn(cur_pos,move_n)
    santa_two.append(new_pos)
#we don’t count 0 in starting values
del santa_two[0] 
del pwd_two[0]
print(f"Part Two Password : {pwd_two[-1]}")

headers = "dial"
data = []
for _ in range(len(lines)):
    entry = {"pos":santa_two[_],"mov":safe_moves[_],"pwd":pwd_two[_]}
    data.append(entry)

history = [(data[_-1],data[_]) for _ in range(1,len(data))]

with open("history.txt","w+") as f:
    for d in history:
        row = f"{d[0]['pos']} mov {d[1]['mov']} to {d[1]['pos']} ; pwd: {d[1]['pwd']}"
        f.write(row+"\n")