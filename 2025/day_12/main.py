from collections.abc import Iterable
import copy
from functools import cache, reduce
from typing import NamedTuple, TypeAlias

import sys

from frozendict import frozendict

fshape = sys.argv[1]
ftree = sys.argv[2]


DIM = 3
CHARACTERS = [chr(_) for _ in range(97, 197)]
IdGiftClass: TypeAlias = int
IdGiftShape: TypeAlias = tuple[int, int]
GiftPacking: TypeAlias = frozendict[IdGiftClass, int]


class Point(NamedTuple):
    x: int
    y: int

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)


def draw_shape(points: frozenset[Point], char="#", width=-1, height=-1) -> str:
    if len(points) == 0:
        x_max = width - 1
        y_max = height - 1
    else:
        x_max: int = max(max(p.x for p in points), width - 1)
        y_max: int = max(max(p.y for p in points), height - 1)
    array_str = [["." for _y in range(y_max + 1)] for _x in range(x_max + 1)]
    for p in points:
        array_str[p.y][p.x] = char
    return reduce(lambda acc, r: acc + "".join(r) + "\n", array_str, "")


def overlap_drawing(
    drawing: str, points: Iterable[Point], char, width=-1, height=-1
) -> str:
    array_str = [[_ for _ in s] for s in drawing.split("\n")]
    for p in points:
        array_str[p.y][p.x] = char
    return reduce(lambda acc, r: acc + "".join(r) + "\n", array_str, "")


def iter_rect(x_min, x_max, y_min, y_max):
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            yield Point(x, y)


def translate(points: Iterable[Point], p: Point) -> frozenset[Point]:
    return frozenset(_.add(p) for _ in points)


def disk(p: Point, x_radius, y_radius, width, height):
    x_min = max(p.x - x_radius + 1, 0)
    x_max = min(p.x + x_radius - 1, width)
    y_min = max(p.y - y_radius + 1, 0)
    y_max = min(p.y + y_radius - 1, height)
    return iter_rect(x_min, x_max, y_min, y_max)


class Shape:
    shape: frozenset[Point]
    width: int
    height: int

    def __init__(self, shape: Iterable[Point], width, height) -> None:
        self.width = width
        self.height = height
        for p in shape:
            if p.x < 0 or p.x >= width or p.y < 0 or p.y >= height:
                raise Exception(f"{p} outside {width,height}")
        self.shape = frozenset(shape)

    def flip(self) -> "Shape":
        flipped = frozenset(Point(self.width - 1 - p.x, p.y) for p in self.shape)
        return Shape(flipped, self.width, self.height)

    def _transpose(self) -> "Shape":
        t = frozenset(Point(p.y, p.x) for p in self.shape)
        return Shape(t, self.height, self.width)

    def rot_cw(self):
        return self._transpose().flip()

    def find_border(self) -> frozenset[Point]:
        def _f(shape: frozenset[Point]):
            # default border is right and bottom edge
            bottom_edge = set(Point(x, self.height) for x in range(self.width + 1))
            right_edge = set(Point(self.width, y) for y in range(self.height + 1))

            visited_cols = set()

            for y in range(self.height - 1, -1, -1):
                for x in range(self.width):
                    if (
                        x not in visited_cols
                        and Point(x, y) not in shape
                        and Point(x, y + 1) in bottom_edge
                    ):
                        bottom_edge.remove(Point(x, y + 1))
                        bottom_edge.add(Point(x, y))
                        visited_cols.add(x)

            visited_rows = set()
            for x in range(self.width - 1, -1, -1):
                for y in range(self.height):
                    if (
                        y not in visited_rows
                        and Point(x, y) not in shape
                        and Point(x + 1, y) in right_edge
                    ):
                        right_edge.remove(Point(x + 1, y))
                        right_edge.add(Point(x, y))
                        visited_cols.add(y)

            return right_edge.union(bottom_edge)

        right_and_bottom_border = translate(_f(self.shape), Point(1, 1))
        top_and_left_border = (
            Shape(_f(self.rot_cw().rot_cw().shape), self.width + 1, self.height + 1)
            .rot_cw()
            .rot_cw()
        ).shape

        corners = set(
            [
                Point(0, 0),
                Point(0, self.height + 1),
                Point(self.width + 1, self.height + 1),
                Point(self.width + 1, 0),
            ]
        )

        return top_and_left_border.union(right_and_bottom_border).union(corners)

    def __repr__(self):
        return draw_shape(self.shape, "#")


class Gift(Shape):
    def __init__(self, shape: Iterable[Point]):
        super().__init__(shape, width=DIM, height=DIM)

    def all_variants(self) -> list["Gift"]:
        shapes = [self.shape]
        c = copy.copy(self)
        for _ in range(3):
            f = c.flip()
            if f.shape not in shapes:
                shapes.append(f.shape)
            c = c.rot_cw()
            if c.shape not in shapes:
                shapes.append(c.shape)
        return [Gift(x) for x in shapes]


class TreeRegion:
    width: int
    height: int
    packed_gifts: dict[Point, Gift]
    border: set[Point]

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.packed_gifts = dict()
        self.border = set()

    def can_add_gift(self, gift: Gift, corner_00: Point) -> bool:
        # check if it fits
        if corner_00.x + DIM > self.width or corner_00.y + DIM > self.height:
            return False
        # check overlap
        gift_grid = translate(gift.shape, corner_00)
        # we check a grid around corner of DIM distance every way
        around_the_corner = disk(corner_00, DIM, DIM, self.width, self.height)
        for p in around_the_corner:
            if p in self.packed_gifts:
                # if we have a gift within DIM distance, we check if there’s overlap
                other_gift = self.packed_gifts[p]
                other_gift_grid = translate(other_gift.shape, p)
                if len(gift_grid.intersection(other_gift_grid)) > 0:
                    return False
        # if it fits and there is no overlap with existing packing, then we may add it
        return True

    def add_gift(self, gift: Gift, corner_00: Point):
        if self.can_add_gift(gift, corner_00):
            # add the gift
            self.packed_gifts[corner_00] = gift
            # update the border

            return True
        else:
            return False

    def draw(self) -> str:
        drawing = draw_shape(frozenset(), "#", self.width, self.height)
        for idx, (corner_00, gift) in zip(
            range(len(self.packed_gifts)), self.packed_gifts.items()
        ):
            gift_grid = translate(gift.shape, corner_00)
            drawing = overlap_drawing(
                drawing, gift_grid, CHARACTERS[idx], self.width, self.height
            )
        return drawing


class Tree:
    regions: list[TreeRegion]
    target_packings: list[GiftPacking]

    def __init__(self) -> None:
        self.regions = list()
        self.target_packings = list()


# READ DATA

shape_classes: list[Gift] = []
with open(fshape) as f:
    lines = f.readlines()
    for id_class in range(len(lines)):
        line = lines[id_class]
        if line[0].isdigit():
            shape_data = [
                lines[id_class + 1].strip(),
                lines[id_class + 2].strip(),
                lines[id_class + 3].strip(),
            ]
            points = set()
            for y in range(len(shape_data)):
                for x in range(len(shape_data[0])):
                    if shape_data[y][x] == "#":
                        points.add(Point(x, y))
            base_shape = Gift(points)
            shape_classes.append(base_shape)

GIFTS: dict[IdGiftClass, list[Gift]] = dict()
for id_class, base_shape in zip(range(len(shape_classes)), shape_classes):
    GIFTS[id_class] = list()
    print(f"=== Shape {id_class} ===")
    for id_shape, shape in zip(
        range(len(Gift.all_variants(base_shape))), Gift.all_variants(base_shape)
    ):
        GIFTS[id_class].append(shape)
        variant_border = shape.find_border()
        border_shape = draw_shape(
            variant_border, width=DIM + 2, height=DIM + 2, char="@"
        )
        variant_drawing = overlap_drawing(
            drawing=border_shape,
            points=translate(shape.shape, Point(1, 1)),
            char="#",
        )
        print(f"{id_class,id_shape}\n{variant_drawing}")


tree = list()
with open(ftree) as f:
    lines = f.readlines()
    for line in lines:
        dims, qty = line.split(":")
        # REGION
        region_size = [int(_) for _ in dims.split("x")]
        region = TreeRegion(*region_size)
        # TARGET
        qty = [int(_) for _ in qty[1:].split(" ")]
        packing = frozendict({_: qty[_] for _ in range(len(qty))})
        tree.append([region, packing])

# TESTS

print(f"=== TESTS ===")

# borders

s = GIFTS[5][1]
b = s.find_border()


# fitting gifts

tiny_region = TreeRegion(3, 3)
gift_13 = GIFTS[1][3]
gift_11 = GIFTS[1][1]
gift_50 = GIFTS[5][0]

assert tiny_region.can_add_gift(GIFTS[1][3], Point(0, 0)) == True
assert tiny_region.can_add_gift(GIFTS[1][3], Point(1, 0)) == False
assert tiny_region.can_add_gift(GIFTS[1][3], Point(0, 1)) == False

assert tiny_region.add_gift(GIFTS[1][3], Point(0, 0)) == True
assert tiny_region.add_gift(GIFTS[1][3], Point(0, 0)) == False
assert tiny_region.add_gift(GIFTS[1][1], Point(0, 0)) == False
tiny_region.packed_gifts = dict()
assert tiny_region.add_gift(GIFTS[1][1], Point(0, 0)) == True

small_region = TreeRegion(7, 7)
draw_shape(GIFTS[5][0].shape, "#")
assert small_region.add_gift(GIFTS[5][0], Point(0, 0)) == True
print(f"=== SMALL REGION ===\n")
print(small_region.draw())
assert small_region.add_gift(GIFTS[5][0], Point(2, 1)) == True
print(small_region.draw())
assert small_region.add_gift(GIFTS[4][1], Point(3, 2)) == False
assert small_region.add_gift(GIFTS[4][1], Point(4, 2)) == True
print(small_region.draw())


# PART ONE

S1 = 0

# create iterator

for region, target_packing in tree:

    @cache
    def _f(r: TreeRegion, packing: GiftPacking):
        if sum(packing.values()) == 0:
            return True
        if len(r.border) == 0:
            return sum(packing.values()) == 0
        for point in r.border:
            for id_class, nb in packing.items():
                if nb == 0:
                    continue
                for gift in GIFTS[id_class]:
                    if r.can_add_gift(gift, point):
                        region1 = copy.copy(r)
                        packing1 = dict(packing)
                        packing1[id_class] = packing1[id_class] - 1
                        region1.add_gift(gift, point)
                        is_packed = _f(region1, frozendict(packing1))
                        if is_packed:
                            return True

    if _f(region, target_packing):
        S1 = S1 + 1

print(f"Solution Part One: {S1}")
