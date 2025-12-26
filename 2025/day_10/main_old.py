import copy
from functools import cache, reduce
from itertools import chain, tee
import itertools
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
        BTN_MATRIX = sympy.Matrix(BTN_LIST).T
        
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

        print(f"Buttons\n")
        sympy.pprint(BTN_MATRIX)
        print(f"===\n")
        print(f"Password: {pwd_data}, Starting Sequence: {btns_win}\n")

        # PART TWO

        MAX_JOLTAGE = max(JOLTAGE)

        BTN_MATRIX = sympy.Matrix(BTN_LIST).T
        J = sympy.Matrix(JOLTAGE)
        levers_free,X = BTN_MATRIX.gauss_jordan_solve(J)

        if len(sum(levers_free).free_symbols)==0: #we have our answer
            S2 = S2 + sum(levers_free)
        else:
            #now we must minimize the amount of presses
            taus = levers_free.free_symbols
            #we determine the constraints per parameter
            #max amount we can use a lever
            def max_amount(lever:list[int]):
                return min([JOLTAGE[_] for _ in range(len(JOLTAGE)) if lever[_]!=0 in lever and JOLTAGE[_]>0])

            ineqs = {_:[] for _ in taus}
            for idx_lever in range(len(BTN_LIST)):
                lever = BTN_LIST[idx_lever]
                num_uses_lever = levers_free[idx_lever]
                if len(num_uses_lever.free_symbols)==1 and len(num_uses_lever.free_symbols.intersection(taus))>0:
                    tau = num_uses_lever.free_symbols.pop()
                    ineqs[tau].append(num_uses_lever>=0)
                    ineqs[tau].append(num_uses_lever<=max_amount(lever))
                    ineqs[tau].append(tau>=0)
            constraints = dict()
            for tau,ineq in ineqs.items():
                c=sympy.reduce_inequalities(ineq)
                if isinstance(c,sympy.Eq):
                    v = c.args[1]
                    levers_free = levers_free.subs(tau,v)
                    continue
                constraints[tau] = c
            taus_min_max = dict()
            #extract min and max values from constraints
            for tau,ineq in constraints.items():
                m,M = ineq.args[0].args[0],ineq.args[1].args[1] # this M is not a real MAX!
                taus_min_max[tau] = (int(m),int(M))


            cartesian_product = list()
            def gen(tau,min,max):
                for _ in range(min,max+1):
                    yield (tau,_)
            #time to try all remaining combineasons to minimize levers_free
            for tau,_ in taus_min_max.items():
                cartesian_product.append([(tau,_) for _ in range(taus_min_max[tau][0],taus_min_max[tau][1]+1)])
            
            s_min,levers_use_min = MAX_JOLTAGE*len(JOLTAGE), None
            for substitution in itertools.product(*cartesian_product):
                levers_uses_candidate = levers_free.subs(substitution)
                values = set(levers_uses_candidate)
                if len([_ for _ in values if _<0])>0:
                    continue
                elif [_ == int(_) for _ in values].count(False)>0:
                    continue
                else:
                    s_candidate = sum(levers_uses_candidate)
                    if s_candidate<s_min:
                        s_min = s_candidate
                        levers_use_min = levers_uses_candidate
            assert levers_use_min != None
            print(f"Joltage {JOLTAGE}")
            print(f"Lever uses: {s_min}, sequence: {[_ for _ in levers_use_min]}")
            S2 = S2 + s_min

        print(f"===\n")


print(f"Solution Part One:{S1}")
print(f"Solution Part Two:{S2}")