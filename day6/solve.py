with open("input.txt") as f:
    lines = f.read().splitlines()
    rows = [line.split() for line in lines]
    columns = [[row[i] for row in rows] for i in range(len(rows[0]))]
    columns = [(list(map(int, column[:-1])), column[-1]) for column in columns]

def part1():
    total = 0
    for col, op in columns:
        subtotal = col[0]
        for val in col[1:]:
            if op == "*":
                subtotal *= val
            elif op == "+":
                subtotal += val
            else:
                print("wtf")
        total += subtotal
    return total

def part2():
    col_data = lines[:-1]
    ops = lines[-1]

    total = 0
    current_op = None
    subtotal = 0

    for i in range(len(ops)):
        if ops[i] in ["*", "+"]:
            current_op = ops[i]
            total += subtotal
            subtotal = 0 if current_op == "+" else 1
        num = ""
        for row in col_data:
            if row[i].isdigit():
                num += row[i]
        if num.isdecimal():
            x = int(num)
            if current_op == "*":
                subtotal *= x
            else:
                subtotal += x
    total += subtotal

    return total

print(part1())
print(part2())
