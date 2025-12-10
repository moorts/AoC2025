from z3 import *

test = False

if test:
    with open("test.txt") as f:
        data = f.read()
else:
    with open("input.txt") as f:
        data = f.read()

machines = data.splitlines()
machines = [machine.split() for machine in machines]

score = 0
for machine in machines:
    target = list(map(int, machine[-1][1:-1].split(',')))

    vectors = [list(map(int, line[1:-1].split(","))) for line in machine[1:-1]]
    new_vectors = []

    for vector in vectors:
        new_vector = [0 for _ in range(len(target))]
        for x in vector:
            new_vector[x] = 1
        new_vectors.append(new_vector)

    vectors = new_vectors

    o = Optimize()
    variables = [Int('x' + str(i)) for i in range(len(vectors))]
    for xi in variables:
        o.add(xi >= 0)
    for i in range(len(target)):
        constraint = sum([xi * vector[i] for xi, vector in zip(variables, vectors)]) == target[i]
        o.add(simplify(constraint))

    res = o.minimize(sum(variables))

    if o.check() == sat:
        score += res.value().as_long()
print(score)
