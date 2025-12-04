with open("input.txt") as f:
    data = f.read().strip().splitlines()

def neighbors(x, y):
    return set([(y + dy, x + dx) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx != 0 or dy != 0)])

def part1():
    n = len(data)
    m = len(data[0])
    rolls = set()
    for y in range(n):
        for x in range(m):
            if data[y][x] == '@':
                rolls.add((y, x))
    score = 0
    for (y, x) in rolls:
        if len(rolls & neighbors(x, y)) < 4:
            score += 1
    return score


def part2():
    n = len(data)
    m = len(data[0])
    rolls = set()
    for y in range(n):
        for x in range(m):
            if data[y][x] == '@':
                rolls.add((y, x))
    score = 0
    while True:
        new_rolls = set()
        updated = False
        for (y, x) in rolls:
            if len(rolls & neighbors(x, y)) < 4:
                score += 1
                updated = True
            else:
                new_rolls.add((y, x))
        if not updated:
            break
        rolls = new_rolls
    return score

def neighbors(x, y):
    return set([(y + dy, x + dx) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx != 0 or dy != 0)])

def part2_better():
    n, m = len(data), len(data[0])
    rolls = set((y, x) for y in range(n) for x in range(m) if data[y][x] == '@')
    working_set = set(rolls)

    score = 0
    while working_set:
        new_working_set = set()
        for (y, x) in working_set:
            if len(rolls & neighbors(x, y)) < 4:
                if (y, x) in rolls:
                    score += 1
                    rolls.remove((y, x))
                    new_working_set |= (neighbors(x, y) & rolls)
        working_set = new_working_set
    return score

print(part1())
print(part2_better())
