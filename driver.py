import sys
import time
from pysat.solvers import Minisat22
import argparse
from solver import Solver

sys.setrecursionlimit(100000)

start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

s = Solver(args['file'])
s.driver()
s.print_model()

end_time = time.time()
print(f'Time Taken: {end_time-start_time}')

# with Minisat22(bootstrap_with=F) as s:
#     s.solve()
#     model = s.get_model()


# minisat_assignment = {}
# for i in model:
#     minisat_assignment[abs(i)] = np.sign(i)

# print(minisat_assignment)
# print(check_assignment(F, minisat_assignment))

# for i in sorted(assignment.keys()):
#     if assignment[i] == 0:
#         assignment[i] = 1

# literal = choose_literal(F, assignment)
# print(dpll_2(F, literal))