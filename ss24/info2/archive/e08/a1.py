def showLit(lit):
    if lit[1]:
        return lit[0]
    else:
        return "~" + lit[0]


# format a clause so that we put v between literals
def showClause(clause):
    return " v ".join(map(showLit, clause))


def showCNF(F):
    return " ^ ".join("(" + showClause(clause) + ")" for clause in F)

a = [('B', False)]
b = [('A', True), ('B', True), ('C', False)]

u = [('C', False)]

c = [a, b]

print(showClause(a) + "\n" + showClause(b))

print(showCNF(c))

def alphaLit(lit, alpha):
    if lit[0] in alpha:
        return lit[1]
    else:
        return False


def alphaClause(clause, alpha):
    # print(showClause(clause))
    # print("~~~clause~~~")
    results = [alphaLit(l, alpha) for l in clause]
    return any(results)


def alphaCNF(cnf, alpha):
    print(showCNF(cnf))
    return all([alphaClause(c, alpha) for c in cnf])


alpha = ['A', 'B']

print("~~~")
print(alphaLit(('A', True), alpha))
print(alphaLit(('B', False), alpha))
print(alphaLit(('C', True), alpha))
print("~~~")
print(alphaClause(a, alpha))
print(alphaClause(b, alpha))
print("~~~")
print(alphaCNF(c, alpha))

import itertools

x = 'X'
y = 'Y'
z = 'Z'
alpha = [x, y, z]


def neg(literal):
    return (literal[0], not literal[1])


def F(x, y, z):
    return [[x, neg(y)], [neg(x), neg(y), neg(z)], [neg(x), z], [x, y, z], [y, neg(z)]]


assignments = list(itertools.product([True, False], repeat=3))
for assignment in assignments:
    lits = tuple(zip(alpha, assignment))
    print(alphaCNF(F(lits[0], lits[1], lits[2]), alpha))
