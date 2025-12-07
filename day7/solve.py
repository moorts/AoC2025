from functools import cache

with open("input.txt") as f:
    grid = f.read().strip().splitlines()

def part1():
    n = len(grid)
    m = len(grid[0])
    print(n, len(grid[0]))
    assert grid[0][m // 2] == 'S'

    beams = { (1, m // 2) }

    score = 0

    for row in grid[2:-1]:
        new_beams = set()
        for y, x in beams:
            ty, tx = y + 1, x
            if grid[ty][tx] == ".":
                new_beams.add((ty, tx))
            elif grid[ty][tx] == '^':
                if 0 < tx:
                    new_beams.add((ty, tx-1))
                if tx < m-1:
                    new_beams.add((ty, tx + 1))
                score += 1
        beams = new_beams

    return score

@cache
def recurse(start_y, start_x, n, m):
    if start_y == n-1:
        return 1

    ty, tx = start_y + 1, start_x

    if grid[ty][tx] == '.':
        return recurse(ty, tx, n, m)
    else:
        score = 0
        if 0 < tx:
            score += recurse(ty, tx - 1, n, m)
        if tx < m - 1:
            score += recurse(ty, tx + 1, n, m)
        return score



def part2():
    n = len(grid)
    m = len(grid[0])
    print(n, len(grid[0]))
    assert grid[0][m // 2] == 'S'

    return recurse(1, m // 2, n, m)

print(part1())
print(part2())
