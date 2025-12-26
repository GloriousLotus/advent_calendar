from collections.abc import Iterable, Iterator
import copy
import sys
from typing import Literal, NamedTuple

fname = sys.argv[1]


# helpers
class Tile(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return repr((self.x, self.y))


def rect_area(lhs: Tile, rhs: Tile):
    width, height = abs(rhs.x - lhs.x), abs(rhs.y - lhs.y)
    return (width + 1) * (height + 1)


def window(l: Iterable[Tile]) -> dict[Literal["x_min", "x_max", "y_min", "y_max"], int]:
    exes: set[int] = set(t.x for t in l)
    whys: set[int] = set(t.y for t in l)
    return {
        "x_min": min(exes),
        "x_max": max(exes),
        "y_min": min(whys),
        "y_max": max(whys),
    }


class Edge(NamedTuple):
    start: Tile
    stop: Tile

    def is_vertical(self) -> bool:
        return self.start.x == self.stop.x

    def it(self) -> Iterator[Tile]:
        # we only have vertical or horizontal edges
        delta = (
            1 if ((self.start.y < self.stop.y) or (self.start.x < self.stop.x)) else -1
        )  # we are on positive slope if stop>start
        if self.start.x == self.stop.x:  # vertical
            return iter(
                Tile(self.start.x, y)
                for y in range(self.start.y, self.stop.y + delta, delta)
            )
        else:  # horizontal
            return iter(
                Tile(x, self.start.y)
                for x in range(self.start.x, self.stop.x + delta, delta)
            )

    def __repr__(self):
        return repr((self.start, self.stop))


class Rectangle:
    corners: list[Tile]

    def __init__(self, corner_00: Tile, corner_11: Tile):
        corner_01 = Tile(corner_00.x, corner_11.y)
        corner_10 = Tile(corner_11.x, corner_00.y)
        self.corners = [corner_00, corner_01, corner_11, corner_10]

    def edges(self):
        return [
            Edge(self.corners[idx], self.corners[(idx + 1) % 4]) for idx in range(4)
        ]

    def area(self) -> int:
        lhs, rhs = self.corners[0], self.corners[2]
        return rect_area(lhs, rhs)

    def window(self) -> dict[Literal["x_min", "x_max", "y_min", "y_max"], int]:
        return window(self.corners)


def read_data(fname: str) -> list[Tile]:
    vertices: list[Tile] = list()
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = lines + [lines[0]]  # our shapes loop
        for line in lines:
            coords = [int(_) for _ in line.split(",")]
            vertices.append(Tile(coords[0], coords[1]))
    return vertices


def draw_shape(vertices: list[Tile]) -> list[list[str]]:
    w = window(vertices)
    shape_txt: dict[tuple[int, int], str] = {
        (x, y): "." for x in range(w["x_max"] + 1) for y in range(w["y_max"] + 1)
    }
    for idx in range(len(vertices) - 1):
        e = Edge(vertices[idx], vertices[idx + 1])
        for t in e.it():
            shape_txt[t.x, t.y] = "X"
        shape_txt[e.start.x, e.start.y] = shape_txt[e.stop.x, e.stop.y] = "#"
    lines = [
        [shape_txt[x, y] for x in range(w["x_max"] + 1)] for y in range(w["y_max"] + 1)
    ]
    return lines


def add_rectangle(shape_txt: list[list[str]], r: Rectangle):
    new_data = copy.copy(shape_txt)
    full_rect = [e.it() for e in r.edges()]
    for line in full_rect:
        for t in line:
            new_data[t.y][t.x] = "O"
    return new_data


def save_shape(fname: str, grid: list[list[str]]):
    with open(fname, "w") as f:
        for chars in grid:
            line = "".join(chars)
            f.write(line + "\n")


# TESTS BECAUSE WE STRUGGLED

e1 = Edge(Tile(0, 3), Tile(0, 5))
e2 = Edge(Tile(7, 0), Tile(1, 0))
e3 = Edge(Tile(0, 5), Tile(0, 1))

assert [t for t in e1.it()][1:-1] == [Tile(0, 4)]
assert [t for t in e2.it()][1:-1] == [Tile(_, 0) for _ in range(6, 1, -1)]
assert [t for t in e3.it()][1:-1] == [Tile(0, _) for _ in range(4, 1, -1)]

real_rectangle = Rectangle(Tile(0, 3), Tile(7, 0))
assert real_rectangle.window() == {"x_min": 0, "x_max": 7, "y_min": 0, "y_max": 3}
assert real_rectangle.area() == 32

# EXAMPLE 1
ex = read_data("example.txt")
ex_shape_txt = draw_shape(ex)
save_shape("./examples/ex1_s.txt", ex_shape_txt)

real_rectangle = Rectangle(Tile(7, 1), Tile(9, 7))
ex_shape_with_rect = add_rectangle(ex_shape_txt, real_rectangle)
save_shape("./examples./ex1_r.txt", ex_shape_with_rect)

# EXAMPLE 2

ex2_shape = read_data("example2.txt")
ex2_shape_txt = draw_shape(ex2_shape)
save_shape("./examples/ex2_s.txt", ex2_shape_txt)

r21 = Rectangle(Tile(2, 2), Tile(20, 4))
ex2_r21 = add_rectangle(copy.deepcopy(ex2_shape_txt), r21)
save_shape("./examples/ex2_r21.txt", ex2_r21)

r22 = Rectangle(Tile(2, 10), Tile(10, 7))
ex2_r22 = add_rectangle(copy.deepcopy(ex2_shape_txt), r22)
save_shape("./examples/ex2_r22.txt", ex2_r22)

r23 = Rectangle(Tile(12, 3), Tile(16, 3))
ex2_r22 = add_rectangle(copy.deepcopy(ex2_shape_txt), r22)
save_shape("./examples/ex2_r22.txt", ex2_r22)

# PUZZLE

DATA = read_data(fname)

# MINIMIZING THE SHAPE

exes = set([t.x for t in DATA])
whys = set([t.y for t in DATA])
coords = list(exes.union(whys))
coords.sort()

OUTLINE = [Tile(coords.index(t.x), coords.index(t.y)) for t in DATA]
NUM_POINTS = len(OUTLINE)
# DRAW THE SHAPE
MIN_SHAPE_TXT = draw_shape(OUTLINE)
save_shape("shape.txt", MIN_SHAPE_TXT)

# PART ONE
area_max = 0
for idx_00 in range(NUM_POINTS):
    for idx_11 in range(idx_00 + 1, NUM_POINTS):
        area_max = max(area_max, rect_area(DATA[idx_00], DATA[idx_11]))

print(f"Solution part one:{area_max}")

# PART TWO

# find the max area of a rect inside the shape


# RECTANGLES
# sorted by area in reverse orser
def _rectangles():
    rectangles = list()
    for idx_00 in range(NUM_POINTS):
        for idx_11 in range(idx_00 + 1, NUM_POINTS):
            mini_00, mini_11 = OUTLINE[idx_00], OUTLINE[idx_11]
            real_00, real_11 = DATA[idx_00], DATA[idx_11]
            rectangles.append(
                {
                    "rectangle": Rectangle(mini_00, mini_11),
                    "area": rect_area(real_00, real_11),
                }
            )
    rectangles.sort(key=lambda entry: entry["area"], reverse=True)
    return rectangles


RECTANGLES = _rectangles()

W = window(OUTLINE)
X_MAX, Y_MAX = W["x_max"], W["y_max"]

# OUTSIDE
# because the shape is a loop, it is connex
# if the outside exists, its starting points are on the frontier
# we check the frontier and explore inwards till we hit the perimeter

# FRONTIER
FRONTIER = list()
for x in range(0, X_MAX + 1):
    FRONTIER.append(Tile(x, 0))
    FRONTIER.append(Tile(x, Y_MAX))
for y in range(0, Y_MAX + 1):
    FRONTIER.append(Tile(0, y))
    FRONTIER.append(Tile(X_MAX, y))


# PERIMITER
PERIMITER = set()
for idx_1 in range(len(OUTLINE) - 1):
    e = Edge(OUTLINE[idx_1], OUTLINE[idx_1 + 1])
    for t in e.it():
        PERIMITER.add(t)


# EXPLORING
def next(t: Tile) -> set[Tile]:
    s = set()
    if t.x > 0:  # down
        s.add(Tile(t.x - 1, t.y))
    if t.x < X_MAX:  # up
        s.add(Tile(t.x + 1, t.y))
    if t.y > 0:  # left
        s.add(Tile(t.x, t.y - 1))
    if t.y < Y_MAX:  # right
        s.add(Tile(t.x, t.y + 1))
    return s


# OUTSIDE = EXPLORING THE FRONTIER TILL HITTING THE PERIMETER
def _outside():
    outside = set()
    destinations = set([s for s in FRONTIER if s not in PERIMITER])
    while len(destinations) > 0:
        new_destinations = set()
        for d in destinations:
            outside.add(d)
            for n in next(d):
                if n not in outside and n not in PERIMITER:
                    new_destinations.add(n)
        destinations = copy.copy(new_destinations)
    return outside


OUTSIDE = _outside()

# let’s draw "OUTSIDE"

OUTSIDE_TXT = copy.copy(MIN_SHAPE_TXT)
for t in OUTSIDE:
    OUTSIDE_TXT[t.y][t.x] = "@"
save_shape("outside.txt", OUTSIDE_TXT)

# SOLUTION


def is_rect_inside(r: Rectangle):
    for e in r.edges():
        for t in e.it():
            if t in OUTSIDE:
                return False
    return True


for d in RECTANGLES:
    r = d["rectangle"]
    if is_rect_inside(r):
        area_max = d["area"]
        break  # RECTANGLES is sorted by area reverse order


print(f"Solution part two:{area_max}")
