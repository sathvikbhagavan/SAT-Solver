import argparse
import copy
import numpy as np
import sys

# sys.setrecursionlimit(100000)

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

with open(args['file'], 'r') as f:
    lines = f.readlines()

F = []

for i, line in enumerate(lines):
    if line[0] == 'c' or line[0] == 'p' :
        continue
    F.append([int(i) for i in line.strip().split(' ')[:-1]])


def input_optimization(cnf):

    d = []
    for i in range(len(cnf)):
        literals = list(set([abs(c) for c in cnf[i]]))
        for l in literals:
            if l in cnf[i] and -l in cnf[i]:
                d.append(i)
                break
    
    for j in sorted(d, reverse=True):
            del cnf[j]

    return cnf


def find_pure_literals(cnf):
    pure = []
    pure_map = dict()

    for c in cnf:
        for i in c:
            if i not in pure_map:
                pure_map[i] = 1

    for i in pure_map.keys():
        if -1*i not in pure_map:
            pure.append(i)
    
    return pure

def find_unit_clauses(cnf):
    unit_clause = []
    for c in cnf:
        if len(c) == 1:
            unit_clause.append(c[0])
    return unit_clause

def eliminate_pure_literals(cnf, assignment):   
    
    pure = find_pure_literals(cnf)

    while len(pure) > 0:
        print('pure_literals',pure)
        for x in pure:
            assignment[abs(x)] = np.sign(x)
            
            contains = []
            for i in range(len(cnf)):
                if x in cnf[i]:
                    contains.append(i)
            
            for c in sorted(contains, reverse=True):
                del cnf[c] 

        pure = find_pure_literals(cnf)
    
    return cnf, assignment

def unit_propogate(cnf, assignment):
    
    unit_clause = find_unit_clauses(cnf)

    while unit_clause:
        for x in unit_clause:
            assignment[abs(x)] = np.sign(x)

            contains = []
            for i in range(len(cnf)):
                if x in cnf[i]:
                    contains.append(i)
            
            for c in sorted(contains, reverse=True):
                del cnf[c]
        
            for i in range(len(cnf)):
                if -1*x in cnf[i]:
                    cnf[i].remove(-1*x)

        unit_clause = find_unit_clauses(cnf)
    
    return cnf, assignment


def choose_literal(cnf, assignment):

    # length = 2
    # max_length = max([len(i) for i in cnf])
    # for l in range(length, max_length+1):
    #     l_map = dict()
    #     for c in cnf:
    #         if len(c) == l:
    #             for i in c:
    #                 if assignment[abs(i)] == 0:
    #                     if i not in l_map.keys():
    #                         l_map[i] = 1
    #                     else:
    #                         l_map[i] += 1
    #     if len(sorted(l_map.keys())) != 0:
    #         v = list(l_map.values())
    #         k = list(l_map.keys())
    #         return k[v.index(max(v))]

    length = 2
    l_map = dict()
    max_length = max([len(i) for i in cnf])
    for c in cnf:
        for i in c:
            if assignment[abs(i)] == 0:
                if i not in l_map.keys():
                    l_map[i] = 1/(2**len(c))
                else:
                    l_map[i] += 1/(2**len(c))
    
    if len(l_map.keys()) != 0:
        v = list(l_map.values())
        k = list(l_map.keys())
        return k[v.index(max(v))]


def solve(cnf, assignment):
    
    # cnf, assignment = unit_propogate(cnf,assignment) 
    # cnf, assignment = eliminate_pure_literals(cnf,assignment)
    
    print(f'Start of the function: {len(cnf)}')

    unit_clause = find_unit_clauses(cnf)

    while len(unit_clause) > 0:
        for x in unit_clause:
            assignment[abs(x)] = np.sign(x)

            contains = []
            for i in range(len(cnf)):
                if x in cnf[i]:
                    contains.append(i)
            
            for c in sorted(contains, reverse=True):
                del cnf[c]
        
            for i in range(len(cnf)):
                if -1*x in cnf[i]:
                    cnf[i].remove(-1*x)

        unit_clause = find_unit_clauses(cnf)
    
    print(f'After unit propagation: {len(cnf)}')

    pure = find_pure_literals(cnf)

    while len(pure) > 0:
        for x in pure:
            assignment[abs(x)] = np.sign(x)
            
            contains = []
            for i in range(len(cnf)):
                if x in cnf[i]:
                    contains.append(i)
            
            for c in sorted(contains, reverse=True):
                del cnf[c] 

        pure = find_pure_literals(cnf)

    print(f'After pure literal elimination: {len(cnf)}')

    if len(cnf) == 0:
        return True, assignment

    
    if any([len(c) == 0 for c in cnf]):
        return False, None
    
    literal = choose_literal(cnf, assignment)

    new_cnf = copy.deepcopy(cnf) + [[literal]]
    new_assignment = copy.deepcopy(assignment)
    sat, new_assignment = solve(new_cnf, new_assignment)
    if sat:
        return True, new_assignment

    new_cnf = copy.deepcopy(cnf) + [[-literal]]
    new_assignment = copy.deepcopy(assignment)
    sat, new_assignment = solve(new_cnf, new_assignment)
    if sat:
        return True, new_assignment

    return False, None


# def dpll_2(cnf, literal):
    
#     contains = []
#     for i in range(len(cnf)):
#         if literal in cnf[i]:
#             contains.append(i)
    
#     for c in sorted(contains, reverse=True):
#         del cnf[c]

#     if len(cnf) == 0:
#         return True

#     for i in range(len(cnf)):
#         if -1*literal in cnf[i]:
#             cnf[i].remove(-1*literal)
    
#     if any([len(c) == 0 for c in cnf]):
#         return False

#     unit_clause = find_unit_clauses(cnf)
#     if len(unit_clause) > 0:
#         return dpll_2(copy.deepcopy(cnf), unit_clause[0])

    
#     pure = find_pure_literals(cnf)
#     if len(pure) > 0:
#         return dpll_2(copy.deepcopy(cnf), pure[0])

    
#     new_literal = choose_literal(cnf)

#     if dpll_2(copy.deepcopy(cnf), -1*new_literal):
#         return True

#     return dpll_2(copy.deepcopy(cnf), new_literal)    
     


def get_assignment(cnf):
    a = {}
    for i in cnf:
        for j in i:
            a[abs(j)] = 0
    return a

def check_assignment(cnf, assignment):
    for c in cnf:
        is_true = False
        for l in c:
            if l > 0 and assignment[abs(l)] == 1:
                is_true = True
                break
            elif l < 0 and assignment[abs(l)] == -1:
                is_true = True
                break
        if not is_true:
            return False

    return True
    
F = input_optimization(F)
assignment = get_assignment(F)
sat, assignment = solve(copy.deepcopy(F), copy.deepcopy(assignment))
print(check_assignment(F, assignment))
if sat:
    print(assignment)

# literal = choose_literal(F, assignment)
# print(dpll_2(F, literal))