from func import rot_dial, point_at_zero
import sys
#CONSTANTS
start_pos = 50

#READING DATA
fname = sys.argv[1]

#dial positions are int in 0,99
#dial moves are signed integer, sign + = right, sign - = left
safe_moves:list[int] = []
with open(fname) as f:
    for save_move_str in f.readlines():
        sign = 1 if save_move_str[0]=="R" else -1
        safe_move_int = sign * int(save_move_str[1:].rstrip())
        safe_moves.append(safe_move_int)

#part one
pwd, dial_pos = 0, start_pos
for mov in safe_moves:
    dial_pos = rot_dial(dial_pos,mov)#move the dial
    if dial_pos == 0:#we count the 0
        pwd = pwd+1

print(f"Part One Password: {pwd}")

#part two
pwd,dial_pos = 0, start_pos
for mov in safe_moves:
    pwd = pwd + point_at_zero(dial_pos,mov) #IF we move the dial, how many times does it point at 0?
    dial_pos = rot_dial(dial_pos,mov) #move the dial

print(f"Part Two Password: {pwd}")