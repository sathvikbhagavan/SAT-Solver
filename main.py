import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

F = pd.read_csv(args['file']).tolist()
M = []

def find_unit_clause(cnf):
    ...


def solve(cnf, assignment):

    unit_literals = []
    while True:
        x = find_unit_clause(cnf)
        
        unit_literals.append(abs(x))
        
        if x is None:
            break
        
        if x < 0:
            assignment[abs(x)] = -1
        else:
            assignment[abs(x)] = 1

        # Remove clauses containing x
        contains = []
        for i in range(len(cnf)):
            for j in range(len(cnf[i])):
                if x == cnf[i][j]:
                    contains.append(i)

        
        for c in contains:
            cnf.pop(c)
        

        # Remove !x from all clauses
        for i in range(len(cnf)):
            cnf[i].remove(-1*x)
        

    if check_null(cnf):
        for u in unit_literals:
            assignment[abs(u)] = 0
        return False, assignment

    if len(cnf) == 0:
        return True, assignment

    new_x = None
    for i in range(1, len(assignment)):
        if assignment[i] == 0:
            new_x = i
            break

    if solve(copy.deepcopy(cnf)+[new_x], copy.deepcopy(assignment)):
        return True, assignment

    elif solve(copy.deepcopy(cnf)+[-new_x], copy.deepcopy(assignment)):
        return True, assignment



    

    




