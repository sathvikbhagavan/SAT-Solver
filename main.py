import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

class Solver:

    def __init__(self, file):
        df = pd.read_csv(file)
        self.F = self.df.tolist()
        self.M = []

    def check_sat(self):
        for clause in self.F:
            is_true = False
            for literal in clause:
                if literal > 0:
                    if self.M[literal] == 1:
                        is_true = True
                        break
                elif literal < 0:    
                    if self.M[literal] == -1:
                        is_true = True
                        break
            if not is_true:
                return False

        return True

    def find_unit_literal(self):
        
        for i in range(len(self.F)):
            count = 0
            unassigned_l = None
            for j in range(len(self.F[i])):
                if (self.F[i][j] > 0 and self.M[abs(self.F[i][j])] < 0) \
                    or (self.F[i][j] < 0 and self.M[abs(self.F[i][j])] > 0):
                    count += 1
                elif self.M[abs(self.F[i][j])] == 0:
                    unassigned_l = j
            if count == len(clause) - 1:
                if self.F[i][j] < 0:
                    self.M[abs(F[i][j])] = -1
                else:
                    self.M[abs(F[i][j])] = 1



    def solve(self):
        
        if self.check_sat():
            return "SAT"
        else:
            return "UNSAT"

        self.find_unit_literal()
