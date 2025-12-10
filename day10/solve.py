from collections import defaultdict
from math import inf
from collections import deque
import heapq

test = False

if test:
    with open("test.txt") as f:
        data = f.read()
else:
    with open("input.txt") as f:
        data = f.read()

machines = data.splitlines()
machines = [machine.split() for machine in machines]

def parseMachine(machine):
    schematic = machine[0][1:-1]
    n = len(schematic)
    schematic = int(schematic.replace('#', '1').replace('.', '0')[::-1], 2)

    G = [[] for _ in range(2**n)]

    for button in machine[1:-1]:
        button = sum([2**int(btn) for btn in button[1:-1].split(",")])

        for source in range(2**n):
            target = source ^ button
            G[source].append(target)

    return G, schematic

def shortest_path(G, target):
    queue = deque()
    queue.append((0, 0))

    dist = 0
    seen = set()

    while queue:
        dist, curr = queue.popleft()

        for neighbor in G[curr]:
            if neighbor in seen:
                continue
            if neighbor == target:
                return dist + 1
            
            queue.append((dist + 1, neighbor))
            seen.add(neighbor)
def part1():
    res = 0
    for machine in machines:
        G, target = parseMachine(machine)

        res += shortest_path(G, target)
    return res

print(part1())
