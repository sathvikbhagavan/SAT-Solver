import argparse
import copy

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

with open(args['file'], 'r') as f:
    lines = f.readlines()

F = []
for line in lines:
    F.append([int(i) for i in line.strip().split(' ')])


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
    print(cnf)
    unit_literals = []
    xs = find_unit_literals(cnf, assignment)
    print(xs)

    for x in xs:
        unit_literals.append(abs(x))
        if x < 0:
            assignment[abs(x)] = -1
        else:
            assignment[abs(x)] = 1

        # Remove clauses containing x
        contains = []
        for i in range(len(cnf)):
            if x in cnf[i]:
                contains.append(i)
        
        for c in sorted(contains, reverse=True):
            del cnf[c]
    
        print(cnf)
        # Remove !x from all clauses
        for i in range(len(cnf)):
            if -1*x in cnf[i]:
                cnf[i].remove(-1*x)
        

    # Check if there is a null clause
    if sum([len(cnf[i]) == 0 for i in range(len(cnf))]):
        for u in unit_literals:
            assignment[abs(u)] = 0
        return False, assignment

    if len(cnf) == 0:
        print(assignment)
        return True, assignment

    literal = None
    for i in assignment.keys():
        if assignment[i] == 0:
            literal = i
            break
    
    if literal is None:
        return False, assignment

    sat, new_assignment = solve(copy.deepcopy(cnf)+[[literal]], copy.deepcopy(assignment))
    if sat:
        return True, new_assignment

    sat, new_assignment = solve(copy.deepcopy(cnf)+[[-literal]], copy.deepcopy(assignment))
    if sat:
        return True, new_assignment

    else:
        for u in unit_literals:
            assignment[abs(u)] = 0
        return False, assignment



def get_assignment(cnf):
    assignment = {}
    for i in cnf:
        for j in i:
            assignment[abs(j)] = 0
    return assignment
    

assignment = get_assignment(F)
sat, assignment = solve(F, assignment)
print(sat, assignment)




