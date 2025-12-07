from functools import reduce
import sys

#helpers
def wrap_required(x:int,y:int,z:int)->int:
    return 2*x*y+2*y*z+2*z*x+ min(x*y,y*z,z*x)

def ribbon_required(x:int,y:int,z:int)->int:
    a,b,c = min(x,y,z),x+y+z-min(x,y,z)-max(x,y,z),max(x,y,z)
    print(x,y,z,a,b,c)
    smallest_perimeter = min(2*(a+b),2*(b+c),2*(c+a))
    shortest_wraparound = 2*a+2*b
    bow = a*b*c
    return min(smallest_perimeter,shortest_wraparound)+bow

#READING DATA

fname = sys.argv[1]

#part 1 & 2
total_wrap = 0
total_ribbon = 0
with open(fname) as f:
    for line in f.readlines():
        dim = [int(_) for _ in line.split("x")]
        wrap_area = wrap_required(*dim)
        ribbon = ribbon_required(*dim)
        total_ribbon = total_ribbon + ribbon
        total_wrap = total_wrap + wrap_area

#3803038 too high
print(f"Part One: {total_wrap}")
print(f"Part Two: {total_ribbon}")

print(ribbon_required(2,3,4))
print(ribbon_required(1,1,10))