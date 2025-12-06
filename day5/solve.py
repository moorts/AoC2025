with open("./input.txt") as f:
    data = f.read()
    ranges, ids = data.split("\n\n")
    ranges, ids = ranges.strip().splitlines(), ids.strip().splitlines()
    ranges = [line.split("-") for line in ranges]
    ranges = [[int(line[0]), int(line[1])] for line in ranges]
    ids = list(map(int, ids))

def part1():
    score = 0
    for ingredient in ids:
        for (start, end) in ranges:
            if start <= ingredient <= end:
                score += 1
                break

    return score

def intersect_ranges(range1, range2):
    if not range2:
        return []

    s1, e1 = range1
    s2, e2 = range2


    if e1 < s2:
        return [range2]
    if s1 > e2:
        return [range2]

    if s1 <= s2 and e1 >= e2:
        return []

    new_intervals = []
    if s2 < s1:
        new_intervals.append([s2, s1-1])
    if e2 > e1:
        new_intervals.append([e1+1, e2])

    return new_intervals

def part2():
    disjoint_ranges = []
    for (start, end) in ranges:
        additions = [(start, end)]
        for rng1 in disjoint_ranges:
            tmp = []
            for rng2 in additions:
                tmp.extend(intersect_ranges(rng1, rng2))
            additions = tmp
        disjoint_ranges.extend(additions)
    return sum([(end - start) + 1 for (start, end) in disjoint_ranges])
            

print(part1())
print(part2())
