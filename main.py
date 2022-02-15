import argparse
import copy
import numpy as np

count = 0

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

with open(args['file'], 'r') as f:
    lines = f.readlines()

F = []
for line in lines:
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

def preprocess(cnf, assignment):

    literals = []
    for i in range(len(cnf)):
        if len(cnf[i]) == 1:
            assignment[abs(cnf[i][0])] = np.sign(cnf[i][0])
            literals.append(cnf[i][0])

    for l in literals:
        d = []
        for i in range(len(cnf)):
            if l in cnf[i]:
                d.append(i)
            if -l in cnf[i]:
                cnf[i].remove(-l)

        for j in sorted(d, reverse=True):
            del cnf[j]

    return cnf, assignment



def find_unit_literals(cnf, assignment):
    unit_literals = []
    for c in cnf:
        count = 0
        for l in c:
            if assignment[abs(l)] != 0:
                count += 1
        if count == len(c)-1:
            for l in c:
                if assignment[abs(l)] == 0:
                    unit_literals.append(l)

    return unit_literals


def solve(cnf, assignment):
    global count
    count += 1
    print(count)
    unit_literals = []
    xs = find_unit_literals(cnf, assignment)

    for x in xs:
        unit_literals.append(abs(x))
        assignment[abs(x)] = np.sign(x)

        # Remove clauses containing x
        contains = []
        for i in range(len(cnf)):
            if x in cnf[i]:
                contains.append(i)
        
        for c in sorted(contains, reverse=True):
            del cnf[c]
    
        # Remove !x from all clauses
        for i in range(len(cnf)):
            if -1*x in cnf[i]:
                cnf[i].remove(-1*x)
        

    # Check if there is a null clause
    if any([len(c) == 0 for c in cnf]):
        for u in unit_literals:
            assignment[abs(u)] = 0
        return False, None

    if len(cnf) == 0:
        return True, assignment

    literal = None
    for i in assignment.keys():
        if assignment[i] == 0:
            literal = i
            break
    
    if literal is None:
        return False, None

    sat, new_assignment = solve(copy.deepcopy(cnf)+[[literal]], copy.deepcopy(assignment))
    if sat:
        return True, new_assignment

    sat, new_assignment = solve(copy.deepcopy(cnf)+[[-literal]], copy.deepcopy(assignment))
    if sat:
        return True, new_assignment

    return False, None


def get_assignment(cnf):
    assignment = {}
    for i in cnf:
        for j in i:
            assignment[abs(j)] = 0
    return assignment
    

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
F, assignment = preprocess(F, assignment)
sat, assignment = solve(F, assignment)
print(sat, assignment)
print(check_assignment(F, assignment))

