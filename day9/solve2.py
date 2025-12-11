from itertools import combinations
from collections import defaultdict
from shapely import Polygon

with open("input.txt") as f:
    tiles = [line.split(",") for line in f.read().splitlines()]
    tiles = [(int(l[1]), int(l[0])) for l in tiles]

area = Polygon(tiles)

mx = 0
for (y1, x1), (y2, x2) in combinations(tiles, 2):
    box = Polygon([(y1, x1), (y1, x2), (y2, x2), (y2, x1)])

    if area.contains(box):
        mx = max(mx, (abs(y2 - y1) + 1) * (abs(x2 - x1) + 1))

print(mx)
