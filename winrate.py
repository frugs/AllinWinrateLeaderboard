def arithmetic_sum(n, expr):
    def inner(i, sum_so_far):
        if i < n:
            return inner(i + 1, sum_so_far + expr(i))
        else:
            return sum_so_far

    return inner(0, 0)


def arithmetic_product(n, expr):
    def inner(i, product_so_far):
        if i <= n:
            return inner(i + 1, product_so_far * expr(i))
        else:
            return product_so_far

    return inner(1, 1)


def factorial(n):
    return arithmetic_product(n, lambda x: x)


def ncr(n, r):
    if r == 1 or n == r:
        return 1

    return factorial(n) / (factorial(r) * factorial(n - r))


def binomial(x, n, p):
    return ncr(n, x) * pow(p, x) * pow(1 - p, n - x)

players = []

file = open("wins.txt")
for line in file:
    split_line = line.split(" ")
    name = split_line[0]
    wins = int(split_line[1])
    played = int(split_line[2])
    losses = played - wins

    if played == 0:
        continue

    probability = 1 - arithmetic_sum(wins, lambda x: binomial(x, played, 0.5))
    players.append((name, probability))

file.close()

sorted_players = sorted(players, key=lambda x: x[1])
for player in sorted_players:
    print(player[0], "{:.2f}%".format(player[1] * 100))
