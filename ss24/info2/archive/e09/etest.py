def showLit(lit):
    if lit[1]:
        return lit[0]
    else:
        return "~" + lit[0]


# format a clause so that we put v between literals and surround the clause with parentheses
def showClause(clause):
    return "(" + " v ".join(map(showLit, clause)) + ")"


def showCNF(F):
    return " ^ ".join(map(showClause, F))


# Implement the resolution rule for propositional logic
# Given two clauses c1 and c2, return the resolvent of c1 and c2
def resolve(c1, c2):
    for lit in c1:
        if (lit[0], not lit[1]) in c2:
            c1.remove(lit)
            c2.remove((lit[0], not lit[1]))
            return c1 + c2
    return None


# Compute Res^n(K(F)) for a given formula F and a given n
def res(KF, n):
    for i in range(n):
        new_clauses = []
        for c1 in range(len(KF)):
            for c2 in range(c1 + 1, len(KF)):
                resolvent = resolve(KF[c1], KF[c2])
                if resolvent is not None:
                    new_clauses.append(resolvent)
        if [] in new_clauses:
            return new_clauses
        else:
            for clause in new_clauses:
                if clause not in KF:
                    KF.append(clause)
    return KF


def is_satisfiable(KF):
    n = 1
    while True:
        res_n = res(KF, n)
        if [] in res_n:
            print("F ist unerfüllbar")
            return False
        elif res_n == res(KF, n - 1):
            print("F ist erfüllbar")
            return True
        n += 1


# F = (X v Y) ^ (~X v ~Y v ~Z) ^ (~X v Z) ^ (X v Y v Z) ^ (Y v ~Z)
KF = [
    [("X", True), ("Y", False)],
    [("X", False), ("Y", False), ("Z", False)],
    [("X", False), ("Z", True)],
    [("X", True), ("Y", True), ("Z", True)],
    [("Y", True), ("Z", False)],
]

# F = (X v Y) ^ (~X v ~Y) ist erfüllbar, z.B. mit X = True, Y = False
KF2 = [[("X", True), ("Y", True)], [("X", False), ("Y", False)]]

if __name__ == "__main__":
    print("K(F) = " + showCNF(KF))
    is_satisfiable(KF)

    print("K(F2) = " + showCNF(KF2))
    is_satisfiable(KF2)

    # KFu = [[("X", True)], [("X", False)]]
    # is_satisfiable(KFu)
