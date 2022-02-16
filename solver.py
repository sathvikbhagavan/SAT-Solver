import copy
import numpy as np


class Solver:

    def __init__(self, filename):

        self.filename = filename

        with open(filename, 'r') as f:
            lines = f.readlines()

        self.F = []

        for i, line in enumerate(lines):
            if line[0] == 'c' or line[0] == 'p' :
                continue
            self.F.append([int(i) for i in line.strip().split(' ')[:-1]])


    def input_optimization(self, cnf):

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


    def find_pure_literals(self, cnf):
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

    def find_unit_clauses(self, cnf):
        unit_clause = []
        for c in cnf:
            if len(c) == 1:
                unit_clause.append(c[0])
        return unit_clause


    def eliminate_pure_literals(self, cnf, assignment):   
        
        pure = self.find_pure_literals(cnf)

        while len(pure) > 0:
            for x in pure:
                assignment[abs(x)] = np.sign(x)
                
                contains = []
                for i in range(len(cnf)):
                    if x in cnf[i]:
                        contains.append(i)
                
                for c in sorted(contains, reverse=True):
                    del cnf[c] 

            pure = self.find_pure_literals(cnf)
        
        return cnf, assignment

    def unit_propogate(self, cnf, assignment):
        
        unit_clause = self.find_unit_clauses(cnf)

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

            unit_clause = self.find_unit_clauses(cnf)
        
        return cnf, assignment


    def choose_literal(self, cnf, assignment):

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


    def solve(self, cnf, assignment):
        
        cnf, assignment = self.unit_propogate(cnf,assignment) 
        cnf, assignment = self.eliminate_pure_literals(cnf,assignment)
        
        if len(cnf) == 0:
            return True, assignment

        
        if any([len(c) == 0 for c in cnf]):
            return False, None
        
        literal = self.choose_literal(cnf, assignment)

        new_cnf = copy.deepcopy(cnf) + [[literal]]
        new_assignment = copy.deepcopy(assignment)
        sat, new_assignment = self.solve(new_cnf, new_assignment)
        if sat:
            return True, new_assignment

        new_cnf = copy.deepcopy(cnf) + [[-literal]]
        new_assignment = copy.deepcopy(assignment)
        sat, new_assignment = self.solve(new_cnf, new_assignment)
        if sat:
            return True, new_assignment

        return False, None


    def get_assignment(self, cnf):
        a = {}
        for i in cnf:
            for j in i:
                a[abs(j)] = 0
        return a

    def check_assignment(self, cnf, assignment):
        if assignment is None:
            return None
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

    def print_model(self):
        
        for i in sorted(self.assignment.keys()):
            print(f'{i}: {self.assignment[i]}')

    def assign_literals(self):

        for i in self.assignment.keys():
            if self.assignment[i] == 0:
                self.assignment[i] = 1 

    def driver(self, print_disable=False):
        
        self.F = self.input_optimization(self.F)
        self.assignment = self.get_assignment(self.F)
        sat, self.assignment = self.solve(copy.deepcopy(self.F), copy.deepcopy(self.assignment))
        
        print('---------------------------------------------')
        print(f'For file {self.filename}...')
        
        sat_string = 'satisfiable' if sat else 'unsatisfiable'
        if not print_disable:
            print(f'It is {sat_string}')
        if sat:
            self.assign_literals()
            check = self.check_assignment(self.F, self.assignment)
            check_string = 'correct' if sat else 'wrong'
            if not print_disable:
                print(f'After checking assignment, it is {check_string}')