from backtracking import backtracking_simple
from backtrackingH import backtracking
import time


def solve_knights_tour(use_heuristic=True):
  
    import time

    start_time = time.time()
    assignment = [(0, 0)]

    if use_heuristic:
        solution = backtracking(assignment)
        end_time = time.time()
        print(f"Temps d'exécution MRV&LCV : {end_time - start_time:.4f} s")# version avec MRV & LCV
    else:
        solution = backtracking_simple(assignment) 
        end_time = time.time()
        print(f"Temps d'exécution simple : {end_time - start_time:.4f} s")# version simple

    return solution
