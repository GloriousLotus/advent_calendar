import sys

# CONSTANTS
START_POS = 50
DIAL_RANGE = 100

# HELPERS

# dial positions are int in 0,99
# dial moves are signed integer, sign + = right, sign - = left


def rot_dial(pos: int, mov: int) -> int:
    x = (pos + mov) % DIAL_RANGE
    # python modulo allow negative values,
    # so we ensure we stay in dial range
    if x < 0:
        x = x + DIAL_RANGE
    return x


def count_point_at_zero(pos: int, mov: int) -> int:
    """
    Count the number of times the dial point at zero
    during the move of pos by mov, dial excluded
    """
    q = abs(mov) // DIAL_RANGE
    if pos == 0:
        return q
    if mov < 0:
        if pos <= abs(mov) % DIAL_RANGE:
            q = q + 1
    elif mov > 0:
        if pos + mov % DIAL_RANGE >= DIAL_RANGE:
            q = q + 1
    return q


# READING DATA

fname = sys.argv[1]
safe_moves: list[int] = []

with open(fname) as f:
    for save_move_str in f.readlines():
        sign = 1 if save_move_str[0] == "R" else -1
        safe_move_int = sign * int(save_move_str[1:].rstrip())
        safe_moves.append(safe_move_int)

# PART ONE
# PWD = amount of times we land on zero during the dial moves

pwd, pos = 0, START_POS
for mov in safe_moves:
    pos = rot_dial(pos, mov)  # move the dial
    if pos == 0:  # if we land on 0, we must increase pwd by 1
        pwd = pwd + 1

print(f"Solution Part One: {pwd}")

# PART TWO
# PWD = amount of times we pass zero during the dial moves

pwd, pos = 0, START_POS
for mov in safe_moves:
    pwd = pwd + count_point_at_zero(
        pos, mov
    )  # if we move the dial by move, how many times does it point at zero ? increase password by that value
    pos = rot_dial(pos, mov)  # move the dial

print(f"Solution Part Two: {pwd}")
