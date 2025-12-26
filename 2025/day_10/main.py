import copy
from functools import reduce
import sys

import sympy

sympy.init_printing(use_unicode=True)

fname = sys.argv[1]

def iter_btn(n:int):
    N = 2**n
    for i in range(1,N):
        yield set(k for k in range(n) if (i>>k)&1 == 1)

S1 = S2 = 0

with open(fname,"r") as f:
    lines = f.readlines()
    for line in lines:
        print(f"Machine: {line}\n")
        #read data
        
        line = line.replace("[","").replace("}","")
        pwd_data,stuff=line.split("]")
        buttons_data,joltage_data = stuff.split("{")
        
        # password
        PWD = list(map(lambda c:1 if c=="#" else 0,pwd_data))
        
        # creating the buttons
        buttons_list = []
        buttons_data = buttons_data.replace(" ","")[1:-1].split(")(")
        for btn_data in buttons_data:
            lever = [0 for _ in PWD]
            for _ in btn_data.split(","):
                lever[int(_)] = 1
            lever = tuple(lever)
            buttons_list.append(lever)
        BTN_LIST = copy.copy(buttons_list)
        
        # joltage requirement
        JOLTAGE = tuple([int(_) for _ in joltage_data.split(",")])
        
        # PART ONE
        btns_win, nb_presses_min = None, len(BTN_LIST)
        for btn_presses in iter_btn(len(BTN_LIST)):
            btns = [BTN_LIST[_] for _ in btn_presses]
            nb_presses = len(btn_presses)
            if nb_presses<nb_presses_min:
                check = reduce(lambda acc,btn:
                               [1 if acc[_] != btn[_] else 0 for _ in range(len(PWD))],
                               btns,
                               PWD)
                if set(check) == set({0}):
                    btns_win, nb_presses_min = btn_presses, nb_presses
        S1 = S1 + nb_presses_min
        print(f"Password: {pwd_data}, Starting Sequence: {btns_win}\n")
        nice_btn_list = reduce(lambda S,btn:S+"\n"+str(btn),BTN_LIST,"")
        print(f"Buttons\n{nice_btn_list}\n===\n")
        
        # PART TWO

        MAX_JOLTAGE = max(JOLTAGE)

        BTN_MATRIX = sympy.Matrix(BTN_LIST).T
        J = sympy.Matrix(JOLTAGE)
        levers_free,X = BTN_MATRIX.gauss_jordan_solve(J)
        params = list(X.atoms())
        
        A,b = sympy.linear_eq_to_matrix(levers_free,params)
        Z = A.row_join(-b)
        def add_row_sum(m:sympy.Matrix):
            return m.col_join(sympy.ones(1,m.rows)*m)
        Z = add_row_sum(Z)


        sympy.pprint([params,add_row_sum(levers_free),Z])

        print(f"===\n")




        
print(f"Solution Part One:{S1}")
print(f"Solution Part Two:{S2}")