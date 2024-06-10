def showLit(lit):
    if lit[1]:
        return lit[0]
    else:
        return "~" + lit[0]


def showClause(clause):
    """
    Formats a clause by putting 'v' between literals
    """
    return " v ".join(map(showLit, clause))


def showCNF(F):
    return " ^ ".join("(" + showClause(clause) + ")" for clause in F)


def alphaLit(lit, alpha):
    if lit[0] in alpha:
        return lit[1]
    else:
        return False


def alphaClause(clause, alpha):
    results = [alphaLit(l, alpha) for l in clause]
    return any(results)


def alphaCNF(cnf, alpha):
    # print(showCNF(cnf))
    return all([alphaClause(c, alpha) for c in cnf])


def neg(literal):
    return (literal[0], not literal[1])


# Formel aus Übung 07
def F(x, y, z):
    return [
        [x, neg(y)],
        [neg(x), neg(y), neg(z)],
        [neg(x), z],
        [x, y, z],
        [y, neg(z)],
    ]


def main():
    import itertools

    print("~~~ 1. ~~~")
    print(showLit(("A", False)) + "\n" + showLit(("B", True)))

    print("~~~ 2. ~~~")
    a = [("B", False)]
    b = [("A", True), ("B", True), ("C", False)]
    c = [a, b]

    print(showClause(a) + "\n" + showClause(b))

    print(showCNF(c))

    print("~~~ 3. ~~~")
    alpha = ["A", "B"]
    print(f'A = {alphaLit(("A", True), alpha)}')
    print(f'B = {alphaLit(("B", False), alpha)}')
    print(f'C = {alphaLit(("C", True), alpha)}')
    print(f"{showClause(a)} = {alphaClause(a, alpha)}")
    print(f"{showClause(b)} = {alphaClause(b, alpha)}")
    print(f"{showCNF(c)} = {alphaCNF(c, alpha)}")

    print("~~~ 4. ~~~")
    # Erfüllende Belegung??
    # alpha_true = {"A": True, "B": False, "C": True}
    alpha_true = {"A": False, "B": False, "C": False}

    # Nicht erfüllende Belegung
    alpha_false = {"A": False, "B": True, "C": True}

    print(f"Erfüllende Belegung: {alpha_true} -> {alphaCNF(c, alpha_true)}")
    print(
        f"Nicht erfüllende Belegung: {alpha_false} -> {alphaCNF(c, alpha_false)}"
    )

    print("~~~ 5. ~~~")
    for assignment in itertools.product([True, False], repeat=3):
        lits = tuple(zip(["X", "Y", "Z"], assignment))
        print(showCNF(F(lits[0], lits[1], lits[2])))
        print(alphaCNF(F(lits[0], lits[1], lits[2]), alpha))


if __name__ == "__main__":
    main()
