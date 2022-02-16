from solver import Solver
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-c', '--case', help='uf20/uf150/uuf150')

args = vars(ap.parse_args())

if args['case'] == 'uf20':
    for i in range(1, 16):
        start_time = time.time()
        s = Solver(f'testcases/uf20-0{i}.cnf')
        s.driver()
        end_time = time.time()
        print(f'it takes {end_time-start_time} seconds')
        print('---------------------------------------------')

elif args['case'] == 'uf150':
    for i in range(1, 16):
        start_time = time.time()
        s = Solver(f'testcases/uf150-0{i}.cnf')
        s.driver()
        end_time = time.time()
        print(f'it takes {end_time-start_time} seconds')
        print('---------------------------------------------')

elif args['case'] == 'uuf150':
    for i in range(1, 21):
        start_time = time.time()
        s = Solver(f'testcases/uuf150-0{i}.cnf')
        s.driver()
        end_time = time.time()
        print(f'it takes {end_time-start_time} seconds')
        print('---------------------------------------------')