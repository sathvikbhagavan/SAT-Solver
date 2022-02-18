import time
from pysat.solvers import Minisat22
import argparse
from solver import Solver

start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', help='path of the csv file')

args = vars(ap.parse_args())

s = Solver(args['file'])
s.driver()

end_time = time.time()
print(f'Time Taken: {end_time-start_time}')

with Minisat22(bootstrap_with=s.F) as sol:
    sol.solve()
    model = sol.get_model()
    print(model)