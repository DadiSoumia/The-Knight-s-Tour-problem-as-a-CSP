'''
from backtracking import backtracking_simple
from backtrackingH import backtracking
import time


def solve_knights_tour(use_heuristic=True):
  


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
'''
def solve_knights_tour(use_heuristic=True):
    import time

    # ← déplacer les imports ICI
    if use_heuristic:
        from backtrackingH import backtracking
    else:
        from backtracking import backtracking_simple

    start_time = time.time()
    assignment = [(0, 0)]

    if use_heuristic:
        solution = backtracking(assignment)
        end_time = time.time()
   
        print(f"Solutionvec heuristique : {solution}")
        print(f"Temps d'exécution MRV&LCV : {end_time - start_time:.4f} s")
    else:
        solution = backtracking_simple(assignment)
        end_time = time.time()
      
        print(f"Solution  : {solution}")
        print(f"Temps d'exécution simple : {end_time - start_time:.4f} s")

    return solution

