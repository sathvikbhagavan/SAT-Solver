import argparse
import copy

from numpy import append

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

with open(args['file'], 'r') as f:
    lines = f.readlines()

F = []
line_count=0
for line in lines:
    line_count+=1
    if line_count>8:
        F.append([int(i) for i in line.strip().split(' ')])

for ll in F:
    ll.pop()

#print(F)


def find_pure_literals(cnf):
    pure=[]
    mapp={}
    for c in cnf:
        for i in c:
            if i not in mapp:
                mapp[i]=1
    for i in mapp.keys():
        if -i not in mapp:
            pure.append(i)
    return pure

def find_unit_clauses(cnf):
    unit_clause=[]
    for c in cnf:
        if len(c)==1:
            unit_clause.append(c[0])
    return unit_clause

def eliminate_pure_literals(cnf, assignment):   
    
    pure=find_pure_literals(cnf)

    while pure:
        print('pure_literals',pure)
        for x in pure:
            if x < 0:
                assignment[abs(x)] = -1
            else:
                assignment[abs(x)] = 1

            contains = []
            for i in range(len(cnf)):
                if x in cnf[i]:
                    contains.append(i)
            
            for c in sorted(contains, reverse=True):
                del cnf[c] 

            pure=find_pure_literals(cnf)
    
    return cnf, assignment

def unit_propogate(cnf, assignment):
    
    unit_clause=find_unit_clauses(cnf)
    while unit_clause:
        print('unit_clauses',unit_clause)
        for x in unit_clause:
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
        
            #print(cnf)
            # Remove !x from all clauses
            for i in range(len(cnf)):
                if -1*x in cnf[i]:
                    cnf[i].remove(-1*x)

        unit_clause=find_unit_clauses(cnf)
    
    return cnf,assignment

def solve(cnf, assignment):
    
    cnf, assignment = unit_propogate(cnf,assignment) 
    cnf, assignment = eliminate_pure_literals(cnf,assignment)
      
    # Check if there is a null clause
    if sum([len(cnf[i]) == 0 for i in range(len(cnf))]):
        return False, assignment

    if len(cnf) == 0:
        #print(assignment)
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
        return False,assignment



def get_assignment(cnf):
    assignment = {}
    for i in cnf:
        for j in i:
            assignment[abs(j)] = 0
    return assignment
    

assignment = get_assignment(F)
sat, assignment = solve(F, assignment)
print(sat)
if sat:
    print(assignment)



